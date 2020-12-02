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

class TestChat(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        delete_data(Message)

        create_user("example1@gmail.com","example1","password")

        self.user_id_1=get_user("example1","password")['Id']
        match_and_player= add_match_db(5, 10,self.user_id_1)
        self.match_id =match_and_player["Match_id"]
        self.player_id_1 = match_and_player["Player_id"]
        self.longusername = "0123456789012345678901234567890"

    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        delete_data(Message)

    def test_send_read_ok(self):
        send_message(self.match_id,"pepe","hola")
        self.assertEqual(read_messages(self.match_id), {0:{"Username":"pepe","Text":"hola"}})
        send_message(self.match_id,"feltes","hola, pepe")
        self.assertEqual(read_messages(self.match_id), {0:{"Username":"pepe","Text":"hola"},1:{"Username":"feltes","Text":"hola, pepe"}})
        send_message(self.match_id,"pepe","como estas?")
        print(read_messages(self.match_id))
        self.assertEqual(read_messages(self.match_id), {0:{"Username":"pepe","Text":"hola"},1:{"Username":"feltes","Text":"hola, pepe"},2:{"Username":"pepe","Text":"como estas?"}})

    def test_send_wrong_mid(self):
        self.assertRaises(MatchNotFound,send_message,self.match_id+1,"pepe","hola")

    def test_send_wrong_username(self):
        self.assertRaises(BadUsername,send_message,self.match_id, self.longusername,"hola")

    def test_read_wrong_mid(self):
        self.assertRaises(MatchNotFound,read_messages,self.match_id+1)
        
if __name__ == "__main__":
    unittest.main()
