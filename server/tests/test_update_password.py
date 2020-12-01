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

        create_user("example@gmail.com","example", "oldpassword")

        self.userid = get_user("example","oldpassword")['Id']
    
    def tearDown(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)


#--------------------------- Test update_password ----------------------------

    def test_update_pass1(self):
        update_password(self.userid, "oldpassword", "newpassword")
        self.assertEqual(get_password(self.userid), "newpassword")
        self.assertNotEqual(get_password(self.userid), "oldpassword")

    def test_update_pass2(self):
        update_password(self.userid, "oldpassword", "newpassword")
        self.assertNotEqual(get_password(self.userid), "anythingelse")

if __name__ == '__main__':
    unittest.main()
