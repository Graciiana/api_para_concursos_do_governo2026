from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_session_db
from app.models.models import User
from app.schema.user_schema import CriarUserSchema, UserSchemaResponse

# ActualizarUserSchema

router = APIRouter()


@router.post(
    "/create", response_model=UserSchemaResponse, status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    dados_user: CriarUserSchema, session: Annotated[Session, Depends(get_session_db)]
):
    smt = select(User).where(User.email == dados_user.email)
    user = session.execute(smt).scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario com esse email, já cadastrado!",
        )
    user_dados = User(**dados_user.model_dump())

    session.add(user_dados)
    session.commit()
    session.refresh(user_dados)

    return user_dados
