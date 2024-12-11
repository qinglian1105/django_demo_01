from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import datetime
from get_pg_data import *
from get_mongo_data import *
from get_prediction import *


class NewXs(BaseModel):
   model_name: str
   islongloan: int
   loan_amnt: float
   int_rate: float
   annual_inc: float


class SelectYear(BaseModel):
   yyyy: str


class InputData(BaseModel):
    annual_inc_bin: int
    loan_amnt_bin: int
    int_rate_bin: float
    purpose: str    
    grade: str
    home_ownership: str
    pub_rec_bankruptcies: str
    


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
   x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   d = "high performance, easy to learn, fast to code, ready for production." 
   return [{"DateTime": x}, {"FastAPI": d}]


@app.get("/api/all_years")
async def all_years():
   print("-"*58)
   ds = get_all_years()   
   return ds


@app.post("/api/loan_amt")
async def loan_amt( selectYear: SelectYear ):
   ds = get_loan_amt(selectYear.yyyy)   
   return ds


@app.post("/api/loan_count")
async def loan_count( selectYear: SelectYear ):
   ds = get_loan_count(selectYear.yyyy)   
   return ds


@app.post("/api/default_amt")
async def default_amt( selectYear: SelectYear ):
   ds = get_default_amt(selectYear.yyyy)   
   return ds  


@app.post("/api/default_count")
async def default_count( selectYear: SelectYear ):
   ds = get_default_count(selectYear.yyyy)   
   return ds 


@app.post("/api/month_loan")
async def month_loan( selectYear: SelectYear ):
   ds = get_month_loan(selectYear.yyyy)   
   return ds


@app.post("/api/month_count")
async def month_count( selectYear: SelectYear ):
   ds = get_month_count(selectYear.yyyy)   
   return ds


@app.post("/api/purpose")
async def purpose( selectYear: SelectYear ):
   ds = get_purpose(selectYear.yyyy)   
   return ds


@app.post("/api/occupation")
async def occupation( selectYear: SelectYear ):
   ds = get_occupation(selectYear.yyyy)   
   return ds


@app.post("/api/ml_predict")
async def occupation( newXs: NewXs ):  
   x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
   print("ml_predict", x)      
   y_pred = predict_with_ml(dict(newXs))   
   return y_pred


@app.post("/api/scorecard_predict")
async def occupation( input_data: InputData ):  
   x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
   print("scorecard_predict", x)   
   res = get_predict_report(input_data)   
   return res


@app.get("/api/default_info")
async def default_info():
   x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
   print("query mongodb - default info", x)         
   dict = default_condition()
   return dict


@app.get("/api/default_age")
async def default_age():  
   x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
   print("query mongodb - default age", x)  
   dict = default_condition_age()
   return dict


@app.get("/tst")
async def tst_root():
   x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
   return [{"DateTime": x}]
