import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # NOVO IMPORT
from core.database import engine, Base
from modules.users import models
from modules.users.routers import router as users_router
from modules.auth.routers import router as auth_router
from modules.products.routers import router as products_router
from modules.orders.routers import router as orders_router
from fastapi.staticfiles import StaticFiles


os.makedirs("static/images", exist_ok=True)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="API - Mercearia do Erinaldo")
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.mount("/static", StaticFiles(directory="static"), name="static")



# --- CONFIGURAÇÃO DO CORS ---
# Isto permite que a nossa página HTML local converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, colocaríamos apenas o domínio real do site
    allow_credentials=True,
    allow_methods=["*"],  # Permite POST, GET, PUT, DELETE
    allow_headers=["*"],
)
# ----------------------------


@app.get("/" , tags=["Raiz"])
def read_root():
    return {"mensagem": "API da Mercearia do Erinaldo funciona!"}