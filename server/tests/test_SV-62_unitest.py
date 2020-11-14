import unittest 
from server.db.crud import *
from server.db.database import *
from server.tests.helpers import *

class TestSV62(unittest.TestCase):

    def setUp(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

        create_user("example1@gmail.com","example1", "password")

        create_user("example2@gmail.com","example2","password")   
        create_user("example3@gmail.com","example3","password")
        create_user("example4@gmail.com","example4","password")
        create_user("example5@gmail.com","example5","password")
        create_user("example6@gmail.com","example6","password")
        create_user("example7@gmail.com","example7", "password")
        create_user("example8@gmail.com","example8","password")
        create_user("example9@gmail.com","example9","password")
        create_user("example10@gmail.com","example10","password")
        create_user("example11@gmail.com","example11","password")

        create_user("example12@gmail.com","example12","password")   
        create_user("example13@gmail.com","example13","password")
        create_user("example14@gmail.com","example14","password")
        create_user("example15@gmail.com","example15","password")
        create_user("example16@gmail.com","example16","password")

        self.user1id = get_user("example1","password")['Id']

        self.user2id = get_user("example2","password")['Id']
        self.user3id = get_user("example3","password")['Id']
        self.user4id = get_user("example4","password")['Id']
        self.user5id = get_user("example5","password")['Id']
        self.user6id = get_user("example6","password")['Id']
        self.user7id = get_user("example7","password")['Id']
        self.user8id = get_user("example8","password")['Id']
        self.user9id = get_user("example9","password")['Id']
        self.user10id = get_user("example10","password")['Id'] 
        self.user11id = get_user("example11","password")['Id'] 

        self.user12id = get_user("example12","password")['Id']
        self.user13id = get_user("example13","password")['Id']
        self.user14id = get_user("example14","password")['Id']
        self.user15id = get_user("example15","password")['Id']
        self.user16id = get_user("example16","password")['Id']   

        self.username1 = get_user_username(self.user1id)
        self.username2 = get_user_username(self.user12id)
        self.username3 = get_user_username(self.user2id)
     
        self.game1 = add_match_db(5, 5, self.user1id) #partuda con 1 jugador
        self.game2 = add_match_db(5, 10, self.user12id) #partida con 5 jugadores
        self.game3 = add_match_db(5, 10, self.user2id) #partida con 10 jugadores

        self.matchid3 = self.game3["Match_id"]
        self.matchid2 = self.game2["Match_id"]
        self.matchid1 = self.game1["Match_id"]

        player2 = add_user_in_match(self.user13id,self.matchid1,1)
        player3 = add_user_in_match(self.user14id,self.matchid1,2)
        player4 = add_user_in_match(self.user15id,self.matchid1,3)
        player5 = add_user_in_match(self.user16id,self.matchid1,4)

        player2 = add_user_in_match(self.user3id,self.matchid1,1)
        player3 = add_user_in_match(self.user4id,self.matchid1,2)
        player4 = add_user_in_match(self.user5id,self.matchid1,3)
        player5 = add_user_in_match(self.user6id,self.matchid1,4)
        player6 = add_user_in_match(self.user7id,self.matchid1,5)
        player7 = add_user_in_match(self.user8id,self.matchid1,6)
        player8 = add_user_in_match(self.user9id,self.matchid1,7)
        player9 = add_user_in_match(self.user10id,self.matchid1,8)   
        player10 = add_user_in_match(self.user11id,self.matchid1,9)   
 
    def tearDown(self):

        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)


#--------------------------- Test get_min_players ----------------------------

    def test_max_players(self):
        self.assertTrue(get_max_players(self.matchid1)==5)

    def test_max_players2(self):
        self.assertTrue(get_max_players(self.matchid2)==10)

    def test_max_players3(self):
        self.assertFalse(get_max_players(self.matchid2)==6)  

    def test_max_players4(self):
        self.assertFalse(get_max_players(self.matchid2)==4)          

#--------------------------- Test set_game_decorated ----------------------------         

    def test_set_game_decorated(self): 
        self.assertIsNotNone(set_game_decorated(self.matchid1))

    def test_set_game_decorated2(self): 
        self.assertIsNotNone(set_game_decorated(self.matchid2))

    def test_set_game_decorated3(self): 
        self.assertIsNotNone(set_game_decorated(self.matchid3))   

    def test_set_game_decorated4(self):
        id1 = self.matchid1
        game = set_game_decorated(id1)    
        self.assertEqual(game, {"Nombre_partida": self.username1, "Min_and_Max": (5,5), "Match_id": id1})

    def test_set_game_decorated5(self):
        id2 = self.matchid2
        game = set_game_decorated(id2)   
        self.assertEqual(game, {"Nombre_partida": self.username2, "Min_and_Max": (5,10), "Match_id": id2})

    def test_set_game_decorated6(self):
        id3 = self.matchid3
        game = set_game_decorated(id3)
        self.assertEqual(game, {"Nombre_partida": self.username3, "Min_and_Max": (5,10), "Match_id": id3})

        