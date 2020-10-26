from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)  

SecretRolDiccionary = {0:"Voldemort",
                       1: "Death Eater",
                       2: "Order of The Phoenix"}

GovRolDiccionary = {0: "HeadMaster",
                    1: "Magic Minister",
                    2: "Citizen"}

class Player(db.Entity):
    PlayerId = PrimaryKey(int, auto=True)
    Position = Required(int, min=0, max=5)
    SecretRol = Required(int, min=0, max=2)
    GovRol = Required(int, min=0, max=2)
    IsDead = Required(bool)
    UserId = Optional('User')
    MatchId = Optional('Match')

class User(db.Entity):
    Id = PrimaryKey(int, auto=True)
    Email = Required(str, unique=True)
    Username = Required(str, max_len=30, unique=True)
    Password = Required(str, hidden=True, max_len=30)
    Players = Set('Player')
    Matches = Set('Match')


db.generate_mapping(create_tables=True)  
