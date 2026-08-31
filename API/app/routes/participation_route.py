from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.examen import Examen
from app.models.classe import Classe
from app.models.etudiant import Etudiant
from app.models.salle_examen import SalleExamen
from app.models.participation import ParticipationExamen
from app.models.exam_classe import ExamenClasse
from app.schemas.participation import SaisirNoteRequest
from app.schemas.participation import AffecterGroupeRequest


router = APIRouter(prefix="/participations", tags=["Participations"])


@router.post("/{examen_id}/affecter-groupe")
def affecter_groupe(
    examen_id: int, data: AffecterGroupeRequest, db: Session = Depends(get_db)
):
    # 1. Vérifier que l'examen existe
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    # 2. Vérifier que la classe existe
    classe = db.query(Classe).filter(Classe.id == data.classe_id).first()

    if classe is None:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    # 3. Vérifier que la classe participe à cet examen
    classe_examen = (
        db.query(ExamenClasse)
        .filter(
            ExamenClasse.examen_id == examen_id,
            ExamenClasse.classe_id == data.classe_id,
        )
        .first()
    )

    if classe_examen is None:
        raise HTTPException(
            status_code=400, detail="Cette classe n'est pas concernée par cet examen"
        )

    # 4. Vérifier que la salle existe
    salle = db.query(SalleExamen).filter(SalleExamen.id == data.salle_id).first()

    if salle is None:
        raise HTTPException(status_code=404, detail="Salle d'examen introuvable")

    # 5. Vérifier que la salle appartient bien à cet examen
    if salle.id_examen != examen_id:
        raise HTTPException(
            status_code=400, detail="Cette salle n'appartient pas à cet examen"
        )

    # 6. Récupérer les étudiants du groupe
    etudiants = (
        db.query(Etudiant)
        .filter(
            Etudiant.classe_id == data.classe_id,
            Etudiant.groupe_exam == data.groupe_exam,
        )
        .all()
    )

    if not etudiants:
        raise HTTPException(
            status_code=404, detail="Aucun étudiant trouvé dans ce groupe"
        )

    # 7. Vérifier les étudiants déjà affectés
    matricules = [e.matr for e in etudiants]

    participations_existantes = (
        db.query(ParticipationExamen)
        .filter(
            ParticipationExamen.examen_id == examen_id,
            ParticipationExamen.etudiant_matr.in_(matricules),
        )
        .all()
    )

    if participations_existantes:
        matricules_existants = [p.etudiant_matr for p in participations_existantes]

        raise HTTPException(
            status_code=409,
            detail={
                "message": "Certains étudiants sont déjà affectés à cet examen",
                "etudiants": matricules_existants,
            },
        )

    # 8. Créer les participations
    for etudiant in etudiants:
        participation = ParticipationExamen(
            etudiant_matr=etudiant.matr,
            examen_id=examen_id,
            salle_id=data.salle_id,
            est_present=False,
            note=None,
        )

        db.add(participation)

    # 9. Valider
    try:
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Erreur lors de l'affectation du groupe"
        )

    return {
        "message": "Groupe affecté avec succès",
        "examen_id": examen_id,
        "classe_id": data.classe_id,
        "groupe_exam": data.groupe_exam,
        "salle_id": data.salle_id,
        "nombre_etudiants": len(etudiants),
    }


@router.patch("/{participation_id}/note")
def saisir_note(
    participation_id: int, data: SaisirNoteRequest, db: Session = Depends(get_db)
):
    participation = (
        db.query(ParticipationExamen)
        .filter(ParticipationExamen.id == participation_id)
        .first()
    )

    if participation is None:
        raise HTTPException(status_code=404, detail="Participation introuvable")

    # Vérifier que l'étudiant était présent
    if not participation.est_present:
        raise HTTPException(
            status_code=400,
            detail="Impossible de saisir une note pour un étudiant absent",
        )

    # Vérifier la validité de la note
    if data.note < 0 or data.note > 20:
        raise HTTPException(
            status_code=400, detail="La note doit être comprise entre 0 et 20"
        )

    participation.note = data.note

    db.commit()
    db.refresh(participation)

    return {
        "message": "Note enregistrée",
        "participation_id": participation.id,
        "etudiant_matr": participation.etudiant_matr,
        "examen_id": participation.examen_id,
        "note": participation.note,
    }


@router.patch("/{participation_id}/presence")
def marquer_present(participation_id: int, db: Session = Depends(get_db)):
    participation = (
        db.query(ParticipationExamen)
        .filter(ParticipationExamen.id == participation_id)
        .first()
    )

    if participation is None:
        raise HTTPException(status_code=404, detail="Participation introuvable")

    if participation.est_present:
        raise HTTPException(
            status_code=409, detail="Cet étudiant est déjà marqué présent"
        )

    participation.est_present = True

    db.commit()
    db.refresh(participation)

    return {
        "message": "Étudiant marqué présent",
        "participation_id": participation.id,
        "etudiant_matr": participation.etudiant_matr,
        "examen_id": participation.examen_id,
        "salle_id": participation.salle_id,
        "est_present": participation.est_present,
    }
