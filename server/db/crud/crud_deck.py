from pony.orm import db_session
from server.db.database import *
from server.db.dicts import *
from server.db.crud.exception_crud import *


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
   