from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from src.application.utils.object_util import ObjectUtil
from src.domain.events.sensor_reading_event import SensorReadingEvent
from src.infrastructure.adapters.mongodb_adapter import MongoDBAdapter
from src.infrastructure.config.env_config import EnvConfig, EnvEntry


class SensorReadingsQuery(BaseModel):
    water_system_id: str = None
    sensor_id: str = None
    start_date: datetime = None
    end_date: datetime = None


class SensorReadingRepository:
    def __init__(self):
        env_config = EnvConfig()
        collection_name = env_config.get(EnvEntry.MONGODB_SENSOR_READINGS_COLLECTION)
        self.db = MongoDBAdapter().get_database()
        self.collection: AsyncIOMotorCollection = self.db[collection_name]

    async def insert_sensor_reading(self, sensor_reading: SensorReadingEvent) -> str:
        """Insere uma nova leitura de sensor."""
        sensor_reading_dict = ObjectUtil.remove_fields(sensor_reading.model_dump(), ["id"])
        result = await self.collection.insert_one(sensor_reading_dict)
        return str(result.inserted_id)

    async def find_readings(self, query: SensorReadingsQuery) -> List[SensorReadingEvent]:
        """Busca leituras por sensor em um intervalo de tempo opcional."""
        mongo_query = {}
        if query.sensor_id:
            mongo_query["sensor_id"] = query.sensor_id
        if query.water_system_id:
            mongo_query["water_system_id"] = query.water_system_id
        if query.start_date:
            mongo_query["create_date"] = {"$gte": query.start_date}
        if query.end_date:
            mongo_query["create_date"] = mongo_query.get("create_date", {})
            mongo_query["create_date"]["$lte"] = query.end_date

        cursor = self.collection.find(mongo_query)
        readings = []
        async for reading in cursor:
            readings.append(SensorReadingEvent(**reading, id=str(reading["_id"])))
        return readings

    async def delete_reading_by_id(self, reading_id: str) -> bool:
        """Remove uma leitura específica pelo ID."""
        result = await self.collection.delete_one({"_id": ObjectId(reading_id)})
        return result.deleted_count > 0
