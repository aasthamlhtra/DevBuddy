from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Annotated, Optional
class UserLogin(BaseModel):
    username : str
    password : str

class UserRegister(UserLogin):
    email : EmailStr

class User(BaseModel):
    id : int
    username : str
    email : EmailStr
    created_at : datetime
    updated_at : datetime
    
    model_config = ConfigDict(from_attributes=True) 

class UserUpdate:
    username : str
    primary_tech_stack : Optional[str] = None
    learning_tech_stack : Optional[str] = None
    updated_at : datetime