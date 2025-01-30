from typing import Annotated
from fastapi import Depends
from schema.data_outline import User, SelectYear
from api.auth import get_current_active_user
from fastapi import APIRouter
import database.db_pg as dpg



router = APIRouter(tags=["pg"], prefix="/api")


@router.get("/pg/all_years")
async def all_years(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    ds = dpg.get_all_years()
    return ds


@router.post("/pg/loan_amt")
async def loan_amt(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_loan_amt(select_year.yyyy)
    return ds


@router.post("/pg/loan_count")
async def loan_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_loan_count(select_year.yyyy)
    return ds


@router.post("/pg/default_amt")
async def default_amt(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_default_amt(select_year.yyyy)
    return ds


@router.post("/pg/default_count")
async def default_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_default_count(select_year.yyyy)
    return ds


@router.post("/pg/month_loan")
async def month_loan(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_month_loan(select_year.yyyy)
    return ds


@router.post("/pg/month_count")
async def month_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_month_count(select_year.yyyy)
    return ds


@router.post("/pg/purpose")
async def purpose(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_purpose(select_year.yyyy)
    return ds


@router.post("/pg/occupation")
async def occupation(
    current_user: Annotated[User, Depends(get_current_active_user)],
    select_year: SelectYear,
):
    ds = dpg.get_occupation(select_year.yyyy)
    return ds


@router.get("/pg/db_info")
async def pg_db_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    ds = dpg.get_pg_db_info()
    return ds
