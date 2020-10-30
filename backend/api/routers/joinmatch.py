from fastapi import APIRouter, HTTPException
from backend.db.crud import *
from backend.db.database import *


router = APIRouter()


@router.post("/game/{mid}")
async def join_game(mid: int, user: int): 

    if there_is_space(mid):

        playerobj = add_user_in_match(user, mid, 5) #hardcodeado position should be there

        if (playerobj is not None):

            playerdic = {
                "Match_id": mid,
                "Player_id": playerobj.to_dict("PlayerId")["PlayerId"]
            }

            return playerdic

        else: 

            raise HTTPException(status_code=404, detail="couldnt add the user")

    else: 

        raise HTTPException(status_code=404, detail="there is no space")

