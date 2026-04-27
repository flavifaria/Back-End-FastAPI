from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Pegamos a URL do banco do arquivo .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# O motor que fala com o PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Nossa fábrica de conexões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A classe base que os modelos vão herdar
Base = declarative_base()

# Função para abrir/fechar o banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()