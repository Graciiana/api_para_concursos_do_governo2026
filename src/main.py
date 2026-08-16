from fastapi import FastAPI

from app.database.db import Base, engine
from app.routes.user_routes import router

app = FastAPI()

app.include_router(router=router, prefix="/user", tags=["Usuarios"])
Base.metadata.create_all(engine)
