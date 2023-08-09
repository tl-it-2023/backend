from src.database import Base

from sqlalchemy.orm import (Mapped,
                            mapped_column)

from sqlalchemy import String


class Temp(Base):
    __tablename__ = "temp"
    id: Mapped[int] = mapped_column(primary_key=True)
    temp: Mapped[str] = mapped_column(String())