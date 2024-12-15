from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.application.utils.object_util import ObjectUtil
from src.domain.events.sensor_reading_event import SensorReadingEvent
from src.infrastructure.adapters.mongodb_adapter import MongoDBAdapter
from src.infrastructure.config.env_config import EnvConfig, EnvEntry


class SensorReadingsRepository:
    def __init__(self):
        env_config = EnvConfig()
        collection_name = env_config.get(EnvEntry.MONGODB_SENSOR_READINGS_COLLECTION)
        self.db = MongoDBAdapter().get_database()
        self.collection: AsyncIOMotorCollection = self.db[collection_name]

    def create_time_series_collection(self):
        """Cria a coleção como time-series, caso ainda não exista."""
        if "sensorReadings" not in self.db.list_collection_names():
            self.db.create_collection(
                "sensorReadings",
                timeseries={
                    "timeField": "create_date",
                    "metaField": "sensor_id",
                    "granularity": "seconds"
                }
            )

    async def insert_sensor_reading(self, sensor_reading: SensorReadingEvent) -> str:
        """Insere uma nova leitura de sensor."""
        sensor_reading_dict = ObjectUtil.remove_fields(sensor_reading.model_dump(), ["id"])
        result = await self.collection.insert_one(sensor_reading_dict)
        return str(result.inserted_id)

    async def find_readings_by_sensor(self, sensor_id: str, start_date: datetime = None, end_date: datetime = None) -> List[SensorReadingEvent]:
        """Busca leituras por sensor em um intervalo de tempo opcional."""
        query = {"sensor_id": sensor_id}
        if start_date:
            query["create_date"] = {"$gte": start_date}
        if end_date:
            query["create_date"] = query.get("create_date", {})
            query["create_date"]["$lte"] = end_date

        readings = []
        async for reading in self.collection.find(query):
            reading["id"] = str(reading["_id"])
            del reading["_id"]
        return [SensorReadingEvent.model_validate(reading) for reading in readings]

    async def delete_reading_by_id(self, reading_id: str) -> bool:
        """Remove uma leitura específica pelo ID."""
        result = await self.collection.delete_one({"_id": ObjectId(reading_id)})
        return result.deleted_count > 0
