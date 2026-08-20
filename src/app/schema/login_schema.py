from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=8)

class Token(BaseModel):
    acess_token: str
    token_type: str = "Bearer"