from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.utils import (
    ALGORITHM,
    JWT_SECRET_KEY,
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
    get_session,
)
from schemas.schemas import LogoutResponse, UserCreate, TokenSchema, RequestDetails, UserRegisterResponse
from models.models import User, TokenTable
from auth.auth_bearer import JWTBearer
from services.core import core_service
import datetime
import logging
import jwt

logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/auth.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserRegisterResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Registers a new user in the system.

    - **user**: The user details for registration.
    - **session**: The database session dependency.

    Returns:
    - A message indicating the success of the registration process.

    Raises:
    - **400 Bad Request**: If the email is already registered.
    - **500 Internal Server Error**: If the user creation fails in the core service.
    """
    logger.info("Tentativa de registro para o email: %s", user.email)

    existing_user = session.query(User).filter_by(email=user.email).first()

    if existing_user:
        logger.warning("Email já registrado: %s", user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já foi registrado."
        )

    user_id = core_service.register_user(user.username, user.email)

    encrypted_password = get_hashed_password(user.password)

    new_user = User(
        id=user_id, username=user.username, email=user.email, password=encrypted_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    logger.info("Usuário registrado com sucesso: %s", user.email)
    return UserRegisterResponse(message="Usuário criado com sucesso.", status_code=status.HTTP_200_OK)


@router.post("/login", response_model=TokenSchema)
def login(request: RequestDetails, session: Session = Depends(get_session)):
    """
    Authenticates a user and generates access and refresh tokens.

    - **request**: The login details provided by the user.
    - **session**: The database session dependency.

    Returns:
    - A message indicating the success of the login process along with access and refresh tokens.

    Raises:
    - **400 Bad Request**: If the email or password is incorrect.
    """
    logger.info("Tentativa de login para o email: %s", request.email)

    user = session.query(User).filter(User.email == request.email).first()

    if user is None:
        logger.warning(
            "Tentativa de login com email incorreto: %s", request.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email incorreto."
        )

    hashed_password = user.password

    if not verify_password(request.password, hashed_password):
        logger.warning("Senha incorreta para o email: %s", request.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Senha incorreta."
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    token_record = TokenTable(
        user_id=user.id, access_token=access_token, refresh_token=refresh_token, status=True
    )

    session.add(token_record)
    session.commit()
    session.refresh(token_record)

    logger.info("Login bem-sucedido para o email: %s", request.email)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", response_model=LogoutResponse)
def logout(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    """
    Logs out a user by invalidating their access token.

    - **token**: JWTBearer dependency to authenticate the user.
    - **session**: The database session dependency.

    Returns:
    - A message indicating the success of the logout process.

    Raises:
    - **401 Unauthorized**: If the token is invalid.
    """
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]

    logger.info("Tentativa de logout para o usuário ID: %s", user_id)

    # Fetch all tokens and check if any are older than 1 day
    all_tokens = session.query(TokenTable).all()
    expired_tokens_user_ids = []

    for record in all_tokens:
        logger.debug("Verificando token com data de criação: %s",
                     record.created_date)
        current_utc_time = datetime.datetime.utcnow()

        if (current_utc_time - record.created_date).days > 1:
            expired_tokens_user_ids.append(record.user_id)

    if expired_tokens_user_ids:
        session.query(TokenTable).filter(
            TokenTable.user_id.in_(expired_tokens_user_ids)
        ).delete()
        session.commit()
        logger.info(
            "Tokens expirados removidos para os IDs de usuário: %s", expired_tokens_user_ids)

    existing_token = session.query(TokenTable).filter(
        TokenTable.user_id == user_id, TokenTable.access_token == token
    ).first()

    if existing_token:
        existing_token.status = False
        session.add(existing_token)
        session.commit()
        session.refresh(existing_token)

    logger.info("Logout bem-sucedido para o usuário ID: %s", user_id)
    return LogoutResponse(message="Logout feito com sucesso.", status_code=status.HTTP_200_OK)
