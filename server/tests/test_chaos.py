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

class TestChaos(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

        create_user("example1@gmail.com","example1","password")
        create_user("example2@gmail.com","example2", "password2")
        create_user("example3@gmail.com","example3","password3")
        create_user("example4@gmail.com","example4","password3")
        create_user("example5@gmail.com","example5","password3")

        self.user_id_1=get_user("example1","password")['Id']
        self.user_id_2=get_user("example2","password2")['Id']
        self.user_id_3=get_user("example3","password3")['Id']
        self.user_id_4=get_user("example4","password3")['Id']
        self.user_id_5=get_user("example5","password3")['Id']
        match_and_player= add_match_db(5, 10,self.user_id_1)
        self.match_id =match_and_player["Match_id"]
        self.player_id_1 = match_and_player["Player_id"]
        self.player_id_2 = add_user_in_match(self.user_id_2,self.match_id,1).to_dict("PlayerId")["PlayerId"]
        self.player_id_3 = add_user_in_match(self.user_id_3,self.match_id,2).to_dict("PlayerId")["PlayerId"]
        self.player_id_4 = add_user_in_match(self.user_id_4,self.match_id,3).to_dict("PlayerId")["PlayerId"]
        self.player_id_5 = add_user_in_match(self.user_id_5,self.match_id,4).to_dict("PlayerId")["PlayerId"]
        self.board_id = get_match_board_id(self.match_id)
        create_deck(self.board_id)
        shuffle_deck(self.board_id)
        get_top_three_proclamation(self.board_id)


    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)


    def test_add_election(self):
        reset_failed_election(self.board_id)
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        self.assertEqual(add_failed_election(self.board_id), 1)
        self.assertEqual(get_failed_election_count(self.board_id), 1)
        self.assertEqual(add_failed_election(self.board_id), 2)
        self.assertEqual(get_failed_election_count(self.board_id), 2)
        self.assertEqual(add_failed_election(self.board_id), 3)
        self.assertEqual(get_failed_election_count(self.board_id), 3)
        self.assertEqual(add_failed_election(self.board_id), 4)
        self.assertEqual(get_failed_election_count(self.board_id), 4)

    def test_add_election_bad_board_id(self):
        self.assertRaises(BoardNotFound,add_failed_election,self.board_id+1)

    def test_reset_election(self):
        reset_failed_election(self.board_id)
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        self.assertEqual(add_failed_election(self.board_id), 1)
        self.assertEqual(get_failed_election_count(self.board_id), 1)
        self.assertEqual(add_failed_election(self.board_id), 2)
        self.assertEqual(get_failed_election_count(self.board_id), 2)
        reset_failed_election(self.board_id)
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        self.assertEqual(add_failed_election(self.board_id), 1)
        self.assertEqual(get_failed_election_count(self.board_id), 1)
        self.assertEqual(add_failed_election(self.board_id), 2)
        self.assertEqual(get_failed_election_count(self.board_id), 2)
        reset_failed_election(self.board_id)
        self.assertEqual(get_failed_election_count(self.board_id), 0)

    def test_reset_failed_election_bad_board_id(self):
        self.assertRaises(BoardNotFound,reset_failed_election,self.board_id+1)

    def test_do_chaos(self):
        self.assertEqual(get_phoenix_proclamations(self.match_id), 0)
        self.assertEqual(get_death_eater_proclamations(self.match_id), 0)
        reset_failed_election(self.board_id)
        self.assertEqual(add_failed_election(self.board_id), 1)
        self.assertEqual(add_failed_election(self.board_id), 2)
        self.assertEqual(add_failed_election(self.board_id), 3)
        self.assertEqual(get_failed_election_count(self.board_id), 3)
        selected= show_selected_deck(self.board_id)
        proclamation = selected[0]
        do_chaos(self.match_id)
        if proclamation == PHOENIX_STR:
            self.assertEqual(get_phoenix_proclamations(self.match_id), 1)
            self.assertEqual(get_death_eater_proclamations(self.match_id), 0)
        else:
            self.assertEqual(get_death_eater_proclamations(self.match_id), 1)
            self.assertEqual(get_phoenix_proclamations(self.match_id), 0)
        
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        self.assertEqual(len(show_selected_deck(self.board_id)), 3)

    def test_do_chaos_shuffle(self):
        self.assertEqual(get_phoenix_proclamations(self.match_id), 0)
        self.assertEqual(get_death_eater_proclamations(self.match_id), 0)
        shuffle_deck(self.board_id)
        j=0
        self.assertEqual(len(show_available_deck(self.board_id)),14)
        for i in range(0,4):
            hand_db = show_selected_deck(self.board_id)
            discarted_db = hand_db[0]
            selected_db_1=hand_db[1]
            selected_db_2=hand_db[2]
            discard_proclamation(self.board_id, selected_db_2)
            discard_proclamation(self.board_id, selected_db_1)
            discard_proclamation(self.board_id, discarted_db)
            j +=3
            self.assertEqual(len(show_available_deck(self.board_id)),(17-j))
            self.assertEqual(len(show_discarded_deck(self.board_id)),j)
            get_top_three_proclamation(self.board_id)
        #12 descartadas, 2 en available, 3 en selected
        self.assertEqual(len(show_available_deck(self.board_id)),2)
        self.assertEqual(len(show_discarded_deck(self.board_id)),12)
        self.assertEqual(len(show_selected_deck(self.board_id)),3)
        #descartar 2 mas
        hand_db = show_selected_deck(self.board_id)
        selected_db_1=hand_db[1]
        selected_db_2=hand_db[2]
        discard_proclamation(self.board_id, selected_db_2)
        discard_proclamation(self.board_id, selected_db_1)
        get_top_proclamation(self.board_id)
        get_top_proclamation(self.board_id)
        #14 descartadas, 0 en available, 3 en selected
        do_chaos(self.match_id)
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        self.assertEqual(len(show_selected_deck(self.board_id)), 3)
        self.assertEqual(len(show_available_deck(self.board_id)),13)
        self.assertEqual(len(show_discarded_deck(self.board_id)),0)

    def test_do_chaos_bad_match_id(self):
        self.assertRaises(MatchNotFound,do_chaos,self.match_id+1)

    def test_failed_election(self):
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        failed_election(self.match_id)
        self.assertEqual(get_failed_election_count(self.board_id), 1)
        failed_election(self.match_id)
        self.assertEqual(get_failed_election_count(self.board_id), 2)
        selected= show_selected_deck(self.board_id)
        proclamation = selected[0]    
        failed_election(self.match_id)
        self.assertEqual(len(show_selected_deck(self.board_id)), 3)
        self.assertEqual(get_failed_election_count(self.board_id), 0)
        if proclamation == PHOENIX_STR:
            self.assertEqual(get_phoenix_proclamations(self.match_id), 1)
            self.assertEqual(get_death_eater_proclamations(self.match_id), 0)
        else:
            self.assertEqual(get_death_eater_proclamations(self.match_id), 1)
            self.assertEqual(get_phoenix_proclamations(self.match_id), 0)
        
    def test_failed_election_bad_match_id(self):
        self.assertRaises(MatchNotFound,failed_election,self.match_id+1)


    def test_check_voldemort_no_proclamation(self):
        make_minister(self.player_id_1)
        set_current_minister(self.match_id, 0)
        make_director(self.player_id_2)
        set_current_director(self.match_id,1)
        self.assertFalse(check_voldemort(self.match_id))

    def test_check_voldemort_no_voldemort(self):
        make_phoenix(self.player_id_1)
        make_phoenix(self.player_id_2)
        make_phoenix(self.player_id_3)
        make_phoenix(self.player_id_4)
        make_phoenix(self.player_id_5)
        make_minister(self.player_id_1)
        set_current_minister(self.match_id, 0)
        make_director(self.player_id_2)
        set_current_director(self.match_id,1)
        enact_proclamation(self.match_id, DEATH_EATER_STR)
        enact_proclamation(self.match_id, DEATH_EATER_STR)
        enact_proclamation(self.match_id, DEATH_EATER_STR)
        self.assertFalse(check_voldemort(self.match_id))

    def test_check_voldemort_true(self):
        make_minister(self.player_id_1)
        set_current_minister(self.match_id, 0)
        make_director(self.player_id_2)
        set_current_director(self.match_id,1)
        make_voldemort(self.player_id_2)
        enact_proclamation(self.match_id, DEATH_EATER_STR)
        enact_proclamation(self.match_id, DEATH_EATER_STR)
        enact_proclamation(self.match_id, DEATH_EATER_STR)
        self.assertTrue(check_voldemort(self.match_id))

    def test_check_voldemort_wrong_mid(self):
        self.assertRaises(MatchNotFound,check_voldemort,self.match_id+1)


if __name__ == "__main__":
    unittest.main()
