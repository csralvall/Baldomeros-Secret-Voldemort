from pony.orm import *

db = Database()
db.bind('sqlite', 'example.sqlite', create_db=True)

db.generate_mapping(create_tables=True)