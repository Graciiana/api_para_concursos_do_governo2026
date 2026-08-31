from datetime import datetime, date
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from fpdf import FPDF

from app.models.models import Candidatura, Candidato, Concurso, User
from app.database.db import get_session_db
from app.util.util_auth import verificar_jwt
from app.schema.candidatura_schema import (
    CriarCandidaturaSchema,
    CandidaturaSchemaResponse,
    MeCandidaturasResponse,
)


router_candidatura = APIRouter()
security = HTTPBearer()


@router_candidatura.post(
    "/criar",
    response_model=CandidaturaSchemaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_candidatura(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    dados_candidatura: CriarCandidaturaSchema,
    session: Annotated[Session, Depends(get_session_db)],
):
    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(
        select(User).where(User.email == pyload.get("email"))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado"
        )

    candidato = session.execute(
        select(Candidato).where(Candidato.id == dados_candidatura.id_candidato)
    ).scalar_one_or_none()

    if not candidato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidato não cadastrado"
        )

    concurso = session.execute(
        select(Concurso).where(Concurso.id == dados_candidatura.id_concurso)
    ).scalar_one_or_none()

    if not concurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Concurso inexistente"
        )

    candidatura_existente = session.execute(
        select(Candidatura).where(
            Candidatura.id_candidato == candidato.id,
            Candidatura.id_concurso == concurso.id,
        )
    ).scalar_one_or_none()

    if candidatura_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Candidatura já existente"
        )

    candidatura = Candidatura(**dados_candidatura.model_dump())

    session.add(candidatura)
    session.commit()
    session.refresh(candidatura)
    return candidatura


# Lista de candidaturas de um candidato especifico


@router_candidatura.get("/{id}/me", response_model=MeCandidaturasResponse)
def me_candidaturas(
    id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session_db)],
):

    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(
        select(User).where(User.email == pyload.get("email"))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado"
        )

    candidato = session.execute(
        select(Candidato).where(Candidato.id == id)
    ).scalar_one()

    candidaturas = session.execute(
        select(Candidatura).where(Candidatura.id_candidato == candidato.id)
    ).scalars()

    if not candidaturas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma candidatura"
        )

    return {
        "candidato": candidato.nome,
        "concursos": [candidatura.concurso.titulo for candidatura in candidaturas],
    }


@router_candidatura.get("/todas")
def todas_as_candidaturas(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session_db)],
):
    token = credentials.credentials
    pyload = verificar_jwt(token)
    candidaturas_list = []

    user = session.execute(
        select(User).where(User.email == pyload.get("email"), User.role == "admin")
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            staus_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado"
        )
    candidaturas = session.execute(select(Candidatura)).scalars()

    if not candidaturas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma candidatura encontrada",
        )

    for i in candidaturas:
        candidaturas_list.append(
            {
                "candidato": i.candidato.nome,
                "concursos": [i.concurso.titulo],
                "media": i.candidato.media,
                "data de candidatura": i.criado_em,
            }
        )

    return candidaturas_list


## mostrar o pdf com os dados desse usuario


@router_candidatura.get("/{id}/pdf")
def gerar_pdf(
    id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session_db)],
):
    token = credentials.credentials
    pyload = verificar_jwt(token)

    user = session.execute(select(User).where(User.email == pyload.get("email")))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado"
        )

    """
     candidato = session.execute(
            select(Candidato).where(Candidato.id == id)
        ).scalar_one()
    
    """
    candidatura = (
        session.execute(select(Candidatura).where(Candidatura.id_candidato == id))
    ).scalar_one()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", size=16)
    pdf.set_fill_color(240, 240, 240)

    pdf.cell(
        0,
        10,
        f"Relatório de Candidatura - {candidatura.concurso.titulo}",
        border=1,
        fill=True,
        ln=True,
        align="C",
    )

    pdf.ln(12)

    pdf.set_font("Arial", "", size=12)
    pdf.multi_cell(
        0,
        8,
        f"Caro candidato(a) {candidatura.candidato.nome} a sua candidatura foi feita com sucesso. "
        "Agurade as próximas indicações.",
        align="C",
    )

    pdf.ln(50)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(
        0,
        10,
        f"Governo de Angola, aos {datetime.now().strftime('%Y-%m-%d')}",
        align="R",
    )

    pdf.output("concursos2026.pdf")

    return FileResponse(
        path="concursos2026.pdf",
        media_type="application/pdf",
        filename="candidatura.pdf",
    )


#
# Ver listas de candidaturas feitas e adicionar um campo em que apenas o usuario conegui ver as suas candidaturas
