from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.etudiant import Etudiant
from app.schemas.etudiant import EtudiantCreate


router = APIRouter(
    prefix="/etudiants",
    tags=["Etudiants"]
)


@router.post("/")
def create_etudiant(
    data: EtudiantCreate,
    db: Session = Depends(get_db)
):
    etudiant = Etudiant(
        matr=data.matr,
        nom=data.nom,
        prenom=data.prenom,
        date_naissance=data.date_naissance,
        lieu_naissance=data.lieu_naissance,
        num_cin=data.num_cin,
        date_cin=data.date_cin,
        lieu_cin=data.lieu_cin,
        email=data.email,
        classe_id=data.classe_id,
        groupe_exam=data.groupe_exam
    )

    db.add(etudiant)
    db.commit()
    db.refresh(etudiant)

    return etudiant