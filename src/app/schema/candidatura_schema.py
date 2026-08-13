from datetime import datetime

from pydantic import BaseModel


class CandidaturaSchema(BaseModel):
    id_candidato: int
    id_concurso: int
    criado_em: datetime


class CriarCandidatoSchema(CandidaturaSchema):
    pass


class ActualizarCandidaturaSchema(BaseModel):
    id_candidato: int | None
    id_concurso: int | None
    actualizado_em: datetime


class CandidatoSchemaResponse(CandidaturaSchema):
    id: int


class GetCandidatoSchemaResponse(BaseModel):
    nome_candidato: str
    concurso: list[str]
