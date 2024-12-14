import os
from enum import Enum


class EnvEntry(Enum):
    MONGODB_CONNECTION_STRING = "MONGODB_CONNECTION_STRING"
    MONGODB_DATABASE_NAME = "MONGODB_DATABASE_NAME"


class EnvConfig:
    @staticmethod
    def get(entry: EnvEntry) -> str:
        return os.getenv(entry.value)
