from sqlalchemy.orm import Session
from modules.products.models import Produto as ProdutoModel
from modules.products.schemas import ProdutoCreate, ProdutoUpdate

class ProdutoRepository:
    def criar(self, db: Session, produto: ProdutoCreate):
        db_produto = ProdutoModel(**produto.model_dump())
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        return db_produto

    def listar_todos(self, db: Session):
        return db.query(ProdutoModel).all()

    def buscar_por_id(self, db: Session, produto_id: int):
        return db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()

    def atualizar(self, db: Session, db_produto: ProdutoModel, produto_atualizado: ProdutoUpdate):
        dados_atualizacao = produto_atualizado.model_dump(exclude_unset=True)
        for chave, valor in dados_atualizacao.items():
            setattr(db_produto, chave, valor)
        db.commit()
        db.refresh(db_produto)
        return db_produto

    def deletar(self, db: Session, db_produto: ProdutoModel):
        db.delete(db_produto)
        db.commit()

