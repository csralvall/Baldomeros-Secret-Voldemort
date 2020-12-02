from pony.orm import db_session, select
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *


@db_session
def eliminate_player_from_match(match_id: int, player_id: int):
    if not Player.exists(PlayerId = player_id):
        raise PlayerNotFound
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    Player[player_id].delete()

@db_session
def eliminate_all_players_from_match(match_id: int):
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    players = Match[match_id].Players
    for p in players:
        p.delete()

@db_session
def add_match(minp: int, maxp: str, creator):
    try:
        newmatch = Match(MaxPlayers=maxp,
            MinPlayers=minp,
            Status=JOINABLE,
            BoardType=SMALL_BOARD,
            CurrentMinister = 0, 
            CandidateDirector = NO_DIRECTOR,
            CurrentDirector = NO_DIRECTOR,
            Winner = NO_WINNER_YET,
            Creator = creator)
        return newmatch
    except Exception:
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
def add_user_in_match(userid: int, matchid: int, position: int):
    try:
        mymatch = Match[matchid]
        myuser= User[userid]
    except Exception:
        return None
    newplayer = Player(Position = position,
        SecretRol = VOLDEMORT, 
        GovRol = MAGICIAN, 
        IsDead = False,
        UserId = myuser,
        MatchId = mymatch)
    return newplayer

@db_session
def add_match_db(minp: int, maxp: int, user_id: int):
    if(minp > maxp):
        return None
    try:
        creator= User[user_id]
    except Exception:
        return None
    
    match = add_match(minp, maxp, creator)
    if match is not None:
        matchId= match.to_dict("Id")["Id"]
        add_board(match)
        player = add_user_in_match(user_id, matchId, 0)
        player.GovRol = 1
        match_and_player = {
            "Match_id": matchId,
            "Player_id": player.to_dict("PlayerId")["PlayerId"]
        }
        return match_and_player
    else:
        return None

@db_session
def restart_positions(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    players = Match[match_id].Players
    position = 0
    for p in players:
        p.Position = position
        position += 1
        
@db_session
def there_is_space(match_id: int):
    try: 
        players = Match[match_id].Players
        MaxPlayers = Match[match_id].MaxPlayers
        if (len(players) < MaxPlayers):
            return True
        else:
            return False
    except Exception:
        return False

@db_session
def get_creator_username_match(match_id: int):
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    return Match[match_id].Creator.Username

@db_session
def get_min_players(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].MinPlayers

@db_session
def get_max_players(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].MaxPlayers

@db_session
def get_creator_id_match(match_id: int):
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    return Match[match_id].Creator.Id
    
@db_session
def set_game_decorated(match_id: int): 
    if not Match.exists(Id=match_id):
        raise MatchNotFound

    creator = Match[match_id].Creator
    minp = get_min_players(match_id)
    maxp = get_max_players(match_id) 
    match = match_id

    game = {
        "Nombre_partida": creator.to_dict("Username")["Username"],
        "Min_and_Max": (minp,maxp),
        "Match_id": match
    }
    return game

@db_session
def list_games_db():

    matches = select(p for p in Match)
    decorated_matches = []

    for p in matches:
        if (p.Status == JOINABLE):

            match_id = p.Id
            game_decorated = set_game_decorated(match_id)

            decorated_matches.append(game_decorated)
    
    return decorated_matches
    