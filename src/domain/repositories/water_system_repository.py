from typing import List

from bson import ObjectId

from src.application.utils.object_util import ObjectUtil
from src.domain.entities.water_system import WaterSystem
from src.infrastructure.adapters.mongodb_adapter import MongoDBAdapter
from src.infrastructure.config.env_config import EnvConfig, EnvEntry


class WaterSystemRepository:
    def __init__(self):
        env_config = EnvConfig()
        collection_name = env_config.get(EnvEntry.MONGODB_WATER_SYSTEMS_COLLECTION)
        db = MongoDBAdapter().get_database()
        self.collection = db[collection_name]

    async def create_water_system(self, water_system: WaterSystem) -> str:
        """Insert a new WaterSystem into the database."""
        water_system_dict = ObjectUtil.remove_fields(water_system.model_dump(), ["id"])
        result = await self.collection.insert_one(water_system_dict)
        return str(result.inserted_id)

    async def get_water_system_by_id(self, water_system_id: str) -> WaterSystem:
        """Retrieve a WaterSystem by its ID."""
        water_system_dict = await self.collection.find_one({"_id": ObjectId(water_system_id)})
        water_system_dict["id"] = str(water_system_dict["_id"])
        del water_system_dict["_id"]
        water_system = WaterSystem.model_validate(water_system_dict)
        return water_system

    async def update_water_system(self, water_system_id: str, update_data: WaterSystem) -> int:
        """Update an existing WaterSystem."""
        update_object = ObjectUtil.remove_fields(update_data.model_dump(), ["id"])
        result = await self.collection.update_one(
            {"_id": ObjectId(water_system_id)}, {"$set": update_object}
        )
        return result.modified_count

    async def delete_water_system(self, water_system_id: str) -> int:
        """Delete a WaterSystem by its ID."""
        result = await self.collection.delete_one({"_id": ObjectId(water_system_id)})
        return result.deleted_count

    async def list_water_systems(self, filter_query=None) -> List[WaterSystem]:
        """List all WaterSystems that match a filter query."""
        filter_query = filter_query or {}
        cursor = self.collection.find(filter_query)
        water_systems_dict = await cursor.to_list(length=None)

        for ws in water_systems_dict:
            ws["id"] = str(ws["_id"])
            del ws["_id"]

        water_systems = [WaterSystem.model_validate(ws) for ws in water_systems_dict]
        return water_systems
