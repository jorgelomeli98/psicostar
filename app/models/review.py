import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from db import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    psicologo_id = Column(String(36), ForeignKey("psychologists.psychologist_id"), nullable=False)
    rating = Column(Float, nullable=False)
    comentario = Column(Text, nullable=True)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)

    usuario = relationship("User", back_populates="review")

    psicologo = relationship("Psychologist", back_populates="review")