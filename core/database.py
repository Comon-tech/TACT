import os
from abc import ABC
from typing import ClassVar, Collection, Self, TypeVar

import dotenv
from colorama import Fore
from pydantic import BaseModel, ValidationError
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Collection, Database
from pymongo.results import UpdateResult

from pyproject import PROJECT


# ----------------------------------------------------------------------------------------------------
# * Database
# ----------------------------------------------------------------------------------------------------
def get_database(name: str):
    dotenv.load_dotenv()
    database = MongoClient(os.getenv("MONGO_URI")).get_database(name)
    host, port = database.client.address
    server_info = database.client.server_info()
    ver = server_info.get("version", "?")
    bits = server_info.get("bits", "?")
    print(
        f"{Fore.GREEN}[🌍{host}:{port}] 📀 MongoDB v{ver}-{bits}bits {name} database connected.{Fore.RESET}\n"
    )
    return database


# ----------------------------------------------------------------------------------------------------
# * Abstract Database Model
# ----------------------------------------------------------------------------------------------------
class DatabaseModel(BaseModel, ABC):
    DATABASE: ClassVar[Database]

    @classmethod
    def __init_subclass__(cls, database_name: str, **kwargs):
        cls.DATABASE = get_database(database_name)
        return super().__init_subclass__(**kwargs)


# ----------------------------------------------------------------------------------------------------
# * Model
# ----------------------------------------------------------------------------------------------------
TModel = TypeVar("TModel", bound="Model")


class Model(DatabaseModel, database_name=PROJECT["name"]):
    COLLECTION: ClassVar[Collection]

    @classmethod
    def __init_subclass__(cls, collection_name: str, **kwargs):
        cls.COLLECTION = cls.DATABASE.get_collection(collection_name)

    @classmethod
    def create(cls, data: dict) -> Self | None:
        """Creates an instance of the model with the provided data. Returns None if error."""
        try:
            if not data:
                return None
            return cls(**data)
        except ValidationError as e:
            print("⛔", e)

    @classmethod
    def load(cls, id: int) -> Self | None:
        """Loads an instance of the model from the database using the specified ID. Returns None if error."""
        try:

            return cls(
                **cls.COLLECTION.find_one_and_update(
                    {"id": id},
                    {"$setOnInsert": {"id": id}},
                    upsert=True,
                    return_document=ReturnDocument.AFTER,
                )
            )
        except Exception as e:
            print("⛔", e)

    def save(self) -> UpdateResult | None:
        """Saves the current instance to the database. Returns None if error."""
        try:
            return self.COLLECTION.update_one(
                {"id": self.id}, {"$set": self.model_dump()}, upsert=True
            )
        except Exception as e:
            print("⛔", e)
