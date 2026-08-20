from typing import Annotated

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import Base, engine
from app.routes.user_routes import router
from app.routes.candidato_routes import router_candidato


app = FastAPI()

app.include_router(router=router, prefix="/user", tags=["Usuarios"])
app.include_router(router=router_candidato, prefix="/candidato", tags=["Candidatos"])
# Base.metadata.create_all(engine)




