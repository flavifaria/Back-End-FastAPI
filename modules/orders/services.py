from sqlalchemy.orm import Session
from fastapi import HTTPException
from modules.orders.repositories import OrderRepository
from modules.products.models import ProdutoModel
from modules.products.history_services import register_stock_movement
from modules.orders.history_services import snapshot_order_items

repo = OrderRepository()


# Verifica stock de cada produto antes de criar
def criar_pedido(db: Session, user_id: int, order_data):
    total = 0.0
    product_map = {}
    for item in order_data.itens:
        produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.product_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.product_id} não encontrado.")
        if produto.estoque < item.quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para o produto {produto.nome}.")
        product_map[item.product_id] = produto
        total += produto.preco * item.quantidade

    pedido_criado = repo.criar(db, order_data, user_id, total)

    for item in order_data.itens:
        produto = product_map[item.product_id]
        item.preco_unitario = produto.preco
        register_stock_movement(
            db,
            produto,
            movement=-item.quantidade,
            movement_type="order_out",
            reference_type="order",
            reference_id=pedido_criado.id,
        )

    snapshot_order_items(db, pedido_criado)
    db.commit()

    return pedido_criado


# Só permite cancelar pedidos pendente. Devolve o stock dos produtos
def cancelar_pedido(db: Session, order_id: int, current_user_id: int):
    pedido = repo.buscar_por_id(db, order_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.user_id != current_user_id:  # type: ignore
        raise HTTPException(status_code=403, detail="Sem permissão para cancelar este pedido.")
    if pedido.status != "pendente":  # type: ignore
        raise HTTPException(status_code=400, detail="Apenas pedidos pendentes podem ser cancelados.")

    pedido.status = "cancelado"  # type: ignore

    for item in pedido.itens:
        produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.product_id).first()
        if produto:
            register_stock_movement(
                db,
                produto,
                movement=item.quantidade,
                movement_type="order_return",
                reference_type="order",
                reference_id=pedido.id,
            )

    snapshot_order_items(db, pedido)
    db.commit()
    db.refresh(pedido)
    return pedido
