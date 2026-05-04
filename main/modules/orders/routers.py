from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db
from modules.orders import schemas, services, repositories
from core.dependencies import get_current_user 
# Importe a sua dependência de usuário logado (ajuste o caminho se necessário)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = repositories.OrderRepository()

# Cria novo pedido 
@router.post("/", response_model=schemas.OrderResponse)
def criar_pedido(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return services.criar_pedido(db, current_user.id, order)

# Lista pedidos do utilizador 
@router.get("/", response_model=list[schemas.OrderResponse])
def listar_pedidos(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return repo.listar_por_user(db, current_user.id)

# Busca um pedido 
@router.get("/{order_id}", response_model=schemas.OrderResponse)
def buscar_pedido(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return repo.buscar_por_id(db, order_id)

# Cancela pedido pendente 
@router.post("/{order_id}/cancelar", response_model=schemas.OrderResponse)
def cancelar_pedido(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return services.cancelar_pedido(db, order_id, current_user.id)

