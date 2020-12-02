from server.db.crud.exception_crud import *
from server.db.crud.crud_spell import *
from server.db.crud.crud_legislative_session import *
from server.db.crud.crud_lobby import *
from server.db.crud.crud_election import *
from server.db.crud.crud_messages import *
from server.db.crud.crud_deck import * 
from server.db.crud.crud_match import *

from server.db.dicts import *

from fastapi import APIRouter, HTTPException, Query, Path, Body

from typing import  List


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
    chat = read_messages(match_id)
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
        'hand': hand,
        'chat':chat
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
            change_ingame_status(match_id, MINISTER_SELECTION)
            if check_voldemort(match_id):
                set_winner(match_id, VOLDEMORT_DIRECTOR)
        else :
            failed_director_election(match_id)
            set_next_minister_failed_election(match_id)
            change_ingame_status(match_id, NOMINATION)
            failed_election(match_id)            

    winner = check_winner(match_id)
    return winner 


@router.get("/{match_id}/player/{player_id}/rol", tags=["Game"])
async def player_rol(match_id: int, player_id: int):
    
    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    if not check_player_in_match(match_id,player_id):
        raise HTTPException(status_code=404, detail="Player not found")

    player_rol = SecretRolDiccionary[get_player_rol(player_id)]
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

    set_roles(num,match_id)
    set_gob_roles(match_id)
    change_match_status(match_id, IN_GAME)
    board_id = get_match_board_id(match_id)
    create_deck(board_id)
    shuffle_deck(board_id)
    get_top_three_proclamation(board_id)
    set_board_type(board_id,num)

    return {"game": "game created successfully"}

        
@router.get("/{match_id}/directors", tags=["Game"])
async def posible_directors(match_id:int):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    posible_directors = get_posible_directors(match_id)

    return posible_directors


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
        if not get_ingame_status(match_id) == MINISTER_SELECTION:
            raise HTTPException(status_code=404, detail="We are not in the minister selection stage.")    
        if not len(selected) == 2:
            raise HTTPException(status_code=404, detail="The number of proclamation selected doesn't match the number of proclamations expected from minister.")    
        try:
            discard_proclamation(board_id, discarded)
            if not sorted(selected) == sorted(show_selected_deck(board_id)):
                raise InvalidProclamation
        except InvalidProclamation:
            raise HTTPException(status_code=404, detail="The proclamation selected doesn't match the proclamations passed.")    

        change_ingame_status(match_id, DIRECTOR_SELECTION)

    elif username == director:
        if not get_ingame_status(match_id) == DIRECTOR_SELECTION:
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

        unlock_expelliarmus(board_id)
        if selected_card == DEATH_EATER_STR:
            if not unlock_spell(match_id) == NO_SPELL:
                change_ingame_status(match_id, USE_SPELL)
            else:
                change_ingame_status(match_id, NOMINATION)
                change_to_exdirector(match_id)
                set_next_minister(match_id)
        else:
            change_ingame_status(match_id, NOMINATION)
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


@router.patch("/{match_id}/chat", tags=["Game"])
async def send_message_endpoint(
    match_id: int = Path(..., title="The ID of the current match"),
    username: str = Query(..., title="Name of user who sends a message"),
    message: str = Body(..., title = "message that the users sends")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    minister = get_minister_username(match_id)
    director = get_director_username(match_id)

    if get_player_id_from_username(match_id, username) is None:
        raise HTTPException(status_code=404, detail="This user is not playing this match")

    if get_all_player_status(match_id)[username]["isDead"]:
        raise HTTPException(status_code=404, detail="Player is dead")

    ingame_status = get_ingame_status(match_id)

    if ((ingame_status == MINISTER_SELECTION or ingame_status == DIRECTOR_SELECTION) and
            (username == minister or username == director)):
        raise HTTPException(status_code=404, detail="Minister and director can't talk during legislative session")
    
    try:
        send_message(match_id,username,message)
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")
    except BadUsername:
        raise HTTPException(status_code=404, detail="username is too long")

    return "Message sent"
