from pony.orm import db_session, select, count
from backend.db.database import *

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
def add_match(minp,maxp,creator):
    try:
        newmatch = Match(MaxPlayers=maxp,
            MinPlayers=minp,
            Status=0,
            BoardType=0, #hardcoded
            LastMinister = 0, #Changes when the match starts
            Creator = creator)
        return newmatch
    except :
        return None

@db_session
def add_board(newmatch):
    newboard = Board(BoardType = newmatch.BoardType,
        PhoenixProclamations = 0,
        DeathEaterProclamations = 0,
        FailedElectionsCount = 0,
        Match = newmatch)
    return newboard

@db_session
def add_user_in_match(user, matchid, position):
    mymatch = Match[matchid]
    newplayer = Player(Position = position,
        SecretRol = 0, #Changes when the match starts
        GovRol = 0, #Changes when the match starts
        IsDead = False,
        UserId = user,
        MatchId = mymatch)
    return newplayer

@db_session
def add_match_db(minp,maxp,uhid):
    if(minp>maxp):
        return None
    try:
        creator= User[uhid]
    except :
        return None
    
    match = add_match(minp,maxp,creator)
    if match is not None:
        matchId= match.to_dict("Id")["Id"]
        add_board(match)
        player = add_user_in_match(creator, matchId, 0)# add the creeator to player table 
        match_and_player = {
            "Match_id": matchId,
            "Player_id": player.to_dict("PlayerId")["PlayerId"]
        }
        return match_and_player
    else:
        return None

#needed for testing
@db_session
def delete_data(table):
    delete(p for p in table)

@db_session
def delete_user(email, username, password):
    user = User.get(Email=email, Username=username, Password=password)
    if user is not None:
        user.delete()

    return user
