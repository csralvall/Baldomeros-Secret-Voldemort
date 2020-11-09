from pony.orm import db_session, select, count, delete
from server.db.database import *
from server.db.crud import DeckNotFound, BoardNotFound

@db_session
def delete_data(table): 
    delete(p for p in table)

@db_session
def delete_user(email, username, password): 
    user = User.get(Email=email, Username=username, Password=password)
    if user is not None:
        user.delete()
    return user

@db_session
def make_minister(pid):
    Player[pid].GovRol = 1

@db_session
def make_magician(pid):
    Player[pid].GovRol = 2

@db_session
def make_director(pid):
    Player[pid].GovRol = 0

@db_session
def set_current_minister(mid,pos):
    Match[mid].CurrentMinister = pos

@db_session
def set_current_director(mid,pos):
    Match[mid].CurrentDirector = pos 

@db_session
def reset_proclamation(mid):
    Match[mid].Board.PhoenixProclamations = 0
    Match[mid].Board.DeathEaterProclamations = 0

@db_session
def change_last_minister(mid,pos):
    Match[mid].CurrentMinister = pos

@db_session
def change_last_director(mid,pos):
    Match[mid].Currentdirector = pos

@db_session
def change_last_director_govrol(pid):
    Player[pid].GovRol = 4

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
def get_position(pid):
    return Player[pid].Position

@db_session
def get_director_username(ID: int): 
    director = Match[ID].Players.filter(lambda p: p.GovRol == 2).first() ##govrol must be == 0.
    return director.UserId.Username 

@db_session
def kill_player(pid):
    Player[pid].IsDead = True