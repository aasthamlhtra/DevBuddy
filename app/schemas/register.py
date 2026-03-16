from pydantic import BaseModel, EmailStr

class RegisterEmail(BaseModel):
    email : EmailStr

class RegisterUser(BaseModel):
    username : str
    password : str
    model_config = {"extra":"forbid"}

