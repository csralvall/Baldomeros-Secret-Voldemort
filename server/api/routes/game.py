from server.db.crud import *

from fastapi import APIRouter, HTTPException, Query, Path

from typing import Optional

router = APIRouter()

@router.get("/{mid}", tags=["Game"])
async def game_status(mid: int):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="this match does not exist")

    minister = get_minister_username(mid)
    player_status = get_all_player_status(mid)
    matchstatus = get_match_status(mid)
    board_id = get_match_board_id(mid)
    board_status = get_board_status(board_id)

    board_status = {k.lower(): v for k, v in board_status.items()}

    status = {
        'minister': minister,
        'matchstatus': matchstatus,
        'playerstatus': player_status,
        'boardstatus': board_status
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
        set_next_director(mid)
        set_next_minister(mid)
        if compute_election_result(mid) == 'lumos':
            enact_proclamation(mid,'death eater')
        restore_election(mid)

    winner = is_victory_from(mid)

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
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")

    return f"{playername} is dead"

