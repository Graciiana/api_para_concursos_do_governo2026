from datetime import datetime, UTC
from enum import StrEnum

from sqlalchemy import DateTime, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.models.candidato_models import Candidato

class RoleEnum(StrEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(14), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum), default=RoleEnum.USER)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    actualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    candidato: Mapped[Candidato] = relationship("Candidato", back_populates="user")
