from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.enums.niveau import Niveau
from typing import TYPE_CHECKING

    
if TYPE_CHECKING:
    from app.models.etudiant import Etudiant
    from app.models.exam_classe import ExamenClasse



class Classe(Base):
    __tablename__ = "classe"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    mention: Mapped[str] = mapped_column(
        String(4),
        nullable=False
    )

    parcours: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    niveau: Mapped[Niveau] = mapped_column(
        Integer,
        nullable=False
    )

    numero_groupe: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    etudiants: Mapped[list["Etudiant"]] = relationship(
        back_populates="classe"
    )

    examens_assoc: Mapped[list["ExamenClasse"]] = relationship(
    back_populates="classe"
    )