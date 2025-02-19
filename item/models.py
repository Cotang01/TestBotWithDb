from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from db.base import Base


class Item(Base):
    __tablename__ = "item"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    data: Mapped[String] = mapped_column(String(255))

    def __str__(self):
        return f"{self.id} {self.data}"
