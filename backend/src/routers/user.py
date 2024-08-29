from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.utils import JWT_SECRET_KEY, ALGORITHM, get_session
from utils.redis import set_data, get_data
from models.models import User
from schemas.schemas import UserResponse
from auth.auth_bearer import JWTBearer
import jwt

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
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]

    cached_user = get_data(f"user_{user_id}")
    if cached_user:
        return cached_user

    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
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

    set_data(f"user_{user_id}", user_data, expiration=300)

    return user
