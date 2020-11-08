from server.db.crud import *

from fastapi import APIRouter, HTTPException, Query, Path

from typing import Optional

router = APIRouter()

@router.post("/new", tags=["Game"])
async def create_match(minp: int, maxp: int, uhid: int):
  
    newmatch = add_match_db(minp,maxp,uhid)

    if (newmatch is not None): 
        return newmatch
    else:
        raise HTTPException(status_code=404, detail="couldnt create the game")  


@router.post("/{mid}", tags=["Game"])
async def join_game(mid: int, user: int): 

    pid = get_player_id(mid,user)
    if pid is not None:
        playerdic = {
            "Match_id": mid,
            "Player_id": pid
        }
        return playerdic
        
    if there_is_space(mid):
        if get_match_status(mid) == "Joinable":
            playerobj = add_user_in_match(user, mid, 5) #hardcodeado position should be there

            if (playerobj is not None):

                playerdic = {
                    "Match_id": mid,
                    "Player_id": playerobj.to_dict("PlayerId")["PlayerId"]
                }
                if not there_is_space(mid):
                    change_match_status(mid, 1)
                    
                return playerdic

            else: 


                raise HTTPException(status_code=404, detail="couldnt add the user")
        else:
            raise HTTPException(status_code=404, detail="game already started")

    else: 
        raise HTTPException(status_code=404, detail="there is no space")


@router.get("/{mid}", tags=["Game"])
async def game_status(mid: int):

    if check_match(mid):

        minister = get_minister_username(mid)
        players = get_player_votes(mid)
        matchstatus = get_match_status(mid)
        boardstatus = get_board_status(mid)


        status = {
            'minister': minister,
            'matchstatus': matchstatus,
            'players': players}

        status.update(boardstatus) 

        status = {k.lower(): v for k, v in status.items()}

        return status
    else:
        raise HTTPException(status_code=404, detail="this match does not exist")


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

        player_votes = get_player_votes(mid)

        if 'missing vote' not in player_votes.values():
            set_next_minister(mid)
            if compute_election_result(mid) == 'lumos':
                enact_proclamation(mid,'death eater')
            restore_election(mid)

        winner = is_victory_from(mid)

        return winner


@router.patch("/{mid}")
async def start_game(mid: int, user: int): 

    if check_match(mid):

        if check_host(user):

            num = get_num_players(mid)

            set_roles(num,mid)
            set_gob_roles(mid)
            change_match_status(mid,1)

            return {"game": "game created succesfully"}

        else:
            raise HTTPException(status_code=404, detail="only the host can start the game") 

    else:
        raise HTTPException(status_code=404, detail="this game does not exist") 


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

    if check_match(mid):

        if check_host(user):

            num = get_num_players(mid)

            set_roles(num,mid)
            set_gob_roles(num,mid)
            change_match_status(mid,1)

            return {"game": "game created succesfully"}

        else:
            raise HTTPException(status_code=404, detail="only the host can start the game") 

    else:
        raise HTTPException(status_code=404, detail="this game does not exist") 
