import unittest 
from server.db.crud import *
from server.db.database import *
from server.tests.helpers import *
from server.db.dicts import *

class TestInMatch(unittest.TestCase):
    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        create_user("example@gmail.com","example","password")
        create_user("example2@gmail.com","example2", "password")
        create_user("example3@gmail.com","example3", "password")
        create_user("example4@gmail.com","example4", "password")
        self.creatorid=get_user("example","password")['Id']
        self.user1id=get_user("example2","password")['Id']
        self.user2id=get_user("example3","password")['Id']
        self.user3id=get_user("example4","password")['Id']
        m_p= add_match_db(5, 5,self.creatorid)
        self.matchid =m_p["Match_id"]
        self.playeridcreator = m_p["Player_id"]
        player1 = add_user_in_match(self.user1id,self.matchid,1)
        self.player1id = player1.to_dict("PlayerId")["PlayerId"]
        player2 = add_user_in_match(self.user2id,self.matchid,2)
        player3 = add_user_in_match(self.user3id,self.matchid,3)

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    def test_player_position(self):
        self.assertEqual(get_player_position(self.player1id),1)
        self.assertEqual(get_player_position(self.playeridcreator),0)
        self.assertNotEqual(get_player_position(self.playeridcreator),get_player_position(self.player1id))

    def test_set_next_candidate(self):
        set_next_candidate_director(self.matchid,1)
        self.assertEqual(get_candidate_director(self.matchid),1)
        set_next_candidate_director(self.matchid,2)
        self.assertEqual(get_candidate_director(self.matchid),2)

    def test_set_next_candidate2(self):
        set_next_candidate_director(self.matchid,1)
        self.assertNotEqual(get_candidate_director(self.matchid),2)
        set_next_candidate_director(self.matchid,2)
        self.assertNotEqual(get_candidate_director(self.matchid),1)

    

    
