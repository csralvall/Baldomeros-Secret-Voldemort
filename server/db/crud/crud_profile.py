from pony.orm import db_session
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *

from server.db.crud.crud_lobby import *
from server.db.crud.crud_match import *


@db_session 
def user_is_registred(name: str, upassword: str):
    try:
        u = User.get(Username = name, Password = upassword)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_username(username: str):
    try: 
        u = User.exists(Username=username)
        return u 
    except Exception:
        return False

@db_session
def check_email(email: str):
    try: 
        u = User.exists(Email=email)
        return u 
    except Exception:
        return False

@db_session
def check_user(user_id: int):
    try: 
        u = User.exists(Id=user_id)
        return u 
    except Exception:
        return False

@db_session 
def get_user(username: str, password: str):
    user = User.get(Username=username, Password=password)
    if user is not None:
        user = user.to_dict("Id Username")
    return user

@db_session
def create_user(email: str, username: str, password: str):
    try:
        User(Email=email, Username=username, Password=password)
        return True
    except Exception:
        return False

@db_session
def get_finished_matches(user_id: int):
    finished_matches = []

    players = User[user_id].Players
    matches = []

    for p in players:
        matches.append(p.MatchId)

    matches.sort(reverse=True)

    for p in matches:
        if (get_match_status(p.Id) == 'Finished'):
            pid = get_player_id(p.Id, user_id)
            rol = get_player_rol(pid)
            winner = check_winner(p.Id)
            match_name = get_creator_username_match(p.Id)

            amIWinner = False
            if(rol == DEATH_EATER or rol == VOLDEMORT):
                if (winner == 'death eater' or winner == 'Voldemort is the director'):
                    amIWinner = True
            else:
                if (winner == 'phoenix' or winner == 'Voldemort died'):
                    amIWinner = True

            match = {
                "Match name": match_name,
                "secret rol": SecretRolDiccionary[rol],
                "winner": winner,
                "amIWinner": amIWinner
            }
            finished_matches.append(match)
    return finished_matches        

@db_session
def get_winrate(user_id: int):
    winrate_phoneix = 100
    winrate_voldemort = 100
    winrate_death_eater = 100
    winrate_total = 100 
    partidas_ganadas_phoenix = 0
    partidas_ganadas_death_eater = 0 
    partidas_ganadas_voldemort = 0 
    partidas_ganadas = 0 
    partidas_jugadas = 0
    partidas_jugadas_phoenix = 0
    partidas_jugadas_voldemort = 0
    partidas_jugadas_death_eater = 0

    winrates = []

    players = User[user_id].Players
    matches = []

    for p in players:
        matches.append(p.MatchId)

    matches.sort(reverse=True)
    
    for p in matches: 
        if (get_match_status(p.Id) == 'Finished'):
            pid = get_player_id(p.Id, user_id)
            rol = get_player_rol(pid)
            winner = check_winner(p.Id)
    
            partidas_jugadas += 1
            if (rol == 2):
                partidas_jugadas_phoenix += 1
                if (winner == 'phoenix' or winner == 'Voldemort died'):
                    partidas_ganadas_phoenix += 1
                    partidas_ganadas += 1

            elif (rol == 1):
                partidas_jugadas_death_eater += 1
                if (winner == 'death eater' or winner == 'Voldemort is the director'):
                    partidas_ganadas_death_eater += 1
                    partidas_ganadas += 1

            else:
                partidas_jugadas_voldemort += 1
                if (winner == 'death eater' or winner == 'Voldemort is the director'):
                    partidas_ganadas_voldemort += 1
                    partidas_ganadas += 1 

    if (partidas_jugadas == 0 ):
        partidas_jugadas = 1
    if (partidas_jugadas_voldemort == 0 ):
        partidas_jugadas_voldemort = 1
    if (partidas_jugadas_death_eater == 0 ):
        partidas_jugadas_death_eater = 1
    if (partidas_jugadas_phoenix == 0 ):
        partidas_jugadas_phoenix = 1

    wint = (partidas_ganadas / partidas_jugadas) * 100
    winv = (partidas_ganadas_voldemort / partidas_jugadas_voldemort) * 100
    wind = (partidas_ganadas_death_eater / partidas_jugadas_death_eater) * 100
    winp = (partidas_ganadas_phoenix / partidas_jugadas_phoenix) * 100

    import math
    winrates = {
        'winrate total': math.ceil(wint),
        'winrate as Voldemort': math.ceil(winv),
        'winrate as Death eater': math.ceil(wind),
        'winrate as Phoenix': math.ceil(winp)
    }
    return winrates

@db_session
def get_email(user_id: int):
    return User[user_id].Email

@db_session
def get_user_username(user_id: int):
    return User[user_id].Username

@db_session
def get_password(user_id: int):
    return User[user_id].Password

@db_session
def get_username_and_email(user_id: int):

    if not User.exists(Id=user_id):
        raise UserNotFound

    username = get_user_username(user_id)
    email = get_email(user_id)

    username_and_email = {
        "Username": username,
        "Email": email
    }

    return username_and_email

@db_session
def update_password(user_id: int, oldp: str, newp: str):

    if not User.exists(Id=user_id):
        raise UserNotFound
       
    if (User[user_id].Password==oldp):
        User[user_id].Password = newp
        return True

    else:
        return False

@db_session
def update_email(user_id: int, olde: str, newe: str):

    if not User.exists(Id=user_id):
        raise UserNotFound
       
    if (User[user_id].Email==olde):
        if not check_email(newe):
            User[user_id].Email = newe
            return True

    else:
        return False

    