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
        change_ingame_status(self.matchid, USE_SPELL)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[USE_SPELL])
        change_ingame_status(self.matchid, EXPELLIARMUS)
        self.assertEqual(get_ingame_status(self.matchid),ingame_status[EXPELLIARMUS])

    def test_change_ingame_status_wrong_match(self):
        self.assertRaises(MatchNotFound, change_ingame_status, self.matchid+1,NOMINATION)

    def test_bad_ingame_status(self):
        self.assertRaises(BadIngameStatus, change_ingame_status, self.matchid, -1)
        self.assertRaises(BadIngameStatus, change_ingame_status, self.matchid, 7)


    def test_change_to_exdirector(self):
        make_director(self.playeridcreator)
        set_current_director(self.matchid, 0)
        change_to_exdirector(self.matchid)
        self.assertEqual(get_exdirector_username(self.matchid), "example" )
        self.assertRaises( NoDirector,change_to_exdirector, self.matchid)

    def test_change_to_exdirector_bad_mid(self):
        self.assertRaises( MatchNotFound,change_to_exdirector, self.matchid+1)

    def test_successful_director_election(self):
        make_magician(self.playeridcreator)
        make_magician(self.player1id)
        set_candidate_director_test(self.matchid,0)
        successful_director_election(self.matchid)
        self.assertEqual(get_director_username(self.matchid), "example")
        self.assertEqual(get_exdirector_username(self.matchid), "No director yet")
        self.assertEqual(get_player_gov_rol(self.playeridcreator),"Head Master")

    def test_successful_director_election_bad_mid(self):
        self.assertRaises(MatchNotFound, successful_director_election, self.matchid+1)

    def test_successful_director_election_no_director(self):
        make_magician(self.playeridcreator)
        make_magician(self.player1id)
        self.assertRaises(NoDirector, successful_director_election, self.matchid)

    def test_failed_director_election(self):
        make_magician(self.playeridcreator)
        make_magician(self.player1id)
        set_candidate_director_test(self.matchid,0)
        failed_director_election(self.matchid)
        self.assertEqual(get_player_gov_rol(self.playeridcreator),"Magician")
        self.assertEqual(get_player_gov_rol(self.player1id),"Magician")
        self.assertRaises(NoDirector, failed_director_election, self.matchid)
        self.assertRaises(NoDirector, change_to_exdirector, self.matchid)

    def test_failed_director_election_bad_mid(self):
        self.assertRaises(MatchNotFound, failed_director_election, self.matchid+1)

    def test_failed_director_election_no_candidate(self):
        make_magician(self.playeridcreator)
        make_magician(self.player1id)
        set_candidate_director_test(self.matchid,0)
        successful_director_election(self.matchid)
        self.assertRaises(NoDirector, failed_director_election, self.matchid)
        
    def test_check_winner_ph(self):
        reset_proclamation(self.matchid)
        for i in range(0,5):
            is_victory_from(self.matchid)
            self.assertEqual(check_winner(self.matchid), "no winner yet")
            enact_proclamation(self.matchid, PHOENIX_STR)
            enact_proclamation(self.matchid, DEATH_EATER_STR)
        is_victory_from(self.matchid)
        self.assertEqual(check_winner(self.matchid), PHOENIX_STR)

    def test_check_winner_de(self):
        reset_proclamation(self.matchid)
        for i in range(0,6):
            is_victory_from(self.matchid)
            self.assertEqual(check_winner(self.matchid), "no winner yet")
            enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        is_victory_from(self.matchid)
        self.assertEqual(check_winner(self.matchid), DEATH_EATER_STR)

    def test_check_winner(self):
        self.assertIsNone(check_winner(self.matchid+1))


if __name__ == '__main__':
    unittest.main()
