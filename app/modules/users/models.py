# app/modules/users/models.py

from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from core.database import Base

class UserRole(str, enum.Enum):
    GESTOR = "gestor"
    VENDEDOR = "vendedor"
    CLIENTE = "cliente"
    FORNECEDOR = "fornecedor"

class User(Base):
    __tablename__ = "users" # Nome da tabela na base de dados

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    
    # O email deve ser único, não podemos ter duas contas com o mesmo email
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)   
    role = Column(Enum(UserRole), default=UserRole.CLIENTE, nullable=False)
    
    # Campo para ativar/desativar utilizadores sem precisar de os apagar da base de dados (Soft Delete)
    is_active = Column(Boolean, default=True)