from pydantic import BaseModel


class ExamenClasseResponse(BaseModel):
    id: int
    examen_id: int
    classe_id: int

    model_config = {"from_attributes": True}
