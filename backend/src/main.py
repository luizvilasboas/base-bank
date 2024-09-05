from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.models import User
from sqlalchemy.orm import Session
from routers import auth, user, pix, transaction
from database.database import Base, engine, SessionLocal
from utils.redis import delete_data
import pika
import logging
import threading
import json
from dotenv import load_dotenv

load_dotenv(".env.secret")

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pix.router)
app.include_router(transaction.router)


RABBITMQ_HOST = "179.189.94.124"
RABBITMQ_PORT = 9080
RABBITMQ_USER = "43fc5c28-adc6-4882-8510-d2cff3404f27"
RABBITMQ_PASSWORD = "B@se_B@nk!2024#Pr0t3ct"

QUEUE_RECEIVE = 'transacao_43fc5c28-adc6-4882-8510-d2cff3404f27_queue'
QUEUE_RESPONSE = 'transacao_43fc5c28-adc6-4882-8510-d2cff3404f27_response_queue'

def get_session():
    """
    Creates a new database session.

    Returns:
        Session: A new database session.
    """
    session = SessionLocal()
    return session


def update_user(session: Session, user_id, amount):
    """Atualiza o saldo do cliente no banco de dados."""
    client = session.query(User).filter(User.id == user_id).first()

    if client:
        client.balance += amount
        session.commit()
        session.refresh(client)
        logger.info(
            f'Saldo de {client.username} atualizado com sucesso para {client.balance}')
    else:
        logger.error(f'Cliente com ID de {user_id} não encontrado')


def on_message(ch, method, properties, body):
    """Callback para processar as mensagens recebidas."""
    mensagem = body.decode()
    logger.info(f"Mensagem recebida: {mensagem}")

    dados = json.loads(mensagem)

    logger.info('Passando dados para JSON')

    if 'usuario_destino' in dados and 'valor' in dados:
        to = dados['usuario_destino']
        amount = dados['valor']

        session = get_session()

        try:
            update_user(session=session, user_id=to, amount=amount)
            delete_data(f"user_{to}")
        except Exception as e:
            logger.error(f"Erro ao processar a transação: {e}")
        finally:
            session.close()
    else:
        logger.error('Estrutura da menssagem errada.')

    resultado = {
        "sucesso": True,
        "mensagem": "Transação realizada com sucesso."
    }

    ch.basic_publish(
        exchange='',
        routing_key=QUEUE_RESPONSE,
        body=json.dumps(resultado),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_rabbitmq_messages():
    """Função para consumir mensagens RabbitMQ."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_RECEIVE, durable=True)
    channel.queue_declare(queue=QUEUE_RESPONSE, durable=True)

    channel.basic_consume(queue=QUEUE_RECEIVE, on_message_callback=on_message, auto_ack=False)

    logger.info(f"Escutando a fila '{QUEUE_RECEIVE}'...")

    channel.start_consuming()


@app.on_event("startup")
def startup_event():
    """Evento de inicialização do FastAPI."""
    threading.Thread(target=consume_rabbitmq_messages, daemon=True).start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
