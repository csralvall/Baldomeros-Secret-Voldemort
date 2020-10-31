from pony.orm import db_session, select, count
from backend.db.database import *
from backend.db.dicts import *

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
def add_user_in_match(userid, matchid, position):
    try:
        mymatch = Match[matchid]
        myuser= User[userid]
    except :
        return None
    newplayer = Player(Position = position,
        SecretRol = 0, #Changes when the match starts
        GovRol = 0, #Changes when the match starts
        IsDead = False,
        UserId = myuser,
        MatchId = mymatch)
    return newplayer

@db_session
def check_player_in_match(gid: int, pid: int): # need testsing
    if Match.exists(Id=gid):
        return exists(p for p in Match[gid].Players if p.PlayerId == pid)
    return False

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
        player = add_user_in_match(uhid, matchId, 0)# add the creeator to player table 
        match_and_player = {
            "Match_id": matchId,
            "Player_id": player.to_dict("PlayerId")["PlayerId"]
        }
        return match_and_player
    else:
        return None

@db_session
def there_is_space(mid):
    try: 
        players = Match[mid].Players
        MaxPlayers = Match[mid].MaxPlayers
        if (len(players) < MaxPlayers):
            return True
        else:
            return False
    except :
        return False

@db_session
def vote_director(player_id: int, vote: str): # need testing
    if vote == 'nox':
        Player[player_id].Vote = 0
    elif vote == 'lumos':
        Player[player_id].Vote = 1
    elif vote == 'missing vote':
        Player[player_id].Vote = 2


@db_session
def delete_data(table): # needed for testing
    delete(p for p in table)

@db_session
def delete_user(email, username, password): # needed for testing
    user = User.get(Email=email, Username=username, Password=password)
    if user is not None:
        user.delete()

    return user

@db_session
def get_minister_username(ID: int): # need testing
    minister = Match[ID].Players.filter(lambda p: p.GovRol == 0).first()
    return minister.UserId.Username 

@db_session
def get_match_status(ID: int): # need testing
    return Status[Match[ID].Status] 

@db_session
def get_board_status(ID: int): # need testing
    board_attr = ["PhoenixProclamations", "DeathEaterProclamations"]
    board_status = Match[ID].Board.to_dict(board_attr)
    board_status['boardtype'] = BoardType[Match[ID].Board.BoardType]
    return board_status    

@db_session
def check_match(mid): # need testing
    return Match.exists(Id=mid)


@db_session
def get_player_votes(match_id: int): # need testing
    def replace(vote: int):
        result = 'missing vote'
        if vote == 0:
            result = 'nox'
        elif vote == 1:
            result = 'lumos'
        return result

    players = Match[match_id].Players.order_by(Player.Position)
    return {x.UserId.Username: replace(x.Vote) for x in players}        

@db_session
def get_player_id(match_id: int, user_id: int): # need testing
    if Match.exists(Id=match_id):
        player = get(p for p in Match[match_id].Players if p.UserId.Id == user_id)
        return player.PlayerId
