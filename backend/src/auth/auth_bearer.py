import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.utils import JWT_SECRET_KEY, ALGORITHM


def decode_jwt(token: str):
    """
    Decodes a JWT token to extract the payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload if the token is valid.
        None: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None


class JWTBearer(HTTPBearer):
    """
    A custom HTTP bearer authentication class that validates JWT tokens.
    """

    def __init__(self, auto_error: bool = True):
        """
        Initializes the JWTBearer class.

        Args:
            auto_error (bool): Whether to automatically throw an error if authentication fails. Defaults to True.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Processes the HTTP request to extract and validate the JWT token.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            str: The JWT token if it is valid.

        Raises:
            HTTPException: If the authentication scheme is invalid or the token is invalid or expired.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme",
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code",
            )

    def verify_jwt(self, token: str) -> bool:
        """
        Verifies the validity of a JWT token.

        Args:
            token (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        is_token_valid: bool = False

        try:
            payload = decode_jwt(token)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


jwt_bearer = JWTBearer()
