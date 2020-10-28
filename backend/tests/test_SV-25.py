import unittest 
from ..crud import *
from ..database import *

class TestAddMatch(unittest.TestCase):

    def setUp(self):
        delete_data(User)
        create_user("exapmle@gmail.com","exapmle","password")
        
    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    def test_ok1(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertTrue(add_match_db(5,5,userId))

    def test_ok2(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertTrue(add_match_db(6,7,userId))

    def test_fail_maxp(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertFalse(add_match_db(5,1,userId))

    def test_fail_maxp2(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertFalse(add_match_db(5,11,userId))

    def test_fail_minp(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertFalse(add_match_db(2,6,userId))

    def test_fail_minp2(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertFalse(add_match_db(11,12,userId))
    
    def test_fail_minp_and_maxp(self):
        user = get_user("exapmle","password")
        userId = user['Id']
        self.assertFalse(add_match_db(7,6,userId))

    #there is a case that this test fails if we reach that id
    def test_fail_id(self):
        self.assertFalse(add_match_db(2,6,99999999999))


if __name__ == '__main__':
    unittest.main()
