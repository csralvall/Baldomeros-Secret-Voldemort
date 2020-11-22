from pony.orm import db_session, select, count, delete
from server.db.database import *
from server.db.crud import DeckNotFound, BoardNotFound
from server.db.dicts import *

@db_session
def delete_data(table): 
    delete(p for p in table)

@db_session
def delete_user(email: str, username: str, password: str): 
    user = User.get(Email=email, Username=username, Password=password)
    if user is not None:
        user.delete()
    return user

@db_session
def make_minister(player_id: int):
    Player[player_id].GovRol = MINISTER

@db_session
def make_ex_minister(player_id: int):
    Player[player_id].GovRol = EX_MINISTER

@db_session
def make_magician(player_id: int):
    Player[player_id].GovRol = MAGICIAN

@db_session
def make_director(player_id: int):
    Player[player_id].GovRol = DIRECTOR

@db_session
def make_voldemort(player_id: int):
    Player[player_id].SecretRol = VOLDEMORT

@db_session
def make_phoenix(player_id: int):
    Player[player_id].SecretRol = PHOENIX

@db_session
def get_player_gov_rol(player_id: int):
    return GovRolDiccionary[Player[player_id].GovRol]

@db_session
def get_exdirector_username(match_id: int):
    director = Match[match_id].Players.filter(lambda p: p.GovRol == EX_DIRECTOR).first()
    if director is None:
        return "No director yet"
    return director.UserId.Username 

@db_session
def set_candidate_director_test(match_id: int, position: int):
    Match[match_id].CandidateDirector = position

@db_session
def set_current_minister(match_id: int, position: int):
    Match[match_id].CurrentMinister = position

@db_session
def set_current_director(match_id: int, position: int):
    Match[match_id].CurrentDirector = position 

@db_session
def get_candidate_director(match_id: int):
    return Match[match_id].CandidateDirector

@db_session
def reset_proclamation(match_id: int):
    Match[match_id].Board.PhoenixProclamations = 0
    Match[match_id].Board.DeathEaterProclamations = 0

@db_session
def change_last_minister(match_id: int, position: int):
    Match[match_id].CurrentMinister = position

@db_session
def change_last_director(match_id: int, position: int):
    Match[match_id].Currentdirector = position

@db_session
def change_last_director_govrol(player_id: int):
    Player[player_id].GovRol = EX_DIRECTOR

@db_session
def change_selected_deck_phoenix(board_id: int):
    deck = Board[board_id].Proclamations
    for card in deck.Cards['selected']:
        deck.Cards['selected'].pop()
    for i in range (0,3):
        deck.Cards['selected'].append("phoenix")

@db_session
def change_selected_deck_death_eater(board_id: int):
    deck = Board[board_id].Proclamations
    for card in deck.Cards['selected']:
        deck.Cards['selected'].pop()
    for i in range (0,3):
        deck.Cards['selected'].append("death eater")

@db_session
def show_available_deck(board_id: int):
    if Board.exists(Id=board_id):
        deck = Board[board_id].Proclamations
        if deck is not None:
            return deck.Cards['available']
        else:
            raise DeckNotFound
    else:
        raise BoardNotFound

@db_session
def show_discarded_deck(board_id: int):
    if Board.exists(Id=board_id):
        deck = Board[board_id].Proclamations
        if deck is not None:
            return deck.Cards['discarded']
        else:
            raise DeckNotFound
    else:
        raise BoardNotFound

@db_session
def show_deck(board_id: int):
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        print(f'Available: {deck.Available}')
        print(f'Discarded: {deck.Discarded}')
        return deck.Cards

@db_session
def get_position(player_id: int):
    return Player[player_id].Position

@db_session
def kill_player(player_id: int):
    Player[player_id].IsDead = True


@db_session
def get_failed_election_count(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound
    return Board[board_id].FailedElectionsCount
