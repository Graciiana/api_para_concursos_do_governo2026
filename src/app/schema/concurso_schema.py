from datetime import datetime

from pydantic import BaseModel, Field  
  
  
class ConcursoSchema(BaseModel):

    titulo: str = Field(min_length=10, max_length=50)
    descricao: str = Field(min_length=10)
    numero_vagas: int
    nota_minima: float

   
class CriarConcursoSchema(ConcursoSchema):
    pass


class ActualizarConcursoSchema(BaseModel):
    titulo: str | None = Field(default=None, min_length=10, max_length=50)
    descricao: str | None = Field(default=None, min_length=10)
    numero_vagas: int | None = None
    nota_minima: float | None = None
    actualizado_em: datetime

class ConcursoSchemaResponse(ConcursoSchema):
    id: int
    