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

#se puede cambiar de user a user_id de nombre de variable, por que es el id
@router.post("/{match_id}", tags=["Game"])
async def join_game(match_id: int, user: int): 

    player_id = get_player_id(match_id,user)
    if player_id is not None:
        playerdic = {
            "Match_id": match_id,
            "Player_id": player_id
        }
        return playerdic
        
    if not there_is_space(match_id):
        raise HTTPException(status_code=404, detail="there is no space")

    if not get_match_status(match_id) == "Joinable":
        raise HTTPException(status_code=404, detail="game already started")

    positionp = get_num_players(match_id)
    playerobj = add_user_in_match(user, match_id, positionp)

    if playerobj is None:
        raise HTTPException(status_code=404, detail="couldnt add the user")

    playerdic = {
        "Match_id": match_id,
        "Player_id": playerobj.to_dict("PlayerId")["PlayerId"]
    }

    return playerdic


@router.get("/list", tags=["Game"])
async def list_games():
    return list_games_db()
      
@router.post("/{mid}/leave/{pid}", tags=["Game"])
async def leave_game(mid: int, user: int):

    if not check_match(mid):
        raise HTTPException(status_code=404, detail="this match does not exist")

    if not check_player_in_match(mid,pid):
        raise HTTPException(status_code=404, detail="Player not found")

    if not get_match_status(mid) == "Joinable":
        raise HTTPException(status_code=404, detail="game already started")

    try:
        playername = get_player_username(pid)
        eliminate_player_from_match(mid, pid)

    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")

    return f"{playername} is not longer in the game"
