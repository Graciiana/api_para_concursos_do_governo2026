from datetime import datetime, UTC

from sqlalchemy import String,DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from models import candidatura_models

class Concurso(Base):
    __tablename__ = "concursos"

    id: Mapped[int] = mapped_column(primary_key=True)

    titulo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str]

    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    actualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    candidaturas: Mapped[candidatura_models.Candidaturas] = relationship("Candidaturas", back_populates="concurso")
