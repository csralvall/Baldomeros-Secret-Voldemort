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

from server.tests.helpers import *

class TestCrudAllowedCases(unittest.TestCase):

    def setUp(self):
        create_user("mati@gmail.com", "mati", "123456")

    def tearDown(self):
        delete_user("mati@gmail.com", "mati", "123456")

    def test_user_is_registred_1(self):
        self.assertTrue(user_is_registred("mati", "123456"))

    def test_check_username_1(self):
        self.assertTrue(check_username("mati"))

    def test_check_mail_1(self):
        self.assertTrue(check_email("mati@gmail.com"))

    def test_get_user(self):
        self.assertEqual(get_user("mati", "123456")['Username'],  "mati")


class TestCrudBadCases(unittest.TestCase):

    def test_user_is_registred_2(self):
        self.assertFalse(user_is_registred("mati", "12345"))

    def test_user_is_registred_3(self):
        self.assertFalse((user_is_registred("", "123456")))

    def test_user_is_registred_4(self): 
        self.assertFalse((user_is_registred("mati", "")))           

    def test_user_is_registred_5(self): 
        self.assertFalse((user_is_registred("", "")))    
    
    def test_check_username_2(self):
        self.assertFalse(check_username("mat"))

    def test_check_username_3(self):
        self.assertFalse(check_username(""))

    def test_check_mail_2(self):
        self.assertFalse(check_email("mati@gmail"))

    def test_check_mail_3(self):
        self.assertFalse(check_email(""))

    def test_get_user_2(self):
        self.assertEqual(get_user("matii", "asfa"), None)


if __name__ == '__main__':
    unittest.main()

