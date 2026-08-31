from sqlalchemy.orm import Session

from app.models.etudiant import Etudiant
from app.models.salle_examen import SalleExamen
from app.models.participation import ParticipationExamen


def verifier_participation(
    db: Session, matricule: str, salle_id: int
) -> tuple[Etudiant, SalleExamen, ParticipationExamen]:
    # 1. Vérifier l'étudiant
    etudiant = db.query(Etudiant).filter(Etudiant.matr == matricule).first()

    if etudiant is None:
        raise ValueError("Étudiant introuvable")

    # 2. Vérifier la salle
    salle = db.query(SalleExamen).filter(SalleExamen.id == salle_id).first()

    if salle is None:
        raise ValueError("Salle d'examen introuvable")

    # 3. Vérifier la participation
    participation = (
        db.query(ParticipationExamen)
        .filter(
            ParticipationExamen.etudiant_matr == matricule,
            ParticipationExamen.salle_id == salle_id,
            ParticipationExamen.examen_id == salle.id_examen,
        )
        .first()
    )

    if participation is None:
        raise ValueError("Cet étudiant n'est pas affecté à cette salle d'examen")

    return etudiant, salle, participation
