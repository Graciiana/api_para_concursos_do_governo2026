from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from app.models.models import RoleEnum


class UserSchema(BaseModel):
    nome: str = Field(min_length=5, max_length=50)
    email: EmailStr
    password: str = Field(max_length=8)
    criado_em: datetime


class CriarUserSchema(UserSchema):
    pass


class ActualizarUserSchema(BaseModel):
    nome: str | None = Field(default=None,min_length=10, max_length=50)
    email: EmailStr | None 
    password: str | None
    actualizado_em: datetime


class UserSchemaResponse(UserSchema):
    id: int
    role: RoleEnum = RoleEnum.USER 
