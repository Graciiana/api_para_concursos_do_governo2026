from datetime import datetime, UTC
from enum import StrEnum

from sqlalchemy import String, Integer, Float, Enum as sqlEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class NivelAcademicoEnum(StrEnum):
    ENSINO_MEDIO = "Ensino Médio"
    LICENCIATURA = "Licenciatura"


class Candidato(Base):
    __tablename__ = "candidatos"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    bi: Mapped[str] = mapped_column(String(14), unique=True)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime) 
    media: Mapped[float]
    curso: Mapped[str] = mapped_column(String(100))
    nivel_academico: Mapped[NivelAcademicoEnum] = mapped_column(
       sqlEnum(NivelAcademicoEnum), default=NivelAcademicoEnum.ENSINO_MEDIO
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    actualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="candidato")
    candidaturas = relationship("Candidaturas", back_populates="candidato")


    @property
    def idade(self)-> int:
        return datetime.now().year - self.data_nascimento.year