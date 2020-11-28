from server.db.crud import *

from server.db.dicts import *

from fastapi import APIRouter, HTTPException, Query, Path, Body


router = APIRouter()


@router.patch("/{match_id}/board/avada-kedavra", tags=["Spells"])
async def use_avada_kedavra(
    match_id: int = Path(..., title="The ID of the current match"),
    playername: str = Query(..., title="Name of player who receives the spell")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    minister = get_minister_username(match_id)

    if minister == playername:
        raise HTTPException(status_code=403, detail="You can't kill yourself")

    try:
        player_id = get_player_id_from_username(match_id, playername)
        board_id = get_match_board_id(match_id)
        avada_kedavra(board_id, player_id)
        change_ingame_status(match_id, NOMINATION)#minister selects director stage
        change_to_exdirector(match_id)
        set_next_minister(match_id)
        if is_voldemort_dead(match_id):
            set_winner(match_id, VOLDEMORT_DEAD)
    except VoldemortNotFound:
        raise HTTPException(status_code=500, detail="Voldemort was not set")
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Resource not found")
    except NoDirector:
        raise HTTPException(status_code=404, detail="There is no director")

    return f"{playername} is dead"

def minister_expelliarmus(match_id: int, minister_desition: str):

    board_id = get_match_board_id(match_id)

    if not get_expelliarmus_status(board_id) == expelliarmus[MINISTER_STAGE]:
        raise HTTPException(status_code=404, detail="No desition to make.")    

    if minister_desition is None:
        raise HTTPException(status_code=404, detail="Minister must decide.")    

    if minister_desition == ingame_status[EXPELLIARMUS]:
        selected_cards = show_selected_deck(board_id)
        if len(selected_cards) > 2:
            raise HTTPException(status_code=404,
                                detail="Minister should discard one card.")    

        for card in selected_cards:
            discard_proclamation(board_id, card)

        set_expelliarmus_status(board_id, UNLOCKED)

        change_ingame_status(match_id, NOMINATION)
        get_top_three_proclamation(board_id)
        failed_election(match_id)
        failed_director_expelliarmus(match_id)
        set_next_minister_failed_election(match_id)

    else:
        set_expelliarmus_status(board_id, REJECTED)
        change_ingame_status(match_id, DIRECTOR_SELECTION)

def director_expelliarmus(match_id: int):
    board_id = get_match_board_id(match_id)

    if not get_expelliarmus_status(board_id) == expelliarmus[UNLOCKED]:
        raise HTTPException(status_code=404, detail="Not allowed.")    

    change_ingame_status(match_id, EXPELLIARMUS)
    set_expelliarmus_status(board_id, MINISTER_STAGE)

@router.patch("/{match_id}/board/expelliarmus", tags=["Spells"])
async def use_expelliarmus(
    match_id: int = Path(..., title="The ID of the current match"),
    playername: str = Query(..., title="The playername of the caller"),
    minister_desition: str = Query(None,
                             alias="minister-desition",
                             title="Minister desition about expelliarmus")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="this match does not exist")

    player_id = get_player_id_from_username(match_id, playername)

    if player_id is None:
        raise HTTPException(status_code=404, detail="Player not found")

    minister = get_minister_username(match_id)
    director = get_director_username(match_id)

    if playername == minister:
       minister_expelliarmus(match_id, minister_desition)
    elif playername == director:
        director_expelliarmus(match_id)

@router.patch("/{match_id}/board/no-spell", tags=["Spells"])
async def disable_spell(match_id: int):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")

    change_ingame_status(match_id, NOMINATION)
    change_to_exdirector(match_id)
    set_next_minister(match_id)

    board_id = get_match_board_id(match_id)
    disable_spell(board_id)

    return 200

@router.get("/{match_id}/board/crucio", tags=["Spells"]) # TODO: tests
async def use_crucio(
    match_id: int = Path(..., title="The ID of the current match"),
    playername: str = Query(..., title="The playername of the caller"),
    investigated: str = Query(..., title="Player under investigation")):

    if not check_match(match_id):
        raise HTTPException(status_code=404, detail="this match does not exist")

    if not get_ingame_status(match_id) == USE_SPELL:
        raise HTTPException(status_code=403, detail="Can't use spell now")

    board_id = get_match_board_id(match_id)

    if not get_available_spell(board_id) == CRUCIO:
        raise HTTPException(status_code=403, detail="Spell not available")

    minister_id = get_player_id_from_username(match_id, playername)
    magician_id = get_player_id_from_username(match_id, investigated)

    if minister_id is None or magician_id is None:
        raise HTTPException(status_code=404, detail="Player not found")

    minister = get_minister_username(match_id)

    if not playername == minister:
        raise HTTPException(status_code=403, detail="You are not minister")

    magician_rol = get_player_rol(magician_id)

    if magician_rol == VOLDEMORT:
        magician_rol = DEATH_EATER

    return SecretRolDiccionary[magician_rol]
