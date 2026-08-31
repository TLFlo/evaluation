from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.etudiant import Etudiant
from app.schemas.etudiant import EtudiantCreate
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.services.face_service import create_embedding


router = APIRouter(prefix="/etudiants", tags=["Étudiants"])


@router.post("/")
def create_etudiant(data: EtudiantCreate, db: Session = Depends(get_db)):
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
        groupe_exam=data.groupe_exam,
    )

    db.add(etudiant)
    db.commit()
    db.refresh(etudiant)

    return etudiant


@router.post(
    "/{matricule}/photo",
    summary="Ajouter la photo d'un étudiant et générer son embedding",
)
async def ajouter_photo_etudiant(
    matricule: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1. Chercher l'étudiant
    etudiant = db.query(Etudiant).filter(Etudiant.matr == matricule).first()

    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")

    # 2. Vérifier le type de fichier
    if photo.content_type not in [
        "image/jpeg",
        "image/png",
    ]:
        raise HTTPException(
            status_code=400, detail="La photo doit être au format JPEG ou PNG."
        )

    # 3. Créer les dossiers
    photo_dir = Path("storage/photos")
    embedding_dir = Path("storage/embeddings")

    photo_dir.mkdir(parents=True, exist_ok=True)

    embedding_dir.mkdir(parents=True, exist_ok=True)

    # 4. Chemins des fichiers
    photo_path = photo_dir / f"{matricule}.jpg"
    embedding_path = embedding_dir / f"{matricule}.npy"

    # 5. Sauvegarder la photo
    contenu = await photo.read()

    with open(photo_path, "wb") as fichier:
        fichier.write(contenu)

    # 6. Générer l'embedding
    try:
        create_embedding(photo_path=str(photo_path), embedding_path=str(embedding_path))

    except ValueError as e:
        # supprimer la photo si la reconnaissance échoue
        if photo_path.exists():
            photo_path.unlink()

        raise HTTPException(status_code=400, detail=str(e))

    # 7. Mettre à jour l'étudiant
    etudiant.chemin_photo = str(photo_path)
    etudiant.chemin_embedding = str(embedding_path)

    db.commit()
    db.refresh(etudiant)

    # 8. Réponse
    return {
        "message": "Photo enregistrée et embedding généré avec succès.",
        "matricule": etudiant.matr,
        "chemin_photo": etudiant.chemin_photo,
        "chemin_embedding": etudiant.chemin_embedding,
    }
