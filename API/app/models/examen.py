from datetime import date, time
from typing import TYPE_CHECKING
from sqlalchemy import Enum, String, Date, Time, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.enums.statut_examen import StatutExamen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.salle_examen import SalleExamen
    from app.models.participation import ParticipationExamen
    from app.models.exam_classe import ExamenClasse


class Examen(Base):
    __tablename__ = "examen"

    id: Mapped[int] = mapped_column(primary_key=True)

    date_examen: Mapped[date] = mapped_column(Date, nullable=False)

    heure_debut: Mapped[time] = mapped_column(Time, nullable=False)

    heure_fin: Mapped[time] = mapped_column(Time, nullable=False)

    matiere: Mapped[str] = mapped_column(String(50), nullable=False)

    professeur: Mapped[str] = mapped_column(String(100), nullable=False)

    session: Mapped[str] = mapped_column(String(50), nullable=True)

    bareme: Mapped[float | None] = mapped_column(Float, nullable=True)

    statut: Mapped[StatutExamen | None] = mapped_column(
        Enum(StatutExamen), nullable=True
    )

    participations: Mapped[list["ParticipationExamen"]] = relationship(
        back_populates="examen"
    )

    salles: Mapped[list["SalleExamen"]] = relationship(back_populates="examen")

    classes_assoc: Mapped[list["ExamenClasse"]] = relationship(back_populates="examen")
