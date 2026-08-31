from pydantic import BaseModel, Field
from app.enums.groupe_exam import GroupeExamEnum


class AffecterGroupeRequest(BaseModel):
    classe_id: int = Field(gt=0)

    groupe_exam: GroupeExamEnum

    salle_id: int = Field(gt=0)


class SaisirNoteRequest(BaseModel):
    note: float = Field(ge=0)
