"""
Módulo de Schemas (Pydantic) de Utilizadores.

Este arquivo define as estruturas de dados para validação e serialização
de entrada e saída da API (Request/Response bodies). Utiliza o Pydantic
para garantir que os dados estejam no formato correto antes de chegarem
ao controlador ou serem enviados ao cliente.
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from modules.users.models import UserRole

class UserBase(BaseModel):
    nome: str
    email: EmailStr 
    role: UserRole = UserRole.CLIENTE

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    # Configuração para permitir a criação a partir de objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)