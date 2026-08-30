from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.enums.groupe_exam import GroupeExamEnum

if TYPE_CHECKING:
    from app.models.participation import ParticipationExamen
    from app.models.classe import Classe


class Etudiant(Base):
    __tablename__ = "etudiant"

    matr: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    nom: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    prenom: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    date_naissance: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    lieu_naissance: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    num_cin: Mapped[str] = mapped_column(
        String(12),
        unique=True
    )

    date_cin: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    lieu_cin: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    chemin_photo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    chemin_embedding: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    groupe_exam: Mapped[GroupeExamEnum] = mapped_column(
        Enum(GroupeExamEnum),
        nullable=True
    )
    # Classe de l'étudiant
    classe_id: Mapped[int] = mapped_column(
        ForeignKey("classe.id"),
        nullable=False
    )

    classe: Mapped["Classe"] = relationship(
        back_populates="etudiants"
    )

    participations: Mapped[list["ParticipationExamen"]] = relationship(
        back_populates="etudiant"
    )