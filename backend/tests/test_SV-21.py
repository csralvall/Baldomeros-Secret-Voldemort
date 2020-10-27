import unittest 
from backend.db.crud import create_user, delete_data
from backend.db.database import *

class TestCrud(unittest.TestCase):

    def setUp(self):
        delete_data(User)
         
    def test_first(self):
        self.assertTrue(create_user("joaco@gmail.com","joaco","kajdsflaskfdjsla"))

    def test_second(self):
        self.assertFalse(create_user("joa@gmail.com","","hola"))

    
    def test_third(self):
        self.assertFalse(create_user("","joaaaa","holaasdsad"))

    def test_fourth(self):
        self.assertFalse(create_user("joafdsa@gmail.com","",""))

    def test_fifth(self):
        self.assertTrue(create_user("joaco1@gmail.com","joaco1","kajdsflaskfdjsla"))

    def test_drop(self):
        self.assertTrue(create_user("joaco@gl.com","co","kajdsflaskfdjsla"))


if __name__ == '__main__':
    unittest.main()
