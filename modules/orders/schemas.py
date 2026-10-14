from pydantic import BaseModel , ConfigDict
from typing import List, Optional 
from datetime import datetime

# Corpo de criação de um item 
class OrderItemCreate(BaseModel):
    product_id: int
    quantidade: int
    preco_unitario: float

# Resposta de um item na listagem 
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantidade: int
    preco_unitario: float

    model_config = ConfigDict(from_attributes=True)

# Corpo de criação de pedido (com lista de itens) 
class OrderCreate(BaseModel):
    observacoes: Optional[str] = None
    itens: List[OrderItemCreate]

# Atualizar status e/ou observações
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    observacoes: Optional[str] = None

# Resposta completa (pedido + itens) 
class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    observacoes: Optional[str] = None
    criado_em: datetime
    itens: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

    #class Config:
    #    from_attributes = True # from_attributes True

