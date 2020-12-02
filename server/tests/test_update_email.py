
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

class Testupdateemail(unittest.TestCase):

    def setUp(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

        create_user("oldemail@gmail.com","example", "password")

        self.userid = get_user("example","password")['Id']
    
    def tearDown(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)


#--------------------------- Test update_email ----------------------------

    def test_update_email1(self):
        update_email(self.userid, "oldemail@gmail.com", "newemail@gmail.com")
        self.assertEqual(get_email(self.userid), "newemail@gmail.com")
        self.assertNotEqual(get_email(self.userid), "oldemail@gmail.com")

    def test_update_email2(self):
        update_email(self.userid, "oldemail@gmail.com", "newemail@gmail.com")
        self.assertNotEqual(get_email(self.userid), "anythingelse")

if __name__ == '__main__':
    unittest.main()