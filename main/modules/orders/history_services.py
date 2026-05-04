from modules.products.history_models import OrderItemHistory


def snapshot_order_items(db, order):
    for item in order.itens:
        db.add(
            OrderItemHistory(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantidade,
                unit_price=item.preco_unitario,
                line_total=item.quantidade * item.preco_unitario,
                status_snapshot=order.status,
            )
        )
