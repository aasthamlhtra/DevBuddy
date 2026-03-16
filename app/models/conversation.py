from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Integer, String, Text, TIMESTAMP, DateTime, text
from ..database import Base
from datetime import datetime, time

class Conversation(Base):
    __tablename__ = "conversation"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id : Mapped[int] = mapped_column(Integer)