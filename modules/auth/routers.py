from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import SessionLocal
from modules.users.repositories import UserRepository
from core.security import verify_password, create_access_token
from modules.auth.schemas import Token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    # O form_data.username guarda o e-mail digitado no Swagger
    user = user_repo.get_by_email(email=form_data.username)
    
    # Valida se usuário existe E se a senha bate
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilizador inativo",
        )
    
    # Cria o Token colocando o email e o perfil dentro dele
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    
    return {"access_token": access_token, "token_type": "bearer"}
