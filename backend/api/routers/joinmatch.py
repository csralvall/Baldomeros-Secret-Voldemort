from fastapi import FastAPI, HTTPException
from backend.db.crud import *

def put_user_in_match(mid,user): return True # esperar funcion de Feltes

@app.post("/game/{gid}")
async def join_game(mid: int, user: int): # Chequear los tipos
  
    if (there_is_space(mid))

        if (put_user_in_match(mid,user))

            return ("user added succesfully")
        else 
            raise HTTPException(status_code=404, detail="couldnt add the user")
    else 
        raise HTTPException(status_code=404, detail="there is no space")