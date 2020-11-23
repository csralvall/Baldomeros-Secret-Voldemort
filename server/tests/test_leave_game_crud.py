import unittest 

from server.db.crud import *

from server.tests.helpers import *

class TestLeaveGame(unittest.TestCase):

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
        delete_data(User)
        delete_data(Player)
        delete_data(Match)
        delete_data(Board)

    def test_eliminate_player_OK(self):
        self.assertEqual(get_num_players(self.matchid), 4)
        self.assertEqual(check_player_in_match(self.matchid,self.player1id),True)
        eliminate_player_from_match(self.matchid, self.player1id)
        self.assertEqual(get_num_players(self.matchid), 3)
        self.assertEqual(check_player_in_match(self.matchid,self.player1id),False)

    def test_raise_player_not_found(self):
        self.assertRaises(PlayerNotFound, eliminate_player_from_match, self.matchid, 99999999)
    
    def test_raise_match_not_exists(self):
        self.assertRaises(PlayerNotFound, eliminate_player_from_match, 9999999, 99999999)

    







if __name__ == "__main__":
    unittest.main()