from sqlalchemy import Column, Integer, String, Float
from core.database import Base # ou de onde você importa o Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, nullable=True)  # <--- ADICIONE ESTA LINHA
    preco = Column(Float)
    # imagem_url = Column(String, nullable=True) # Se já tiver adicionado a imagem, mantenha esta linha. Caso contrário, adicione-a para armazenar a URL da imagem.
    estoque = Column(Integer, default=0) # <--- ADICIONE AQUI (default=0 evita que fique vazio)