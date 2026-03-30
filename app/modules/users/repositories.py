"""
Módulo de Repositório de Utilizadores.

Este módulo implementa o padrão Repository para abstrair a camada de acesso a dados.
Ele centraliza as operações de consulta e persistência relacionadas à entidade 'User',
mantendo o código de acesso ao banco separado das regras de negócio.
"""

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
        
        # Adiciona o novo usuário à sessão do banco de dados para ser persistido
        self.db.add(db_user)
        # Confirma as mudanças no banco de dados, executando a inserção
        self.db.commit()
        # Atualiza o objeto db_user com os dados do banco (como o ID gerado automaticamente)
        self.db.refresh(db_user)
        # Retorna o usuário recém-criado
        return db_user