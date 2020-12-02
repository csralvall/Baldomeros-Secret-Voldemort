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

class TestSV65(unittest.TestCase):

    def setUp(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

        create_user("example2@gmail.com","example2", "password")
        create_user("example3@gmail.com","example3","password")
        create_user("example4@gmail.com","example4","password")
        create_user("example5@gmail.com","example5","password")
        create_user("example6@gmail.com","example6","password")

        self.user1id = get_user("example2","password")['Id']
        self.user2id = get_user("example3","password")['Id']
        self.user3id = get_user("example4","password")['Id']
        self.user4id = get_user("example5","password")['Id']
        self.user5id = get_user("example6","password")['Id']

        m_p = add_match_db(5, 5,self.user1id)

        self.match_id = m_p["Match_id"]
        self.board_id = get_match_board_id(self.match_id)
  

        player2 = add_user_in_match(self.user2id,self.match_id,1)
        player3 = add_user_in_match(self.user3id,self.match_id,2)
        player4 = add_user_in_match(self.user4id,self.match_id,3)
        player5 = add_user_in_match(self.user5id,self.match_id,4)

        n = get_num_players(self.match_id)


        set_roles(n,self.match_id)
        set_gob_roles(self.match_id)        

    def tearDown(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

#--------------------------- Test check_host ----------------------------

    def test_check_host(self):
        self.assertTrue(check_host(self.user1id))

    def test_check_host2(self):
        self.assertFalse(check_host(self.user2id))

#--------------------------- Test get_min_players ----------------------------

    def test_min_players(self):
        self.assertTrue(get_min_players(self.match_id)==5)

    def test_min_players(self):
        self.assertFalse(get_min_players(self.match_id)==4)

    def test_min_players(self):
        self.assertFalse(get_min_players(self.match_id)==6)        
#--------------------------- Test get_num_players ----------------------------  

    def test_get_num_players(self):
        self.assertEqual(get_num_players(self.match_id), 5)
  
    def test_get_num_players2(self):
        self.assertNotEqual(get_num_players(self.match_id), 4)   

    def test_get_num_players3(self):
        self.assertNotEqual(get_num_players(self.match_id), 6)                
            
#--------------------------- Test set_roles ----------------------------    

    def test_set_roles(self):
        self.assertTrue(get_num_phoenix(self.match_id)==3)
        self.assertTrue(get_num_death(self.match_id)==1)
        self.assertTrue(get_num_voldemort(self.match_id)==1)


#--------------------------- Test set_gob_roles ----------------------------    

    def test_set_gob_roles(self):
        self.assertTrue(get_num_minister(self.match_id)==1) 
        self.assertTrue(get_num_magicians(self.match_id)==4)

#---------------------------Test set_board_type-----------------------------

    def test_set_board_type_5_players(self):
        set_board_type(self.board_id, 5)
        self.assertEqual(get_board_status(self.board_id)['boardtype'], BoardType[SMALL_BOARD])
    
    def test_set_board_type_5_players(self):
        set_board_type(self.board_id, 6)
        self.assertEqual(get_board_status(self.board_id)['boardtype'], BoardType[SMALL_BOARD])

    def test_set_board_type_7_players(self):
        set_board_type(self.board_id, 7)
        self.assertEqual(get_board_status(self.board_id)['boardtype'], BoardType[MEDIUM_BOARD])

    def test_set_board_type_8_players(self):
        set_board_type(self.board_id, 8)
        self.assertEqual(get_board_status(self.board_id)['boardtype'], BoardType[MEDIUM_BOARD])

    def test_set_board_type_9_players(self):
        set_board_type(self.board_id, 9)
        self.assertEqual(get_board_status(self.board_id)['boardtype'], BoardType[BIG_BOARD])

    def test_set_board_type_10_players(self):
        set_board_type(self.board_id, 10)
        self.assertEqual(get_board_status(self.board_id)['boardtype'], BoardType[BIG_BOARD])


    def test_set_board_type_wrong_board(self):
        self.assertRaises(BoardNotFound, set_board_type, self.board_id+1, 10)


if __name__ == '__main__':
    unittest.main()
