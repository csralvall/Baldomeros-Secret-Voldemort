import unittest
from crud import user_is_registred, check_email, check_username


class TestCrud(unittest.TestCase):

    def test_user_is_registred_1(self):
        self.assertTrue(user_is_registred("mati", "123456"))

    def test_user_is_registred_2(self):
        self.assertFalse(user_is_registred("mati", "12345"))

    def test_user_is_registred_3(self):
        self.assertFalse((user_is_registred("", "123456")))

    def test_user_is_registred_4(self): 
        self.assertFalse((user_is_registred("mati", "")))           

    def test_user_is_registred_5(self): 
        self.assertFalse((user_is_registred("", "")))    
    
    def test_check_username_1(self):
        self.assertTrue(check_username("mati"))

    def test_check_username_2(self):
        self.assertFalse(check_username("mat"))

    def test_check_username_3(self):
        self.assertFalse(check_username(""))

    def test_check_mail_1(self):
        self.assertTrue(check_email("mati@gmail.com"))

    def test_check_mail_2(self):
        self.assertFalse(check_email("mati@gmail"))

    def test_check_mail_3(self):
        self.assertFalse(check_email(""))

    def test_get_user(self):
        self.assertEqual(get_user("mati", "123456"), {"Id": 12, "Username": "mati"})

    def test_get_user_2(self):
        self.assertEqual(get_user("matii", "asfa"), None)

if __name__ == '__main__':
    unittest.main()

