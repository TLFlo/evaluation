from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field
from app.enums.salle import SalleEnum
from app.enums.statut_examen import StatutExamen
from app.enums.statut_examen import StatutExamen


class EtudiantNoteResponse(BaseModel):
    id_participation: int
    matricule: str
    nom: str
    prenom: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ChangerStatutRequest(BaseModel):
    statut: StatutExamen


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

    model_config = {"from_attributes": True}


class DefinirBaremeRequest(BaseModel):
    bareme: float = Field(gt=0)


class ClasseExamenResponse(BaseModel):
    parcours: str
    niveau: str


class ExamensResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_examen: date
    heure_debut: time
    heure_fin: time
    matiere: str
    professeur: str
    session: str
    statut: StatutExamen

    classes_concernees: list[ClasseExamenResponse]


class EtudiantSalleResponse(BaseModel):
    id_participation: int
    matricule: str
    nom: str
    prenom: str | None = None
    est_present: bool

    model_config = ConfigDict(from_attributes=True)


class SalleExamenProgrammeResponse(BaseModel):
    salle_id: int
    num_salle: SalleEnum
    matiere: str
    heure_debut: time
    heure_fin: time
    classes: list[ClasseExamenResponse]

    model_config = ConfigDict(from_attributes=True)


class ExamenTermineResponse(BaseModel):
    id: int
    date_examen: date
    heure_debut: time
    heure_fin: time
    matiere: str
    professeur: str
    session: str | None = None
    nombre_participants_presents: int
