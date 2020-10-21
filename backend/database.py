from pony.orm import *

db = Database()
db.bind('sqlite', 'example.sqlite', create_db=True)

class User(db.Entity):
    Id = PrimaryKey(int, auto=True)
    Email = Required(str, unique=True)
    Username = Required(str, max_len=30, unique=True)
    Password = Required(str, hidden=True, max_len=30)
    Players = Set('Player')
    Matches = Set('Match')

db.generate_mapping(create_tables=True)


