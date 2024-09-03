from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.utils import JWT_SECRET_KEY, ALGORITHM, get_session
from models.models import PixKey
from schemas.schemas import TransactionCreate, TransactionCreateResponse
from auth.auth_bearer import JWTBearer
from tasks.transaction_tasks import process_transaction
import jwt
import logging

logger = logging.getLogger("transaction")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/transaction.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    dependencies=[Depends(JWTBearer())],
)


@router.post("/create", response_model=TransactionCreateResponse)
def create_transaction(
    transaction_data: TransactionCreate,
    token: str = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Creates a new transaction between two users using their Pix keys.

    Args:
        transaction_data (TransactionCreate): The data for the transaction, including sender and receiver Pix keys and the amount.
        token (str): JWT token for the authenticated user, provided by JWTBearer.
        session (Session): The database session dependency.

    Returns:
        dict: A message indicating the success of the transaction along with the transaction ID.

    Raises:
        HTTPException: If the sender's Pix key is not found.
        HTTPException: If the receiver's Pix key is not found.
        HTTPException: If the sender has insufficient balance for the transaction.
    """
    logger.info("Tentativa de criação de transação para o token: %s", token)

    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    sender_id = payload["sub"]

    logger.info("Buscando chave PIX do remetente: %s para o usuário ID: %s",
                transaction_data.sender_pix_key, sender_id)

    sender_pix_key = (
        session.query(PixKey)
        .filter(PixKey.key == transaction_data.sender_pix_key, PixKey.user_id == sender_id)
        .first()
    )

    if not sender_pix_key:
        logger.warning("Chave PIX do remetente não encontrada: %s para o usuário ID: %s",
                       transaction_data.sender_pix_key, sender_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave PIX do remetente não encontrada.",
        )

    logger.info("Buscando chave PIX do destinatário: %s",
                transaction_data.receiver_pix_key)

    receiver_pix_key = (
        session.query(PixKey)
        .filter(PixKey.key == transaction_data.receiver_pix_key)
        .first()
    )

    if not receiver_pix_key:
        logger.warning("Chave PIX do destinatário não encontrada: %s",
                       transaction_data.receiver_pix_key)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave PIX do destinatário não encontrada.",
        )

    logger.info("Iniciando transação de %s para %s, valor: %s",
                sender_pix_key.key, receiver_pix_key.key, transaction_data.amount)

    result = process_transaction.delay(
        sender_id=sender_pix_key.user_id,
        receiver_id=receiver_pix_key.user_id,
        pix_key=transaction_data.receiver_pix_key,
        amount=transaction_data.amount
    )

    logger.info("Transação iniciada com sucesso. Task ID: %s", result.id)

    return TransactionCreateResponse(message="Transação realizada com sucesso.", task_id=result.id)
