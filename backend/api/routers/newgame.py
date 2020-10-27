from fastapi import FastAPI, HTTPException
from backend.db.crud import *

app = FastAPI()

@app.post("/game/new")
async def create_match(minp: int, maxp: int, uhid: int):
  
    newmatch = add_match_db(minp,maxp,uhid)

    if (newmatch is not None): 
        return newmatch
    else:
        raise HTTPException(status_code=404, detail="couldnt create a game")  


