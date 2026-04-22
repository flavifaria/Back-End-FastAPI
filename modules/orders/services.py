from sqlalchemy.orm import Session
from fastapi import HTTPException
from modules.orders.repositories import OrderRepository
from modules.products.models import ProdutoModel # Importa o modelo de Produto para ver o estoque

repo = OrderRepository()

# Verifica stock de cada produto antes de criar 
def criar_pedido(db: Session, user_id: int, order_data):
    total = 0.0
    # Validação de estoque e cálculo do total
    for item in order_data.itens:
        produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.product_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.product_id} não encontrado.")
        if produto.estoque < item.quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para o produto {produto.nome}.")
        
        total += item.preco_unitario * item.quantidade

    # Se ok, cria o pedido e desconta o stock automaticamente
    pedido_criado = repo.criar(db, order_data, user_id, total)

    # Descontando o estoque
    for item in order_data.itens:
        produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.product_id).first()
        ProdutoModel.estoque -= item.quantidade
    db.commit()

    return pedido_criado

# Só permite cancelar pedidos pendente. Devolve o stock dos produtos 
def cancelar_pedido(db: Session, order_id: int):
    pedido = repo.buscar_por_id(db, order_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.status != "pendente":#type: ignore
        raise HTTPException(status_code=400, detail="Apenas pedidos pendentes podem ser cancelados.")
    
    pedido.status = "cancelado"#type: ignore
    
    # Devolve o estoque
    for item in pedido.itens:
        produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.product_id).first()
        if produto:
            produto.estoque -= item.quantidade
            
    db.commit()
    db.refresh(pedido)
    return pedido

