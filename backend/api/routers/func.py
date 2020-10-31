from pony.orm import db_session, select, count

from models import *

Status = {0: "Joinable",
          1: "In Game",
          2: "Finished"}

GovRolDiccionary = {0: "Head Master",
                    1: "Magic Minister",
                    3: "Citizen"}

BoardType = {0: "5-6",
             1: "7-8",
             2: "9-10"}

@db_session
def load_data_User():
    users = [
        ("mati@gmail.com", "mati", "123456"),
        ("manu@gmail.com", "manu", "123456"),
        ("cesar@gmail.com", "cesar", "123456"),
        ("guido@gmail.com", "guido", "123456"),
        ("joaquin@gmail.com", "joaquin", "123456"),
        ("rodri@gmail.com", "rodri", "123456")
    ]
    for mail, uname, upassword in users:
        user = User(Email=mail, Username=uname, Password=upassword)


@db_session
def load_data_player():
    players = [
        (1,1,0,0,0,False),
        (2,1,1,1,0,False),
        (3,1,2,2,0,False),
        (4,1,3,2,0,False),
        (5,1,4,2,0,False),
        (6,1,5,2,0,False)
    ]
    for user_id, match_id, position, secret_rol, gov_rol, is_dead in players:
        user = User.get(Id=user_id)
        match = Match.get(Id=match_id)
        player = Player(UserId=user, MatchId = match, Position = position, SecretRol = secret_rol, GovRol = gov_rol, IsDead = is_dead)
        User[user_id].Players += player
        match.Players += player

@db_session
def load_data_board():
    Board(BoardType=0,PhoenixProclamations=0,DeathEaterProclamations=0,FailedElectionsCount=0,Match=Match[1])

@db_session
def load_data_match():
    Match(Max_players=5, Min_players=6, Status=0, BoardType=0)

@db_session
def update_data_match_player(playerid,matchid):
    match = Match.get(Id=matchid)
    Player[playerid].MatchId = match

@db_session
def update_data_Board_Match(matchid,boardid):
    board = Board.get(Id=boardid)
    Match[matchid].Board = board


@db_session
def user_is_registred(name, upassword):
    try:
        u = User.get(Username = name, Password = upassword)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_username(name):
    try:
        u = User.get(Username = name)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_email(mail):
    try:
        u = User.get(Email = mail)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def get_playersid_from_user(username):
    try:
        u = (User.get(Username = username)).Players
        if u:
            return u
        else:
            return {}
    except Exception:
        return {}

@db_session
def add_user(username, password, email):
    try:
      User(Username = username, Password = password, Email = email)
      return True
    except Exception:
      return False

@db_session
def add_match(max_,min_,status,board):
    try:
        Match(Max_players=max_, Min_players=min_, Status=status, BoardType = board)
        return True
    except Exception:
        return False
        
@db_session
def get_match(ID):
    return Match[ID]

@db_session
def get_board(ID: int):
    return Match[ID].Board

@db_session
def get_match_status(ID: int):
    return Status[Match[ID].Status] #string

@db_session
def vote(ID):

@db_session
def get_player_votes(ID):
    players = Match[ID].Players.order_by(Player.Position)
    return {x.UserId.Username: x.Vote for x in players}

@db_session
def get_board_status(ID: int):
    board_attr = ["PhoenixProclamations", "DeathEaterProclamations"]
    board_status = Match[ID].Board.to_dict(board_attr)
    board_status['boardtype'] = BoardType[Match[ID].Board.BoardType]
    return board_status # dict

@db_session
def get_players_usernames(ID: int):
    players = Match[ID].Players.order_by(Player.Position)
    return [x.UserId.Username for x in players] #lista de user

@db_session
def get_minister_username(ID: int):
    minister = Match[ID].Players.filter(lambda p: p.GovRol == 0).first()
    return minister.UserId.Username #string

@db_session
def dump_boards():
    query = select(c for c in Board)
    return list(query)

@db_session
def dump_players(ID):
    return list(Match[ID].Players.order_by(Player.Position))

@db_session
def increment_failed_election_counter(ID: int):
    Match[ID].Board.FailedElectionsCount += 1

@db_session
def reset_election_counter(ID: int):
    Match[ID].Board.FailedElectionsCount = 0

@db_session
def enact_proclamation(ID: int, proclamation: str):
    if proclamation == "phoenix":
        Match[ID].Board.PhoenixProclamations += 1
    elif proclamation == "death eater":
        Match[ID].Board.DeathEaterProclamations += 1

@db_session
def get_available_spell(ID):
    return Match[ID].Board.AvailableSpell

@db_session
def unlock_spell(ID: int):
    board = Match[ID].Board
    death_eater_proclamations = board.DeathEaterProclamations
    if board.BoardType == 0:
        spell = unlock_spell_small_board(death_eater_proclamations)
    elif board.BoardType == 1:
        spell = unlock_spell_medium_board(death_eater_proclamations)
    elif board.BoardType == 2:
        spell = unlock_spell_big_board(death_eater_proclamations)
    board.AvailableSpell = spell
    

@db_session
def get_phoenix_proclamations(ID):
    return Match[ID].Board.PhoenixProclamations

@db_session
def get_death_eater_proclamations(ID):
    return Match[ID].Board.DeathEaterProclamations

@db_session
def activate_expelliarmus(ID):
    board = Match[ID].Board
    if board.DeathEaterProclamations == 5:
        board.Expelliarmus = True

@db_session
def unlock_spell_small_board(death_eater_proclamations):
    if death_eater_proclamations == 3:
        spell = "adivinacion"
    elif death_eater_proclamations > 3:
        spell = "avada kedavra"

    return spell

@db_session
def unlock_spell_medium_board(death_eater_proclamations):
    if death_eater_proclamations == 2:
        spell = "crucio"
    elif death_eater_proclamations == 3:
        spell = "imperio"
    elif death_eater_proclamations > 3:
        spell = "avada kedavra"

    return spell

@db_session
def unlock_spell_medium_board(death_eater_proclamations):
    if death_eater_proclamations in range(1,3):
        spell = "crucio"
    elif death_eater_proclamations == 3:
        spell = "imperio"
    elif death_eater_proclamations > 3:
        spell = "avada kedavra"

    return spell

def is_victory_from(ID: int):
    winner = None
    if get_death_eater_proclamations(ID) == 6:
        winner = "death eater"
    elif get_phoenix_proclamations(ID) == 5:
        winner = "phoenix"

    return winner