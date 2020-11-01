from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.crud import *

from backend.api.routers import users, newgame, joinmatch, gamestatus, game

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
  return {"secret voldemort": "initial page"}

# USER

app.include_router(users.router)

@app.put("/session")
async def update_session():
  return {"secret voldemort": "update session status"}

@app.delete("/session")
async def close_session():
  return {"secret voldemort": "close session"}

@app.get("/user/{uid}")
async def get_user_profile():
  return {"user": "profile"}

@app.patch("/user/{uid}")
async def load_user_data():
  return {"user": "new data"}

@app.put("/user/{uid}/password")
async def change_user_password():
  return {"user": "password changed"}

# USER

# OPEN GAMES

app.include_router(newgame.router)
app.include_router(joinmatch.router)
app.include_router(gamestatus.router)
app.include_router(game.router)

# @app.get("/games")
# async def status_games():
#   return {"games": "game status"}

# @app.post("/game/new")
# async def create_game():
#   return {"game": "created game"}

# @app.post("/game/{mid}")
# async def join_game():
#   return {"game": "your game"}


@app.patch("/game/{gid}")
async def start_game():
  return {"game": "started game"}

@app.get("/game/{gid}/players")
async def get_game_players():
  return {"game": "list of players"}

# OPEN GAMES

# RUNNING GAMES

#@app.get("/game/{gid}/player/{pid}")
#async def get_player_info():
  #return {"game": "player info"}

#@app.put("/game/{gid}/player/{pid}/vote")
#async def vote_candidate():
#  return {"game": "vote"}

@app.get("/game/{gid}/election")
async def get_election_info():
  return {"game": "election info"}

@app.get("/game/{gid}/deck")
async def get_proclamations():
  return {"game": "proclamations"}

@app.put("/game/{gid}/proclamation")
async def discard_proclamations():
  return {"game": "proclamations discarded"}

@app.get("/game/{gid}/board")
async def get_phoenix_proclamations():
  return {"game": "board infor"}

# RUNNING GAMES
