from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class ProductPriceHistory(Base):
    __tablename__ = "product_price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    change_reason = Column(String, nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    product = relationship("ProdutoModel")


class ProductStockHistory(Base):
    __tablename__ = "product_stock_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    old_stock = Column(Integer, nullable=False)
    movement = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    movement_type = Column(String, nullable=False)
    reference_type = Column(String, nullable=True)
    reference_id = Column(Integer, nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    product = relationship("ProdutoModel")


class OrderItemHistory(Base):
    __tablename__ = "order_item_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    status_snapshot = Column(String, nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    order = relationship("Order")
    product = relationship("ProdutoModel")
