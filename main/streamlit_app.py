import pandas as pd
import streamlit as st
from sqlalchemy import text

from core.database import SessionLocal

st.set_page_config(page_title="Base Histórica - Mercearia", layout="wide")
st.title("Base conceitual e técnica de histórico")

st.markdown(
    """
### DER expandido (visão textual)
- **produtos** (1) ─── (N) **product_price_history**
- **produtos** (1) ─── (N) **product_stock_history**
- **orders** (1) ─── (N) **order_items**
- **orders** (1) ─── (N) **order_item_history**
- **produtos** (1) ─── (N) **order_item_history**

As tabelas históricas foram planejadas para manter trilha de auditoria de preço, estoque e itens dos pedidos.
"""
)

queries = {
    "Histórico de preços": "SELECT * FROM product_price_history ORDER BY changed_at DESC LIMIT 50",
    "Histórico de estoque": "SELECT * FROM product_stock_history ORDER BY changed_at DESC LIMIT 50",
    "Histórico de itens de pedido": "SELECT * FROM order_item_history ORDER BY captured_at DESC LIMIT 50",
}

session = SessionLocal()
for titulo, query in queries.items():
    st.subheader(titulo)
    try:
        rows = session.execute(text(query)).mappings().all()
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    except Exception as exc:
        st.warning(f"Tabela ainda não criada ou sem dados: {exc}")

session.close()
