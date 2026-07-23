from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
# mapped: type de l'objet dans python, cad dans le code
# mapped_column: type de champs dans postgres, psycogfait la conversion Strinng==>Varchar dans la base de donnees

from app.core.database import Base
from app.enum.niveau import Niveau

if TYPE_CHECKING:
    from app.models.participation import ParticipationExamen


class Etudiant(Base):
    __tablename__ = "etudiant"

    matr: Mapped[str] = mapped_column(String(10), primary_key=True)

    nom: Mapped[str] = mapped_column(String(50), nullable=False)

    prenom: Mapped[str] = mapped_column(String(150), nullable=True)

    date_naissance: Mapped[date] = mapped_column(Date, nullable=False)

    lieu_naissance: Mapped[str] = mapped_column(String(50), nullable=False)

    num_cin: Mapped[str] = mapped_column(String(12), unique=True)

    date_cin: Mapped[date] = mapped_column(Date)

    lieu_cin: Mapped[str] = mapped_column(String(50))

    mention: Mapped[str] = mapped_column(String(4))

    parcours: Mapped[str] = mapped_column(String(3))

    niveau: Mapped[Niveau] = mapped_column(Integer)

    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    chemin_photo: Mapped[str | None] = mapped_column(String(255), nullable=True)

    chemin_embedding: Mapped[str | None] = mapped_column(String(255), nullable=True)

    participations: Mapped[list["ParticipationExamen"]] = relationship(
        back_populates="etudiant"
    )
