from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.classe import Classe
from app.core.database import get_db
from app.models.examen import Examen
from app.schemas.examen import ExamenCreate, ExamenResponse
from app.models.exam_classe import ExamenClasse
from app.schemas.examen_classe import ExamenClasseResponse
from app.models.salle_examen import SalleExamen
from app.schemas.salle_examen import SalleExamenCreate

router = APIRouter(
    prefix="/examens",
    tags=["Examens"]
)

@router.post("/", response_model=ExamenResponse, status_code=201)
def create_examen(
    examen_data: ExamenCreate,
    db: Session = Depends(get_db)
):
    examen = Examen(
        date_examen=examen_data.date_examen,
        heure_debut=examen_data.heure_debut,
        heure_fin=examen_data.heure_fin,
        matiere=examen_data.matiere,
        professeur=examen_data.professeur,
        session=examen_data.session
    )

    db.add(examen)
    db.commit()
    db.refresh(examen)

    return examen

@router.get("/", response_model=list[ExamenResponse])
def get_examens(db: Session = Depends(get_db)):
    examens = db.query(Examen).all()

    return examens


@router.get("/{examen_id}", response_model=ExamenResponse)
def get_examen(
    examen_id: int,
    db: Session = Depends(get_db)
):
    examen = db.query(Examen).filter(
        Examen.id == examen_id
    ).first()

    if examen is None:
        raise HTTPException(
            status_code=404,
            detail="Examen introuvable"
        )

    return examen

@router.post(
    "/{examen_id}/classes/{classe_id}",
    response_model=ExamenClasseResponse,
    status_code=201
)

@router.post("/{examen_id}/salles", status_code=201)
def creer_salle_examen(
    examen_id: int,
    salle_data: SalleExamenCreate,
    db: Session = Depends(get_db)
):
    # Vérifier que l'examen existe
    examen = db.query(Examen).filter(
        Examen.id == examen_id
    ).first()

    if examen is None:
        raise HTTPException(
            status_code=404,
            detail="Examen introuvable"
        )

    # Vérifier que la salle n'est pas déjà utilisée
    salle_existante = db.query(SalleExamen).filter(
        SalleExamen.num_salle == salle_data.num_salle,
        SalleExamen.id_examen == examen_id
    ).first()

    if salle_existante:
        raise HTTPException(
            status_code=409,
            detail="Cette salle est déjà affectée à cet examen"
        )

    # Création
    salle = SalleExamen(
        num_salle=salle_data.num_salle,
        surveillant=salle_data.surveillant,
        id_examen=examen_id
    )

    db.add(salle)
    db.commit()
    db.refresh(salle)

    return salle

    
def affecter_classe_a_examen(
    examen_id: int,
    classe_id: int,
    db: Session = Depends(get_db)
):
    # Vérifier que l'examen existe
    examen = db.query(Examen).filter(
        Examen.id == examen_id
    ).first()

    if examen is None:
        raise HTTPException(
            status_code=404,
            detail="Examen introuvable"
        )

    # Vérifier que la classe existe
    classe = db.query(Classe).filter(
        Classe.id == classe_id
    ).first()

    if classe is None:
        raise HTTPException(
            status_code=404,
            detail="Classe introuvable"
        )

    # Vérifier que l'association n'existe pas déjà
    association_existante = db.query(ExamenClasse).filter(
        ExamenClasse.examen_id == examen_id,
        ExamenClasse.classe_id == classe_id
    ).first()

    if association_existante is not None:
        raise HTTPException(
            status_code=409,
            detail="Cette classe est déjà affectée à cet examen"
        )

    # Créer l'association
    association = ExamenClasse(
        examen_id=examen_id,
        classe_id=classe_id
    )

    db.add(association)
    db.commit()
    db.refresh(association)

    return association