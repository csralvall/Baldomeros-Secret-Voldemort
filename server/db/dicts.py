
DEATH_EATER_STR = "death eater"
PHOENIX_STR = "phoenix"
NO_WINNER_YET = "no winner yet"

Status = {0: "Joinable",
          1: "In Game",
          2: "Finished"}

JOINABLE = 0
IN_GAME = 1
FINISHED = 2

BoardType = {0: "5-6",
             1: "7-8",
             2: "9-10"}

SMALL_BOARD = 0
MEDIUM_BOARD = 1
BIG_BOARD = 2

SecretRolDiccionary = {0: "Voldemort",
                       1: "Death Eater",
                       2: "Order of The Phoenix"}

VOLDEMORT = 0
DEATH_EATER = 1
PHOENIX = 2

GovRolDiccionary = {0: "Head Master",
                    1: "Magic Minister",
                    2: "Magician",
                    3: "Ex Minister",
                    4: "Ex Director"}

DIRECTOR = 0
MINISTER = 1
MAGICIAN = 2
EX_MINISTER = 3
EX_DIRECTOR = 4
NO_DIRECTOR = 99

VoteType = {0: "nox",
            1: "lumos",
            2: "missing vote"}

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
CHAOS = 5#hay que agregarlo en database y en un if que chequea si el estado es legal
EXPELLIARMUS = 6

expelliarmus = ("locked", "unlocked", "minister stage", "rejected")

LOCKED = 0
UNLOCKED = 1
MINISTER_STAGE = 2
REJECTED = 3

