from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from db import Base

class ConexionApproach(Base):
    __tablename__ = "conexion_approachs"

    conexion_approach_id = Column(Integer, primary_key=True, autoincrement=True)
    approach_id = Column(Integer, ForeignKey("approachs.approach_id"), nullable=False)
    psychologist_id = Column(String(36), ForeignKey("psychologists.psychologist_id"), nullable=False)

    psicologo = relationship("Psychologist",back_populates="enfoques")

    enfoque = relationship("Approach", back_populates="psicologos")