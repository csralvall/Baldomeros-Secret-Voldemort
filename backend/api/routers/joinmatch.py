from fastapi import FastAPI, HTTPException
from backend.db.crud import *

app = FastAPI()

def there_is_space(mid): return True

@app.post("/game/{gid}")
async def join_game(mid: int, user: int): 

    if there_is_space(mid):

        playerobj = add_user_in_match(user, mid, 5) #hardcodeado position should be there

        if (playerobj is not None):

            playerdic = {
                "Match_id": mid['Id'],
                "Player_id": playerobj['Id']
            }

            return playerdic

        else: 

            raise HTTPException(status_code=404, detail="couldnt add the user")

    else: 

        raise HTTPException(status_code=404, detail="there is no space")

