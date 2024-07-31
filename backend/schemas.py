from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class RequestDetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TransactionCreate(BaseModel):
    sender_pix_key: str
    receiver_pix_key: str
    amount: float


class PixKeyCreate(BaseModel):
    key: str


class PixKeyResponse(BaseModel):
    id: int
    key: str
    user_id: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    balance: float
