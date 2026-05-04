from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.products.schemas import ProdutoCreate, ProdutoUpdate
from modules.products.repositories import ProdutoRepository
from modules.products.history_services import register_price_change, register_stock_movement

repo = ProdutoRepository()


class ProdutoService:
    def criar_produto(self, db: Session, produto: ProdutoCreate):
        novo = repo.criar(db, produto)
        register_stock_movement(db, novo, movement=novo.estoque, movement_type="initial")
        db.commit()
        return novo

    def listar_produtos(self, db: Session):
        return repo.listar_todos(db)

    def buscar_produto(self, db: Session, produto_id: int):
        produto = repo.buscar_por_id(db, produto_id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return produto

    def atualizar_produto(self, db: Session, produto_id: int, produto_atualizado: ProdutoUpdate):
        db_produto = self.buscar_produto(db, produto_id)
        dados = produto_atualizado.model_dump(exclude_unset=True)

        if "preco" in dados:
            register_price_change(db, db_produto, dados["preco"], reason="update_produto")
            db_produto.preco = dados["preco"]

        if "estoque" in dados:
            movement = dados["estoque"] - db_produto.estoque
            if movement != 0:
                register_stock_movement(db, db_produto, movement=movement, movement_type="manual_adjustment")

        for campo in ["nome", "descricao"]:
            if campo in dados:
                setattr(db_produto, campo, dados[campo])

        db.commit()
        db.refresh(db_produto)
        return db_produto

    def deletar_produto(self, db: Session, produto_id: int):
        db_produto = self.buscar_produto(db, produto_id)
        repo.deletar(db, db_produto)
