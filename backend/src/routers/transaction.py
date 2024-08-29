from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.utils import JWT_SECRET_KEY, ALGORITHM, get_session
from models.models import PixKey, Transaction, User
from schemas.schemas import TransactionCreate, TransactionCreateResponse
from auth.auth_bearer import JWTBearer
import jwt

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
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    sender_id = payload["sub"]

    # Verify if the sender's Pix key exists and belongs to the sender
    sender_pix_key = (
        session.query(PixKey)
        .filter(PixKey.key == transaction_data.sender_pix_key, PixKey.user_id == sender_id)
        .first()
    )
    if not sender_pix_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave PIX do remetente não encontrada.",
        )

    # Verify if the receiver's Pix key exists
    receiver_pix_key = (
        session.query(PixKey)
        .filter(PixKey.key == transaction_data.receiver_pix_key)
        .first()
    )
    if not receiver_pix_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave PIX do destinatário não encontrada.",
        )

    # Retrieve sender and receiver user data
    sender = session.query(User).filter(
        User.id == sender_pix_key.user_id).first()
    receiver = session.query(User).filter(
        User.id == receiver_pix_key.user_id).first()

    if sender.balance < transaction_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar a transação.",
        )

    sender.balance -= transaction_data.amount
    receiver.balance += transaction_data.amount

    new_transaction = Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=transaction_data.amount,
    )

    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)

    return TransactionCreateResponse(message="Transação realizada com sucesso.", transaction_id=new_transaction.id, status_code=status.HTTP_200_OK)
