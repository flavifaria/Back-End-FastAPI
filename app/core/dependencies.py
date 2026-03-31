from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from core.config import settings
from core.database import SessionLocal
from modules.users.repositories import UserRepository

# 1. Este é o "detetor de crachás". 
# Ele vai procurar o Token no cabeçalho (Header) da requisição.
# O 'tokenUrl' diz ao Swagger onde é que o utilizador deve ir para obter o Token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Função que já tínhamos para abrir a base de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. CORREÇÃO NO SEGURANÇA PRINCIPAL
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):    
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])["sub"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador não encontrado no banco de dados."
        )
    return user


# 2. CRIAÇÃO DO SEGURANÇA VIP (Apenas Gestor)
def get_current_gestor(current_user = Depends(get_current_user)):
    """Verifica se o utilizador autenticado tem o perfil de gestor."""
    
    if current_user.role != "gestor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas gestores podem realizar esta ação."
        )
        
    # ATENÇÃO: Devolvemos a variável correta (current_user)!
    return current_user

