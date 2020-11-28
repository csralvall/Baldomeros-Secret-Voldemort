
DEATH_EATER_STR = "death eater"
PHOENIX_STR = "phoenix"
NO_WINNER_YET = "no winner yet"
VOLDEMORT_DEAD = "Voldemort died"
VOLDEMORT_DIRECTOR = "Voldemort is the director"


Status = ("Joinable", "In Game", "Finished", "Closed")

JOINABLE = 0
IN_GAME = 1
FINISHED = 2
CLOSED = 3

BoardType = ("5-6", "7-8", "9-10")

SMALL_BOARD = 0
MEDIUM_BOARD = 1
BIG_BOARD = 2

SecretRolDiccionary = ("Voldemort", "Death Eater", "Order of The Phoenix")

VOLDEMORT = 0
DEATH_EATER = 1
PHOENIX = 2

GovRolDiccionary = ("Head Master",
                    "Magic Minister",
                    "Magician",
                    "Ex Minister",
                    "Ex Director")

DIRECTOR = 0
MINISTER = 1
MAGICIAN = 2
EX_MINISTER = 3
EX_DIRECTOR = 4
NO_DIRECTOR = 99

VoteType = ("nox", "lumos", "missing vote")

NOX = 0
LUMOS = 1
MISSING_VOTE = 2

spells = (None, "Avada Kedavra", "Imperio", "Crucio", "Adivination")

NO_SPELL = 0
AVADA_KEDAVRA = 1
IMPERIO = 2
CRUCIO = 3
ADIVINATION = 4

ingame_status = ("nomination",
                 "election",
                 "minister selection",
                 "director selection",
                 "use spell",
                 "chaos",
                 "expelliarmus")

NOMINATION = 0
ELECTION = 1
MINISTER_SELECTION = 2
DIRECTOR_SELECTION = 3
USE_SPELL = 4
CHAOS = 5
EXPELLIARMUS = 6

expelliarmus = ("locked", "unlocked", "minister stage", "rejected")

LOCKED = 0
UNLOCKED = 1
MINISTER_STAGE = 2
REJECTED = 3
