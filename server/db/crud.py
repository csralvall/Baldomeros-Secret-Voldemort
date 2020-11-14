from pony.orm import db_session, select, count
from server.db.database import *
from server.db.dicts import *

class NotEnoughProclamations(Exception):
    """ Raised when there are only two cards available
    to take on the deck. """
    def __init__(
        self,
        proclamations,
        message="proclamations in deck are less than 3"):
        self.proclamations = proclamations
        self.message = message

    def __str__(self):
        return f'Proclamations = {self.proclamations} -> {self.message}'

class ResourceNotFound(Exception):
    """ Raised when the resource searched does not exist. """
    pass

class DeckNotFound(ResourceNotFound):
    """ Raised when there is not deck with the parameters passed. """
    pass

class BoardNotFound(ResourceNotFound):
    """ Raised when there is not board with the parameters passed. """
    pass

class MatchNotFound(ResourceNotFound):
    """ Raised when there is not match with the parameters passed. """
    pass

class PlayerNotFound(ResourceNotFound):
    """ Raised when there is not player with the parameters passed. """
    pass

class InvalidProclamation(Exception):
    """ Raised when the proclamation passed is invalid. """
    pass

class EmptySelectedProclamations(Exception):
    """ Raised when there aren't selected proclamations to remove. """
    pass

class BadIngameStatus(Exception):
    """ Raised when the ingame status passed is invalid. """
    pass

class NoDirector(Exception):
    """ Raised when moving director to ex-director, but there is no current director. """
    pass

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
            CurrentMinister = 0, #Changes when the match starts
            CandidateDirector = NO_DIRECTOR,
            CurrentDirector = NO_DIRECTOR,
            Winner = "no winner yet",
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
def add_user_in_match(userid, matchid, position):
    try:
        mymatch = Match[matchid]
        myuser= User[userid]
    except Exception:
        return None
    newplayer = Player(Position = position,
        SecretRol = 0, #Changes when the match starts
        GovRol = 2, #Changes when the match starts
        IsDead = False,
        UserId = myuser,
        MatchId = mymatch)
    return newplayer#need to refactor so it only returns id

@db_session
def check_player_in_match(gid: int, pid: int):
    if Match.exists(Id=gid):
        return exists(p for p in Match[gid].Players if p.PlayerId == pid)
    return False

@db_session
def add_match_db(minp, maxp, uhid):
    if(minp > maxp):
        return None
    try:
        creator= User[uhid]
    except Exception:
        return None
    
    match = add_match(minp, maxp, creator)
    if match is not None:
        matchId= match.to_dict("Id")["Id"]
        add_board(match)
        player = add_user_in_match(uhid, matchId, 0)# add the creator to player table 
        player.GovRol = 1
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
    except Exception:
        return False

@db_session
def create_deck(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    available = []
    for i in range(0,6):
        available.append("phoenix")
    for i in range(0,11):
        available.append("death eater")

    size = len(available)
    cards = {'available': available, 'discarded': [], 'selected': []}
    try:
        Deck(Discarded=0,Available=size,Cards=cards,Board=board_id)
        return True
    except Exception:
        return False

@db_session
def get_selected_card(board_id: int):
    if not Deck.exists(Board=board_id):
        raise DeckNotFound

    deck = Deck.get(Board=board_id)
    if not deck.Cards['selected']:
        raise EmptySelectedProclamations

    deck.Cards['selected'].reverse()
    return deck.Cards['selected'].pop()

@db_session
def show_selected_deck(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    deck = Board[board_id].Proclamations
    if deck is None:
        raise DeckNotFound

    return deck.Cards['selected']
    
@db_session
def shuffle_deck(board_id: int):
    import random
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        available = deck.Cards['available']
        random.shuffle(available)
        return True
    return False

@db_session
def get_top_proclamation(board_id: int):
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        if deck.Available > 0:
            card = deck.Cards['available'].pop()
            deck.Available -= 1
            deck.Cards['selected'].append(card)
            return True
        else:
            raise NotEnoughProclamations(deck.Available)
    else:
        raise DeckNotFound

@db_session
def get_top_three_proclamation(board_id:int):
    if not Deck.exists(Board=board_id):
        raise DeckNotFound        
    deck = Deck.get(Board=board_id)
    if deck.Available > 2:
        raise NotEnoughProclamations(deck.Available)
    for i in range(0,3):
        get_top_proclamation(board_id)
    return True

@db_session
def discard_proclamation(board_id: int, proclamation: str):
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        if proclamation in deck.Cards['selected']:
            deck.Cards['selected'].remove(proclamation)
            deck.Cards['discarded'].append(proclamation)
            deck.Discarded += 1
            return True
        else:
            raise InvalidProclamation
    else:
        raise DeckNotFound

@db_session
def refill_deck(board_id: int):
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        discarded = deck.Cards['discarded']
        deck.Cards['available'] += discarded
        deck.Available = len(deck.Cards['available'])
        deck.Cards['discarded'] = []
        deck.Discarded = 0
        return True
    else:
        raise DeckNotFound

@db_session
def deck_status(board_id: int):
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        deck_attributes = ['Available', 'Discarded']
        return deck.to_dict(deck_attributes)
    else:
        raise DeckNotFound

@db_session
def vote_director(player_id: int, vote: str):
    if vote == 'nox':
        Player[player_id].Vote = 0
    elif vote == 'lumos':
        Player[player_id].Vote = 1
    elif vote == 'missing vote':
        Player[player_id].Vote = 2


@db_session
def get_minister_username(ID: int): 
    minister = Match[ID].Players.filter(lambda p: p.GovRol == 1).first()
    if minister is None:
        return "No minister yet"
    return minister.UserId.Username


@db_session
def get_director_username(ID: int):
    director = Match[ID].Players.filter(lambda p: p.GovRol == 0).first()
    if director is None:
        return "No director yet"
    return director.UserId.Username 

@db_session
def change_ingame_status(match_id: int, status: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    if not (status >= NOMINATION and status <= USE_SPELL) :
        raise BadIngameStatus
    bid= get_match_board_id(match_id)
    Board[bid].BoardStatus=status

@db_session
def get_ingame_status(match_id: int):
    bid= get_match_board_id(match_id)
    return ingame_status[Board[bid].BoardStatus]


@db_session
def get_match_status(ID: int):
    return Status[Match[ID].Status] 

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
    board_status['spell'] = spells[Board[board_id].AvailableSpell]
    board_status['status'] = ingame_status[Board[board_id].BoardStatus]
    board_status['boardtype'] = BoardType[Board[board_id].BoardType]

    return board_status    

@db_session
def check_match(mid):
    return Match.exists(Id=mid)

@db_session
def get_all_player_status(match_id: int): 
    def replace(vote: int):
        result = 'missing vote'
        if vote == 0:
            result = 'nox'
        elif vote == 1:
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
def get_player_id(match_id: int, user_id: int):
    if Match.exists(Id=match_id):
        player = get(p for p in Match[match_id].Players if p.UserId.Id == user_id)
        if player is not None:
            return player.PlayerId

@db_session
def set_next_minister(match_id: int):
    if Match.exists(Id=match_id):
        query = Match[match_id].Players.order_by(Player.Position)
        players = [x for x in query]
        last_minister = Match[match_id].CurrentMinister
        players[last_minister].GovRol = 3#exminister
        current_minister = (last_minister + 1) % len(players)
        players[current_minister].GovRol = 1
        Match[match_id].CurrentMinister = current_minister
        return current_minister


@db_session
def set_next_minister_failed_election(match_id: int):
    if Match.exists(Id=match_id):
        query = Match[match_id].Players.order_by(Player.Position)
        players = [x for x in query]
        last_minister = Match[match_id].CurrentMinister
        players[last_minister].GovRol = 2#magician
        current_minister = (last_minister + 1) % len(players)
        players[current_minister].GovRol = 1
        Match[match_id].CurrentMinister = current_minister
        return current_minister

@db_session
def change_to_exdirector(mid):
    if not Match.exists(Id=mid):
        raise MatchNotFound
    query = Match[mid].Players.order_by(Player.Position)
    players = [x for x in query]
    director = Match[mid].CurrentDirector
    if director == NO_DIRECTOR:
        raise NoDirector
    players[director].GovRol = 4 #Ex Director.
    Match[mid].CurrentDirector = NO_DIRECTOR

@db_session
def successful_director_election(mid):
    if not Match.exists(Id=mid):
        raise MatchNotFound
    query = Match[mid].Players.order_by(Player.Position)
    players = [x for x in query]
    candidate_director = Match[mid].CandidateDirector
    if candidate_director == NO_DIRECTOR:
        raise NoDirector
    players[candidate_director].GovRol = 0 #director
    Match[mid].CandidateDirector = NO_DIRECTOR
    Match[mid].CurrentDirector = candidate_director


@db_session
def failed_director_election(mid):
    if not Match.exists(Id=mid):
        raise MatchNotFound
    query = Match[mid].Players.order_by(Player.Position)
    players = [x for x in query]
    candidate_director = Match[mid].CandidateDirector
    if candidate_director == NO_DIRECTOR:
        raise NoDirector
    players[candidate_director].GovRol = 2#magician
    Match[mid].CandidateDirector = NO_DIRECTOR
    Match[mid].CurrentDirector = NO_DIRECTOR


@db_session
def set_next_candidate_director(mid,pos):
    if Match.exists(Id=mid):
        Match[mid].CandidateDirector = pos

@db_session
def compute_election_result(match_id: int):
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        lumos = 0
        voting_cutoff = 0.5000001
        result = 'nox'
        if not exists(p for p in players if p.Vote == 2):
            total = count(p for p in players)
            lumos = count(p for p in players if p.Vote == 1)
            lumos = lumos/total
        else:
            result = 'missing vote'

        if lumos > voting_cutoff:
            result = 'lumos'

        return result

@db_session
def restore_election(match_id: int): 
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            p.Vote = 2

@db_session
def enact_proclamation(match_id: int, proclamation: str):
    if proclamation == "phoenix":
        Match[match_id].Board.PhoenixProclamations += 1
    elif proclamation == "death eater":
        Match[match_id].Board.DeathEaterProclamations += 1

@db_session
def get_phoenix_proclamations(match_id: int): 
    return Match[match_id].Board.PhoenixProclamations

@db_session
def get_death_eater_proclamations(match_id):
    return Match[match_id].Board.DeathEaterProclamations

@db_session
def is_victory_from(match_id: int):
    if Match.exists(Id=match_id):
        if not Match[match_id].Winner == "no winner yet":
            return Match[match_id].Winner
        winner = "no winner yet"
        if get_death_eater_proclamations(match_id) == 6:
            winner = "death eater"
            Match[match_id].Status = 2
        elif get_phoenix_proclamations(match_id) == 5:
            winner = "phoenix"
            Match[match_id].Status = 2

        Match[match_id].Winner = winner
        return winner

@db_session
def check_winner(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].Winner

@db_session
def change_match_status(mid,status):
    Match[mid].Status = status

@db_session
def check_host(user_id):
    try: 
        u = Match.exists(Creator=user_id)
        return u 
    except Exception:
        return False

@db_session
def get_num_players(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            n = n + 1 
    return n  

@db_session
def get_num_phoenix(match_id: int): # to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == 2):
                n = n + 1 
    return n 

@db_session
def get_num_magicians(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.GovRol == 2 or p.GovRol == 3 or p.GovRol == 4):
                n = n + 1 
    return n    


@db_session
def get_num_death(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == 1):
                n = n + 1 
    return n     

@db_session
def get_num_minister(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.GovRol == 1):
                n = n + 1 
    return n    

@db_session
def get_num_voldemort(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == 0):
                n = n + 1 
    return n 

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
            p.SecretRol = 2
            phoenix = phoenix - 1
        elif (death > 0):
            p.SecretRol = 1
            death = death - 1
        else:
            p.SecretRol = 0

@db_session
def set_gob_roles(match_id: int):
    import random
    players = Match[match_id].Players   
    k = random.randint(0,(get_num_players(match_id) - 1))
    Match[match_id].CurrentMinister = k
    
    for p in players:
        if (p.Position == k):
            p.GovRol = 1
        else:
            p.GovRol = 2

@db_session# no estaba la db session, tiene que ir ?
def change_player_rol(pid,rol):
    Player[pid].SecretRol = rol

@db_session
def get_min_players(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].MinPlayers

@db_session
def get_player_rol(pid):
    return SecretRolDiccionary[Player[pid].SecretRol]

@db_session
def get_user_username(uid):
    return User[uid].Username

@db_session
def get_player_username(pid):
    return (User[(Player[pid].UserId).Id].Username)

@db_session
def change_player_rol(pid,rol):
    Player[pid].SecretRol = rol

@db_session
def get_posible_directors(mid):
    players_alive_in_match = select(p for p in Match[mid].Players if p.IsDead == False)
    posible_directors = list()
    for p in players_alive_in_match:
        if (p.GovRol != 3 and p.GovRol != 4):
            posible_directors.append(get_player_username(p.PlayerId))

    return {"posible directors": posible_directors}

@db_session
def get_death_eater_players_in_match(mid):
    players_death_eaters = select(p for p in Match[mid].Players if p.SecretRol == 1)
    deatheaters = list()
    player_voldemort = select(p for p in Match[mid].Players if p.SecretRol == 0).first()
    voldemort = get_player_username(player_voldemort.PlayerId)

    for p in players_death_eaters:
        deatheaters.append(get_player_username(p.PlayerId))
    return {"Death Eater": deatheaters, "Voldemort": voldemort}

@db_session
def avada_kedavra(board_id: int, player_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    if not Player.exists(PlayerId=player_id):
        raise PlayerNotFound

    Player[player_id].IsDead = True
    Board[board_id].AvailableSpell = NO_SPELL

@db_session
def get_player_id_from_username(match_id: int, username: str):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    players = Match[match_id].Players
    return get(p.PlayerId for p in players if p.UserId.Username == username)

