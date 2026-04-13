from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from modules.products.schemas import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from modules.products.services import ProdutoService
from core.dependences import get_db

import shutil
import os
from sqlalchemy.orm import Session
from modules.products.models import Produto


router = APIRouter(prefix="/produtos", tags=["Produtos"])
service = ProdutoService()

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def adicionar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return service.criar_produto(db=db, produto=produto)

@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return service.listar_produtos(db=db)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto_especifico(produto_id: int, db: Session = Depends(get_db)):
    return service.buscar_produto(db=db, produto_id=produto_id)

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    return service.atualizar_produto(db=db, produto_id=produto_id, produto_atualizado=produto)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    service.deletar_produto(db=db, produto_id=produto_id)
    return None

@router.post("/{produto_id}/imagem")
def upload_imagem_produto(
    produto_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 1. Verificar se o produto existe no banco
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # 2. Validar se é realmente uma imagem (opcional, mas recomendado)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser uma imagem")

    # 3. Definir o nome e o caminho onde a imagem será salva
    # Dica: Usar o ID do produto no nome evita nomes duplicados
    extensao = file.filename.split(".")[-1]
    nome_arquivo = f"produto_{produto_id}.{extensao}"
    caminho_completo = f"static/images/{nome_arquivo}"

    # 4. Salvar o arquivo fisicamente na pasta
    with open(caminho_completo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 5. Atualizar o banco de dados com a URL da imagem
    # A URL será o caminho que o Front-end vai usar para acessar a foto
    produto.imagem_url = f"/static/images/{nome_arquivo}"
    db.commit()
    db.refresh(produto)

    return {"mensagem": "Imagem salva com sucesso!", "imagem_url": produto.imagem_url}

