from backend.db.crud import *

from fastapi import APIRouter, HTTPException, Query, Path

from typing import Optional

router = APIRouter()

@router.put("/game/{mid}/player/{pid}", tags=["Game"], status_code=200)
async def vote_candidate(
        mid: int = Path(..., title="The ID of the current game"),
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


