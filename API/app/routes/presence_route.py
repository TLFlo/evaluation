import os
import tempfile

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.presence import PointageResponse
from app.services.presence_service import verifier_participation
from app.services.face_service import verifier_visage


router = APIRouter(prefix="/salles-examen", tags=["Pointage"])


@router.post(
    "/{salle_id}/pointage",
    response_model=PointageResponse,
    summary="Pointer un étudiant par reconnaissance faciale",
    description="""
    Vérifie la présence d'un étudiant dans une salle d'examen.

    Le frontend fournit :
    - le matricule de l'étudiant ;
    - une photo prise par la caméra.

    Le backend vérifie l'identité, la salle,
    la participation à l'examen et le visage.
    """,
)
async def pointer_etudiant(
    salle_id: int,
    matricule: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # --------------------------------
    # 1. Vérifier la participation
    # --------------------------------

    try:
        etudiant, salle, participation = verifier_participation(
            db=db, matricule=matricule, salle_id=salle_id
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # --------------------------------
    # 2. Vérifier l'embedding
    # --------------------------------

    if not etudiant.chemin_embedding:
        raise HTTPException(
            status_code=400,
            detail="Aucun embedding facial enregistré pour cet étudiant",
        )

    if not os.path.exists(etudiant.chemin_embedding):
        raise HTTPException(status_code=500, detail="Fichier embedding introuvable")

    # --------------------------------
    # 3. Sauvegarder la photo
    # --------------------------------

    suffix = os.path.splitext(photo.filename or ".jpg")[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        contenu = await photo.read()
        temp_file.write(contenu)

        photo_path = temp_file.name

    # --------------------------------
    # 4. Reconnaissance faciale
    # --------------------------------

    try:
        visage_correspond = verifier_visage(
            photo_path=photo_path, embedding_path=etudiant.chemin_embedding
        )

    finally:
        os.remove(photo_path)

    # --------------------------------
    # 5. Refuser si visage incorrect
    # --------------------------------

    if not visage_correspond:
        return PointageResponse(
            success=False, message="Le visage ne correspond pas à l'étudiant indiqué"
        )

    # --------------------------------
    # 6. Marquer présent
    # --------------------------------

    participation.est_present = True

    db.commit()
    db.refresh(participation)

    # --------------------------------
    # 7. Réponse
    # --------------------------------

    return PointageResponse(
        success=True,
        message="Étudiant reconnu et marqué présent",
        participation_id=participation.id,
        matricule=etudiant.matr,
        nom=etudiant.nom,
        prenom=etudiant.prenom,
        est_present=participation.est_present,
    )
