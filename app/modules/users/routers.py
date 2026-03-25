"""
Módulo de Rotas (Routers) de Utilizadores.

Este módulo define os endpoints da API relacionados aos utilizadores.
Utiliza o FastAPI APIRouter para organizar as rotas e injeta as dependências
necessárias (como a sessão de banco de dados) para os controladores.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from modules.users.schemas import UserCreate, UserResponse
from modules.users.services import UserService

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
