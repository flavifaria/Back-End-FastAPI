from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from modules.users.schemas import UserCreate, UserResponse
from modules.users.services import UserService

from core.dependences import get_current_user ,get_current_gestor
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

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_usuario(
    user_id: int, 
    db: Session = Depends(get_db),
    
    # ATENÇÃO AQUI: Trocámos o 'get_current_user' pelo 'get_current_gestor'!
    current_user: User = Depends(get_current_gestor) 
):
    """
    Rota Protegida (Nível: Gestor)!
    Apenas utilizadores com o perfil 'gestor' conseguem chegar a esta linha.
    """
    service = UserService(db)
    service.delete_user(user_id)
    
    return None
