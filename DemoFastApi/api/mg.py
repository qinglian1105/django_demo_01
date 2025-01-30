from typing import Annotated
from fastapi import Depends
from schema.data_outline import User
from api.auth import get_current_active_user
from fastapi import APIRouter
import database.db_mg as dmg
import datetime as dt


router = APIRouter(tags=["mg"], prefix="/api")


@router.get("/mg/default_info")
async def default_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("query mongodb - default info", t)
    ds = dmg.default_condition()
    return ds


@router.get("/mg/default_age")
async def default_age(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("query mongodb - default age", t)
    ds = dmg.default_condition_age()
    return ds


@router.get("/mg/db_info")
async def mg_db_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("query mongodb - db_info", t)
    ds = dmg.get_mongodb_info()
    return ds
