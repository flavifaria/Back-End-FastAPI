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
    """
    Enumeração para os tipos de perfil de utilizador (Roles).

    Define os níveis de acesso ou categorias de utilizadores disponíveis no sistema.
    Herda de `str` para facilitar a serialização e de `enum.Enum` para validação.
    """
    GESTOR = "gestor"
    VENDEDOR = "vendedor"
    CLIENTE = "cliente"
    FORNECEDOR = "fornecedor"

class User(Base):
    """
    Modelo de Dados do Utilizador (SQLAlchemy).

    Representa a tabela 'users' na base de dados. Contém todas as informações
    cadastrais e de autenticação dos utilizadores do sistema.

    Attributes:
        id (int): Identificador único do utilizador (Primary Key).
        nome (str): Nome completo do utilizador.
        email (str): Endereço de email único (usado para login).
        hashed_password (str): Hash seguro da senha do utilizador.
        role (UserRole): Perfil de acesso do utilizador (default: CLIENTE).
        is_active (bool): Indica se a conta está ativa (default: True).
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)   
    hashed_password = Column(String, nullable=False) 
    role = Column(Enum(UserRole), default=UserRole.CLIENTE, nullable=False)   
    is_active = Column(Boolean, default=True)