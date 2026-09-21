from typing import Annotated

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.database.db import Base, engine
from src.app.routes.user_routes import router
from src.app.routes.candidato_routes import router_candidato
from src.app.routes.candidatura_routes import router_candidatura
from src.app.routes.concurso_routes import router_concurso



app = FastAPI()

app.include_router(router=router, prefix="/user", tags=["Usuarios"])
app.include_router(router=router_candidato, prefix="/candidato", tags=["Candidatos"])
app.include_router(router=router_concurso, prefix="/concurso", tags=["Concursos"])
app.include_router(router=router_candidatura, prefix="/candidatura", tags=["Candidaturas"])
Base.metadata.create_all(engine)




