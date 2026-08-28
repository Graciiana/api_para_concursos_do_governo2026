from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Concurso
from app.models.models import User
from app.schema.concurso_schema import (
    ActualizarConcursoSchema,
    CriarConcursoSchema,
    ConcursoSchemaResponse,
)
from app.database.db import get_session_db
from app.util.util_auth import verificar_jwt


security = HTTPBearer()
router_concurso = APIRouter()


# Inicialmente preciso analisar se for o admin ou não
@router_concurso.post(
    "/registrar",
    response_model=ConcursoSchemaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_concursos(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    dados_concurso: CriarConcursoSchema,
    session: Annotated[Session, Depends(get_session_db)],
):
    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(
        select(User).where(User.email == pyload.get("email"), User.role == "admin")
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User não autorizado"
        )

    concurso_existe = session.execute(
        select(Concurso).where(Concurso.titulo == dados_concurso.titulo)
    ).scalar_one_or_none()

    if concurso_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Concurso já cadastrado"
        )

    concurso = Concurso(**dados_concurso.model_dump())
    session.add(concurso)
    session.commit()
    session.refresh(concurso)

    return concurso


# eliminar concurso


@router_concurso.get("/lista", response_model=list[ConcursoSchemaResponse])
def get_all_concurso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session_db)],
):
    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(
        select(User).where(User.email == pyload.get("email"), User.role == "admin")
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não autorizado"
        )

    concurso = session.execute(select(Concurso)).scalars()

    return concurso
