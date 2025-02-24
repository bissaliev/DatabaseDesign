from decimal import Decimal
from typing import TYPE_CHECKING

from database.database import BaseModel
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

if TYPE_CHECKING:
    pass


class Genre(BaseModel):
    """Модель жанров"""

    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_genre: Mapped[str] = mapped_column(String(250), index=True)

    books: Mapped[list["Book"]] = relationship(back_populates="genre")


class Author(BaseModel):
    """Модель авторов"""

    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    name_author: Mapped[str] = mapped_column(String(250), index=True)

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(BaseModel):
    """Модель книг"""

    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id"))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    amount: Mapped[int]

    author: Mapped[Author] = relationship(back_populates="books")
    genre: Mapped[Genre] = relationship(back_populates="books")

    @validates("amount")
    def validate_amount(self, key, value):
        if value < 0:
            raise ValueError("Количество не должно быть меньше нуля")
        return value
