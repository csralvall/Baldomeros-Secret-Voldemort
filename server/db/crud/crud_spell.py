from pony.orm import db_session
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *



@db_session
def unlock_spell(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    board = Match[match_id].Board
    death_eater_proclamations = board.DeathEaterProclamations
    if board.BoardType == SMALL_BOARD:
        spell = unlock_spell_small_board(death_eater_proclamations)
    elif board.BoardType == MEDIUM_BOARD:
        spell = unlock_spell_medium_board(death_eater_proclamations)
    elif board.BoardType == BIG_BOARD:
        spell = unlock_spell_big_board(death_eater_proclamations)

    board.AvailableSpell = spell

    return spell

@db_session
def unlock_spell_small_board(death_eater_proclamations: int):
    if death_eater_proclamations == 3:
        spell = ADIVINATION
    elif death_eater_proclamations > 3:
        spell = AVADA_KEDAVRA
    else:
        spell = NO_SPELL

    return spell

@db_session
def unlock_spell_medium_board(death_eater_proclamations: int):
    if death_eater_proclamations == 2:
        spell = CRUCIO
    elif death_eater_proclamations == 3:
        spell = IMPERIO
    elif death_eater_proclamations > 3:
        spell = AVADA_KEDAVRA
    else:
        spell = NO_SPELL

    return spell

@db_session
def unlock_spell_big_board(death_eater_proclamations: int):
    if death_eater_proclamations in range(1,3):
        spell = CRUCIO
    elif death_eater_proclamations == 3:
        spell = IMPERIO
    elif death_eater_proclamations > 3:
        spell = AVADA_KEDAVRA
    else:
        spell = NO_SPELL

    return spell

@db_session
def get_available_spell(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    return Board[board_id].AvailableSpell

@db_session
def disable_spell(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    Board[board_id].AvailableSpell = NO_SPELL

@db_session
def imperio(board_id: int, player_id: int):
    if not Player.exists(PlayerId=player_id):
        raise PlayerNotFound

    if not Board.exists(Id=board_id):
        raise BoardNotFound

    Player[player_id].GovRol = IMPERIO_MINISTER
    Board[board_id].AvailableSpell = NO_SPELL

@db_session
def avada_kedavra(board_id: int, player_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    if not Player.exists(PlayerId=player_id):
        raise PlayerNotFound

    Player[player_id].IsDead = True
    Board[board_id].AvailableSpell = NO_SPELL
    