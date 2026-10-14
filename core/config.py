"""
Arquivo de configuração da aplicação FastAPI.

Este módulo define as configurações globais da aplicação usando Pydantic BaseSettings.
As configurações podem ser sobrescritas por variáveis de ambiente definidas no arquivo .env.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe de configurações da aplicação.

    Herda de BaseSettings do Pydantic para gerenciar configurações de forma tipada e segura.
    Permite carregar valores de variáveis de ambiente ou de um arquivo .env.

    Atributos:
        PROJECT_NAME (str): Nome do projeto da API.
        VERSION (str): Versão atual da aplicação.
        DATABASE_URL (str): URL de conexão com o banco de dados SQLite.
        SECRET_KEY (str): Chave secreta para assinatura de tokens JWT.
        ALGORITHM (str): Algoritmo de criptografia usado para JWT (HS256).
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tempo de expiração dos tokens de acesso em minutos.
        model_config: Configuração do Pydantic para carregar do arquivo .env com codificação UTF-8.
    """

    PROJECT_NAME: str = "API - Mercearia do João"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./mercearia.db"
    SECRET_KEY: str = "sua-chave-super-secreta-aqui-mude-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()