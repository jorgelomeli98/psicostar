from fastapi import APIRouter, status, HTTPException
from db import SessionDep
from sqlalchemy import select
from app.models.psychologist import Psychologist
from app.schemas.psychologist import PsychologistResponse
from app.models.conexionapproach import ConexionApproach



router = APIRouter(prefix="/psychologists")

@router.get("/", response_model=list[PsychologistResponse], status_code=status.HTTP_200_OK)
async def get_psychologists(db: SessionDep):
    """
    Get all psychologists.
    """
    psychologists = db.execute(select(Psychologist)).scalars().all()

    return psychologists

@router.get("/{id}", response_model=PsychologistResponse, status_code=status.HTTP_200_OK)
async def get_psychologist_by_id(db: SessionDep, 
                                  id: str):
    """
    Get a psychologist by ID.
    """
    psychologist = db.execute(select(Psychologist).where(Psychologist.psychologist_id == id)).scalar()

    if not psychologist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Psychologist not found")

    return psychologist

@router.get("/by-approach/{approach_id}", response_model=list[PsychologistResponse], status_code=status.HTTP_200_OK)
async def get_psychologist_by_approach(db: SessionDep, 
                                        approach_id: int):
    """
    Get psychologists by approach ID.
    """
    psychologists = db.execute(select(Psychologist).join(ConexionApproach).where(ConexionApproach.approach_id == approach_id)).scalars().all()

    if not psychologists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Psychologists not found")

    return psychologists