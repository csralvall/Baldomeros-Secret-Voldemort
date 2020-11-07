import unittest 

from server.db.crud import *

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
        proclamations = ['phoenix', 'phoenix', 'phoenix', 'phoenix', 'phoenix',
        'phoenix', 'death eater', 'death eater', 'death eater', 'death eater',
        'death eater', 'death eater', 'death eater', 'death eater',
        'death eater', 'death eater', 'death eater']

        self.assertTrue(create_deck(self.board))

        cards = get_available_deck(self.board)

        self.assertEqual(proclamations, cards)
        self.assertEqual(deck_status(self.board)['Available'], 17)
        self.assertEqual(deck_status(self.board)['Discarded'], 0)


    def test_creation_bad_id(self):
        self.assertRaises(BoardNotFound, create_deck, self.board+1)


    def test_creation_shuffle_deck(self):
        proclamations_ordered = ['phoenix', 'phoenix', 'phoenix',
        'phoenix', 'phoenix', 'phoenix', 'death eater', 'death eater',
        'death eater', 'death eater', 'death eater', 'death eater',
        'death eater', 'death eater', 'death eater', 'death eater',
        'death eater']
        self.assertTrue(create_deck(self.board))
        self.assertTrue(shuffle_deck(self.board))

        cards = get_available_deck(self.board)

        self.assertNotEqual(proclamations_ordered, cards)


    def test_creation_shuffle_deck_bad_id(self):
        self.assertTrue(create_deck(self.board))
        self.assertFalse(shuffle_deck(self.board+1))


    def test_get_top_proclamation(self):
        self.assertTrue(create_deck(self.board))
        self.assertEqual(get_top_proclamation(self.board), 'death eater')
        self.assertEqual(deck_status(self.board)['Available'], 16)


    def test_get_top_proclamations_not_enough_cards(self):
        self.assertTrue(create_deck(self.board))

        for i in range(0,15):
            get_top_proclamation(self.board)

        self.assertRaises(NotEnoughProclamations,
                get_top_proclamation, self.board)


    def test_get_top_proclamations_bad_board_id(self):
        self.assertRaises(DeckNotFound, get_top_proclamation, self.board+1)


    def test_discard_proclamation(self):
        self.assertTrue(create_deck(self.board))

        self.assertTrue(discard_proclamation(self.board,
                        get_top_proclamation(self.board)))

        self.assertEqual(deck_status(self.board)['Discarded'], 1)

        self.assertEqual(get_discarded_deck(self.board), ['death eater'])


    def test_discard_bad_proclamation(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(InvalidProclamation,
                discard_proclamation,self.board,'alja')


    def test_discard_proclamation_bad_board_id(self):
        self.assertTrue(create_deck(self.board))

        self.assertRaises(DeckNotFound, discard_proclamation,
                                    self.board+1, 'death eater')


    def test_refill_deck(self):
        self.assertTrue(create_deck(self.board))

        self.assertTrue(discard_proclamation(self.board,
                        get_top_proclamation(self.board)))

        self.assertEqual(deck_status(self.board)['Discarded'], 1)

        self.assertTrue(refill_deck(self.board))

        self.assertEqual(deck_status(self.board)['Discarded'], 0)

        self.assertEqual(deck_status(self.board)['Discarded'], 0)

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

if __name__ == '__main__':
    unittest.main()
