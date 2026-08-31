from pydantic import BaseModel


class PointageResponse(BaseModel):
    success: bool
    message: str

    participation_id: int | None = None
    matricule: str | None = None
    nom: str | None = None
    prenom: str | None = None
    est_present: bool | None = None
