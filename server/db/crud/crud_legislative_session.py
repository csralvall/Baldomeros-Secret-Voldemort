from pony.orm import db_session
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *


@db_session
def enact_proclamation(match_id: int, proclamation: str):
    if proclamation == PHOENIX_STR:
        Match[match_id].Board.PhoenixProclamations += 1
    elif proclamation == DEATH_EATER_STR:
        Match[match_id].Board.DeathEaterProclamations += 1

@db_session
def unlock_expelliarmus(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    board = Board[board_id]

    if board.DeathEaterProclamations >= 5:
        board.Expelliarmus = UNLOCKED

@db_session
def get_expelliarmus_status(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    status = Board[board_id].Expelliarmus

    return expelliarmus[status]

@db_session
def set_expelliarmus_status(board_id: int, status: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    board = Board[board_id]

    if board.DeathEaterProclamations >= 5 and status != LOCKED:
        board.Expelliarmus = status
