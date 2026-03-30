from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from core.config import settings
from core.database import SessionLocal
from modules.users.repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
    )
    
    try:
        # Tenta ler o Token usando a nossa Chave Secreta
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise erro_credenciais
    except jwt.InvalidTokenError:
        raise erro_credenciais
        
    # Busca o usuário no banco para garantir que ele não foi deletado
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=email)
    
    if user is None or not user.is_active:
        raise erro_credenciais
        
    return user
