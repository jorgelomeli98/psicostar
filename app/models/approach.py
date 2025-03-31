from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Approach(Base):
    __tablename__ = "approachs"

    approach_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)


    psicologos = relationship("ConexionApproach", back_populates="enfoque")