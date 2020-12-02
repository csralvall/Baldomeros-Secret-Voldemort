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

class Testupdatepass(unittest.TestCase):

    def setUp(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

        create_user("example@gmail.com","example", "password")

        self.userid = get_user("example","password")['Id']
    
    def tearDown(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

#--------------------------- Test get_user_and_email ----------------------------

    def test_get_user_and_email1(self):
        self.assertEqual(get_username_and_email(self.userid), {'Username':'example', 'Email':'example@gmail.com'})

    def test_get_user_and_email2(self):
        self.assertNotEqual(get_username_and_email(self.userid), {'Username':'example@gmail.com', 'Email':'example'})

    def test_get_user_and_email3(self):
        self.assertNotEqual(get_username_and_email(self.userid), {'Username':'Example', 'Email':'Example@gmail.com'})



if __name__ == '__main__':
    unittest.main()
