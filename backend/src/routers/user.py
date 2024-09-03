from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.utils import JWT_SECRET_KEY, ALGORITHM, get_session
from utils.redis import set_data, get_data
from models.models import User
from schemas.schemas import UserResponse
from auth.auth_bearer import JWTBearer
import logging
import jwt

logger = logging.getLogger("users")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/users.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: str = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Retrieves the current authenticated user's information.

    Args:
        token (str): JWT token for the authenticated user, provided by JWTBearer.
        session (Session): The database session dependency.

    Returns:
        UserResponse: The user data for the authenticated user.

    Raises:
        HTTPException: If the user is not found in the database.
    """
    logger.info(
        "Tentativa de acesso às informações do usuário com o token: %s", token)

    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]

    logger.info("Verificando cache para o usuário ID: %s", user_id)
    cached_user = get_data(f"user_{user_id}")
    if cached_user:
        logger.info("Usuário ID: %s encontrado no cache", user_id)
        return cached_user

    logger.info(
        "Buscando informações do usuário ID: %s no banco de dados", user_id)
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning(
            "Usuário ID: %s não encontrado no banco de dados", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "balance": user.balance,
    }

    logger.info("Armazenando informações do usuário ID: %s no cache", user_id)
    set_data(f"user_{user_id}", user_data, expiration=300)

    logger.info("Informações do usuário ID: %s retornadas com sucesso", user_id)
    return user
