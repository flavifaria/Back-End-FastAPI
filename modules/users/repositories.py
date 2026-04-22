# app/modules/users/repositories.py
from sqlalchemy.orm import Session
from modules.users.models import User
from modules.users.schemas import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_in: UserCreate):
        db_user = User(
            nome=user_in.nome,
            email=user_in.email,
            hashed_password=user_in.password,
            role=user_in.role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    # ADICIONE ESTA FUNÇÃO AQUI (Atenção ao alinhamento/indentação!):
    def delete(self, user_id: int):
        # 1. Procura o utilizador pelo ID
        user = self.db.query(User).filter(User.id == user_id).first()
        
        # 2. Se encontrar, fazemos o "Soft Delete" (inativamos)
        if user:
            user.is_active = False
            self.db.commit() # Salva a alteração
            self.db.refresh(user)
            
        return user