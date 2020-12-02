from pony.orm import db_session, select
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *

from server.db.crud.crud_spell import *


@db_session
def check_match(match_id: int):
    return Match.exists(Id=match_id)
    
@db_session
def check_player_in_match(match_id: int, player_id: int):
    if Match.exists(Id=match_id):
        return exists(p for p in Match[match_id].Players if p.PlayerId == player_id)
    return False

@db_session
def get_minister_username(match_id: int):
    all_players = Match[match_id].Players
    imp_min = get(p for p in all_players if p.GovRol == IMPERIO_MINISTER)
    if imp_min is not None:
        return imp_min.UserId.Username
    minister = Match[match_id].Players.filter(lambda p: p.GovRol == MINISTER).first()
    if minister is None:
        return "No minister yet"
    return minister.UserId.Username

@db_session
def get_director_username(match_id: int):
    director = Match[match_id].Players.filter(lambda p: p.GovRol == 0).first()
    if director is None:
        return "No director yet"
    return director.UserId.Username 

@db_session
def get_ingame_status(match_id: int):
    board_id= get_match_board_id(match_id)
    return Board[board_id].BoardStatus

@db_session
def get_match_status(match_id: int):
    return Status[Match[match_id].Status] 

@db_session
def get_match_board_id(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound

    board = Match[match_id].Board

    if board is None:
        raise BoardNotFound

    return board.Id

@db_session
def get_board_status(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    board_attr = ["PhoenixProclamations", "DeathEaterProclamations"]
    board_status = Board[board_id].to_dict(board_attr)
    board_status['spell'] = spells[get_available_spell(board_id)]
    board_status['expelliarmus'] = expelliarmus[Board[board_id].Expelliarmus]
    board_status['status'] = ingame_status[Board[board_id].BoardStatus]
    board_status['boardtype'] = BoardType[Board[board_id].BoardType]
    board_status['failcounter'] = Board[board_id].FailedElectionsCount
    return board_status 

@db_session
def get_all_player_status(match_id: int): 
    def replace(vote: int):
        result = 'missing vote'
        if vote == NOX:
            result = 'nox'
        elif vote == LUMOS:
            result = 'lumos'
        return result

    if not Match.exists(Id=match_id):
        raise MatchNotFound
        
    players = Match[match_id].Players.order_by(Player.Position)
    status = {
        p.UserId.Username: {"vote": replace(p.Vote), "isDead": p.IsDead}
        for p in players
    }        

    return status

@db_session
def change_ingame_status(match_id: int, status: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    if not (status >= NOMINATION and status <= EXPELLIARMUS) :
        raise BadIngameStatus
    board_id= get_match_board_id(match_id)
    Board[board_id].BoardStatus=status

@db_session
def get_player_id(match_id: int, user_id: int):
    if Match.exists(Id=match_id):
        player = get(p for p in Match[match_id].Players if p.UserId.Id == user_id)
        if player is not None:
            return player.PlayerId

@db_session
def check_voldemort(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    if get_death_eater_proclamations(match_id)>2:
        director = get_director_username(match_id)
        director_player_id = get_player_id_from_username(match_id, director)
        director_secret_rol= Player[director_player_id].SecretRol
        return director_secret_rol == VOLDEMORT
    else:
        return False

@db_session
def get_player_position(player_id: int):
    if Player.exists(PlayerId=player_id):
        return Player[player_id].Position
    else:
        raise PlayerNotFound

@db_session
def get_user_id_from_player_id(match_id: int, player_id: int):
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    if not Player.exists(PlayerId = player_id):
        raise PlayerNotFound
    return Player[player_id].UserId.Id

@db_session
def get_player_id_from_username(match_id: int, username: str):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    players = Match[match_id].Players
    return get(p.PlayerId for p in players if p.UserId.Username == username)

@db_session
def get_death_eater_players_in_match(match_id: int):
    players_death_eaters = select(p for p in Match[match_id].Players if p.SecretRol == DEATH_EATER)
    deatheaters = list()
    player_voldemort = select(p for p in Match[match_id].Players if p.SecretRol == VOLDEMORT).first()
    voldemort = get_player_username(player_voldemort.PlayerId)

    for p in players_death_eaters:
        deatheaters.append(get_player_username(p.PlayerId))
    return {"Death Eater": deatheaters, "Voldemort": voldemort}

@db_session
def get_player_rol(player_id: int):
    return Player[player_id].SecretRol

@db_session
def get_player_username(player_id: int):
    return (User[(Player[player_id].UserId).Id].Username)

@db_session
def set_board_type(board_id: int, number_of_players: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound
    if number_of_players<=6:
        Board[board_id].BoardType = SMALL_BOARD
    elif number_of_players<=8:
        Board[board_id].BoardType = MEDIUM_BOARD
    elif number_of_players<=10:
        Board[board_id].BoardType = BIG_BOARD

@db_session
def get_num_players(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            n = n + 1 
    return n      

@db_session
def set_gob_roles(match_id: int):
    import random
    players = Match[match_id].Players   
    k = random.randint(0,(get_num_players(match_id) - 1))
    Match[match_id].CurrentMinister = k
    
    for p in players:
        if (p.Position == k):
            p.GovRol = MINISTER
        else:
            p.GovRol = MAGICIAN

@db_session
def set_roles(num: int, match_id: int):
    import random
    phoenix = (num // 2) + 1  
    death = (num - phoenix) - 1
    players = Match[match_id].Players  
    playersids = []

    for p in players:
        playersids.append(p.PlayerId)

    random.shuffle(playersids)

    for id in playersids:
        p = Player[id]
        if (phoenix > 0):
            p.SecretRol = PHOENIX
            phoenix = phoenix - 1
        elif (death > 0):
            p.SecretRol = DEATH_EATER
            death = death - 1
        else:
            p.SecretRol = VOLDEMORT

@db_session
def check_host(user_id: int):
    try: 
        u = Match.exists(Creator=user_id)
        return u 
    except Exception:
        return False

@db_session
def change_match_status(match_id: int, status: int):
    Match[match_id].Status = status

@db_session
def set_winner(match_id: int, winner: str):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    Match[match_id].Winner = winner
    Match[match_id].Status = FINISHED

@db_session
def check_winner(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].Winner

@db_session
def is_voldemort_dead(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    players = Match[match_id].Players
    voldemort =  select(p for p in players if p.SecretRol == VOLDEMORT).first()
    if voldemort is None:
        raise VoldemortNotFound
    return voldemort.IsDead

@db_session
def get_phoenix_proclamations(match_id: int): 
    return Match[match_id].Board.PhoenixProclamations

@db_session
def get_death_eater_proclamations(match_id: int):
    return Match[match_id].Board.DeathEaterProclamations

@db_session
def is_victory_from(match_id: int):
    if Match.exists(Id=match_id):
        if not Match[match_id].Winner == NO_WINNER_YET:
            return Match[match_id].Winner
        winner = NO_WINNER_YET
        if get_death_eater_proclamations(match_id) == 6:
            winner = DEATH_EATER_STR
            Match[match_id].Status = FINISHED
        elif get_phoenix_proclamations(match_id) == 5:
            winner = PHOENIX_STR
            Match[match_id].Status = FINISHED

        Match[match_id].Winner = winner
        return winner
        