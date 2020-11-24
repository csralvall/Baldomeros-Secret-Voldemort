import unittest 

from server.db.crud import *

from server.tests.helpers import *

class TestDeck(unittest.TestCase):

    def setUp(self):
        delete_data(User)
        delete_data(Player)
        delete_data(Match)
        delete_data(Board)
        create_user("foo@foo.com","foo","foo")
        self.userid = get_user("foo","foo")["Id"]
        _match_ = add_match_db(5,5,self.userid)
        self.match = _match_["Match_id"]
        self.playerid = _match_["Player_id"]
        self.board = get_match_board_id(self.match)


    def tearDown(self):
        delete_data(User)
        delete_data(Player)
        delete_data(Match)
        delete_data(Board)

    # TODO: move to test_player_crud.py
    def test_get_player_id_from_username(self):
        self.assertEqual(get_player_id_from_username(self.match, "foo"),
                         self.playerid)

    # TODO: move to test_player_crud.py
    def test_get_player_id_from_username_bad_match(self):
        self.assertRaises(MatchNotFound, get_player_id_from_username,
                          self.match+1, "foo")

    # TODO: move to test_player_crud.py
    def test_get_player_id_from_username_not_existing_player(self):
        self.assertEqual(get_player_id_from_username(self.match, "dfa"), None)

    def test_unlock_spell_with_small_board(self):
        enact_proclamation(self.match, DEATH_EATER_STR)
        enact_proclamation(self.match, DEATH_EATER_STR)
        enact_proclamation(self.match, DEATH_EATER_STR)
        self.assertEqual(unlock_spell(self.match), ADIVINATION)
        enact_proclamation(self.match, DEATH_EATER_STR)
        self.assertEqual(unlock_spell(self.match), AVADA_KEDAVRA)

    def test_unlock_spell_bad_match_id(self):
        self.assertRaises(MatchNotFound, unlock_spell, self.match+1)

    def test_unlock_spell_small_board(self):
        self.assertEqual(unlock_spell_small_board(-1), NO_SPELL)
        self.assertEqual(unlock_spell_small_board(0), NO_SPELL)
        self.assertEqual(unlock_spell_small_board(1), NO_SPELL)
        self.assertEqual(unlock_spell_small_board(2), NO_SPELL)
        self.assertEqual(unlock_spell_small_board(3), ADIVINATION)
        self.assertEqual(unlock_spell_small_board(4), AVADA_KEDAVRA)
        self.assertEqual(unlock_spell_small_board(5), AVADA_KEDAVRA)
        self.assertEqual(unlock_spell_small_board(20), AVADA_KEDAVRA)

    def test_unlock_spell_medium_board(self):
        self.assertEqual(unlock_spell_medium_board(-1), NO_SPELL)
        self.assertEqual(unlock_spell_medium_board(0), NO_SPELL)
        self.assertEqual(unlock_spell_medium_board(1), NO_SPELL)
        self.assertEqual(unlock_spell_medium_board(2), CRUCIO)
        self.assertEqual(unlock_spell_medium_board(3), IMPERIO)
        self.assertEqual(unlock_spell_medium_board(4), AVADA_KEDAVRA)
        self.assertEqual(unlock_spell_medium_board(5), AVADA_KEDAVRA)
        self.assertEqual(unlock_spell_medium_board(52), AVADA_KEDAVRA)

    def test_unlock_spell_medium_board(self):
        self.assertEqual(unlock_spell_big_board(-1), NO_SPELL)
        self.assertEqual(unlock_spell_big_board(0), NO_SPELL)
        self.assertEqual(unlock_spell_big_board(1), CRUCIO)
        self.assertEqual(unlock_spell_big_board(2), CRUCIO)
        self.assertEqual(unlock_spell_big_board(3), IMPERIO)
        self.assertEqual(unlock_spell_big_board(4), AVADA_KEDAVRA)
        self.assertEqual(unlock_spell_big_board(5), AVADA_KEDAVRA)
        self.assertEqual(unlock_spell_big_board(52), AVADA_KEDAVRA)

    def test_avada_kedavra(self):
        self.assertTrue(create_user("bar@bar.com","bar","bar"))
        new_userid = get_user("bar","bar")["Id"]
        add_user_in_match(new_userid, self.match, 2)
        player_id = get_player_id(self.match, new_userid)
        avada_kedavra(self.board, player_id)
        self.assertTrue(get_all_player_status(self.match)["bar"]["isDead"])

    def test_avada_kedavra_board_not_found(self):
        self.assertRaises(BoardNotFound, avada_kedavra, self.board+1, 2)

    def test_avada_kedavra_board_not_found(self):
        self.assertRaises(PlayerNotFound, avada_kedavra, self.board, -1)

    def test_is_voldemort_dead(self):
        self.assertTrue(create_user("bar@bar.com","bar","bar"))
        new_userid = get_user("bar","bar")["Id"]
        add_user_in_match(new_userid, self.match, 2)
        player_id = get_player_id(self.match, new_userid)
        change_player_rol(player_id, VOLDEMORT)
        change_player_rol(self.playerid, PHOENIX)
        self.assertEqual(get_player_rol(player_id),
                        SecretRolDiccionary[VOLDEMORT])
        self.assertEqual(get_player_rol(self.playerid),
                        SecretRolDiccionary[PHOENIX])
        avada_kedavra(self.board, player_id)
        self.assertTrue(is_voldemort_dead(self.match))

    def test_is_voldemort_dead_not_setted_voldemort(self):
        change_player_rol(self.playerid, PHOENIX)
        self.assertEqual(get_player_rol(self.playerid),
                        SecretRolDiccionary[PHOENIX])
        self.assertRaises(VoldemortNotFound, is_voldemort_dead, self.match)

    def test_is_voldemort_dead_match_not_found(self):
        self.assertRaises(MatchNotFound, is_voldemort_dead, self.match+1)

    def test_set_death_eater_winner(self):
        set_death_eater_winner(self.match)
        self.assertEqual(get_match_status(self.match), Status[FINISHED])
        self.assertEqual(check_winner(self.match), DEATH_EATER_STR)
        

    def test_set_death_eater_winner_match_not_found(self):
        self.assertRaises(MatchNotFound, set_death_eater_winner, self.match+1)

    def test_unlock_expelliarmus_before_five_death_eater_cards(self):
        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        for i in range(3):
            enact_proclamation(self.match, DEATH_EATER_STR)

        unlock_expelliarmus(self.board)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

    def test_unlock_expelliarmus_after_five_death_eater_cards(self):
        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        for i in range(5):
            enact_proclamation(self.match, DEATH_EATER_STR)

        unlock_expelliarmus(self.board)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[UNLOCKED])

    def test_unlock_expelliarmus_bad_board_id(self):
        self.assertRaises(BoardNotFound, unlock_expelliarmus, self.board+1)

    def test_get_expelliarmus_status_bad_board_id(self):
        self.assertRaises(BoardNotFound, get_expelliarmus_status, self.board+1)


    def test_set_expelliarmus_status_after_five_death_eater_cards(self):
        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        for i in range(5):
            enact_proclamation(self.match, DEATH_EATER_STR)

        unlock_expelliarmus(self.board)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[UNLOCKED])

        set_expelliarmus_status(self.board, MINISTER_STAGE)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[MINISTER_STAGE])

        set_expelliarmus_status(self.board, REJECTED)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[REJECTED])

    def test_set_expelliarmus_status_before_five_death_eater_cards(self):
        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        for i in range(3):
            enact_proclamation(self.match, DEATH_EATER_STR)

        unlock_expelliarmus(self.board)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        set_expelliarmus_status(self.board, MINISTER_STAGE)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        set_expelliarmus_status(self.board, REJECTED)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

    def test_set_expelliarmus_status_lock_after_unlock(self):
        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[LOCKED])

        for i in range(5):
            enact_proclamation(self.match, DEATH_EATER_STR)

        unlock_expelliarmus(self.board)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[UNLOCKED])

        set_expelliarmus_status(self.board, LOCKED)

        self.assertEqual(get_expelliarmus_status(self.board),
                         expelliarmus[UNLOCKED])

    def test_set_expelliarmus_status_bad_board_id(self):
        self.assertRaises(BoardNotFound, set_expelliarmus_status,
                          self.board+1, MINISTER_STAGE)


if __name__ == "__main__":
    unittest.main()

