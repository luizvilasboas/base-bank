from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user, pix, transaction
from database.database import Base, engine
import pika
import os
import logging
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '179.189.94.124')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 9080))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', '43fc5c28-adc6-4882-8510-d2cff3404f27')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'B@se_B@nk!2024#Pr0t3ct')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_rabbitmq_connection():
    retry_interval = 5
    max_retries = 5
    
    for attempt in range(max_retries):
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            logger.info(f'Conexão com RabbitMQ bem-sucedida -> PORT: {RABBITMQ_PORT}, HOST: {RABBITMQ_HOST}')
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Erro ao conectar ao RabbitMQ (tentativa {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_interval)

    logger.error("Não foi possível conectar ao RabbitMQ após várias tentativas.")
    return None, None

connection, channel = get_rabbitmq_connection()

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
