from server.db.crud import *

from server.db.dicts import *

from fastapi import APIRouter, HTTPException, Query, Path, Body

from typing import Optional, List


router = APIRouter()


@router.get("/{mid}", tags=["Game"])
async def game_status(mid: int):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="this match does not exist")

    minister = get_minister_username(mid)
    director = get_director_username(mid)
    player_status = get_all_player_status(mid)
    matchstatus = get_match_status(mid)
    board_id = get_match_board_id(mid)
    board_status = get_board_status(board_id)
    hand = show_selected_deck(board_id)
    winner = check_winner(mid)

    
    board_status = {k.lower(): v for k, v in board_status.items()}

    status = {
        'minister': minister,
        'director': director,
        'matchstatus': matchstatus,
        'winner': winner,
        'playerstatus': player_status,
        'boardstatus': board_status,
        'hand': hand
    }

    return status


@router.put("/{mid}/player/{pid}", tags=["Game"], status_code=200)
async def vote_candidate(
    mid: int = Path(..., title="The ID of the current match"),
    pid: int = Path(..., title="The ID of the player who votes"),
    vote: str = Query(..., regex="^(nox|lumos)$")):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="Match not found")

    if not check_player_in_match(mid,pid):
        raise HTTPException(status_code=404, detail="Player not found")

    vote_director(pid, vote)

    player_status = get_all_player_status(mid)

    player_votes = { k: v['vote'] for k, v in player_status.items() }

    if 'missing vote' not in player_votes.values():
        if compute_election_result(mid) == 'lumos':
            successful_director_election(mid)
            change_ingame_status(mid, MINISTER_SELECTION)#minister selects cards stage
        else :
            failed_director_election(mid)
            set_next_minister_failed_election(mid)
            change_ingame_status(mid, NOMINATION)# new minister chooses new director
        restore_election(mid)     

    winner = check_winner(mid)
    return winner 


@router.get("/{mid}/player/{pid}/rol", tags=["Game"])
async def player_rol(mid: int, pid: int):
    
    if not check_match(mid):
        raise HTTPException(status_code=404, detail="Match not found")

    if not check_player_in_match(mid,pid):
        raise HTTPException(status_code=404, detail="Player not found")

    player_rol = get_player_rol(pid)
    player_username = get_player_username(pid)

    rol = {
        "username": player_username,
        "rol": player_rol}
    
    return rol

@router.get("/{mid}/death_eaters", tags=["Game"])
async def death_eaters_in_match(mid: int):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="Match not found")

    death_eaters = get_death_eater_players_in_match(mid)
    
    return death_eaters

    
@router.patch("/{mid}")
async def start_game(mid: int, user: int): 

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="this game does not exist") 

    if not check_host(user):
        raise HTTPException(status_code=404, detail="only the host can start the game") 

    num = get_num_players(mid)
    minp = get_min_players(mid)
                
    if not num >= minp: 
        raise HTTPException(status_code=404, detail="we need more people to start :)")

    set_roles(num,mid)
    set_gob_roles(mid)
    change_match_status(mid,1)
    bid = get_match_board_id(mid)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    return {"game": "game created successfully"}
        
@router.get("/{mid}/directors", tags=["Game"])
async def posible_directors(mid:int):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="Match not found")

    posible_directors = get_posible_directors(mid)

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
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")
    except NoDirector:
        raise HTTPException(status_code=404, detail="There is no director")
    return f"{playername} is dead"


@router.post("/{mid}/proclamation/{pid}", tags=["Game"])
async def receive_cards(mid: int, pid: int, discarded: str, selected: List[str]=Body(...)):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="this match does not exist")

    if not check_player_in_match(mid,pid):
        raise HTTPException(status_code=404, detail="Player not found")

    username = get_player_username(pid)
    bid = get_match_board_id(mid)
    minister = get_minister_username(mid)
    director = get_director_username(mid)

    if username == minister:
        if not get_ingame_status(mid) == ingame_status[MINISTER_SELECTION]:
            raise HTTPException(status_code=404, detail="We are not in the minister selection stage.")    
        if not len(selected) == 2:
            raise HTTPException(status_code=404, detail="The number of proclamation selected doesn't match the number of proclamations expected from minister.")    
        try:
            discard_proclamation(bid, discarded)
            if not sorted(selected) == sorted(show_selected_deck(bid)):
                raise InvalidProclamation
        except InvalidProclamation:
            raise HTTPException(status_code=404, detail="The proclamation selected doesn't match the proclamations passed.")    

        change_ingame_status(mid, DIRECTOR_SELECTION)#director selects cards stage

    elif username == director:
        if not get_ingame_status(mid) == ingame_status[DIRECTOR_SELECTION]:
            raise HTTPException(status_code=404, detail="We are not in the director selection stage.")    
        if not len(selected) == 1:
            raise HTTPException(status_code=404, detail="The number of proclamation selected doesn't match the number of proclamations expected from director.")    
        try:
            discard_proclamation(bid, discarded)
            selected_card = get_selected_card(bid)
        except InvalidProclamation:
            raise HTTPException(status_code=404, detail="The proclamation discarded doesn't match the proclamations passed.")    
        except DeckNotFound:
            raise HTTPException(status_code=404, detail="Deck not found")
        except EmptySelectedProclamations:
            raise HTTPException(status_code=404, detail="There is no cards selected")
        if not selected_card == selected[0]:
            raise HTTPException(status_code=404, detail="The proclamation selected doesn't match the proclamations passed.")    
        
        enact_proclamation(mid, selected_card)
        winner = is_victory_from(mid)

        #-----------------------------------CAMBIAR--------------------------------------------------------
        #cambiar este if por funcion de si hay hechizo
        # tambien habilitar el hechizo adentro(puede ser todo en una funcion)
        # if get_death_eater_proclamations > 2:
        #     change_ingame_status(mid, USE_SPELL)#spell stage
        # else:
        #cambiar indentacion a esto para que quede en el else cuando se agregue lo de hechizos
        change_ingame_status(mid, NOMINATION)#minister selects director stage
        change_to_exdirector(mid)
        set_next_minister(mid)
        
        try:
            get_top_three_proclamation(bid)
        except NotEnoughProclamations:
            refill_deck(bid)
            shuffle_deck(bid)
            get_top_three_proclamation(bid)
        except DeckNotFound:
            raise HTTPException(status_code=404, detail="Deck not found.")

    else:
        raise HTTPException(status_code=404, detail="This user is not the director or the minister.")
    
    winner = check_winner(mid)
    return winner 

