from datetime import datetime, date

from pydantic import BaseModel, Field

from app.models.models import NivelAcademicoEnum


class CandidatoSchema(BaseModel):
    nome: str = Field(min_length=5, max_length=50)
    bi: str = Field(max_length=15)
    media: float
    curso: str = Field(min_length=10, max_length=100)
    nivel_academico: NivelAcademicoEnum = NivelAcademicoEnum.ENSINO_MEDIO


class CriarCandidatoSchema(CandidatoSchema):
    data_nascimento: date
    # id_user: int
    
    


class ActualizarCandidatoSchema(BaseModel):
    nome: str | None = Field(default=None, min_length=10, max_length=50)
    bi: str | None = Field(default=None, max_length=15)
    media: float | None = None
    curso: str | None = Field(default=None, min_length=10, max_length=100)
    nivel_academico: NivelAcademicoEnum | None = None
    actualizado_em: datetime | None = None


class CandidatoSchemaResponse(CandidatoSchema):
    id: int
    idade: int
    id_user: int
