from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_session_db
from app.models.models import User
from app.schema.user_schema import (
    ActualizarUserSchema,
    CriarUserSchema,
    UserSchemaResponse,
)
from app.schema.login_schema import LoginSchema, Token
from app.util.util_auth import gerar_token, verificar_jwt
from app.util.util_hash import gerar_hash, verificar_senha


# ActualizarUserSchema

router = APIRouter()
security = HTTPBearer()


@router.post(
    "/criar", response_model=UserSchemaResponse, status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    dados_user: CriarUserSchema, session: Annotated[Session, Depends(get_session_db)]
):
    smt = select(User).where(User.email == dados_user.email)
    user = session.execute(smt).scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario com esse email, já foi cadastrado!",
        )

    dados_user.password = gerar_hash(dados_user.password)
    user_dados = User(**dados_user.model_dump())

    session.add(user_dados)
    session.commit()
    session.refresh(user_dados)

    return user_dados


@router.post("/login", response_model=Token)
def user_login(
    dados_login: LoginSchema,
    session: Annotated[Session, Depends(get_session_db)],
):
    user_existente = session.execute(
        select(User).where(User.email == dados_login.email)
    ).scalar_one_or_none()

    if not user_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Emal incorrecto"
        )

    senha = verificar_senha(dados_login.password, user_existente.password)
    if not senha:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha inválida"
        )

    acess_token = gerar_token(user_existente.email)
    token = Token(acess_token=acess_token)
    return token


# patch
@router.patch("/{id}/actualizar", response_model=UserSchemaResponse)
def actualizar_user(
    id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    dados_user: ActualizarUserSchema,
    session: Annotated[Session, Depends(get_session_db)],
):
    # Autenticacao
    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(
        select(User).where(User.email == pyload.get("email"))
    ).scalar_one()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não autorizado"
        )

    user_existente = session.execute(
        select(User).where(User.id == id)
    ).scalar_one_or_none()

    actualizar_user = dados_user.model_dump(exclude_unset=True)

    for chave, valor in actualizar_user.items():
        setattr(user_existente, chave, valor)

    session.commit()
    session.refresh(user_existente)
    return user_existente


# Autorizado apenas para o admin - ver listas dos users

@router.get("/lista", response_model=list[UserSchemaResponse])
def get_users(
    session: Annotated[Session, Depends(get_session_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):

    token = credentials.credentials
    pyload = verificar_jwt(token)
    user = session.execute(
        select(User).where(User.email == pyload.get("email"), User.role == "admin")
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não autorizado"
        )

    users = session.execute(select(User)).scalars()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum usuario cadastrado"
        )
    return users
