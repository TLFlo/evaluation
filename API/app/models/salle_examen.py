from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.enums.salle import SalleEnum

if TYPE_CHECKING:
    from app.models.participation import ParticipationExamen
    from app.models.examen import Examen


class SalleExamen(Base):
    __tablename__ = "salle_examen"

    id: Mapped[int] = mapped_column(primary_key=True)

    num_salle: Mapped[SalleEnum] = mapped_column(Enum(SalleEnum), nullable=False)

    surveillant: Mapped[str] = mapped_column(String(100), nullable=False)

    id_examen: Mapped[int] = mapped_column(ForeignKey("examen.id"), nullable=False)

    examen: Mapped["Examen"] = relationship(back_populates="salles")

    participations: Mapped[list["ParticipationExamen"]] = relationship(
        back_populates="salle"
    )
