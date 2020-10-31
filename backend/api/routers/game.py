from backend.db.crud import *

from fastapi import APIRouter, HTTPException, Query, Path

from typing import Optional

router = APIRouter()

@router.put("/game/{gid}/player/{pid}", tags=["Game"], status_code=200)
async def vote_candidate(
        gid: int = Path(..., title="The ID of the current game"),
        pid: int = Path(..., title="The ID of the player who votes"),
        vote: str = Query(..., regex="^(nox|lumos)$")):

        if not check_match(gid):
            raise HTTPException(status_code=404, detail="Match not found")

        if not check_player_in_match(gid,pid):
            raise HTTPException(status_code=404, detail="Player not found")

        vote_director(pid, vote)

        return vote

