from __future__ import annotations
import uuid
from enum import Enum
from sqlalchemy import TIMESTAMP, Column, Enum as SQLEnum, String, func
from sqlalchemy.orm import relationship
from db import Base

class TipoUsuario(str, Enum):
    USER = "user"
    PSYCHOLOGIST = "psychologist"

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    tipo_usuario = Column(SQLEnum(TipoUsuario), nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())

    psicologo = relationship("Psychologist", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

    review = relationship("Review", back_populates="usuario")