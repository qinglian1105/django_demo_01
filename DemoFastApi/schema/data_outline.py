from pydantic import BaseModel


class NewXs(BaseModel):
   algo_name: str
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



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

    
class User(BaseModel):
    username: str  
    disabled: bool | None = None  
    

class UserInDB(User):
    hashed_password: str



