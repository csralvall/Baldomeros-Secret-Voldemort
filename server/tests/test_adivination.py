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

    def test_adivination(self):
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)

        self.assertEqual(unlock_spell(self.matchid1), ADIVINATION) 

        disable_spell(self.board_id)

        self.assertEqual(get_board_status(self.board_id)['spell'], None)

    def test_adivination2(self):
        self.assertRaises(BoardNotFound, disable_spell, self.board_id + 1)

    def test_adivination3(self):
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)
        enact_proclamation(self.matchid1, DEATH_EATER_STR)

        self.assertNotEqual(unlock_spell(self.matchid1), ADIVINATION) 
