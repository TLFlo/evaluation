from datetime import date, time
from typing import TYPE_CHECKING
from sqlalchemy import String, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.salle_examen import SalleExamen
    from app.models.participation import ParticipationExamen


class Examen(Base):
    __tablename__ = "examen"

    id: Mapped[int] = mapped_column(primary_key=True)

    date_examen: Mapped[date] = mapped_column(Date, nullable=False)

    heure_debut: Mapped[time] = mapped_column(Time, nullable=False)

    heure_fin: Mapped[time] = mapped_column(Time, nullable=False)

    matiere: Mapped[str] = mapped_column(String(50), nullable=False)

    professeur: Mapped[str] = mapped_column(String(100), nullable=False)

    participations: Mapped[list["ParticipationExamen"]] = relationship(
        back_populates="examen"
    )

    salles: Mapped[list["SalleExamen"]] = relationship(back_populates="examen")
