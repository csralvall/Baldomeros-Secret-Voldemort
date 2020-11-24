import unittest 
from server.db.crud import *
from server.db.database import *
from server.tests.helpers import *

class Testadivination(unittest.TestCase):

    def setUp(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

        create_user("example1@gmail.com","example1", "password")

        self.user1id = get_user("example1","password")['Id']
    
        self.game1 = add_match_db(5, 5, self.user1id) 

        self.matchid1 = self.game1["Match_id"]

        self.board_id = get_match_board_id(self.matchid1)

    def tearDown(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

#--------------------------- Test get_min_players ----------------------------

    def test_adivnination(self):
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)

        self.assertEqual(unlock_spell(self.matchid1), ADIVINATION) 

        adivination(self.board_id)

        self.assertEqual(get_board_status(self.board_id)['spell'], None)

    def test_adivnination2(self):
        self.assertRaises(BoardNotFound, adivination, self.board_id + 1)

    def test_adivnination3(self):
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)

        self.assertNotEqual(unlock_spell(self.matchid1), ADIVINATION) 

