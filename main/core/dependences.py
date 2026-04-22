from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from core.config import settings
from core.database import SessionLocal
from modules.users.repositories import UserRepository

# Informa ao Swagger onde fica a rota de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):    
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])["sub"]) 

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador não encontrado no banco de dados."
        )
    return user 


def get_current_gestor(current_user = Depends(get_current_user)):
    # Se o perfil do utilizador não for 'gestor', barramos a operação!
    if current_user.role != "gestor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas gestores podem realizar esta ação."
        )
        
    return current_user
