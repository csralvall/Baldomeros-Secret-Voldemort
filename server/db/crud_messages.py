from pony.orm import db_session, select, count
from server.db.database import *
from server.db.dicts import *
from server.db.crud import ResourceNotFound, MatchNotFound

class BadUsername(Exception):
    """ Raised when the username is longer than the accepted in the database. """
    pass 


@db_session
def send_message(match_id: int, username: str, text: str):
    if not Match.exists(Id = match_id):
        raise MatchNotFound
    if len(username)>30:
        raise BadUsername
    messages_db = Match[match_id].Messages.order_by(Message.Number)
    new_message= Message(
        Match= Match[match_id],
        Username = username,
        Text = text,
        Number =len(messages_db))

@db_session
def read_messages(match_id: int):
    if not Match.exists(Id = match_id):
        raise MatchNotFound    
    messages_db = Match[match_id].Messages
    messages = dict()
    for m in messages_db:
        messages[m.Number]=m.to_dict(['Username','Text'])
    return messages