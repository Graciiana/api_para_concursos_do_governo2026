from datetime import datetime, UTC
from enum import StrEnum

from sqlalchemy import String, Integer, Float, Enum as SqlEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class NivelAcademicoEnum(StrEnum):
    ENSINO_MEDIO = "Ensino Médio"
    LICENCIATURA = "Licenciatura"


class RoleEnum(StrEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(14), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum), default=RoleEnum.USER)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    actualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    candidato = relationship("Candidato", back_populates="user")



class Candidato(Base):
    __tablename__ = "candidatos"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    bi: Mapped[str] = mapped_column(String(14), unique=True)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime)
    media: Mapped[float]
    curso: Mapped[str] = mapped_column(String(100))
    nivel_academico: Mapped[NivelAcademicoEnum] = mapped_column(
        SqlEnum(NivelAcademicoEnum), default=NivelAcademicoEnum.ENSINO_MEDIO
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    actualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="candidato")
    candidaturas = relationship("Candidatura", back_populates="candidato")

    @property
    def idade(self) -> int:
        return datetime.now().year - self.data_nascimento.year



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

    candidato = relationship("Candidato", back_populates="candidaturas")
    concurso = relationship("Concurso", back_populates="candidaturas")


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
