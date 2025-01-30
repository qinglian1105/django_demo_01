from typing import Annotated
from fastapi import Depends
from schema.data_outline import User, NewXs, InputData 
from api.auth import get_current_active_user
from fastapi import APIRouter
import ml_predictor.ml_inference as infer
import datetime as dt


router = APIRouter(tags=["ml"], prefix="/api")


@router.post("/ml/ml_predict")
async def ml_predict(
    current_user: Annotated[User, Depends(get_current_active_user)], new_xs: NewXs
):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("ml_predict", t)    
    y_pred = infer.predict_with_ml(dict(new_xs))
    return y_pred


@router.post("/ml/scorecard_predict")
async def scorecard_predict(
    current_user: Annotated[User, Depends(get_current_active_user)],
    input_data: InputData,
):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("scorecard_predict", t)
    res = infer.get_predict_report(dict(input_data))
    return res
