from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.products.schemas import ProdutoCreate, ProdutoUpdate
from modules.products.repositories import ProdutoRepository

repo = ProdutoRepository()

class ProdutoService:
    def criar_produto(self, db: Session, produto: ProdutoCreate):
        return repo.criar(db, produto)

    def listar_produtos(self, db: Session):
        return repo.listar_todos(db)

    def buscar_produto(self, db: Session, produto_id: int):
        produto = repo.buscar_por_id(db, produto_id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return produto

    def atualizar_produto(self, db: Session, produto_id: int, produto_atualizado: ProdutoUpdate):
        db_produto = self.buscar_produto(db, produto_id) # Reaproveita a validação de erro 404
        return repo.atualizar(db, db_produto, produto_atualizado)

    def deletar_produto(self, db: Session, produto_id: int):
        db_produto = self.buscar_produto(db, produto_id)
        repo.deletar(db, db_produto)

