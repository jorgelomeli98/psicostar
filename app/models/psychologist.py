from __future__ import annotations
import uuid
from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Psychologist(Base):
    __tablename__ = "psychologists"

    psychologist_id = Column(String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), unique=True, nullable=False)
    cedula = Column(String(50), unique=True, nullable=False)
    experiencia = Column(String(500))
    rating = Column(Float, nullable=False, default=0)
    ubicacion = Column(String(255), nullable=True)

    usuario = relationship("User", back_populates="psicologo", )

    enfoques = relationship("ConexionApproach", back_populates="psicologo")

    review = relationship("Review", back_populates="psicologo")
