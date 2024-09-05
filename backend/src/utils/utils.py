from functools import wraps
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt
from database.database import SessionLocal
from models.models import TokenTable

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    """
    Creates a new database session.

    Yields:
        Session: A new database session.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def token_required(func):
    """
    Decorator that checks if the provided token is valid and not blocked.

    Args:
        func (callable): The function to wrap with token validation.

    Returns:
        callable: The wrapped function with token validation.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.get("dependencies")
        session = kwargs.get("session")
        
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["sub"]
        token_record = (
            session.query(TokenTable)
            .filter_by(user_id=user_id, access_token=token, status=True)
            .first()
        )
        
        if token_record:
            return func(*args, **kwargs)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token blocked or invalid.",
            )

    return wrapper


def get_hashed_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies that the provided password matches the hashed password.

    Args:
        password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return password_context.verify(password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Creates an access token with an expiration time.

    Args:
        subject (Union[str, Any]): The subject for which the token is created (typically user ID).
        expires_delta (int, optional): The expiration time in minutes for the token.

    Returns:
        str: The generated JWT access token.
    """
    current_utc_time = datetime.now(timezone.utc)
    expires_delta = current_utc_time + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Creates a refresh token with an expiration time.

    Args:
        subject (Union[str, Any]): The subject for which the token is created (typically user ID).
        expires_delta (int, optional): The expiration time in minutes for the refresh token.

    Returns:
        str: The generated JWT refresh token.
    """
    current_utc_time = datetime.now(timezone.utc)
    expires_delta = current_utc_time + (expires_delta if expires_delta else timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
