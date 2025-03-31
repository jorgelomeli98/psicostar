from fastapi import APIRouter, status, HTTPException
from db import SessionDep
from sqlalchemy import select
from security import CurrentUser
from app.models.approach import Approach
from app.models.conexionapproach import ConexionApproach
from app.models.psychologist import Psychologist
from app.schemas.approach import ApproachResponse, ApproachCreate
from app.schemas.conexionapproach import ConexionApproachResponse
from app.routers.users import usuario_no_encontrado

router = APIRouter(prefix="/approachs")

enfoque_existente = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Enfoque existente")

@router.get("/{approach_id}", response_model=ApproachResponse, status_code=status.HTTP_200_OK)
async def read_approach(db: SessionDep, approach_id: int):
    return db.get(Approach, approach_id)

@router.get("/", response_model=list[ApproachResponse], status_code=status.HTTP_200_OK)
async def read_approachs(db: SessionDep):
    return db.execute(select(Approach)).scalars().all()

@router.post("/", response_model=ApproachResponse, status_code=status.HTTP_201_CREATED)
async def create_approach(db: SessionDep, 
                          approach_data: ApproachCreate):
    approach_db = Approach(**approach_data.model_dump())
    db.add(approach_db)
    db.commit()
    db.refresh(approach_db)
    return approach_db

@router.put("/{approach_id}", response_model=ApproachResponse, status_code=status.HTTP_200_OK)
async def update_approach(db: SessionDep, 
                          approach_id: int, 
                          approach_data: ApproachCreate):
    approach_db = db.get(Approach, approach_id)
    setattr(approach_db, "name", approach_data.name)
    db.commit()
    db.refresh(approach_db)
    return approach_db

@router.delete("/{approach_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approach(db: SessionDep, approach_id: int):
    approach_db = db.get(Approach, approach_id)
    db.delete(approach_db)
    db.commit()
    return None

@router.post("/psychologist/{approach_id}", response_model=ConexionApproachResponse, status_code=status.HTTP_201_CREATED)
async def add_approach_to_psychologist(db: SessionDep, 
                                       current_user: CurrentUser,
                                       approach_id: int):
    psychologist = db.execute(select(Psychologist).where(Psychologist.user_id == current_user["user_id"])).scalar()
    if not psychologist:
        raise usuario_no_encontrado
    conexion_db = db.execute(select(ConexionApproach).where(ConexionApproach.psychologist_id == psychologist.psychologist_id, ConexionApproach.approach_id == approach_id)).scalar()
    if conexion_db:
        raise enfoque_existente
    conexion_register = ConexionApproach(psychologist_id=psychologist.psychologist_id, approach_id=approach_id)
    db.add(conexion_register)
    db.commit()
    db.refresh(conexion_register)
    return conexion_register