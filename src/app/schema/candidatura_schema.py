from pydantic import BaseModel


class CandidaturaSchema(BaseModel):
    id_candidato: int
    id_concurso: int


class CriarCandidaturaSchema(CandidaturaSchema):
    pass


class CandidaturaSchemaResponse(CandidaturaSchema):
    id: int


class GetCandidatoSchemaResponse(BaseModel):
    nome_candidato: str
    concurso: str

# ADICIONAR 
class MeCandidaturasResponse(BaseModel):
    candidato: str
    concursos: list[str]