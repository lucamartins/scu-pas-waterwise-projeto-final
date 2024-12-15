from datetime import datetime, timezone, timedelta
from typing import List

import pandas

from src.domain.entities.water_system import WaterSystem
from src.domain.events.sensor_reading_event import SensorReadingEvent
from src.domain.repositories.sensor_reading_repository import SensorReadingRepository, SensorReadingsQuery
from src.domain.repositories.water_system_repository import WaterSystemRepository
from src.infrastructure.config.env_config import EnvConfig, EnvEntry
from src.logging_config import get_custom_logger


class ProcessingPipelineService:
    def __init__(self):
        env_config = EnvConfig()
        self.logger = get_custom_logger(ProcessingPipelineService.__name__)
        self.sensor_reading_repository = SensorReadingRepository()
        self.water_system_repository = WaterSystemRepository()
        self.default_water_system_id = env_config.get(EnvEntry.DEFAULT_WATER_SYSTEM_ID)

    def process_water_system_twinning_window_readings(self, water_system: WaterSystem, sensor_readings: List[SensorReadingEvent]):
        if len(sensor_readings) == 0:
            self.logger.warning(f"No sensor readings for within last twinning window for Water System {water_system.id}")
            return

        readings_raw_data = [r.model_dump() for r in sensor_readings]
        dataframe = pandas.DataFrame(readings_raw_data)
        dataframe["create_date"] = pandas.to_datetime(dataframe["create_date"])
        dataframe = dataframe.sort_values(by=["sensor_id", "create_date"])

        sensors_statistics = dataframe.groupby("sensor_id").agg(
            mean_value=("value", "mean"),
            min_value=("value", "min"),
            max_value=("value", "max"),
            last_value=("value", "last"),
            last_value_date=("create_date", "last")
        )

        for sensor_id, row in sensors_statistics.iterrows():
            water_system_sensor = next((sensor for sensor in water_system.sensors if sensor.sensor_id == sensor_id), None)

            if not water_system_sensor:
                self.logger.warning(f"Found no matching Water System sensor for twinning.\n"
                                    f"Details: Water System ID = {water_system.id}, Sensor ID = {sensor_id}")
                return

            water_system_sensor.mean_value = row["mean_value"]
            water_system_sensor.min_value = row["min_value"]
            water_system_sensor.max_value = row["max_value"]
            water_system_sensor.last_value = row["last_value"]
            water_system_sensor.last_value_date = row["last_value_date"]
            water_system_sensor.last_updated = datetime.now(timezone.utc)

    async def run(self):
        self.logger.info("Processing pipeline triggered")

        monitored_water_systems = await self.water_system_repository.list_water_systems({ "status": "online" })
        for water_system in monitored_water_systems:
            sensor_readings_query = SensorReadingsQuery(
                water_system_id=water_system.id,
                start_date=datetime.now(tz=timezone.utc) + timedelta(seconds=-water_system.twinning_rate_seconds)
            )
            sensor_readings = await self.sensor_reading_repository.find_readings(sensor_readings_query)
            self.process_water_system_twinning_window_readings(water_system, sensor_readings)
            await self.water_system_repository.update_water_system(water_system.id, water_system)
