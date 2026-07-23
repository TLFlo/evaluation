from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.etudiant import Etudiant
    from app.models.examen import Examen
    from app.models.salle_examen import SalleExamen


class ParticipationExamen(Base):
    __tablename__ = "participation_examen"

    id: Mapped[int] = mapped_column(primary_key=True)

    etudiant_matr: Mapped[str] = mapped_column(
        ForeignKey("etudiant.matr"), nullable=False
    )

    examen_id: Mapped[int] = mapped_column(ForeignKey("examen.id"), nullable=False)

    salle_id: Mapped[int] = mapped_column(ForeignKey("salle_examen.id"), nullable=False)

    est_present: Mapped[bool] = mapped_column(Boolean, default=False)

    note: Mapped[float | None] = mapped_column(Float, nullable=True)

    etudiant: Mapped["Etudiant"] = relationship(back_populates="participations")

    examen: Mapped["Examen"] = relationship(back_populates="participations")

    salle: Mapped["SalleExamen"] = relationship(back_populates="participations")
