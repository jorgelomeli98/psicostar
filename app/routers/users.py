from pydantic import EmailStr
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from db import SessionDep
from app.models.user import User
from app.models.psychologist import Psychologist
from app.models.conexionapproach import ConexionApproach
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.schemas.psychologist import PsychologistCreate, PsychologistResponse, PsychologistUpdate
from security import verify_password, create_access_token, CurrentUser, hash_password

router = APIRouter(prefix="/users")

usuario_no_encontrado = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
usuario_existente = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Usuario existente")
error_interno = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno")
contraseña_incorrecta = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")

def search_user_by_email(db: SessionDep, 
                         email: EmailStr):
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: SessionDep):
    return db.execute(select(User)).scalars().all()

@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(db: SessionDep, 
                         id: str):
    user = db.execute(select(User).where(User.user_id == id)).scalar()

    if user is None:
        raise usuario_no_encontrado
    
    return user

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(db: SessionDep, 
                data: OAuth2PasswordRequestForm = Depends()):
    user = db.execute(select(User).where(User.email == data.username)).scalar_one_or_none()
    if not user:
        raise usuario_no_encontrado
    
    if not verify_password(data.password, user.hashed_password):
        raise contraseña_incorrecta
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=(UserResponse), status_code=status.HTTP_201_CREATED)
async def register(db: SessionDep, 
                   user_data: UserCreate):
    if not db.execute(select(User).where(User.email == user_data.email)):
        raise usuario_existente

    user_db = User(**user_data.model_dump(exclude={"password"}), hashed_password = hash_password(user_data.password))
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@router.post("/psychologist", response_model=PsychologistResponse, status_code=status.HTTP_201_CREATED)
async def register_psychologist(db: SessionDep,  
                                psychologist_data: PsychologistCreate, 
                                current_user: CurrentUser):
    
    user = db.execute(select(User).where(User.user_id == current_user["user_id"])).scalar()
    if not user:
        raise usuario_no_encontrado
    
    psychologist_dict = psychologist_data.model_dump()
    
    psychologist_db = Psychologist(user_id=user.user_id, 
                                   cedula=psychologist_dict["cedula"], 
                                   experiencia=psychologist_dict["experiencia"], 
                                   ubicacion=psychologist_dict["ubicacion"])
    
    if user.tipo_usuario == "user":
        setattr(user, "tipo_usuario", "psychologist")
        db.add(user)
        db.commit()
        db.refresh(user)

    db.add(psychologist_db)
    db.commit()
    db.refresh(psychologist_db)

    conexion_approach = ConexionApproach(psychologist_id=psychologist_db.psychologist_id, 
                                         approach_id=psychologist_dict["approach_id"])
    
    db.add(conexion_approach)
    db.commit()
    db.refresh(conexion_approach)
    
    return psychologist_db


@router.patch("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def patch_user(db: SessionDep, 
                     user_data: UserUpdate, 
                     current_user: CurrentUser):
    user_db = db.get(User, current_user["user_id"])
    if not user_db:
        raise usuario_no_encontrado
    
    user_dict = user_data.model_dump(exclude_unset=True)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay contendio que actualizar")
    
    for key, value in user_dict.items():
        setattr(user_db, key, value)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@router.patch("/psychologist", status_code=status.HTTP_200_OK)
async def patch_psychologist(db: SessionDep, 
                             current_user: CurrentUser,
                             psychologist_data: PsychologistUpdate):
    psychologist_db = db.execute(select(Psychologist).where(Psychologist.user_id == current_user["user_id"])).scalar_one_or_none()


    if not psychologist_db:
        raise usuario_no_encontrado
    
    psychologist_dict = psychologist_data.model_dump(exclude_unset=True)

    if not psychologist_dict:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay contendio que actualizar")
    
    try:
        for key, value in psychologist_dict.items():
            setattr(psychologist_db, key, value)
        
        db.add(psychologist_db)
        db.commit()
        db.refresh(psychologist_db)
        return psychologist_db
    except Exception as e:
        raise error_interno


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user(db: SessionDep, 
                      current_user: CurrentUser):
    
    user = db.execute(select(User).where(User.user_id == current_user["user_id"])).scalar_one_or_none()
    
    if user is None:
        raise usuario_no_encontrado
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado"}

