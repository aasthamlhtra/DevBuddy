from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, TIMESTAMP, DateTime, text
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, time
from typing import List
from .conversation import Conversation
 
class User(Base):
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    username : Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email : Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(30), nullable=False)
    bio : Mapped[str] = mapped_column(Text)
    primary_tech_stack : Mapped[str] = mapped_column(String(100))
    learning_tech_stack : Mapped[str] = mapped_column(String(100))
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"))
    # conversations : Mapped[List["Conversation"]] 