from pydantic import BaseModel


class UserRegisterResponse(BaseModel):
    """
    Schema for the response of user registration.

    Attributes:
        message (str): A message indicating the result of the registration process.
        status_code (int): The HTTP status code of the registration response.
    """
    message: str
    status_code: int


class LogoutResponse(BaseModel):
    """
    Schema for the response of user logout.

    Attributes:
        message (str): A message indicating the result of the logout process.
        status_code (int): The HTTP status code of the logout response.
    """
    message: str
    status_code: int


class PixKeyCreateResponse(BaseModel):
    """
    Schema for the response when creating a new Pix key.

    Attributes:
        message (str): A message indicating the result of the Pix key creation.
        pix_key (str): The created Pix key value.
        status_code (int): The HTTP status code of the Pix key creation response.
    """
    message: str
    pix_key: str
    status_code: int


class TransactionCreateResponse(BaseModel):
    """
    Schema for the response when creating a new transaction.

    Attributes:
        message (str): A message indicating the result of the transaction creation.
        transaction_id (int): The unique identifier of the created transaction.
        status_code (int): The HTTP status code of the transaction creation response.
    """
    message: str
    transaction_id: int
    status_code: int


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): The username of the new user.
        email (str): The email of the new user.
        password (str): The password of the new user.
    """
    username: str
    email: str
    password: str


class RequestDetails(BaseModel):
    """
    Schema for user login request details.

    Attributes:
        email (str): The email of the user trying to log in.
        password (str): The password of the user trying to log in.
    """
    email: str
    password: str


class TokenSchema(BaseModel):
    """
    Schema for the access and refresh tokens.

    Attributes:
        access_token (str): The JWT access token for the user.
        refresh_token (str): The JWT refresh token for the user.
    """
    access_token: str
    refresh_token: str


class TransactionCreate(BaseModel):
    """
    Schema for creating a new transaction.

    Attributes:
        sender_pix_key (str): The Pix key of the sender.
        receiver_pix_key (str): The Pix key of the receiver.
        amount (float): The amount of the transaction.
    """
    sender_pix_key: str
    receiver_pix_key: str
    amount: float


class PixKeyCreate(BaseModel):
    """
    Schema for creating a new Pix key.

    Attributes:
        key (str): The Pix key to be created.
    """
    key: str


class PixKeyResponse(BaseModel):
    """
    Schema for the response when retrieving Pix key details.

    Attributes:
        id (int): The unique identifier of the Pix key.
        key (str): The Pix key value.
        user_id (int): The ID of the user associated with the Pix key.
    """
    id: int
    key: str
    user_id: int


class UserResponse(BaseModel):
    """
    Schema for the response when retrieving user details.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        balance (float): The current balance of the user.
    """
    id: int
    username: str
    email: str
    balance: float
