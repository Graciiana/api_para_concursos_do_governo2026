from datetime import datetime, UTC

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from models import concurso_models, candidato_models

class Candidatura(Base):
    __tablename__ = "candidaturas"

    id: Mapped[int] = mapped_column(primary_key=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    actualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    id_candidato: Mapped[int] = mapped_column(ForeignKey("candidatos.id"))
    id_concurso: Mapped[int] = mapped_column(ForeignKey("concursos.id"))

    candidato: Mapped[candidato_models.Candidato] = relationship("Candidato", back_populates="candidaturas")
    concurso: Mapped[concurso_models.Concurso] = relationship("Concurso", back_populates="candidaturas")