from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.models import Concurso
from src.app.models.models import User
from src.app.schema.concurso_schema import (
    ActualizarConcursoSchema,
    CriarConcursoSchema,
    ConcursoSchemaResponse,
)
from src.app.database.db import get_session_db
from src.app.util.util_auth import verificar_jwt


security = HTTPBearer()
router_concurso = APIRouter()


# Inicialmente preciso analisar se for o admin ou não
@router_concurso.post(
    "/registrar",
    response_model=ConcursoSchemaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_concurso(
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
        select(Concurso).where(Concurso.identificador == dados_concurso.identificador)
    ).scalar_one_or_none()

    if concurso_existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Concurso já cadastrado"
        )

    concurso = Concurso(**dados_concurso.model_dump())
    session.add(concurso)
    session.commit()
    session.refresh(concurso)

    return concurso


# eliminar concurso
@router_concurso.delete("/{id}/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_concurso(
    id: int,
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

    concurso = session.execute(
        select(Concurso).where(Concurso.id == id)
    ).scalar_one_or_none()
    if not concurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Concurso não encontrado"
        )
    session.delete(concurso)
    session.commit()



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


# Actualizar
@router_concurso.patch("/{id}/actualizar", response_model=ConcursoSchemaResponse)
def actualizar_concurso(
    id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    dados_concurso: ActualizarConcursoSchema,
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
        select(Concurso).where(Concurso.id == id)
    ).scalar_one_or_none()

    if concurso_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Concurso inexistente"
        )

    concurso = dados_concurso.model_dump(exclude_unset=True)
    for chave, valor in concurso.items():
        setattr(concurso_existe, chave, valor)
    session.commit()
    session.refresh(concurso)

    return concurso_existe
