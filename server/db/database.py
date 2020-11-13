from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)  

class Match(db.Entity):
    Id = PrimaryKey(int, auto=True)
    MaxPlayers = Required(int, min=5, max=10)
    MinPlayers = Required(int, min=5, max=10)
    Status = Required(int, min=0, max=2)
    IngameStatus = Required(int, min=0, max=4)
    BoardType = Required(int, min=0, max=2)
    CandidateDirector = Optional(int)
    CurrentMinister = Optional(int)
    CurrentDirector = Optional(int)
    Players = Set('Player')
    Board = Optional('Board', cascade_delete=True)
    Creator = Required('User')
    Winner = Required(str)
    
class Board(db.Entity):
    Id = PrimaryKey(int, auto=True)
    BoardType = Required(int, min=0, max=2)
    PhoenixProclamations = Optional(int, min=0, max=5)
    DeathEaterProclamations = Optional(int, min=0, max=6)
    FailedElectionsCount = Optional(int)
    AvailableSpell = Optional(int, min=0, max=4, default=0)
    BoardStatus = Optional(int, min=0, max=4, default=0)
    Proclamations = Optional('Deck', cascade_delete=True)
    Match = Required(Match)

class Deck(db.Entity):
    Id = PrimaryKey(int, auto=True)
    Discarded = Required(int, min=0, max=17)
    Available = Required(int, min=0, max=17)
    Cards = Required(Json)
    Board = Required(Board)

class Player(db.Entity):
    PlayerId = PrimaryKey(int, auto=True)
    Position = Required(int, min=0, max=9)
    SecretRol = Required(int, min=0, max=2)
    GovRol = Required(int, min=0, max=4)
    IsDead = Required(bool)
    Vote = Optional(int, min=0, max=2)
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

