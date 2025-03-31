
from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.user import TipoUsuario

class UserBase(BaseModel):
    name: str
    email: EmailStr
    tipo_usuario: TipoUsuario

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserResponse(UserBase):
    user_id: uuid.UUID
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)