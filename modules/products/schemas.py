from typing import Optional
from pydantic import BaseModel, ConfigDict


# Base com os campos comuns
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int


# Usado para CRIAR (exige todos os campos da base)
class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int = 0 


# Usado para ATUALIZAR (todos os campos se tornam opcionais)
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None


# Usado para RESPONDER (inclui o ID do banco)
class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int


class Config:
        orm_mode = True