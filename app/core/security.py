from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from core.config import settings

# 1. Configura o Triturador (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Recebe a senha limpa e devolve o Hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada com o Hash do banco"""
    return pwd_context.verify(plain_password, hashed_password)

# 2. Configura o Gerador de Crachás (JWT)
def create_access_token(data: dict) -> str:
    """Gera o Token com prazo de validade"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Assina o token com a nossa CHAVE SECRETA (que está no .env)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
