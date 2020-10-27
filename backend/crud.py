
from pony.orm import db_session, select, count
from .database import *

@db_session #Bool
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
def check_username(username):
    try: 
        u = User.exists(Username=username)
        return u 
    except Exception:
        return False

@db_session
def check_email(email):
    try: 
        u = User.exists(Email=email)
        return u 
    except Exception:
        return False

@db_session #get the User object.
def get_user(username, password):
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
def add_match_db(minp,maxp,uhid):
    try:
        creator= User[uhid]
        newmatch = Match(MaxPlayers=maxp,
            MinPlayers=minp,
            Status=0,
            BoardType=0, #Por ahora hardcodeado
            LastMinister = 0, #Cambia cuando empieza la partida
            Creator = creator)

        #inicializamos el tablero
        Board(BoardType = newmatch.BoardType,
            PhoenixProclamations = 0,
            DeathEaterProclamations = 0,
            FailedElectionsCount = 0,
            Match = newmatch
        )
        #agregamos al creador a la tabla player
        Player(Position = 0,
            SecretRol = 0, #definir en el inicio de partida
            GovRol = 0, #definir en el inicio de partida
            IsDead = False,
            UserId = creator,
            MatchId = newmatch
        )
        return True
    except Exception:
        return False


#needed for testing
@db_session
def delete_data(table):
    delete(p for p in table)

