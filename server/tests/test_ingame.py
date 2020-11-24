import unittest 
from server.db.crud import *
from server.db.database import *
from server.tests.helpers import *

class TestInMatch(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        create_user("example@gmail.com","example","password")
        create_user("example2@gmail.com","example2", "password2")
        create_user("example3@gmail.com","example3","password3")
        self.creatorid=get_user("example","password")['Id']
        self.user1id=get_user("example2","password2")['Id']
        self.user2id=get_user("example3","password3")['Id']
        m_p= add_match_db(5, 5,self.creatorid)
        m_p2= add_match_db(5,5,self.user2id)
        self.matchid =m_p["Match_id"]
        self.matchid2=m_p2["Match_id"]
        self.playeridcreator = m_p["Player_id"]
        self.player3id = m_p2["Player_id"]
        player1 = add_user_in_match(self.user1id,self.matchid,1)
        self.player1id = player1.to_dict("PlayerId")["PlayerId"]

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    #-------------------------check player in match ------------------------
    def test_OK_creator(self):
        self.assertTrue(check_player_in_match(self.matchid,self.playeridcreator))

    def test_OK_creator2(self):
        self.assertTrue(check_player_in_match(self.matchid2,self.player3id))

    def test_OK_player1(self):
        self.assertTrue(check_player_in_match(self.matchid,self.player1id))

    def test_fail_pid(self):
        self.assertFalse(check_player_in_match(self.matchid,9999999))#can fail if one of my players has this id

    def test_fail_gid(self):
        self.assertFalse(check_player_in_match(9999999,self.playeridcreator))#can fail if match has this id
    
    #-------------------------get_player_votes ------------------------
    def test_getpv_OK_return(self):
        self.assertIsNotNone(get_all_player_status(self.matchid))

    def test_getpv_fail_mid(self):
        self.assertRaises(MatchNotFound, get_all_player_status, 99999999)#can fail if match has this id


    def test_getpv_OK_votes(self):
        vote_director(self.playeridcreator, 'lumos')
        vote_director(self.player1id, 'nox')
        player_status = get_all_player_status(self.matchid)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertEqual(votes, {'example': 'lumos', 'example2': 'nox'})
        
    def test_getpv_OK_votes2(self):
        vote_director(self.playeridcreator, 'nox')
        vote_director(self.player1id, 'lumos')
        player_status = get_all_player_status(self.matchid)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertEqual(votes, {'example': 'nox', 'example2': 'lumos'})

    def test_getpv_different_match(self):
        restore_election(self.matchid2)
        vote_director(self.player1id, 'nox')
        player_status = get_all_player_status(self.matchid2)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertEqual(votes,{'example3': 'missing vote'})

    #-------------------------restore_election ------------------------
    def test_restore_ok(self):
        vote_director(self.playeridcreator, 'lumos')
        restore_election(self.matchid)
        player_status = get_all_player_status(self.matchid)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertEqual(votes, {'example': 'missing vote', 'example2': 'missing vote'})

    def test_restore_fail_mid(self):
        vote_director(self.playeridcreator, 'lumos')
        restore_election(9999999)#can fail if match has this id
        player_status = get_all_player_status(self.matchid)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertNotEqual(votes, {'example': 'missing vote', 'example2': 'missing vote'})

    #--------------12 tests ^-------------------------
    #-------------------------vote_director ------------------------
    #won't receive a wrong playerid bc we check that before calling it

    def test_vote_OK(self):
        restore_election(self.matchid)
        vote_director(self.playeridcreator,'nox')
        vote_director(self.player1id,'lumos')
        player_status = get_all_player_status(self.matchid)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertEqual(votes, {'example': 'nox', 'example2': 'lumos'})

    def test_vote_fail(self):
        restore_election(self.matchid)
        vote_director(self.player1id,'blabla')
        vote_director(self.playeridcreator,'blablabla')
        player_status = get_all_player_status(self.matchid)
        votes = { k: v['vote'] for k, v in player_status.items() }
        self.assertEqual(votes, {'example': 'missing vote', 'example2': 'missing vote'})


    #------------------------get_minister_username----------------------
    #won't receive a wrong matchid bc we check that before calling it
    def test_get_minister_ok(self):
        make_minister(self.playeridcreator)
        self.assertEqual(get_minister_username(self.matchid),"example")


    def test_get_minister_fail(self):
        make_magician(self.playeridcreator)
        make_minister(self.player1id)
        self.assertNotEqual(get_minister_username(self.matchid),"example")


    def test_get_minister_ok2(self):
        make_magician(self.playeridcreator)
        make_minister(self.player1id)
        self.assertEqual(get_minister_username(self.matchid),"example2")

    def test_get_minister_nominister(self):
        make_magician(self.playeridcreator)
        make_magician(self.player1id)
        self.assertEqual(get_minister_username(self.matchid),"No minister yet")

    #------------------------get_candidate_director_username----------------------
    #won't receive a wrong matchid bc we check that before calling it
    def test_get_candidate_director_ok(self):
        set_next_candidate_director(self.matchid,0)
        self.assertEqual(get_candidate_director_username(self.matchid),"example")

    def test_get_candidate_director_fail(self):
        make_magician(self.playeridcreator)
        set_next_candidate_director(self.matchid,1)
        self.assertNotEqual(get_candidate_director_username(self.matchid),"example")

    def test_get_candidate_director_nominister(self):
        set_next_candidate_director(self.matchid, NO_DIRECTOR)
        self.assertEqual(get_candidate_director_username(self.matchid),"No director candidate yet")

    def test_get_candidate_director_bad_match_id(self):
        self.assertRaises(MatchNotFound, get_candidate_director_username, self.matchid+500)


    #------------------------get_match_status//change_match_status----------------------
    #won't receive a wrong matchid bc we check that before calling it
    def test_get_mstatus_ok(self):
        change_match_status(self.matchid, 0)
        self.assertEqual(get_match_status(self.matchid), "Joinable" )

    def test_get_mstatus_ok2(self):
        change_match_status(self.matchid, 1)
        self.assertEqual(get_match_status(self.matchid), "In Game" )

    def test_get_mstatus_ok3(self):
        change_match_status(self.matchid, 2)
        self.assertEqual(get_match_status(self.matchid), "Finished" )

    #------------------------get_board_status//enact proclamation----------------------
    #won't receive a wrong matchid bc we check that before calling it
    
    def test_get_bstatus_ok(self):
        reset_proclamation(self.matchid)
        board = {'DeathEaterProclamations': 0,
                'PhoenixProclamations': 0,
                'boardtype': '5-6',
                'spell': None,
                'expelliarmus': expelliarmus[LOCKED],
                'status': 'nomination',
                'failcounter': 0}
        board_id = get_match_board_id(self.matchid)
        self.assertEqual(get_board_status(board_id), board)

    def test_enact_proclamation(self):
        reset_proclamation(self.matchid)
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        board_id = get_match_board_id(self.matchid)
        add_failed_election(board_id)
        board = {'DeathEaterProclamations': 1,
                'PhoenixProclamations': 3,
                'boardtype': '5-6',
                'expelliarmus': expelliarmus[LOCKED],
                'spell': None,
                'status': 'nomination',
                'failcounter': 1}

        self.assertEqual(get_board_status(board_id), board)

    def test_enact_proclamation_fail(self):
        reset_proclamation(self.matchid)
        enact_proclamation(self.matchid, "death")
        board = {'DeathEaterProclamations': 0,
                'PhoenixProclamations': 0,
                'boardtype': '5-6',
                'spell': None,
                'expelliarmus': expelliarmus[LOCKED],
                'status': 'nomination',
                'failcounter': 0}
        board_id = get_match_board_id(self.matchid)
        self.assertEqual(get_board_status(board_id), board)

    #------------------------get_phoenix_proclamations----------------------
    #won't receive a wrong matchid bc we check that before calling it

    def test_get_fp_OK(self):
        reset_proclamation(self.matchid)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 0)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 1)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 2)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 3)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 4)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 5)

    def test_get_fp_OK2(self):
        reset_proclamation(self.matchid)
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(get_phoenix_proclamations(self.matchid), 2)

    #------------------------get_death_eater_proclamations----------------------
    #won't receive a wrong matchid bc we check that before calling it

    def test_get_dp_OK(self):
        reset_proclamation(self.matchid)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 0)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 1)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 2)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 3)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 4)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 5)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 6)

    def test_get_dp_OK2(self):
        reset_proclamation(self.matchid)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(get_death_eater_proclamations(self.matchid), 2)

    #-------------27 test^-------------------
    #------------------------is_victory_from----------------------

    def test_is_victory_OK(self):
        reset_proclamation(self.matchid)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")

    def test_is_victory_OK_de(self):
        reset_proclamation(self.matchid)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), DEATH_EATER_STR)

    def test_is_victory_OK_de2(self):
        reset_proclamation(self.matchid)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), DEATH_EATER_STR)

    def test_is_victory_OK_ph(self):
        reset_proclamation(self.matchid)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), PHOENIX_STR)

    def test_is_victory_OK_ph2(self):
        reset_proclamation(self.matchid)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, PHOENIX_STR)
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), "no winner yet")
        enact_proclamation(self.matchid, DEATH_EATER_STR)
        enact_proclamation(self.matchid, PHOENIX_STR)
        self.assertEqual(is_victory_from(self.matchid), PHOENIX_STR)

    def test_is_victory_fail(self):
        self.assertIsNone(is_victory_from(999999))#can fail if match has this id


    #-------------33 test^-------------------
    #------------------------check_match----------------------

    def test_check_match_OK(self):
        self.assertTrue(check_match(self.matchid))

    def test_check_match_OK2(self):
        self.assertTrue(check_match(self.matchid2))

    def test_check_match_fail(self):
        self.assertFalse(check_match(999999))#can fail if match has this id
        

    #------------------------get_player_id----------------------

    def test_get_player_id_OK(self):
        self.assertEqual(get_player_id(self.matchid, self.creatorid), self.playeridcreator)

    def test_get_player_id_OK2(self):
        self.assertEqual(get_player_id(self.matchid, self.user1id), self.player1id)

    def test_get_player_id_OK3(self):
        self.assertEqual(get_player_id(self.matchid2, self.user2id), self.player3id)

    def test_get_player_id_fail(self):
        self.assertIsNone(get_player_id(9999999, self.creatorid))#can fail if match has this id

    def test_get_player_id_fail2(self):
        self.assertIsNone(get_player_id(self.matchid, 9999999))#can fail if user has this id

    def test_get_player_id_fail3(self):
        self.assertIsNone(get_player_id(self.matchid, self.user2id))

    def test_get_player_id_fail4(self):
        self.assertIsNone(get_player_id(self.matchid2, self.user1id))

    #-------------43 test^-------------------
    #------------------------set_next_minister----------------------

    def test_set_next_minister_OK(self):
        self.assertIsNotNone(set_next_minister(self.matchid))

    def test_set_next_minister_fail(self):
        self.assertIsNone(set_next_minister(9999999))#can fail if match has this id

    def test_set_next_minister_OK2(self):
        change_last_minister(self.matchid,0)
        make_magician(self.player1id)
        make_minister(self.playeridcreator)
        self.assertEqual(set_next_minister(self.matchid),1)# 1 is player1id position 

    def test_set_next_minister_OK3(self):
        change_last_minister(self.matchid,0)
        make_magician(self.player1id)
        make_minister(self.playeridcreator)
        self.assertEqual(set_next_minister(self.matchid),1)
        self.assertEqual(set_next_minister(self.matchid),0)
        self.assertEqual(set_next_minister(self.matchid),1)
        self.assertEqual(set_next_minister(self.matchid),0)

    def test_set_next_minister_username(self):
        change_last_minister(self.matchid,0)
        make_magician(self.player1id)
        make_minister(self.playeridcreator)
        self.assertEqual(set_next_minister(self.matchid),1)
        self.assertEqual(get_minister_username(self.matchid), 'example2')
        self.assertEqual(set_next_minister(self.matchid),0)
        self.assertEqual(get_minister_username(self.matchid), 'example')

    #------------------------set_next_minister_failed_election----------------------

    def test_set_next_minister_failed_election_OK(self):
        self.assertIsNotNone(set_next_minister_failed_election(self.matchid))

    def test_set_next_minister_failed_election_fail(self):
        self.assertIsNone(set_next_minister_failed_election(9999999))#can fail if match has this id

    def test_set_next_minister_failed_election_OK2(self):
        change_last_minister(self.matchid,0)
        make_magician(self.player1id)
        make_minister(self.playeridcreator)
        self.assertEqual(set_next_minister_failed_election(self.matchid),1)# 1 is player1id position 

    def test_set_next_minister_failed_election_OK3(self):
        change_last_minister(self.matchid,0)
        make_magician(self.player1id)
        make_minister(self.playeridcreator)
        self.assertEqual(set_next_minister_failed_election(self.matchid),1)
        self.assertEqual(set_next_minister_failed_election(self.matchid),0)
        self.assertEqual(set_next_minister_failed_election(self.matchid),1)
        self.assertEqual(set_next_minister_failed_election(self.matchid),0)

    def test_set_next_minister_failed_election_username(self):
        change_last_minister(self.matchid,0)
        make_magician(self.player1id)
        make_minister(self.playeridcreator)
        self.assertEqual(set_next_minister_failed_election(self.matchid),1)
        self.assertEqual(get_minister_username(self.matchid), 'example2')
        self.assertEqual(set_next_minister_failed_election(self.matchid),0)
        self.assertEqual(get_minister_username(self.matchid), 'example')



    #-------------48 test^-------------------
    #------------------------compute_election_result----------------------

    def test_compute_election_fail_mid(self):
        self.assertIsNone(compute_election_result(999999))#can fail if match has this id

    def test_compute_election_OK(self):
        restore_election(self.matchid)
        vote_director(self.playeridcreator, 'lumos')
        vote_director(self.player1id,'lumos')
        self.assertEqual(compute_election_result(self.matchid),'lumos')

    def test_compute_election_OK2(self):
        restore_election(self.matchid)
        vote_director(self.playeridcreator, 'nox')
        vote_director(self.player1id,'lumos')
        self.assertEqual(compute_election_result(self.matchid),'nox')

    def test_compute_election_OK3(self):
        restore_election(self.matchid)
        vote_director(self.playeridcreator, 'nox')
        vote_director(self.player1id,'nox')
        self.assertEqual(compute_election_result(self.matchid),'nox')

    def test_compute_election_OK4(self):
        restore_election(self.matchid)
        vote_director(self.playeridcreator, 'lumos')
        self.assertEqual(compute_election_result(self.matchid),'missing vote')
 

    def test_compute_election_other_match(self):
        restore_election(self.matchid)
        restore_election(self.matchid2)
        vote_director(self.playeridcreator, 'lumos')
        vote_director(self.player1id,'lumos')
        self.assertEqual(compute_election_result(self.matchid),'lumos')
        self.assertEqual(compute_election_result(self.matchid2),'missing vote')
        
    #-------------54 test^-------------------


if __name__ == '__main__':
    unittest.main()
