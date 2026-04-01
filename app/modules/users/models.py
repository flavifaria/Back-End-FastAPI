"""
Módulo de Modelos de Utilizadores.

Este arquivo define os modelos de dados (tabelas) para o módulo de utilizadores
usando o ORM SQLAlchemy. Define a estrutura da tabela 'users' e os tipos de
funções (roles) permitidos no sistema.
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from core.database import Base

class UserRole(str, enum.Enum):

    GESTOR = "gestor"
    VENDEDOR = "vendedor"
    CLIENTE = "cliente"
    FORNECEDOR = "fornecedor"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)   
    hashed_password = Column(String, nullable=False) 
    role = Column(Enum(UserRole), default=UserRole.CLIENTE, nullable=False)   
    is_active = Column(Boolean, default=True)