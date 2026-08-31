from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.participation import ParticipationExamen
from app.models.classe import Classe
from app.core.database import get_db
from app.models.examen import Examen
from app.schemas.examen import (
    ChangerStatutRequest,
    ClasseExamenResponse,
    ExamenCreate,
    ExamenResponse,
    DefinirBaremeRequest,
    ExamenTermineResponse,
    ExamensResponse,
    SalleExamenProgrammeResponse,
)
from app.enums.statut_examen import StatutExamen
from app.models.exam_classe import ExamenClasse
from app.schemas.examen_classe import ExamenClasseResponse
from app.models.salle_examen import SalleExamen
from app.schemas.salle_examen import SalleExamenCreate
from app.enums.niveau import Niveau
from app.schemas.examen import EtudiantNoteResponse
from app.schemas.examen import EtudiantSalleResponse


router = APIRouter(prefix="/examens", tags=["Examens"])


@router.post("/", response_model=ExamenResponse, status_code=201)
def create_examen(examen_data: ExamenCreate, db: Session = Depends(get_db)):
    examen = Examen(
        date_examen=examen_data.date_examen,
        heure_debut=examen_data.heure_debut,
        heure_fin=examen_data.heure_fin,
        matiere=examen_data.matiere,
        professeur=examen_data.professeur,
        session=examen_data.session,
        statut=StatutExamen.PROGRAMMEE,
    )

    db.add(examen)
    db.commit()
    db.refresh(examen)

    return examen


@router.get("/", response_model=list[ExamenResponse])
def get_examens(db: Session = Depends(get_db)):
    examens = db.query(Examen).all()

    return examens


@router.get("/filtre", response_model=list[ExamensResponse])
def get_examens_filtre(
    statut: StatutExamen | None = Query(
        default=None, description="Filtrer les examens par statut."
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Examen)

    if statut is not None:
        query = query.filter(Examen.statut == statut)

    examens = query.all()

    result = []

    for examen in examens:
        classes_uniques = set()

        for association in examen.classes_assoc:
            classe = association.classe

            classes_uniques.add((classe.parcours, classe.niveau))
            classes_concernees = [
                ClasseExamenResponse(parcours=parcours, niveau=Niveau(niveau).name)
                for parcours, niveau in classes_uniques
            ]

        result.append(
            ExamensResponse(
                id=examen.id,
                date_examen=examen.date_examen,
                heure_debut=examen.heure_debut,
                heure_fin=examen.heure_fin,
                matiere=examen.matiere,
                professeur=examen.professeur,
                session=examen.session,
                statut=examen.statut,
                classes_concernees=classes_concernees,
            )
        )

    return result

@router.get(
    "/termines",
    response_model=list[ExamenTermineResponse],
    summary="Lister les examens terminés",
    description=(
        "Retourne tous les examens terminés avec le nombre total "
        "d'étudiants présents, toutes salles et toutes classes confondues."
    ),
)
def get_examens_termines(db: Session = Depends(get_db)):
    examens = (
        db.query(
            Examen,
            func.count(ParticipationExamen.id).label("nombre_participants_presents"),
        )
        .outerjoin(
            ParticipationExamen,
            (ParticipationExamen.examen_id == Examen.id)
            & (ParticipationExamen.est_present.is_(True)),
        )
        .filter(Examen.statut == StatutExamen.TERMINEE)
        .group_by(Examen.id)
        .order_by(Examen.date_examen.desc())
        .all()
    )

    return [
        ExamenTermineResponse(
            id=examen.id,
            date_examen=examen.date_examen,
            heure_debut=examen.heure_debut,
            heure_fin=examen.heure_fin,
            matiere=examen.matiere,
            professeur=examen.professeur,
            session=examen.session,
            nombre_participants_presents=nombre_participants_presents,
        )
        for examen, nombre_participants_presents in examens
    ]



@router.post("/{examen_id}/salles", status_code=201)
def creer_salle_examen(
    examen_id: int, salle_data: SalleExamenCreate, db: Session = Depends(get_db)
):
    # Vérifier que l'examen existe
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    # Vérifier que la salle n'est pas déjà utilisée
    salle_existante = (
        db.query(SalleExamen)
        .filter(
            SalleExamen.num_salle == salle_data.num_salle,
            SalleExamen.id_examen == examen_id,
        )
        .first()
    )

    if salle_existante:
        raise HTTPException(
            status_code=409, detail="Cette salle est déjà affectée à cet examen"
        )

    # Création
    salle = SalleExamen(
        num_salle=salle_data.num_salle,
        surveillant=salle_data.surveillant,
        id_examen=examen_id,
    )

    db.add(salle)
    db.commit()
    db.refresh(salle)

    return salle


@router.get("/{examen_id}", response_model=ExamenResponse)
def get_examen(examen_id: int, db: Session = Depends(get_db)):
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    return examen


@router.post(
    "/{examen_id}/classes/{classe_id}",
    response_model=ExamenClasseResponse,
    status_code=201,
)
def affecter_classe_a_examen(
    examen_id: int, classe_id: int, db: Session = Depends(get_db)
):
    # Vérifier que l'examen existe
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    # Vérifier que la classe existe
    classe = db.query(Classe).filter(Classe.id == classe_id).first()

    if classe is None:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    # Vérifier que l'association n'existe pas déjà
    association_existante = (
        db.query(ExamenClasse)
        .filter(
            ExamenClasse.examen_id == examen_id, ExamenClasse.classe_id == classe_id
        )
        .first()
    )

    if association_existante is not None:
        raise HTTPException(
            status_code=409, detail="Cette classe est déjà affectée à cet examen"
        )

    # Créer l'association
    association = ExamenClasse(examen_id=examen_id, classe_id=classe_id)

    db.add(association)
    db.commit()
    db.refresh(association)

    return association


@router.patch(
    "/{examen_id}/statut",
    response_model=ExamenResponse,
    summary="Modifier le statut d'un examen",
    description="Modifie le statut d'un examen : programmee, publiee ou terminee.",
)
def changer_statut_examen(
    examen_id: int, data: ChangerStatutRequest, db: Session = Depends(get_db)
):
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable.")

    examen.statut = data.statut

    db.commit()
    db.refresh(examen)

    return examen


@router.patch("/{examen_id}/bareme")
def definir_bareme(
    examen_id: int, data: DefinirBaremeRequest, db: Session = Depends(get_db)
):
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    examen.bareme = data.bareme

    db.commit()
    db.refresh(examen)

    return {
        "message": "Barème enregistré",
        "examen_id": examen.id,
        "bareme": examen.bareme,
    }


@router.get(
    "/{examen_id}/etudiants-a-noter",
    response_model=list[EtudiantNoteResponse],
    summary="Récupérer les étudiants présents sans note",
    description=(
        "Retourne les étudiants ayant participé à l'examen, "
        "marqués présents et dont la note n'a pas encore été saisie."
    ),
)
def get_etudiants_a_noter(examen_id: int, db: Session = Depends(get_db)):
    # Vérifier que l'examen existe
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable.")

    participations = (
        db.query(ParticipationExamen)
        .filter(
            ParticipationExamen.examen_id == examen_id,
            ParticipationExamen.est_present.is_(True),
            ParticipationExamen.note.is_(None),
        )
        .all()
    )

    return [
        EtudiantNoteResponse(
            id_participation=participation.id,
            matricule=participation.etudiant.matr,
            nom=participation.etudiant.nom,
            prenom=participation.etudiant.prenom,
        )
        for participation in participations
    ]


@router.get(
    "/{examen_id}/salles/{salle_id}/etudiants",
    response_model=list[EtudiantSalleResponse],
    summary="Lister les étudiants d'une salle d'examen",
    description=(
        "Retourne les étudiants affectés à une salle pour un examen "
        "dont le statut est 'programmee'. "
        "Pour chaque étudiant, retourne le matricule, le nom, le prénom, "
        "l'identifiant de participation et son statut de présence."
    ),
)
def get_etudiants_salle_examen(
    examen_id: int, salle_id: int, db: Session = Depends(get_db)
):
    # 1. Vérifier que l'examen existe
    examen = db.query(Examen).filter(Examen.id == examen_id).first()

    if examen is None:
        raise HTTPException(status_code=404, detail="Examen introuvable.")

    # 2. Vérifier que l'examen est encore programmé
    if examen.statut != StatutExamen.PROGRAMMEE:
        raise HTTPException(
            status_code=400,
            detail=(
                "Les étudiants d'une salle ne peuvent être consultés "
                "que pour un examen dont le statut est 'programmee'."
            ),
        )

    # 3. Vérifier que la salle existe et appartient à cet examen
    salle = (
        db.query(SalleExamen)
        .filter(SalleExamen.id == salle_id, SalleExamen.id_examen == examen_id)
        .first()
    )

    if salle is None:
        raise HTTPException(
            status_code=404, detail="Salle introuvable pour cet examen."
        )

    # 4. Récupérer les participations de cette salle
    participations = (
        db.query(ParticipationExamen)
        .filter(
            ParticipationExamen.examen_id == examen_id,
            ParticipationExamen.salle_id == salle_id,
        )
        .all()
    )

    # 5. Construire la réponse
    return [
        EtudiantSalleResponse(
            id_participation=participation.id,
            matricule=participation.etudiant.matr,
            nom=participation.etudiant.nom,
            prenom=participation.etudiant.prenom,
            est_present=participation.est_present,
        )
        for participation in participations
    ]


@router.get(
    "/programmes/salles",
    response_model=list[SalleExamenProgrammeResponse],
    summary="Lister les salles des examens programmés",
    description=(
        "Retourne les salles affectées aux examens ayant le statut "
        "'programmee', avec la matière, les horaires et les classes "
        "des étudiants affectés dans chaque salle."
    ),
)
def get_salles_examens_programmes(db: Session = Depends(get_db)):
    salles = (
        db.query(SalleExamen)
        .join(SalleExamen.examen)
        .filter(Examen.statut == StatutExamen.PROGRAMMEE)
        .all()
    )

    result = []

    for salle in salles:
        classes_uniques = set()

        for participation in salle.participations:
            etudiant = participation.etudiant

            if etudiant.classe is not None:
                classe = etudiant.classe

                classes_uniques.add((classe.parcours, classe.niveau))

        classes = [
            ClasseExamenResponse(
                parcours=parcours,
                niveau=(
                    niveau.name if isinstance(niveau, Niveau) else Niveau(niveau).name
                ),
            )
            for parcours, niveau in classes_uniques
        ]

        result.append(
            SalleExamenProgrammeResponse(
                salle_id=salle.id,
                num_salle=salle.num_salle,
                matiere=salle.examen.matiere,
                heure_debut=salle.examen.heure_debut,
                heure_fin=salle.examen.heure_fin,
                classes=classes,
            )
        )

    return result


