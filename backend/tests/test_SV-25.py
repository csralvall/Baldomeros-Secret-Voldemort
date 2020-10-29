import unittest 
from backend.db.crud import *
from backend.db.database import *

class TestAddMatch(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        create_user("exapmle@gmail.com","exapmle","password")
        create_user("one@gmail.com","one","one")

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    def test_ok1(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(5,5,userId)
        self.assertIsNotNone(mp["Match_id"])
        self.assertIsNotNone(mp["Player_id"])

    def test_ok2(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(6,7,userId)
        self.assertIsNotNone(mp["Match_id"])
        self.assertIsNotNone(mp["Player_id"])

    def test_fail_maxp(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(5,1,userId)
        self.assertIsNone(mp)

    def test_fail_maxp2(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(5,11,userId)
        self.assertIsNone(mp)

    def test_fail_minp(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(2,6,userId)
        self.assertIsNone(mp)

    def test_fail_minp2(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(11,12,userId)
        self.assertIsNone(mp)


    def test_fail_minp_and_maxp(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        mp = add_match_db(7,6,userId)
        self.assertIsNone(mp)

    #there is a case that this test fails if we reach that id
    def test_fail_id(self):
        mp = add_match_db(2,6,99999999999)
        self.assertIsNone(mp)

    def test_add_userplayer_ok(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        oneu = get_user("one","one")
        oneid = oneu['Id']
        matchid= add_match_db(7,9,userId)["Match_id"]
        self.assertTrue(add_user_in_match(oneid,matchid,1))

    def test_add_userplayer_fail_uid(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        matchid= add_match_db(7,9,userId)["Match_id"]
        self.assertFalse(add_user_in_match(99999999999,matchid,1))

    def test_add_userplayer_fail_mid(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertFalse(add_user_in_match(userId,99999999999,1))


if __name__ == '__main__':
    unittest.main()
