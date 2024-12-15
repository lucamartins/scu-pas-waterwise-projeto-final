from src.domain.events.sensor_reading_event import SensorReadingEvent
from src.domain.repositories.sensor_reading_repository import SensorReadingsRepository
from src.logging_config import get_custom_logger


class EventService:
    def __init__(self):
        self.logger = get_custom_logger("EventService")
        self.sensor_reading_repository = SensorReadingsRepository()

    async def process_sensor_reading(self, sensor_reading: SensorReadingEvent):
        self.logger.info("Processing sensor reading...")
        await self.sensor_reading_repository.insert_sensor_reading(sensor_reading)
        self.logger.info("Sensor reading processed.")
