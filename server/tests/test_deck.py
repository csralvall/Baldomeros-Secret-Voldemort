import unittest 

from server.db.crud.exception_crud import *
from server.db.crud.crud_deck import *
from server.db.crud.crud_election import *
from server.db.crud.crud_legislative_session import *
from server.db.crud.crud_lobby import *
from server.db.crud.crud_match import *
from server.db.crud.crud_messages import *
from server.db.crud.crud_profile import *
from server.db.crud.crud_spell import *


from server.tests.helpers import *

class TestDeck(unittest.TestCase):

    def setUp(self):
        delete_data(User)
        delete_data(Player)
        delete_data(Match)
        delete_data(Board)
        create_user('foo@foo.com','foo','foo')
        self.userId = get_user('foo','foo')['Id']
        _match_ = add_match_db(5,5,self.userId)
        self.match = _match_['Match_id']
        self.board = get_match_board_id(self.match)


    def tearDown(self):
        delete_data(User)
        delete_data(Player)
        delete_data(Match)
        delete_data(Board)


    def test_creation_correct_id(self):
        proclamations = [PHOENIX_STR, PHOENIX_STR, PHOENIX_STR, PHOENIX_STR, PHOENIX_STR,
        PHOENIX_STR, DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR,
        DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR,
        DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR]

        self.assertTrue(create_deck(self.board))

        cards = show_available_deck(self.board)

        self.assertEqual(proclamations, cards)
        self.assertEqual(deck_status(self.board)['Available'], 17)
        self.assertEqual(deck_status(self.board)['Discarded'], 0)


    def test_creation_bad_id(self):
        self.assertRaises(BoardNotFound, create_deck, self.board+1)


    def test_creation_shuffle_deck(self):
        proclamations_ordered = [PHOENIX_STR, PHOENIX_STR, PHOENIX_STR,
        PHOENIX_STR, PHOENIX_STR, PHOENIX_STR, DEATH_EATER_STR, DEATH_EATER_STR,
        DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR,
        DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR, DEATH_EATER_STR,
        DEATH_EATER_STR]
        self.assertTrue(create_deck(self.board))
        self.assertTrue(shuffle_deck(self.board))

        cards = show_available_deck(self.board)

        self.assertNotEqual(proclamations_ordered, cards)


    def test_creation_shuffle_deck_bad_id(self):
        self.assertTrue(create_deck(self.board))
        self.assertFalse(shuffle_deck(self.board+1))


    def test_get_top_proclamation(self):
        self.assertTrue(create_deck(self.board))
        self.assertTrue(get_top_proclamation(self.board))
        self.assertEqual(show_selected_deck(self.board), [DEATH_EATER_STR])
        self.assertEqual(deck_status(self.board)['Available'], 16)


    def test_get_top_proclamations_not_enough_cards(self):
        self.assertTrue(create_deck(self.board))

        for i in range(0,17):
            get_top_proclamation(self.board)

        self.assertRaises(NotEnoughProclamations,
                get_top_proclamation, self.board)


    def test_get_top_proclamations_bad_board_id(self):
        self.assertRaises(DeckNotFound, get_top_proclamation, self.board+1)


    def test_get_top_three_proclamations(self):
        self.assertTrue(create_deck(self.board))
        self.assertTrue(get_top_three_proclamation(self.board))
        self.assertEqual(show_selected_deck(self.board), [DEATH_EATER_STR,DEATH_EATER_STR,DEATH_EATER_STR])
        self.assertEqual(deck_status(self.board)['Available'], 14)

    def test_get_top_three_proclamations_not_enough_cards(self):
        self.assertTrue(create_deck(self.board))

        for i in range(0,5):
            get_top_three_proclamation(self.board)

        self.assertRaises(NotEnoughProclamations,
                get_top_three_proclamation, self.board)

    def test_get_top_three_proclamations_bad_board_id(self):
        self.assertRaises(DeckNotFound, get_top_three_proclamation, self.board+1)

    def test_discard_proclamation(self):
        self.assertTrue(create_deck(self.board))

        self.assertTrue(get_top_proclamation(self.board))

        self.assertEqual(show_selected_deck(self.board), [DEATH_EATER_STR])

        self.assertTrue(discard_proclamation(self.board, DEATH_EATER_STR))

        self.assertEqual(deck_status(self.board)['Discarded'], 1)

        self.assertEqual(show_discarded_deck(self.board), [DEATH_EATER_STR])

        self.assertEqual(show_selected_deck(self.board), [])


    def test_discard_bad_proclamation(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(InvalidProclamation,
                discard_proclamation,self.board,'alja')


    def test_discard_proclamation_bad_board_id(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(DeckNotFound, discard_proclamation,
                                    self.board+1, DEATH_EATER_STR)


    def test_refill_deck(self):
        self.assertTrue(create_deck(self.board))

        self.assertTrue(get_top_proclamation(self.board))

        self.assertEqual(show_selected_deck(self.board), [DEATH_EATER_STR])

        self.assertTrue(discard_proclamation(self.board, DEATH_EATER_STR))

        self.assertEqual(show_discarded_deck(self.board), [DEATH_EATER_STR])

        self.assertEqual(show_selected_deck(self.board), [])

        self.assertEqual(deck_status(self.board)['Discarded'], 1)

        self.assertTrue(refill_deck(self.board))

        self.assertEqual(deck_status(self.board)['Discarded'], 0)

        self.assertEqual(deck_status(self.board)['Available'], 17)

    def test_refill_deck_bad_board_id(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(DeckNotFound, refill_deck, self.board+1)


    def test_deck_status(self):
        expected_dict = {'Available': 17, 'Discarded': 0}
        self.assertTrue(create_deck(self.board))

        self.assertEqual(deck_status(self.board), expected_dict)


    def test_deck_bad_board_id(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(DeckNotFound, deck_status, self.board+1)

    def test_get_selected_card(self):
        self.assertTrue(create_deck(self.board))

        self.assertTrue(get_top_proclamation(self.board))

        self.assertEqual(show_selected_deck(self.board), [DEATH_EATER_STR])

        self.assertEqual(get_selected_card(self.board), DEATH_EATER_STR)

        self.assertEqual(show_selected_deck(self.board), [])

    def test_get_selected_card_empty_proclamation(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(EmptySelectedProclamations,
                            get_selected_card, self.board)

    def test_get_selected_card_bad_board_id(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(DeckNotFound,
                            get_selected_card, self.board+1)

    def test_show_selected_deck(self):
        self.assertTrue(create_deck(self.board))

        self.assertTrue(get_top_proclamation(self.board))

        self.assertEqual(show_selected_deck(self.board), [DEATH_EATER_STR])

    def test_show_selected_deck_bad_board_id(self):
        self.assertRaises(BoardNotFound,
                            show_selected_deck, self.board+1)
        
    def test_show_selected_deck_not_created_deck(self):
        self.assertRaises(DeckNotFound,
                            show_selected_deck, self.board)

if __name__ == '__main__':
    unittest.main()

