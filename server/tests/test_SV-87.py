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

class TestSV87(unittest.TestCase):

    def setUp(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)
        create_user("example@gmail.com","example","password")
        create_user("example2@gmail.com","example2", "password")
        create_user("example3@gmail.com","example3","password")
        create_user("example4@gmail.com","example4","password")
        create_user("example5@gmail.com","example5","password")
        create_user("example6@gmail.com","example6","password")
        self.userid = get_user("example","password")['Id']
        self.user1id = get_user("example2","password")['Id']
        self.user2id = get_user("example3","password")['Id']
        self.user3id = get_user("example4","password")['Id']
        self.user4id = get_user("example5","password")['Id']
        self.user5id = get_user("example6","password")['Id']
        m_p = add_match_db(5, 5,self.user1id)
        m_p2 = add_match_db(5,5,self.user2id)
        self.matchid = m_p["Match_id"]
        self.matchid2 = m_p2["Match_id"]
        player2 = add_user_in_match(self.user2id,self.matchid,2)
        player3 = add_user_in_match(self.user3id,self.matchid,3)
        player4 = add_user_in_match(self.user4id,self.matchid,4)
        player5 = add_user_in_match(self.user5id,self.matchid,5)
        player = add_user_in_match(self.userid,self.matchid,6)
        self.player1id= m_p["Player_id"]
        self.playerid = player.to_dict("PlayerId")["PlayerId"]
        self.player2id = player2.to_dict("PlayerId")["PlayerId"]
        self.player3id = player3.to_dict("PlayerId")["PlayerId"]
        self.player4id = player4.to_dict("PlayerId")["PlayerId"]
        self.player5id = player5.to_dict("PlayerId")["PlayerId"]
        change_player_rol(self.player1id,0) #voldemort
        change_player_rol(self.player2id,1) #death_eater
        change_player_rol(self.player3id,2) #phoenix
        change_player_rol(self.player4id,2) #phoenix
        change_player_rol(self.player5id,2) #phoenix


    def tearDown(self):
        delete_data(Board)
        delete_data(Player)
        delete_data(Match)
        delete_data(User)

    #--------------------------- Test get_player_rol ----------------------------

    def test_is_voldemort(self):
        self.assertEqual(get_player_rol(self.player1id), VOLDEMORT)
    
    def test_is_death_eater(self):
        self.assertEqual(get_player_rol(self.player2id), DEATH_EATER)

    def test_is_Phoenix(self):
        self.assertEqual(get_player_rol(self.player3id), PHOENIX)

    def test_get_player_rol_2(self):
        self.assertEqual(get_player_rol(self.player1id), VOLDEMORT)
        self.assertEqual(get_player_rol(self.player2id), DEATH_EATER)
        self.assertEqual(get_player_rol(self.player3id), PHOENIX)
        self.assertEqual(get_player_rol(self.player4id), PHOENIX)
        self.assertEqual(get_player_rol(self.player5id), PHOENIX)

    #--------------------------- Test get_player_username ----------------------------

    def test_get_player_username(self):
        self.assertEqual(get_player_username(self.player1id), get_user_username(self.user1id))
        self.assertEqual(get_player_username(self.player2id), get_user_username(self.user2id))
        self.assertEqual(get_player_username(self.player3id), get_user_username(self.user3id))
        self.assertEqual(get_player_username(self.player4id), get_user_username(self.user4id))
        self.assertEqual(get_player_username(self.player5id), get_user_username(self.user5id))

    #--------------------------- Test get_death_eater_players_in_match ----------------------------

    def test_get_death_eater_players_in_match(self):
        #Example2 is voldemort, Example3 is Death Eater (look in setUp)
        self.assertEqual(get_death_eater_players_in_match(self.matchid),{'Voldemort':'example2', 'Death Eater': ['example3']})
        self.assertNotEqual(get_death_eater_players_in_match(self.matchid),{'Voldemort':'example3', 'Death Eater': ['example2']})
        
    def test_get_death_eater_players_in_match2(self):
        change_player_rol(self.player3id,1) 
        change_player_rol(self.player4id,1) 
        self.assertEqual(get_death_eater_players_in_match(self.matchid),{'Voldemort':'example2', 'Death Eater': ['example3','example4','example5']})
        
    #--------------------------- Test get_posible_directors ----------------------------

    def test_get_posible_directors(self):
        make_magician(self.player1id)
        make_magician(self.playerid)
        make_magician(self.player2id)
        make_magician(self.player3id)
        make_magician(self.player4id)
        make_magician(self.player5id)
        make_minister(self.player1id)#example2 es el ministro
        self.assertEqual(get_posible_directors(self.matchid), {"posible directors": ['example3','example4','example5','example6','example']})
        make_ex_minister(self.player2id)#example3 es exministro,no tienen que mostrarlo porque son 6.
        self.assertEqual(get_num_players(self.matchid),6)
        self.assertEqual(get_posible_directors(self.matchid), {"posible directors": ['example4','example5','example6','example']})
        kill_player(self.playerid)#ahora se tiene que mostar el 3
        self.assertEqual(get_posible_directors(self.matchid), {"posible directors": ['example3','example4','example5','example6']})


if __name__ == '__main__':
    unittest.main()
