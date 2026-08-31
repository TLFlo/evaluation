from pydantic import BaseModel

from app.enums.salle import SalleEnum


class SalleExamenCreate(BaseModel):
    num_salle: SalleEnum
    surveillant: str
