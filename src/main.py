from fastapi import FastAPI

from app.routes.user_routes import router
from app.database.db import Base, engine

app = FastAPI()

app.include_router(router=router, prefix="/user", tags=["Usuarios"])
Base.metadata.create_all(engine)