from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.users.repositories import UserRepository
from modules.users.schemas import UserCreate

from core.security import get_password_hash

# NOVO: Importamos a função que faz o hash da palavra-passe
from core.security import get_password_hash 

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    
    def create_user(self, user_in: UserCreate):
        existing_user = self.repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        
        # MAGIA ACONTECENDO AQUI: Substituímos a senha limpa pelo Hash!
        user_in.password = get_password_hash(user_in.password)
        
        return self.repository.create(user_in)

    def delete_user(self, user_id: int, current_user_id: int, current_user_role: str):
            if user_id == current_user_id and current_user_role in ("gestor", "admin"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Administrador não pode se autoexcluir."
                )
            # Manda o repositório apagar
            deleted_user = self.repository.delete(user_id)
            
            # Se o repositório não encontrou o ID, lançamos erro 404
            if not deleted_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado."
                )
            return deleted_user
