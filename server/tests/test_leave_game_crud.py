import unittest 

from server.db.crud import *

from server.tests.helpers import *

class TestEliminatePlayer(unittest.TestCase):

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
        self.player2id = player2.to_dict("PlayerId")["PlayerId"]
        player3 = add_user_in_match(self.user3id,self.matchid,3)
        self.player3id = player3.to_dict("PlayerId")["PlayerId"]
        self.player3position = player3.to_dict("Position")["Position"]

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
        self.assertRaises(MatchNotFound, eliminate_player_from_match, 9999999, self.player1id)

    #eliminate_all_players_from_match#
    def test_eliminate_all_players_OK(self):
        self.assertEqual(get_num_players(self.matchid), 4)
        eliminate_all_players_from_match(self.matchid)
        self.assertEqual(get_num_players(self.matchid), 0)
    
    def test_eliminate_all_players_match_not_found(self):
        self.assertRaises(MatchNotFound, eliminate_all_players_from_match, 9999999)

    #get_user_id_from_player_id#
    def test_get_user_id_from_player_id_OK(self):
        self.assertEqual(self.user1id, get_user_id_from_player_id(self.matchid, self.player1id))
        self.assertEqual(self.creatorid, get_user_id_from_player_id(self.matchid, self.playeridcreator))
    
    def test_get_user_id_from_player_id_player_not_found(self):
        self.assertRaises(PlayerNotFound, get_user_id_from_player_id, self.matchid, 9999999)

    def test_get_user_id_from_player_id_Match_not_found(self):
        self.assertRaises(MatchNotFound, get_user_id_from_player_id, 9999999, 9999999)

    #get_creator_id_match#
    def test_get_creator_id_match_OK(self):
        self.assertEqual(self.creatorid, get_creator_id_match(self.matchid))

    def test_get_creator_id_match_Match_not_found(self):
        self.assertRaises(MatchNotFound, get_creator_id_match, 9999999)

    #restart_positions(match_id: int)#
    def restart_positions_OK(self):
        self.assertEqual(get_position(self.player3id), self.player3position)
        eliminate_player_from_match(self.matchid, self.player3id)
        players = get_players_from_match(match_id)
        for p in players:
            self.assertNotEqual(get_position(p.PlayerId), self.player3position)
        eliminate_player_from_match(self.matchid, self.player2id)
        player3 = add_user_in_match(self.user3id,self.matchid,2)
        player3position = player3.to_dict("Position")["Position"]
        self.assertEqual(player3position, 2)




if __name__ == "__main__":
    unittest.main()
