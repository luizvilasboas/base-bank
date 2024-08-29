from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.utils import JWT_SECRET_KEY, ALGORITHM, get_session
from utils.redis import delete_data, set_data, get_data
from models.models import PixKey
from schemas.schemas import PixKeyCreate, PixKeyCreateResponse, PixKeyResponse
from typing import List
from auth.auth_bearer import JWTBearer
import jwt

router = APIRouter(
    prefix="/pix",
    tags=["pix"],
    dependencies=[Depends(JWTBearer())],
)


@router.post("/create", response_model=PixKeyCreateResponse)
def create_pix_key(
    pix_key_data: PixKeyCreate,
    token: str = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Creates a new Pix key for the authenticated user.

    Args:
        pix_key_data (PixKeyCreate): The data for the new Pix key.
        token (str): JWT token for the authenticated user, provided by JWTBearer.
        session (Session): The database session dependency.

    Returns:
        dict: A message indicating the success of Pix key creation along with the created Pix key.

    Raises:
        HTTPException: If the Pix key already exists.
    """
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]

    existing_pix_key = session.query(PixKey).filter(
        PixKey.key == pix_key_data.key).first()
    if existing_pix_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chave do pix já existe."
        )

    new_pix_key = PixKey(user_id=user_id, key=pix_key_data.key)

    session.add(new_pix_key)
    session.commit()
    session.refresh(new_pix_key)

    delete_data(f"pix_keys_{user_id}")

    return PixKeyCreateResponse(message="Chave do pix criada com sucesso.", pix_key=new_pix_key.key, status_code=status.HTTP_200_OK)


@router.get("/list", response_model=List[PixKeyResponse])
def list_pix_keys(
    token: str = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Retrieves all Pix keys associated with the authenticated user.

    Args:
        token (str): JWT token for the authenticated user, provided by JWTBearer.
        session (Session): The database session dependency.

    Returns:
        List[PixKeyResponse]: A list of Pix keys associated with the authenticated user.
    """
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]

    cached_keys = get_data(f"pix_keys_{user_id}")
    if cached_keys:
        return cached_keys

    pix_keys = session.query(PixKey).filter_by(user_id=user_id).all()

    pix_keys_data = [
        {
            "id": pix_key.id,
            "key": pix_key.key,
            "user_id": pix_key.user_id,
        }
        for pix_key in pix_keys
    ]

    set_data(f"pix_keys_{user_id}", pix_keys_data, expiration=300)
    
    return pix_keys
