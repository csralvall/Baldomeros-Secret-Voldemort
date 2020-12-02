from pony.orm import db_session, select, count
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *

from server.db.crud.crud_deck import *
from server.db.crud.crud_match import *
from server.db.crud.crud_legislative_session import *

@db_session
def vote_director(player_id: int, vote: str):
    if vote == 'nox':
        Player[player_id].Vote = NOX
    elif vote == 'lumos':
        Player[player_id].Vote = LUMOS
    elif vote == 'missing vote':
        Player[player_id].Vote = MISSING_VOTE

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
def get_posible_directors(match_id: int):
    players_alive_in_match = select(p for p in Match[match_id].Players if p.IsDead == False)
    posible_directors = list()
    if len(players_alive_in_match)<=5:
        for p in players_alive_in_match:
            if (p.GovRol != EX_DIRECTOR and p.GovRol != MINISTER and p.GovRol != IMPERIO_MINISTER):
                posible_directors.append(get_player_username(p.PlayerId))
    else:
        for p in players_alive_in_match:
            if (p.GovRol != EX_MINISTER and p.GovRol != EX_DIRECTOR and p.GovRol != MINISTER and p.GovRol != IMPERIO_MINISTER):
                posible_directors.append(get_player_username(p.PlayerId))
    return {"posible directors": posible_directors}

@db_session
def set_next_candidate_director(match_id: int, pos: int):
    if Match.exists(Id=match_id):
        Match[match_id].CandidateDirector = pos

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
def set_next_minister(match_id: int):
    if Match.exists(Id=match_id):
        all_players = Match[match_id].Players
        query = all_players.order_by(Player.Position)
        exMinister = [x for x in query if x.GovRol == EX_MINISTER]
        if len(exMinister):
            exMinister[0].GovRol = MAGICIAN
        players = [x for x in query]
        last_minister = Match[match_id].CurrentMinister
        # set imperio minister as ex minister
        imp_min = get(p for p in all_players if p.GovRol == IMPERIO_MINISTER)
        if imp_min is not None:
            imp_min.GovRol = EX_MINISTER 
            players[last_minister].GovRol = MAGICIAN
        else:
            players[last_minister].GovRol = EX_MINISTER

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
def exminister_to_magician(match_id: int):
    if not Match.exists(Id=match_id):
        raise MatchNotFound

    all_players = Match[match_id].Players
    query = all_players.order_by(Player.Position)
    exMinister = [x for x in query if x.GovRol == EX_MINISTER]
    if len(exMinister):
        exMinister[0].GovRol = MAGICIAN

@db_session
def set_next_minister_failed_election(match_id: int):
    if Match.exists(Id=match_id):
        all_players = Match[match_id].Players
        query = all_players.order_by(Player.Position)
        imp_min = get(p for p in all_players if p.GovRol == IMPERIO_MINISTER)
        if imp_min is not None:
            imp_min.GovRol = MAGICIAN 
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
