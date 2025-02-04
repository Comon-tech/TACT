import os
from typing import ClassVar

import dotenv
from pydantic import BaseModel, PositiveInt, PrivateAttr
from pymongo import MongoClient
from pymongo.collection import Collection

from pyproject import PROJECT

dotenv.load_dotenv()


# ----------------------------------------------------------------------------------------------------
# * Model
# ----------------------------------------------------------------------------------------------------
class Model(BaseModel):
    _database: ClassVar = MongoClient(os.getenv("MONGO_URI"))[PROJECT["name"]]
    _collection: ClassVar[Collection]

    @classmethod
    def load(cls, id: int):
        return cls(
            **cls._collection.find_one_and_update(
                {"id": id},
                {"$setOnInsert": {"id": id}},
                upsert=True,
                return_document=True,
            )
        )

    def save(self):
        return self._collection.update_one(
            {"id": self.id}, {"$set": self.model_dump()}, upsert=True
        )
