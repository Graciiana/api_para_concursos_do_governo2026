from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import get_session_db
from app.models.models import Candidato, User
from app.schema.candidato_schema import (
    ActualizarCandidatoSchema,
    CriarCandidatoSchema,
    CandidatoSchemaResponse,
)
from app.util.util_auth import gerar_token, verificar_jwt


router_candidato = APIRouter()
security = HTTPBearer()


@router_candidato.post(
    "/cadastrar",
    response_model=CandidatoSchemaResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_candidato(
    dado_candidato: CriarCandidatoSchema,
    session: Annotated[Session, Depends(get_session_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):

    token = credentials.credentials
    pyload = verificar_jwt(token)
    # buscar user com um certo id e guardar nos candidatos

    user = session.execute(
        select(User).where(User.email == pyload.get("email"))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Candidato não autorizado"
        )

    candidato = session.execute(
        select(Candidato).where(Candidato.id_user == user.id)
    ).scalar_one_or_none()
    if candidato:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Candidato já cadastrado"
        )

    candidato_dado = Candidato(**dado_candidato.model_dump(), id_user=user.id)
    session.add(candidato_dado)
    session.commit()
    session.refresh(candidato_dado)

    return candidato_dado


@router_candidato.post("/id/actualizar", response_model=CandidatoSchemaResponse)
def actualizar_candidato(
    id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    dados_candidato: ActualizarCandidatoSchema,
    session: Annotated[Session, Depends(get_session_db)],
):
    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(
        select(User).where(User.email == pyload.get("email"))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario nao autorizado"
        )

    candidato = session.execute(
        select(Candidato).where(Candidato.id == id)
    ).scalar_one_or_none()

    if not candidato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidato não encontrado"
        )

    actualizar_candidato = dados_candidato.model_dump(exclude_unset=True)

    for chave, valor in actualizar_candidato.items():
        setattr(candidato, chave, valor)
    session.commit()
    session.refresh(candidato)
    return candidato


@router_candidato.get("/lista", response_model=list[CandidatoSchemaResponse])
def get_all_candidatos(
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

    candidato = session.execute(select(Candidato)).scalars()

    return candidato


