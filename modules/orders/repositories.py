from sqlalchemy.orm import Session
from modules.orders.models import Order, OrderItem

class OrderRepository:
    # Cria pedido + itens (calcula o total automaticamente) 
    def criar(self, db: Session, order_data, user_id: int, total: float):
        db_order = Order(
            user_id=user_id,
            total=total,
            observacoes=order_data.observacoes
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        for item in order_data.itens:
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_order)
        return db_order

    # Pedidos de um utilizador 
    def listar_por_user(self, db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).all()

    # Busca um pedido com .first() 
    def buscar_por_id(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    # Atualiza só o status 
    def atualizar_status(self, db: Session, db_order: Order, status: str):
        db_order.status = status#type: ignore
        db.commit()
        db.refresh(db_order)
        return db_order
    
    # Remove pedido e itens (cascade) 
    def deletar(self, db: Session, db_order: Order):
        db.delete(db_order)
        db.commit()

