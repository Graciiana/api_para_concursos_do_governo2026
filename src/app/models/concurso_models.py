from datetime import datetime, UTC

from sqlalchemy import String,DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

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

    candidaturas = relationship("Candidatura", back_populates="concurso")
