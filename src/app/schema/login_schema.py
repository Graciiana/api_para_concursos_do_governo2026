from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    acess_token: str
    token_type: str = "Bearer"