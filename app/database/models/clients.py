from datetime import date
from typing import TYPE_CHECKING

from database.database import BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

if TYPE_CHECKING:
    from models.buys import Buy


class City(BaseModel):
    """Модель городов"""

    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_city: Mapped[str] = mapped_column(String(250))
    days_delivery: Mapped[date]

    clients: Mapped[list["Client"]] = relationship(back_populates="city")

    @validates("days_delivery")
    def validate_days_delivery(self, key, value):
        today = date.today()
        if value < today:
            raise ValueError("Дата доставки не должно быть меньше текущей")
        return value


class Client(BaseModel):
    """Модель клиентов"""

    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    name_client: Mapped[str] = mapped_column(String(250), index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
    email: Mapped[str] = mapped_column(String(250), unique=True)

    city: Mapped[City] = relationship(back_populates="clients")
    buys: Mapped[list["Buy"]] = relationship(back_populates="client")
