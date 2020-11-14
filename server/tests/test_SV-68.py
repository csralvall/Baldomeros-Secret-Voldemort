import unittest 
from server.db.crud import *
from server.db.database import *
from server.tests.helpers import *

class TestSV87(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        create_user("example@gmail.com","example","password")
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
        m_p2 = add_match_db(5,5,self.user2id)
        self.matchid = m_p["Match_id"]
        self.matchid2 = m_p2["Match_id"]
        player1 = add_user_in_match(self.user1id,self.matchid,1)
        player2 = add_user_in_match(self.user2id,self.matchid,2)
        player3 = add_user_in_match(self.user3id,self.matchid,3)
        player4 = add_user_in_match(self.user4id,self.matchid,4)
        player5 = add_user_in_match(self.user5id,self.matchid,5)
        self.player1id = player1.to_dict("PlayerId")["PlayerId"]
        self.player2id = player2.to_dict("PlayerId")["PlayerId"]
        self.player3id = player3.to_dict("PlayerId")["PlayerId"]
        self.player4id = player4.to_dict("PlayerId")["PlayerId"]
        self.player5id = player5.to_dict("PlayerId")["PlayerId"]
        change_player_rol(self.player1id,0) #voldemort
        change_player_rol(self.player2id,1) #death_eater
        change_player_rol(self.player3id,2) #phoenix
        change_player_rol(self.player4id,2) #phoenix
        change_player_rol(self.player5id,2) #phoenix
        set_next_candidate_director(self.matchid,get_position(self.player2id))
        set_current_director(self.matchid,2)
        set_current_minister(self.matchid,1)

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)


# ------------------------Test Set Next Director ----------------------


    # def test_set_next_director_OK(self):
    #     self.assertIsNotNone(set_next_director(self.matchid))

    # def test_set_next_director_fail(self):
    #     self.assertIsNone(set_next_director(9999999))#can fail if match has this id

    # def test_set_next_director_OK2(self):
    #     change_last_director(self.matchid,1)
    #     make_magician(self.player1id)
    #     make_director(self.player2id)
    #     self.assertEqual(set_next_director(self.matchid),2)
    #     set_next_candidate_director(self.matchid,1)
    #     self.assertEqual(set_next_director(self.matchid),1)
    #     set_next_candidate_director(self.matchid,2)
    #     self.assertEqual(set_next_director(self.matchid),2)
    #     set_next_candidate_director(self.matchid,4)
    #     self.assertEqual(set_next_director(self.matchid),4)

    # def test_set_next_director_username(self):
    #     change_last_director(self.matchid,1)
    #     make_magician(self.player1id)
    #     make_director(self.player2id)
    #     set_next_candidate_director(self.matchid,3)
    #     self.assertEqual(set_next_director(self.matchid),3)
    #     self.assertEqual(get_director_username(self.matchid), 'example3')
    #     set_next_candidate_director(self.matchid,4)
    #     self.assertEqual(set_next_director(self.matchid),4)
    #     self.assertEqual(get_director_username(self.matchid), 'example4')    