from fastapi import APIRouter, HTTPException
from backend.db.crud import *
from backend.db.database import *


router = APIRouter()

@router.get("/games")
async def status_games(mid: int):

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
