from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)  

Status = {0: "Joinable",
          1: "In Game",
          2: "Finished"}

BoardType = {0: "5-6",
             1: "7-8",
             2: "9-10"}

SecretRolDiccionary = {0:"Voldemort",
                       1: "Death Eater",
                       2: "Order of The Phoenix"}

GovRolDiccionary = {0: "HeadMaster",
                    1: "Magic Minister",
                    2: "Citizen"}

class Match(db.Entity):
    Id = PrimaryKey(int, auto=True)
    MaxPlayers = Required(int, min=5, max=10)
    MinPlayers = Required(int, min=5, max=10)
    Status = Required(int, min=0, max=2)
    BoardType = Required(int, min=0, max=2)
    LastMinister = Optional(int)
    Players = Set('Player')
    Board = Optional('Board')
    Creator = Required('User')
    

class Board(db.Entity):
    Id = PrimaryKey(int, auto=True)
    BoardType = Required(int, min=0, max=2)
    PhoenixProclamations = Optional(int, min=0, max=5)
    DeathEaterProclamations = Optional(int, min=0, max=5)
    FailedElectionsCount = Optional(int)
    Match = Required(Match)


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
