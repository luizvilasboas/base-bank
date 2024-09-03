from tasks.celery_config import celery_app
from sqlalchemy.orm import Session
from models.models import Transaction, User
from utils.utils import get_session
from utils.redis import delete_data
from fastapi import HTTPException, status


@celery_app.task(name="src.tasks.transaction_tasks.process_transaction")
def process_transaction(sender_id, receiver_id, amount):
    session: Session = next(get_session())

    try:
        sender = session.query(User).filter(User.id == sender_id).first()
        if not sender:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sender com ID {sender_id} não encontrado."
            )

        receiver = session.query(User).filter(User.id == receiver_id).first()
        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receiver com ID {receiver_id} não encontrado."
            )

        if sender.balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saldo insuficiente para realizar a transação."
            )

        sender.balance -= amount
        receiver.balance += amount

        new_transaction = Transaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=amount,
        )

        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)

        delete_data(f"user_{sender.id}")
        delete_data(f"user_{receiver.id}")

        return {"message": "Transação realizada com sucesso.", "transaction_id": new_transaction.id}

    except HTTPException as http_exc:
        session.rollback()
        raise http_exc

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar transação."
        )

    finally:
        session.close()
