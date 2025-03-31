import uuid
from pydantic import BaseModel, ConfigDict

class ConexionApproachBase(BaseModel):
    pass

class ConexionApproachResponse(ConexionApproachBase):
    conexion_approach_id: int
    approach_id: int
    psychologist_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)