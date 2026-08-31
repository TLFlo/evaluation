from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ExamenClasse(Base):
    __tablename__ = "examen_classe"

    id: Mapped[int] = mapped_column(primary_key=True)

    examen_id: Mapped[int] = mapped_column(ForeignKey("examen.id"), nullable=False)

    classe_id: Mapped[int] = mapped_column(ForeignKey("classe.id"), nullable=False)

    examen = relationship("Examen", back_populates="classes_assoc")

    classe = relationship("Classe", back_populates="examens_assoc")
