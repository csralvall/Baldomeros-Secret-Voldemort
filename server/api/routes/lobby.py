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
        
    if not there_is_space(mid):
        raise HTTPException(status_code=404, detail="there is no space")

    if not get_match_status(mid) == "Joinable":
        raise HTTPException(status_code=404, detail="game already started")

    positionp = get_num_players(mid)
    playerobj = add_user_in_match(user, mid, positionp)

    if playerobj is None:
        raise HTTPException(status_code=404, detail="couldnt add the user")

    playerdic = {
        "Match_id": mid,
        "Player_id": playerobj.to_dict("PlayerId")["PlayerId"]
    }

    return playerdic

