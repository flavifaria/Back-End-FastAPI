from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Order(Base):
    __tablename__ = "orders" 
    id = Column(Integer, primary_key=True, index=True) # Primary Key 
    user_id = Column(Integer, ForeignKey("users.id")) # FK -> users.id 
    status = Column(String, default="pendente") # pendente, pago, enviado, cancelado, entregue 
    total = Column(Float, default=0.0) # Soma de (preco_unitario * quantidade) dos itens 
    observacoes = Column(Text, nullable=True) # Notas opcionais 
    criado_em = Column(DateTime, default=datetime.utcnow) # Data de criação 

    # Relacionamentos
    itens = relationship("OrderItem", back_populates="pedido", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items" # Itens individuais do pedido 

    id = Column(Integer, primary_key=True, index=True) # Primary Key 
    order_id = Column(Integer, ForeignKey("orders.id")) # FK -> orders.id 
    product_id = Column(Integer, ForeignKey("produtos.id")) # FK -> produtos.id 
    quantidade = Column(Integer) # Quantidade do produto 
    preco_unitario = Column(Float) # Preço no momento da compra 

    # Relacionamentos
    pedido = relationship("Order", back_populates="itens")

