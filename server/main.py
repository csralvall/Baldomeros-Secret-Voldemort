from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.db.crud.exception_crud import *
from server.db.crud.crud_deck import *
from server.db.crud.crud_election import *
from server.db.crud.crud_legislative_session import *
from server.db.crud.crud_lobby import *
from server.db.crud.crud_match import *
from server.db.crud.crud_messages import *
from server.db.crud.crud_profile import *
from server.db.crud.crud_spell import *

from server.api.routes import authentication, game, lobby, spells

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# USER
app.include_router(authentication.router)

# OPEN GAMES
app.include_router(lobby.router, prefix="/game")

app.include_router(game.router, prefix="/game")

app.include_router(spells.router, prefix="/game")

