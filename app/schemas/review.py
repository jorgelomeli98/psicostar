import uuid
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    comentario: str

class ReviewCreate(ReviewBase):
    psicologo_id: uuid.UUID

class ReviewResponse(ReviewBase):
    review_id: int
    psicologo_id: uuid.UUID
    user_id: uuid.UUID
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)
