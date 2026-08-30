from datetime import date, time

from pydantic import BaseModel


class ExamenCreate(BaseModel):
    date_examen: date
    heure_debut: time
    heure_fin: time
    matiere: str
    professeur: str
    session: str | None = None


class ExamenResponse(BaseModel):
    id: int
    date_examen: date
    heure_debut: time
    heure_fin: time
    matiere: str
    professeur: str
    session: str | None = None

    model_config = {
        "from_attributes": True
    }