import os
from enum import Enum


class EnvEntry(Enum):
    MONGODB_CONNECTION_STRING = "MONGODB_CONNECTION_STRING"
    MONGODB_DATABASE_NAME = "MONGODB_DATABASE_NAME"
    MONGODB_SENSOR_READINGS_COLLECTION = "MONGODB_SENSOR_READINGS_COLLECTION"
    MONGODB_WATER_SYSTEMS_COLLECTION = "MONGODB_WATER_SYSTEMS_COLLECTION"
    MQTT_BROKER_URL = "MQTT_BROKER_URL"
    MQTT_BROKER_PORT = "MQTT_BROKER_PORT"
    MQTT_BROKER_CLIENT_ID = "MQTT_BROKER_CLIENT_ID"


class EnvConfig:
    @staticmethod
    def get(entry: EnvEntry) -> str:
        return os.getenv(entry.value)
