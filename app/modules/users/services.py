from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.users.repositories import UserRepository
from modules.users.schemas import UserCreate
from core.security import get_password_hash
from core.security import get_password_hash 

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    
    def create_user(self, user_in: UserCreate):
        existing_user = self.repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        
        user_in.password = get_password_hash(user_in.password)
        
        return self.repository.create(user_in)
