from fastapi import FastAPI, HTTPException

#import ../backend/models.py # importar models

app = FastAPI()


def add_match_db(minp,maxp,uhid): return (minp < maxp)

@app.post("/game/new")
async def create_match(minp: int, maxp: int, uhid: int):
  
    if add_match_db(minp,maxp,uhid): 

        return {"game": "created game"} #chequear esto
    else:
        raise HTTPException(status_code=404, detail="couldnt create a game")  