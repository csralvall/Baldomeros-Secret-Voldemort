from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)  

Status = {0: "Joinable",
          1: "In Game",
          2: "Finished"}

BoardType = {0: "5-6",
             1: "7-8",
             2: "9-10"}

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

db.generate_mapping(create_tables=True)  

