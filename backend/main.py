from typing import List

from psycopg2.errors import UniqueViolation
from schemas import (
    UserCreate,
    TokenSchema,
    RequestDetails,
    TransactionCreate,
    UserResponse,
    PixKeyCreate,
    PixKeyResponse,
)
from models import User, TokenTable, Transaction, PixKey
from database import Base, engine, SessionLocal
from utils import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    JWT_SECRET_KEY,
    ALGORITHM,
)
from auth_bearer import JWTBearer
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import jwt
from functools import wraps

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        payload = jwt.decode(kwargs["dependencies"], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload["sub"]
        data = (
            kwargs["session"]
            .query(TokenTable)
            .filter_by(user_id=user_id, access_toke=kwargs["dependencies"], status=True)
            .first()
        )
        if data:
            return func(kwargs["dependencies"], kwargs["session"])

        else:
            return {"msg": "Token blocked"}

    return wrapper


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


@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já foi registrado."
        )

    encrypted_password = get_hashed_password(user.password)

    new_user = User(
        username=user.username, email=user.email, password=encrypted_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "Usuário criado com sucesso.", "status_code": status.HTTP_200_OK}


@app.post("/login", response_model=TokenSchema)
def login(request: RequestDetails, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == request.email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email incorreto."
        )

    hashed_pass = user.password

    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Senha incorreta."
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = TokenTable(
        user_id=user.id, access_token=access, refresh_token=refresh, status=True
    )

    session.add(token_db)
    session.commit()
    session.refresh(token_db)

    return {
        "message": "Usuário logado com sucesso.",
        "status_code": status.HTTP_200_OK,
        "access_token": access,
        "refresh_token": refresh,
    }


@app.post("/logout")
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]
    token_record = db.query(TokenTable).all()
    info = []

    for record in token_record:
        print("record", record)
        current_utc_time = datetime.now(timezone.utc).replace(tzinfo=None)

        if (current_utc_time - record.created_date).days > 1:
            info.append(record.user_id)

    if info:
        existing_token = (
            db.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
        )
        db.commit()

    existing_token = (
        db.query(TokenTable)
        .filter(TokenTable.user_id == user_id, TokenTable.access_token == token)
        .first()
    )

    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)

    return {"message": "Logout feito com sucesso.", "status_code": status.HTTP_200_OK}


@app.post("/pix_keys", dependencies=[Depends(JWTBearer())])
def create_pix_key(
    pix_key: PixKeyCreate,
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]

    existing_pix_key = session.query(PixKey).filter(PixKey.key == pix_key.key).first()
    if existing_pix_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chave do pix já existe."
        )

    new_pix_key = PixKey(user_id=user_id, key=pix_key.key)
    
    session.add(new_pix_key)
    session.commit()
    session.refresh(new_pix_key)

    return {
        "message": "Chave do pix criada com sucesso.",
        "pix_key": new_pix_key.key,
        "status_code": status.HTTP_200_OK,
    }


@app.get(
    "/pix_keys",
    response_model=List[PixKeyResponse],
    dependencies=[Depends(JWTBearer())],
)
def get_pix_keys(
    dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]

    pix_keys = session.query(PixKey).filter_by(user_id=user_id).all()
    return pix_keys


@app.get("/me", response_model=UserResponse, dependencies=[Depends(JWTBearer())])
def get_me(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]

    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    return user


@app.post("/transfer", dependencies=[Depends(JWTBearer())])
def transfer(transaction: TransactionCreate, dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]

    sender_key = session.query(PixKey).filter(PixKey.user_id == user_id).first()
    receiver_key = session.query(PixKey).filter(PixKey.key == transaction.pix_key).first()

    if sender_key is None or receiver_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário ou chave PIX não encontrado.")

    sender = session.query(User).filter(User.id == sender_key.user_id).first()
    receiver = session.query(User).filter(User.id == receiver_key.user_id).first()

    if sender.balance < transaction.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Balança insuficiente para fazer essa transação.")

    sender.balance -= transaction.amount
    receiver.balance += transaction.amount

    new_transaction = Transaction(sender_id=sender.id, receiver_id=receiver.id, amount=transaction.amount)

    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)

    return {
        "message": "Transação feita com sucesso.",
        "transaction_id": new_transaction.id,
        "status_code": status.HTTP_200_OK,
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
