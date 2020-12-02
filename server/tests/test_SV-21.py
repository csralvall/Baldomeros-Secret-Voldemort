import unittest 
from server.db.database import *
from server.tests.helpers import *
from server.db.crud.exception_crud import *
from server.db.crud.crud_deck import *
from server.db.crud.crud_election import *
from server.db.crud.crud_legislative_session import *
from server.db.crud.crud_lobby import *
from server.db.crud.crud_match import *
from server.db.crud.crud_messages import *
from server.db.crud.crud_profile import *
from server.db.crud.crud_spell import *


class TestCreation(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)    

    def test_first(self):
        self.assertTrue(create_user("example@gmail.com","example","password"))

    def test_second(self):
        self.assertFalse(create_user("example1@gmail.com","","password1"))

    def test_third(self):
        self.assertFalse(create_user("","example2","password2"))

    def test_fourth(self):
        self.assertFalse(create_user("example3@gmail.com","",""))

    def test_fifth(self):
        self.assertTrue(create_user("example4@gmail.com","example4","password"))

    def test_drop(self):
        self.assertTrue(create_user("example5@gmail.com","example5","password"))


if __name__ == '__main__':
    unittest.main()
