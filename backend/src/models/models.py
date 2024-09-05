from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import datetime


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for the user.
        username (str): The username of the user, must be unique and not null.
        email (str): The user's email, must be unique and not null.
        password (str): The user's password, stored as a hash, and cannot be null.
        balance (float): The user's balance, defaults to 1000.0.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    balance = Column(Float, default=1000.0)


class PixKey(Base):
    """
    Represents a Pix key associated with a user.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for the Pix key.
        key (str): The Pix key value, must be unique and not null.
        user_id (int): Foreign key to the user's ID, cannot be null.
        user (User): Relationship to the User model, linking a Pix key to a specific user.
    """
    __tablename__ = "pix_keys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])


class TokenTable(Base):
    """
    Represents tokens for authentication and session management.

    Attributes:
        user_id (int): Identifier for the user associated with the tokens.
        access_token (str): The access token, primary key for the table.
        refresh_token (str): The refresh token, cannot be null.
        status (bool): The status of the token, indicating if it is active.
        created_date (datetime): The date and time when the token was created, defaults to the current date and time.
    """
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)


class Transaction(Base):
    """
    Represents a transaction between two users.

    Attributes:
        id (int): Primary key, auto-incremented identifier for the transaction.
        sender_id (int): Key to the sender's user ID, cannot be null.
        receiver_id (int): Key to the receiver's user ID, cannot be null.
        amount (float): The amount of the transaction, cannot be null.
        timestamp (datetime): The date and time of the transaction, defaults to the current UTC time.
    """
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
