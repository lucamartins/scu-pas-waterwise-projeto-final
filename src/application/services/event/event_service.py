from datetime import timezone, timedelta

from src.domain.events.sensor_reading_event import SensorReadingEvent
from src.domain.repositories.sensor_reading_repository import SensorReadingRepository
from src.infrastructure.config.env_config import EnvConfig, EnvEntry
from src.logging_config import get_custom_logger


class EventService:
    def __init__(self):
        env_config = EnvConfig()
        self.logger = get_custom_logger(EventService.__name__)
        self.sensor_reading_repository = SensorReadingRepository()
        self.default_water_system_id = env_config.get(EnvEntry.DEFAULT_WATER_SYSTEM_ID)

    async def process_sensor_reading(self, sensor_reading: SensorReadingEvent):
        if sensor_reading.water_system_id is None:
            sensor_reading.water_system_id = self.default_water_system_id

        utc_minus_3 = timezone(timedelta(hours=-3))
        sensor_reading.create_date = sensor_reading.create_date.replace(tzinfo=utc_minus_3)

        inserted_id = await self.sensor_reading_repository.insert_sensor_reading(sensor_reading)
        self.logger.info(f"Successfully processed sensor reading ({inserted_id}): "
                         f"Water System = {sensor_reading.water_system_id}, "
                         f"Sensor = {sensor_reading.sensor_id} ({sensor_reading.sensor.value}), "
                         f"Value = {sensor_reading.value} {sensor_reading.measure_unit.value}")
