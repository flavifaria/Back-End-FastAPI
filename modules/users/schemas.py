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
    """
    Schema base com os atributos comuns do Utilizador.

    Attributes:
        nome (str): Nome completo do utilizador.
        email (EmailStr): Endereço de email válido.
        role (UserRole): Perfil de acesso (padrão: CLIENTE).
    """
    nome: str
    email: EmailStr 
    role: UserRole = UserRole.CLIENTE

class UserCreate(UserBase):
    """
    Schema para criação de um novo utilizador (Input).

    Herda de UserBase e adiciona a senha, que é obrigatória
    apenas no momento do registo.
    
    Attributes:
        password (str): Senha em texto plano (será hashada no serviço).
    """
    password: str

class UserResponse(UserBase):
    """
    Schema para resposta de dados do utilizador (Output).

    Herda de UserBase e adiciona campos gerados pelo sistema,
    como ID e status. Removemos a senha para segurança.

    Attributes:
        id (int): Identificador único.
        is_active (bool): Estado da conta.
    """
    id: int
    is_active: bool

    # Configuração para permitir a criação a partir de objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)