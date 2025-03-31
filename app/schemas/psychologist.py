import uuid
from pydantic import BaseModel, ConfigDict

class PsychologistBase(BaseModel):
    cedula: str
    experiencia: str | None = None
    ubicacion: str | None = None

class PsychologistCreate(PsychologistBase):
    approach_id: int

class PsychologistUpdate(BaseModel):
    cedula: str | None = None
    experiencia: str | None = None
    ubicacion: str | None = None

class PsychologistResponse(PsychologistBase):
    psychologist_id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)