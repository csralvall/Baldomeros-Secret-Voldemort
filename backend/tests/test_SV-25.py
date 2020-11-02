import unittest 
from backend.db.crud import *
from backend.db.database import *

class TestAddMatch(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        create_user("example@gmail.com","example","password")
        create_user("one@gmail.com","one","one")
        create_user("one1@gmail.com","one1","one")
        create_user("one2@gmail.com","one2","one")
        create_user("one3@gmail.com","one3","one")
        create_user("one4@gmail.com","one4","one")
        create_user("one5@gmail.com","one5","one")
        create_user("one6@gmail.com","one6","one")
        create_user("one7@gmail.com","one7","one")
        create_user("one8@gmail.com","one8","one")
        user = get_user("example","password")
        self.userId = user['Id']


    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    def test_ok1(self):
        mp = add_match_db(5,5,self.userId)
        self.assertIsNotNone(mp["Match_id"])
        self.assertIsNotNone(mp["Player_id"])

    def test_ok2(self):
        mp = add_match_db(6,7,self.userId)
        self.assertIsNotNone(mp["Match_id"])
        self.assertIsNotNone(mp["Player_id"])

    def test_fail_maxp(self):
        mp = add_match_db(5,1,self.userId)
        self.assertIsNone(mp)

    def test_fail_maxp2(self):
        mp = add_match_db(5,11,self.userId)
        self.assertIsNone(mp)

    def test_fail_minp(self):
        mp = add_match_db(2,6,self.userId)
        self.assertIsNone(mp)

    def test_fail_minp2(self):
        mp = add_match_db(11,12,self.userId)
        self.assertIsNone(mp)


    def test_fail_minp_and_maxp(self):
        mp = add_match_db(7,6,self.userId)
        self.assertIsNone(mp)

    #there is a case that this test fails if we reach that id
    def test_fail_id(self):
        mp = add_match_db(2,6,99999999999)
        self.assertIsNone(mp)

    def test_add_userplayer_ok(self):
        oneid = get_user("one","one")['Id']
        matchid= add_match_db(7,9,self.userId)["Match_id"]
        self.assertTrue(add_user_in_match(oneid,matchid,1))

    def test_add_userplayer_fail_uid(self):
        matchid= add_match_db(7,9,self.userId)["Match_id"]
        self.assertFalse(add_user_in_match(99999999999,matchid,1))

    def test_add_userplayer_fail_mid(self):
        self.assertFalse(add_user_in_match(self.userId,99999999999,1))

    def test_space_ok(self):
        mp = add_match_db(5,5,self.userId)
        self.assertTrue(there_is_space(mp["Match_id"]))


    def test_space_ok2(self):
        mp = add_match_db(5,5,self.userId)
        oneid = get_user("one","one")['Id']
        one1id = get_user("one1","one")['Id']
        one2id = get_user("one2","one")['Id']
        add_user_in_match(oneid,mp["Match_id"],1)
        add_user_in_match(one1id,mp["Match_id"],1)
        add_user_in_match(one2id,mp["Match_id"],1)
        self.assertTrue(there_is_space(mp["Match_id"]))


    def test_space_false(self):
        mp = add_match_db(5,5,self.userId)
        oneid = get_user("one","one")['Id']
        one1id = get_user("one1","one")['Id']
        one2id = get_user("one2","one")['Id']
        one3id = get_user("one3","one")['Id']
        add_user_in_match(oneid,mp["Match_id"],1)
        add_user_in_match(one1id,mp["Match_id"],1)
        add_user_in_match(one2id,mp["Match_id"],1)
        add_user_in_match(one3id,mp["Match_id"],1)
        self.assertFalse(there_is_space(mp["Match_id"]))


    def test_space_false2(self):
        mp = add_match_db(5,10,self.userId)
        oneid = get_user("one","one")['Id']
        one1id = get_user("one1","one")['Id']
        one2id = get_user("one2","one")['Id']
        one3id = get_user("one3","one")['Id']
        one4id = get_user("one4","one")['Id']
        one5id = get_user("one5","one")['Id']
        one6id = get_user("one6","one")['Id']
        one7id = get_user("one7","one")['Id']
        one8id = get_user("one8","one")['Id']
        add_user_in_match(oneid,mp["Match_id"],1)
        add_user_in_match(one1id,mp["Match_id"],1)
        add_user_in_match(one2id,mp["Match_id"],1)
        add_user_in_match(one3id,mp["Match_id"],1)
        add_user_in_match(one4id,mp["Match_id"],1)
        add_user_in_match(one5id,mp["Match_id"],1)
        add_user_in_match(one6id,mp["Match_id"],1)
        add_user_in_match(one7id,mp["Match_id"],1)
        add_user_in_match(one8id,mp["Match_id"],1)
        self.assertFalse(there_is_space(mp["Match_id"]))

    def test_space_ok10(self):
        mp = add_match_db(5,10,self.userId)
        oneid = get_user("one","one")['Id']
        one1id = get_user("one1","one")['Id']
        one2id = get_user("one2","one")['Id']
        one3id = get_user("one3","one")['Id']
        one4id = get_user("one4","one")['Id']
        one5id = get_user("one5","one")['Id']
        one6id = get_user("one6","one")['Id']
        one7id = get_user("one7","one")['Id']
        add_user_in_match(oneid,mp["Match_id"],1)
        add_user_in_match(one1id,mp["Match_id"],1)
        add_user_in_match(one2id,mp["Match_id"],1)
        add_user_in_match(one3id,mp["Match_id"],1)
        add_user_in_match(one4id,mp["Match_id"],1)
        add_user_in_match(one5id,mp["Match_id"],1)
        add_user_in_match(one6id,mp["Match_id"],1)
        add_user_in_match(one7id,mp["Match_id"],1)
        self.assertTrue(there_is_space(mp["Match_id"]))


if __name__ == '__main__':
    unittest.main()
