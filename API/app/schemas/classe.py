from pydantic import BaseModel

from app.enums.niveau import Niveau


class ClasseCreate(BaseModel):
    mention: str
    parcours: str
    niveau: Niveau
    numero_groupe: int

class ClasseResponse(BaseModel):
    id: int
    mention: str
    parcours: str
    niveau: Niveau
    numero_groupe: int

    model_config = {
        "from_attributes": True
    }