from datetime import date

from pydantic import BaseModel, EmailStr

from app.enums.groupe_exam import GroupeExamEnum


class EtudiantCreate(BaseModel):
    matr: str
    nom: str
    prenom: str | None = None

    date_naissance: date
    lieu_naissance: str

    num_cin: str | None = None
    date_cin: date | None = None
    lieu_cin: str | None = None

    email: EmailStr

    classe_id: int

    groupe_exam: GroupeExamEnum | None = None