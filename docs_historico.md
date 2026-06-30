# DER expandido + tabelas históricas planejadas

## Objetivo
Criar a base conceitual e técnica para registrar:
1. Histórico de preços;
2. Histórico de estoque;
3. Snapshot histórico dos itens de pedidos.

## Entidades históricas

### `product_price_history`
- `id` (PK)
- `product_id` (FK -> `produtos.id`)
- `old_price`
- `new_price`
- `change_reason`
- `changed_at`

### `product_stock_history`
- `id` (PK)
- `product_id` (FK -> `produtos.id`)
- `old_stock`
- `movement` (positivo/negativo)
- `new_stock`
- `movement_type` (`initial`, `manual_adjustment`, `order_out`, `order_return`)
- `reference_type` (ex.: `order`)
- `reference_id`
- `changed_at`

### `order_item_history`
- `id` (PK)
- `order_id` (FK -> `orders.id`)
- `product_id` (FK -> `produtos.id`)
- `quantity`
- `unit_price`
- `line_total`
- `status_snapshot`
- `captured_at`

## Fluxos planejados
- Atualização de produto com alteração de preço cria registro em `product_price_history`.
- Criação e cancelamento de pedido geram movimentações em `product_stock_history`.
- Criação/cancelamento de pedido geram snapshot em `order_item_history`.

## Streamlit
Arquivo `streamlit_app.py` oferece visualização rápida do DER textual e das 3 tabelas históricas.
