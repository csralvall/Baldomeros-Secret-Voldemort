from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

