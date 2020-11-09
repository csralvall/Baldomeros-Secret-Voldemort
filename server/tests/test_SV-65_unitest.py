import unittest 
from server.db.crud import *
from server.db.database import *

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

        self.matchid = m_p["Match_id"]
  
        self.pid = get_player_id(self.matchid, self.user1id)

        player2 = add_user_in_match(self.user2id,self.matchid,1)
        player3 = add_user_in_match(self.user3id,self.matchid,2)
        player4 = add_user_in_match(self.user4id,self.matchid,3)
        player5 = add_user_in_match(self.user5id,self.matchid,4)

        n = get_num_players(self.matchid)

        self.player2id = player2.to_dict("PlayerId")["PlayerId"]
        self.player3id = player3.to_dict("PlayerId")["PlayerId"]
        self.player4id = player4.to_dict("PlayerId")["PlayerId"]
        self.player5id = player5.to_dict("PlayerId")["PlayerId"]

        set_roles(n,self.matchid)
        set_gob_roles(self.matchid)        

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

# #--------------------------- Test get_num_players ----------------------------  

    def test_get_num_players(self):
        self.assertEqual(get_num_players(self.matchid), 5)
  
    def test_get_num_players2(self):
        self.assertNotEqual(get_num_players(self.matchid), 4)   

    def test_get_num_players3(self):
        self.assertNotEqual(get_num_players(self.matchid), 6)                
            
#--------------------------- Test set_roles ----------------------------    

    def test_set_roles(self):
        self.assertTrue(get_num_phoenix(self.matchid)==3)
        self.assertTrue(get_num_death(self.matchid)==1)
        self.assertTrue(get_num_voldemort(self.matchid)==1)


#--------------------------- Test set_gob_roles ----------------------------    

    def test_set_gob_roles(self):
        self.assertEqual(get_player_gob_rol(self.pid), 0) 
        self.assertEqual(get_player_gob_rol(self.player2id), 2)
        self.assertEqual(get_player_gob_rol(self.player3id), 2)
        self.assertEqual(get_player_gob_rol(self.player4id), 2)
        self.assertEqual(get_player_gob_rol(self.player5id), 2)            