from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from app.models.models import RoleEnum


class UserSchema(BaseModel):
    email: EmailStr
    role: RoleEnum = RoleEnum.USER
    criado_em: datetime


class CriarUserSchema(UserSchema):
    password: str = Field(max_length=8)
    


class ActualizarUserSchema(BaseModel):
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None, max_length=8)
    actualizado_em: datetime


class UserSchemaResponse(UserSchema):
    id: int

