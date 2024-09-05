from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.models.models import User
from backend.src.utils.utils import get_session
from routers import auth, user, pix, transaction
from database.database import Base, engine
import pika
import os
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


def on_message(ch, method, properties, body):
    """Callback para processar as mensagens recebidas."""
    mensagem = body.decode()
    logger.info(f"Mensagem recebida: {mensagem}")

    ammount = mensagem['valor']
    to = mensagem['usuario_destino']

    session = get_session()

    try:
        user = session.query(User).filter_by(id=to).first()

        if user:
            user.balance += ammount
            session.commit()

            logger.info(f"Adicionado {ammount} para usuário {user.username}, que agora tem {user.balance}")
            resultado = {
                "sucesso": True,
                "mensagem": "Transação realizada com sucesso."
            }
        else:
            logger.info("Usuário não encontrado.")
            resultado = {
                "sucesso": False,
                "mensagem": "Usuário não encontrado."
            }
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao processar a transação: {e}")
        resultado = {
            "sucesso": False,
            "mensagem": "Erro ao processar a transação."
        }
    finally:
        session.close()

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
