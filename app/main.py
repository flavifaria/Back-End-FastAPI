"""
Arquivo Principal (Entry Point) da Aplicação.

Este módulo inicializa a aplicação FastAPI, configura as rotas e
cria as tabelas no banco de dados caso ainda não existam.
"""

from fastapi import FastAPI
from core.database import engine, Base
from modules.users import models
from modules.users.routers import router as users_router 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API - Mercearia do Erinaldo")

app.include_router(users_router) 

@app.get("/", tags=["Health Check"])
def read_root():
    return {"mensagem": "API da Mercearia do João está a funcionar!"}
