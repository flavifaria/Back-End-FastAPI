"""
Módulo de Configuração de Banco de Dados.

Este arquivo é responsável por configurar a conexão com o banco de dados
usando o SQLAlchemy. Ele define o 'engine' de conexão, a fábrica de
sessões (SessionLocal) e a classe base declarativa (Base) da qual todos
os modelos ORM devem herdar.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Cria o motor de conexão (Engine) do SQLAlchemy.
# connect_args={"check_same_thread": False} é específico para SQLite,
# permitindo que mais de uma thread interaja com o banco (necessário para FastAPI).
engine = create_engine(SQLALCHEMY_DATABASE_URL , connect_args={"check_same_thread": False})

# Fábrica de sessões (SessionLocal). Cada instância será uma conexão com o banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base Declarativa. Todos os modelos de dados devem herdar desta classe.
Base = declarative_base()