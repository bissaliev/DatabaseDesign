from datetime import date
from typing import TYPE_CHECKING

from database.database import BaseModel
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.books import Book
    from models.clients import Client


class BuyBook(BaseModel):
    """Модель позиций покупок"""

    __tablename__ = "buy_books"
    __table_args__ = (
        UniqueConstraint("buy_id", "book_id", name="unique_buy_book"),
    )

    buy_book_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    buy_id: Mapped[int] = mapped_column(ForeignKey("buys.buy_id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"))
    amount: Mapped[int] = mapped_column(default=1, server_default="1")

    buy: Mapped["Buy"] = relationship(back_populates="items")
    book: Mapped["Book"] = relationship()


class Buy(BaseModel):
    """Модель покупок"""

    __tablename__ = "buys"

    buy_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    buy_description: Mapped[str] = mapped_column(Text)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"))

    client: Mapped["Client"] = relationship(back_populates="buys")
    items: Mapped[list["BuyBook"]] = relationship(back_populates="buy")
    steps: Mapped[list["Step"]] = relationship(
        secondary="buy_steps", back_populates="buys"
    )


class Step(BaseModel):
    """Модель этапов обработки заказа"""

    __tablename__ = "steps"

    step_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_step: Mapped[str] = mapped_column(String(150))

    buys: Mapped[list["Buy"]] = relationship(
        secondary="buy_steps", back_populates="steps"
    )


class BuyStep(BaseModel):
    __tablename__ = "buy_steps"

    buy_step_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    buy_id: Mapped[int] = mapped_column(ForeignKey("buys.buy_id"))
    step_id: Mapped[int] = mapped_column(ForeignKey("steps.step_id"))
    date_step_beg: Mapped[date] = mapped_column(
        server_default=func.now(), default=date.today()
    )
    date_step_end: Mapped[date | None]
