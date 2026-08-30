from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.classe import Classe
from app.schemas.classe import ClasseCreate, ClasseResponse


router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)


@router.post("/")
def create_classe(
    classe_data: ClasseCreate,
    db: Session = Depends(get_db)
):
    classe = Classe(
        mention=classe_data.mention,
        parcours=classe_data.parcours,
        niveau=classe_data.niveau,
        numero_groupe=classe_data.numero_groupe
    )

    db.add(classe)
    db.commit()
    db.refresh(classe)

    return classe

@router.get("/", response_model=list[ClasseResponse])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Classe).all()

    return classes