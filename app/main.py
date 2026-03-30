from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # NOVO IMPORT
from core.database import engine, Base
from modules.users import models
from modules.users.routers import router as users_router
from modules.auth.routers import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API - Mercearia do Erinaldo")
app.include_router(users_router)
app.include_router(auth_router)


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

app.include_router(users_router)

@app.get("/")
def read_root():
    return {"mensagem": "API da Mercearia do Erinaldo está a funcionar!"}
