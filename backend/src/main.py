from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user, pix, transaction
from database.database import Base, engine
import pika
import os
import logging
import threading
import time

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

Base.metadata.create_all(bind=engine)

app = FastAPI()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '179.189.94.124')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 9080))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', '43fc5c28-adc6-4882-8510-d2cff3404f27')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'B@se_B@nk!2024#Pr0t3ct')

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


def get_rabbitmq_connection():
    """Estabelece conexão com o RabbitMQ e retorna a conexão e o canal."""
    while True:
        try:
            credentials = pika.PlainCredentials(
                RABBITMQ_USER, RABBITMQ_PASSWORD)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            logger.info(
                f'Consegui conectar com RabbitMQ -> PORT:{RABBITMQ_PORT}, HOST: {RABBITMQ_HOST}')
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Erro ao conectar ao RabbitMQ: {e}")
            time.sleep(2)


def rabbitmq_consumer():
    """Função que consome mensagens da fila RabbitMQ."""
    connection, channel = get_rabbitmq_connection()

    channel.queue_declare(queue='base_bank_fila')

    def callback(ch, method, properties, body):
        logger.info(f"Mensagem recebida: {body.decode()}")

    channel.basic_consume(queue='base_bank_fila', on_message_callback=callback, auto_ack=True)

    logger.info('Esperando mensagens do RabbitMQ...')
    try:
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Erro durante o consumo de mensagens: {e}")
        channel.close()
        connection.close()
        rabbitmq_consumer()


thread = threading.Thread(target=rabbitmq_consumer)
thread.start()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
