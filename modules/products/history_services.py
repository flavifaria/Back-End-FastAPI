from modules.products.history_models import ProductPriceHistory, ProductStockHistory
from fastapi import HTTPException


def register_price_change(db, product, new_price: float, reason: str | None = None):
    old_price = product.preco
    if old_price == new_price:
        return

    db.add(
        ProductPriceHistory(
            product_id=product.id,
            old_price=old_price,
            new_price=new_price,
            change_reason=reason,
        )
    )


def register_stock_movement(
    db,
    product,
    movement: int,
    movement_type: str,
    reference_type: str | None = None,
    reference_id: int | None = None,
):
    old_stock = product.estoque
    new_stock = old_stock + movement
    if new_stock < 0:
        raise HTTPException(status_code=400, detail=f"Estoque não pode ficar negativo para o produto {product.nome}.")

    db.add(
        ProductStockHistory(
            product_id=product.id,
            old_stock=old_stock,
            movement=movement,
            new_stock=new_stock,
            movement_type=movement_type,
            reference_type=reference_type,
            reference_id=reference_id,
        )
    )

    product.estoque = new_stock
