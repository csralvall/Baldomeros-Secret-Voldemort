import unittest 
from ..crud import *
from ..database import *

class TestAddMatch(unittest.TestCase):

    def setUp(self):
        create_user("joaco@gmail.com","joaco","kajdsflaskfdjsla")
    
    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    def test_ok1(self):
        user = get_user("joaco","kajdsflaskfdjsla")
        userId = user['Id']
        self.assertTrue(add_match_db(5,5,userId))

    def test_ok2(self):
        user = get_user("joaco","kajdsflaskfdjsla")
        userId = user['Id']
        self.assertTrue(add_match_db(6,7,userId))

    def test_fail_maxp(self):
        user = get_user("joaco","kajdsflaskfdjsla")
        userId = user['Id']
        self.assertFalse(add_match_db(5,1,userId))

    def test_fail_minp(self):
        user = get_user("joaco","kajdsflaskfdjsla")
        userId = user['Id']
        self.assertFalse(add_match_db(2,6,userId))

    def test_fail_id(self):
        self.assertFalse(add_match_db(2,6,'3252135'))


if __name__ == '__main__':
    unittest.main()
