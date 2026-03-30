# app/modules/users/repositories.py

from sqlalchemy.orm import Session
from modules.users.models import User
from modules.users.schemas import UserCreate

class UserRepository:
    # Quando o Repository for chamado, ele precisa de receber uma sessão de base de dados aberta
    def __init__(self, db: Session):
        self.db = db

    # Função para procurar um utilizador pelo email (útil para validar se o email já existe)
    def get_by_email(self, email: str):
        # Vai à tabela User, filtra pelo email e devolve o primeiro resultado (ou None)
        return self.db.query(User).filter(User.email == email).first()

    # Função para criar um novo utilizador
    def create(self, user_in: UserCreate):
        # 1. Transformamos o "Schema" (dados recebidos) num "Model" (formato da base de dados)
        # ATENÇÃO: Por agora, vamos guardar a password diretamente. 
        # Na Semana 2 do plano de aulas, isto será substituído pelo hash gerado no security.py!
        db_user = User(
            nome=user_in.nome,
            email=user_in.email,
            hashed_password=user_in.password, # <- Alerta didático para os alunos!
            role=user_in.role
        )
        
        # 2. Adicionamos o novo utilizador à sessão atual
        self.db.add(db_user)
        
        # 3. Guardamos efetivamente na base de dados (o INSERT acontece aqui)
        self.db.commit()
        
        # 4. Atualizamos o objeto com os dados gerados pela base de dados (ex: o 'id' que foi criado)
        self.db.refresh(db_user)
        
        # 5. Devolvemos o utilizador criado
        return db_user