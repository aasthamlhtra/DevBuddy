from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text

class TechStack(Base):
    __tablename__ = "techstack"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category : Mapped[str] = mapped_column(String, nullable=False)
    description : Mapped[str] = mapped_column(Text)
    
