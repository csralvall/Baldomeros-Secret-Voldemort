from pony.orm import *

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
    MatchId = Optional(Match)