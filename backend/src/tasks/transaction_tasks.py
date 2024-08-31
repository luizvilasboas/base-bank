from tasks.celery_config import celery_app
from sqlalchemy.orm import Session
from models.models import Transaction, User
from utils.utils import get_session
from utils.redis import delete_data

@celery_app.task(name="src.tasks.transaction_tasks.process_transaction")
def process_transaction(sender_id, receiver_id, amount):
    session: Session = next(get_session())

    try:
        sender = session.query(User).filter(User.id == sender_id).first()
        if not sender:
            print(f"Sender com ID {sender_id} não encontrado.")
            return {"error": f"Sender com ID {sender_id} não encontrado."}

        receiver = session.query(User).filter(User.id == receiver_id).first()
        if not receiver:
            print(f"Receiver com ID {receiver_id} não encontrado.")
            return {"error": f"Receiver com ID {receiver_id} não encontrado."}

        if sender.balance < amount:
            print("Saldo insuficiente para realizar a transação.")
            return {"error": "Saldo insuficiente para realizar a transação."}

        sender.balance -= amount
        receiver.balance += amount
        print(f"Transferindo {amount} de {sender_id} para {receiver_id}")

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

        print("Transação realizada com sucesso.")
        return {"message": "Transação realizada com sucesso.", "transaction_id": new_transaction.id}

    except Exception as e:
        session.rollback()
        print(f"Erro ao processar transação: {str(e)}")
        return {"error": str(e)}

    finally:
        session.close()
