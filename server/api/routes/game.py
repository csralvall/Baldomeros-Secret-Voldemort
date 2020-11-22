from server.db.crud import *

from server.db.dicts import *

from fastapi import APIRouter, HTTPException, Query, Path, Body

from typing import Optional, List


router = APIRouter()


@router.get("/{match_id}", tags=["Game"])
async def game_status(match_id: int):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="this match does not exist")

    minister = get_minister_username(match_id)
    director = get_director_username(match_id)
    candidate = get_candidate_director_username(match_id)
    player_status = get_all_player_status(match_id)
    matchstatus = get_match_status(match_id)
    board_id = get_match_board_id(match_id)
    board_status = get_board_status(board_id)

    try:
        hand = show_selected_deck(board_id)
    except DeckNotFound:
        hand = []

    winner = check_winner(match_id)

    board_status = {k.lower(): v for k, v in board_status.items()}

    status = {
        'minister': minister,
        'director': director,
        'candidate': candidate,
        'matchstatus': matchstatus,
        'winner': winner,
        'playerstatus': player_status,
        'boardstatus': board_status,
        'hand': hand
    }

    return status


@router.put("/{match_id}/player/{player_id}", tags=["Game"], status_code=200)
async def vote_candidate(
    match_id: int = Path(..., title="The ID of the current match"),
    player_id: int = Path(..., title="The ID of the player who votes"),
    vote: str = Query(..., regex="^(nox|lumos)$")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    if not check_player_in_match(match_id,player_id):
        raise HTTPException(status_code=404, detail="Player not found")

    vote_director(player_id, vote)

    player_status = get_all_player_status(match_id)
    player_alive = dict()

    for k, v in player_status.items():
        if not v['isDead']:
            player_alive[k] = {"vote": v['vote'], "isDead": v['isDead']}

    player_votes = { k: v["vote"] for k, v in player_alive.items() }
    if 'missing vote' not in player_votes.values():
        if compute_election_result(match_id) == 'lumos':
            successful_director_election(match_id)
            change_ingame_status(match_id, MINISTER_SELECTION)#minister selects cards stage
            if check_voldemort(match_id):
                set_death_eater_winner(match_id)
        else :
            failed_director_election(match_id)
            set_next_minister_failed_election(match_id)
            change_ingame_status(match_id, NOMINATION)# new minister chooses new director
            failed_election(match_id)            

    winner = check_winner(match_id)
    return winner 


@router.get("/{match_id}/player/{player_id}/rol", tags=["Game"])
async def player_rol(match_id: int, player_id: int):
    
    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    if not check_player_in_match(match_id,player_id):
        raise HTTPException(status_code=404, detail="Player not found")

    player_rol = get_player_rol(player_id)
    player_username = get_player_username(player_id)

    rol = {
        "username": player_username,
        "rol": player_rol}
    
    return rol

@router.get("/{match_id}/death_eaters", tags=["Game"])
async def death_eaters_in_match(match_id: int):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    death_eaters = get_death_eater_players_in_match(match_id)
    
    return death_eaters

    
@router.patch("/{match_id}")
async def start_game(match_id: int, user: int): 

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="this game does not exist") 

    if not check_host(user):
        raise HTTPException(status_code=404, detail="only the host can start the game") 

    num = get_num_players(match_id)
    minp = get_min_players(match_id)
                
    if not num >= minp: 
        raise HTTPException(status_code=404, detail="we need more people to start :)")
    #BoardType=SMALL_BOARD, #hardcoded_hay que cambiarlo cuando empieza la partida
    set_roles(num,match_id)
    set_gob_roles(match_id)
    change_match_status(match_id, IN_GAME)
    board_id = get_match_board_id(match_id)
    create_deck(board_id)
    shuffle_deck(board_id)
    get_top_three_proclamation(board_id)

    return {"game": "game created successfully"}

        
@router.get("/{match_id}/directors", tags=["Game"])
async def posible_directors(match_id:int):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    posible_directors = get_posible_directors(match_id)

    return posible_directors

@router.patch("/{match_id}/board/avada-kedavra", tags=["Game"])
async def use_avada_kedavra(
    match_id: int = Path(..., title="The ID of the current match"),
    playername: str = Query(..., title="Name of player who receives the spell")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    minister = get_minister_username(match_id)

    if minister == playername:
        raise HTTPException(status_code=403, detail="You can't kill yourself")

    try:
        player_id = get_player_id_from_username(match_id, playername)
        board_id = get_match_board_id(match_id)
        avada_kedavra(board_id, player_id)
        change_ingame_status(match_id, NOMINATION)#minister selects director stage
        change_to_exdirector(match_id)
        set_next_minister(match_id)
        if is_voldemort_dead(match_id):
            set_phoenix_winner(match_id)
    except VoldemortNotFound:
        raise HTTPException(status_code=500, detail="Voldemort was not set")
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")
    except NoDirector:
        raise HTTPException(status_code=404, detail="There is no director")

    return f"{playername} is dead"


@router.post("/{match_id}/proclamation/{player_id}", tags=["Game"])
async def receive_cards(match_id: int, player_id: int, discarded: str, selected: List[str]=Body(...)):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="this match does not exist")

    if not check_player_in_match(match_id,player_id):
        raise HTTPException(status_code=404, detail="Player not found")

    username = get_player_username(player_id)
    board_id = get_match_board_id(match_id)
    minister = get_minister_username(match_id)
    director = get_director_username(match_id)

    if username == minister:
        if not get_ingame_status(match_id) == ingame_status[MINISTER_SELECTION]:
            raise HTTPException(status_code=404, detail="We are not in the minister selection stage.")    
        if not len(selected) == 2:
            raise HTTPException(status_code=404, detail="The number of proclamation selected doesn't match the number of proclamations expected from minister.")    
        try:
            discard_proclamation(board_id, discarded)
            if not sorted(selected) == sorted(show_selected_deck(board_id)):
                raise InvalidProclamation
        except InvalidProclamation:
            raise HTTPException(status_code=404, detail="The proclamation selected doesn't match the proclamations passed.")    

        change_ingame_status(match_id, DIRECTOR_SELECTION)#director selects cards stage

    elif username == director:
        if not get_ingame_status(match_id) == ingame_status[DIRECTOR_SELECTION]:
            raise HTTPException(status_code=404, detail="We are not in the director selection stage.")    
        if not len(selected) == 1:
            raise HTTPException(status_code=404, detail="The number of proclamation selected doesn't match the number of proclamations expected from director.")    
        try:
            discard_proclamation(board_id, discarded)
            selected_card = get_selected_card(board_id)
        except InvalidProclamation:
            raise HTTPException(status_code=404, detail="The proclamation discarded doesn't match the proclamations passed.")    
        except DeckNotFound:
            raise HTTPException(status_code=404, detail="Deck not found")
        except EmptySelectedProclamations:
            raise HTTPException(status_code=404, detail="There is no cards selected")
        if not selected_card == selected[0]:
            raise HTTPException(status_code=404, detail="The proclamation selected doesn't match the proclamations passed.")    
        
        enact_proclamation(match_id, selected_card)
        reset_failed_election(board_id)
        winner = is_victory_from(match_id)

        if selected_card == "death eater":
            if not unlock_spell(match_id) == NO_SPELL:
                change_ingame_status(match_id, USE_SPELL)#spell stage
            else:
                change_ingame_status(match_id, NOMINATION)#minister selects director stage
                change_to_exdirector(match_id)
                set_next_minister(match_id)
        else:
            change_ingame_status(match_id, NOMINATION)#minister selects director stage
            change_to_exdirector(match_id)
            set_next_minister(match_id)

        try:
            get_top_three_proclamation(board_id)
        except NotEnoughProclamations:
            refill_deck(board_id)
            shuffle_deck(board_id)
            get_top_three_proclamation(board_id)
        except DeckNotFound:
            raise HTTPException(status_code=404, detail="Deck not found.")

    else:
        raise HTTPException(status_code=404, detail="This user is not the director or the minister.")
    
    winner = check_winner(match_id)
    return winner 

@router.patch("/{match_id}/director", tags=["Game"])
async def select_director(
    match_id: int = Path(..., title="The ID of the current match"),
    playername: str = Query(..., title="Name of player who receives the spell")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    player_id = get_player_id_from_username(match_id, playername)

    if not check_player_in_match(match_id,player_id):
        raise HTTPException(status_code=404, detail="Player not found")

    try:
        restore_election(match_id)     
        position = get_player_position(player_id)
        set_next_candidate_director(match_id,position)
        playername = get_player_username(player_id)
        change_ingame_status(match_id, ELECTION)
    
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")

    return f"{playername} is the candidate to director"


@router.patch("/{match_id}/board/adivination", tags=["Game"])
async def use_adivination(match_id: int):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    change_ingame_status(match_id, NOMINATION)
    change_to_exdirector(match_id)
    set_next_minister(match_id)

    board_id = get_match_board_id(match_id)
    adivination(board_id)

    return 200
