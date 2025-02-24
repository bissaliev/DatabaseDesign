from database.database import BaseModel, engine
from database.models.books import Author, Book  # noqa: F401
from database.models.buys import Buy, BuyBook, BuyStep  # noqa: F401
from database.models.clients import City, Client  # noqa: F401

print(BaseModel.metadata.tables.keys())

BaseModel.metadata.create_all(bind=engine)
