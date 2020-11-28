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

class UserNotFound(ResourceNotFound):
    """ Raised when there is not User with the parameters passed. """
    pass

class VoldemortNotFound(ResourceNotFound):
    """ Raised when there is not Voldemort within the game. """
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

@db_session #get the User object.
def get_user(username: str, password: str):
    user = User.get(Username=username, Password=password)
    if user is not None:
        user = user.to_dict("Id Username")
    return user

@db_session
def eliminate_player_from_match(match_id: int, player_id: int):
    if not Player.exists(PlayerId = player_id):
        raise PlayerNotFound
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    Player[player_id].delete()


@db_session
def create_user(email: str, username: str, password: str):
    try:
        User(Email=email, Username=username, Password=password)
        return True
    except Exception:
        return False

@db_session
def add_match(minp: int, maxp: str, creator):
    try:
        newmatch = Match(MaxPlayers=maxp,
            MinPlayers=minp,
            Status=JOINABLE,
            BoardType=SMALL_BOARD, #hardcoded_hay que cambiarlo cuando empieza la partida
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
    return newplayer#need to refactor so it only returns id

@db_session
def check_player_in_match(match_id: int, player_id: int):
    if Match.exists(Id=match_id):
        return exists(p for p in Match[match_id].Players if p.PlayerId == player_id)
    return False

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
        player = add_user_in_match(user_id, matchId, 0)# add the creator to player table 
        player.GovRol = 1
        match_and_player = {
            "Match_id": matchId,
            "Player_id": player.to_dict("PlayerId")["PlayerId"]
        }
        return match_and_player
    else:
        return None

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
def create_deck(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    available = []
    for i in range(0,6):
        available.append(PHOENIX_STR)
    for i in range(0,11):
        available.append(DEATH_EATER_STR)

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
    if not deck.Available > 2:
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
        Player[player_id].Vote = NOX
    elif vote == 'lumos':
        Player[player_id].Vote = LUMOS
    elif vote == 'missing vote':
        Player[player_id].Vote = MISSING_VOTE


@db_session
def get_minister_username(match_id: int): 
    minister = Match[match_id].Players.filter(lambda p: p.GovRol == 1).first()
    if minister is None:
        return "No minister yet"
    return minister.UserId.Username

@db_session
def get_candidate_director_username(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    query = Match[match_id].Players.order_by(Player.Position)
    players = [x for x in query]
    candidate_director = Match[match_id].CandidateDirector
    if candidate_director == NO_DIRECTOR:
        return "No director candidate yet"
    return players[candidate_director].UserId.Username

@db_session
def get_director_username(match_id: int):
    director = Match[match_id].Players.filter(lambda p: p.GovRol == 0).first()
    if director is None:
        return "No director yet"
    return director.UserId.Username 

@db_session
def change_ingame_status(match_id: int, status: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    if not (status >= NOMINATION and status <= EXPELLIARMUS) :
        raise BadIngameStatus
    board_id= get_match_board_id(match_id)
    Board[board_id].BoardStatus=status

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
def get_available_spell(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    return Board[board_id].AvailableSpell

@db_session
def check_match(match_id: int):
    return Match.exists(Id=match_id)

#no habria que llamar a el dict de voteType?
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
def get_player_id(match_id: int, user_id: int):
    if Match.exists(Id=match_id):
        player = get(p for p in Match[match_id].Players if p.UserId.Id == user_id)
        if player is not None:
            return player.PlayerId

@db_session
def set_next_minister(match_id: int):
    if Match.exists(Id=match_id):
        query = Match[match_id].Players.order_by(Player.Position)
        exMinister = [x for x in query if x.GovRol==3]
        if len(exMinister):
            exMinister[0].GovRol = MAGICIAN
        players = [x for x in query]
        last_minister = Match[match_id].CurrentMinister
        players[last_minister].GovRol = EX_MINISTER
        current_minister = (last_minister + 1) % len(players)
        while players[current_minister].IsDead:
            current_minister = (current_minister + 1) % len(players)
        players[current_minister].GovRol = MINISTER
        Match[match_id].CurrentMinister = current_minister
        return current_minister

@db_session
def set_next_minister_failed_election(match_id: int):
    if Match.exists(Id=match_id):
        query = Match[match_id].Players.order_by(Player.Position)
        players = [x for x in query]
        last_minister = Match[match_id].CurrentMinister
        players[last_minister].GovRol = MAGICIAN
        current_minister = (last_minister + 1) % len(players)
        while players[current_minister].IsDead:
            current_minister = (current_minister + 1) % len(players)
        players[current_minister].GovRol = MINISTER
        Match[match_id].CurrentMinister = current_minister
        return current_minister

@db_session
def change_to_exdirector(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    query = Match[match_id].Players.order_by(Player.Position)
    players = [x for x in query]
    director = Match[match_id].CurrentDirector
    if director == NO_DIRECTOR:
        raise NoDirector
    exDirector = [x for x in query if x.GovRol==4]
    if len(exDirector) > 0:
        exDirector[0].GovRol = MAGICIAN
    players[director].GovRol = EX_DIRECTOR
    Match[match_id].CurrentDirector = NO_DIRECTOR

@db_session
def successful_director_election(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    query = Match[match_id].Players.order_by(Player.Position)
    players = [x for x in query]
    candidate_director = Match[match_id].CandidateDirector
    if candidate_director == NO_DIRECTOR:
        raise NoDirector
    players[candidate_director].GovRol = DIRECTOR
    Match[match_id].CandidateDirector = NO_DIRECTOR
    Match[match_id].CurrentDirector = candidate_director


@db_session
def failed_director_election(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    query = Match[match_id].Players.order_by(Player.Position)
    players = [x for x in query]
    candidate_director = Match[match_id].CandidateDirector
    if candidate_director == NO_DIRECTOR:
        raise NoDirector
    players[candidate_director].GovRol = MAGICIAN
    Match[match_id].CandidateDirector = NO_DIRECTOR
    Match[match_id].CurrentDirector = NO_DIRECTOR

@db_session
def failed_director_expelliarmus(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    query = Match[match_id].Players.order_by(Player.Position)
    players = [x for x in query]
    current_director = Match[match_id].CurrentDirector
    if current_director == NO_DIRECTOR:
        raise NoDirector
    players[current_director].GovRol = MAGICIAN
    Match[match_id].CandidateDirector = NO_DIRECTOR
    Match[match_id].CurrentDirector = NO_DIRECTOR


@db_session
def set_next_candidate_director(match_id: int, pos: int):
    if Match.exists(Id=match_id):
        Match[match_id].CandidateDirector = pos

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
def compute_election_result(match_id: int):
    if Match.exists(Id=match_id):
        lumos = 0
        voting_cutoff = 0.5000001
        result = 'nox'
        players = select(p for p in Match[match_id].Players if not p.IsDead)
        if not exists(p for p in players if p.Vote == MISSING_VOTE):
            total = count(p for p in players)
            lumos = count(p for p in players if p.Vote == LUMOS)
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
            p.Vote = MISSING_VOTE

@db_session
def add_failed_election(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound
    Board[board_id].FailedElectionsCount += 1
    return Board[board_id].FailedElectionsCount

@db_session
def reset_failed_election(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound
    Board[board_id].FailedElectionsCount = 0

@db_session
def do_chaos(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    board_id = get_match_board_id(match_id) 
    proclamation = get_selected_card(board_id)
    enact_proclamation(match_id, proclamation)
    reset_failed_election(board_id)
    is_victory_from(match_id)
    # change_ingame_status(match_id, CHAOS) #will be added in the next sprint
    try:
        get_top_proclamation(board_id)
    except NotEnoughProclamations:
        refill_deck(board_id)
        shuffle_deck(board_id)
        get_top_proclamation(board_id)

@db_session
def failed_election(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    board_id = get_match_board_id(match_id)
    failed_election_count = add_failed_election(board_id)
    if failed_election_count == 3:
        do_chaos(match_id)

@db_session
def enact_proclamation(match_id: int, proclamation: str):
    if proclamation == PHOENIX_STR:
        Match[match_id].Board.PhoenixProclamations += 1
    elif proclamation == DEATH_EATER_STR:
        Match[match_id].Board.DeathEaterProclamations += 1

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
def change_match_status(match_id: int, status: int):
    Match[match_id].Status = status

@db_session
def check_host(user_id: int):
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
            if (p.SecretRol == PHOENIX):
                n = n + 1 
    return n 

@db_session
def get_num_magicians(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.GovRol == MAGICIAN or p.GovRol == EX_MINISTER or p.GovRol == EX_DIRECTOR):
                n = n + 1 
    return n    


@db_session
def get_num_death(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == DEATH_EATER):
                n = n + 1 
    return n     

@db_session
def get_num_minister(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.GovRol == MINISTER):
                n = n + 1 
    return n    

@db_session
def get_num_voldemort(match_id: int): #to helpers
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == VOLDEMORT):
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
            p.SecretRol = PHOENIX
            phoenix = phoenix - 1
        elif (death > 0):
            p.SecretRol = DEATH_EATER
            death = death - 1
        else:
            p.SecretRol = VOLDEMORT

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
def change_player_rol(player_id: int, rol: int):
    Player[player_id].SecretRol = rol

@db_session
def get_min_players(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].MinPlayers

@db_session
def get_player_rol(player_id: int):
    return Player[player_id].SecretRol

@db_session
def get_user_username(user_id: int):
    return User[user_id].Username

@db_session
def get_player_username(player_id: int):
    return (User[(Player[player_id].UserId).Id].Username)

@db_session
def change_player_rol(player_id: int, rol: int):
    Player[player_id].SecretRol = rol

@db_session
def get_posible_directors(match_id: int):
    players_alive_in_match = select(p for p in Match[match_id].Players if p.IsDead == False)
    posible_directors = list()
    if len(players_alive_in_match)<=5:
        for p in players_alive_in_match:
            if (p.GovRol != EX_DIRECTOR and p.GovRol != MINISTER):
                posible_directors.append(get_player_username(p.PlayerId))
    else:
        for p in players_alive_in_match:
            if (p.GovRol != EX_MINISTER and p.GovRol != EX_DIRECTOR and p.GovRol != MINISTER):
                posible_directors.append(get_player_username(p.PlayerId))
    return {"posible directors": posible_directors}

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
def avada_kedavra(board_id: int, player_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    if not Player.exists(PlayerId=player_id):
        raise PlayerNotFound

    Player[player_id].IsDead = True
    Board[board_id].AvailableSpell = NO_SPELL

@db_session
def disable_spell(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound

    Board[board_id].AvailableSpell = NO_SPELL

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

@db_session
def get_player_id_from_username(match_id: int, username: str):
    if not Match.exists(Id=match_id):
        raise MatchNotFound
    players = Match[match_id].Players
    return get(p.PlayerId for p in players if p.UserId.Username == username)

@db_session
def get_max_players(match_id: int):
    if Match.exists(Id=match_id):
        return Match[match_id].MaxPlayers

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
def update_password(user_id: int, oldp: str, newp: str):

    if not User.exists(Id=user_id):
        raise UserNotFound
       
    if (User[user_id].Password==oldp):
        User[user_id].Password = newp
        return True

    else:
        return False

@db_session
def get_password(user_id: int):
    return User[user_id].Password