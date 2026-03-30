from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from modules.users.schemas import UserCreate, UserResponse
from modules.users.services import UserService

from core.dependencies import get_current_user
from modules.users.models import User


router = APIRouter(prefix="/users", tags=["Utilizadores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db) 
    return service.create_user(user_in)


@router.get("/me", response_model=UserResponse)
def ler_dados_do_meu_perfil(current_user: User = Depends(get_current_user)):
    return current_user
