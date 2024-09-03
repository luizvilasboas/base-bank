from tasks.celery_config import celery_app
from sqlalchemy.orm import Session
from models.models import Transaction, User
from utils.utils import get_session
from utils.redis import delete_data
from services.core import core_service

@celery_app.task(name="src.tasks.transaction_tasks.process_transaction")
def process_transaction(sender_id, receiver_id, pix_key, amount):
    session: Session = next(get_session())

    try:
        sender = session.query(User).filter(User.id == sender_id).first()
        if not sender:
            raise ValueError(f"Sender com ID {sender_id} não encontrado.")

        if sender.balance < amount:
            raise ValueError("Saldo insuficiente para realizar a transação.")

        core_service.transaction(pix_key, amount, receiver_id)

        sender.balance -= amount

        receiver = session.query(User).filter(User.id == receiver_id).first()

        if receiver:
            receiver.balance += amount

            new_transaction = Transaction(
                sender_id=sender.id,
                receiver_id=receiver.id,
                amount=amount,
            )
            session.add(new_transaction)
        else:
            new_transaction = Transaction(
                sender_id=sender.id,
                receiver_id=None,
                amount=amount,
            )
            session.add(new_transaction)

        session.commit()
        session.refresh(new_transaction)

        delete_data(f"user_{sender.id}")

        if receiver:
            delete_data(f"user_{receiver.id}")

        return {"message": "Transação realizada com sucesso.", "transaction_id": new_transaction.id}

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
