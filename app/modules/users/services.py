# app/modules/users/services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.users.repositories import UserRepository
from modules.users.schemas import UserCreate

class UserService:
    def __init__(self, db: Session):
        # O Serviço precisa do Repositório para falar com o banco
        self.repository = UserRepository(db)

    def create_user(self, user_in: UserCreate):
        existing_user = self.repository.get_by_email(user_in.email)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email já está cadastrado no sistema."
            )
            
        
        return self.repository.create(user_in)