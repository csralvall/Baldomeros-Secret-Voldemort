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
        create_user("example2@gmail.com","example2", "password2")
        self.creatorid=get_user("example","password")['Id']
        self.user1id=get_user("example2","password2")['Id']
        m_p= add_match_db(5, 5,self.creatorid)
        self.matchid =m_p["Match_id"]
        self.playeridcreator = m_p["Player_id"]
        player1 = add_user_in_match(self.user1id,self.matchid,1)
        self.player1id = player1.to_dict("PlayerId")["PlayerId"]

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        

    def test_get_director_ok(self):
        make_director(self.playeridcreator)
        make_magician(self.player1id)
        self.assertEqual(get_director_username(self.matchid),"example")


    def test_get_director_fail(self):
        make_magician(self.playeridcreator)
        make_director(self.player1id)
        self.assertNotEqual(get_director_username(self.matchid),"example")


    def test_get_director_ok2(self):
        make_magician(self.playeridcreator)
        make_director(self.player1id)
        self.assertEqual(get_director_username(self.matchid),"example2")

    def test_get_director_nodirector(self):
        make_magician(self.playeridcreator)
        make_magician(self.player1id)
        self.assertEqual(get_director_username(self.matchid),"No director yet")

        
    def test_change_ingame_status(self):
        change_ingame_status(self.matchid, NOMINATION)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[NOMINATION])
        change_ingame_status(self.matchid, ELECTION)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[ELECTION])
        change_ingame_status(self.matchid, MINISTER_SELECTION)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[MINISTER_SELECTION])
        change_ingame_status(self.matchid, DIRECTOR_SELECTION)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[DIRECTOR_SELECTION])        
        change_ingame_status(self.matchid, CAST_SPELLING)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[CAST_SPELLING])

    def test_change_ingame_status_wrong_match(self):
        self.assertRaises(MatchNotFound, change_ingame_status, self.matchid+1,NOMINATION)

    def test_bad_ingame_status(self):
        self.assertRaises(BadIngameStatus, change_ingame_status, self.matchid, -1)
        self.assertRaises(BadIngameStatus, change_ingame_status, self.matchid, 5)



if __name__ == '__main__':
    unittest.main()
