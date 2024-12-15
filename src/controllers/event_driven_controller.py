import asyncio
import json

from tenacity import retry, wait_fixed

from src.application.services.event.event_service import EventService
from src.domain.events.sensor_reading_event import SensorReadingEvent
from src.infrastructure.adapters.mqtt_broker_adapter import MQTTBrokerAdapter, MQTTConfig
from src.infrastructure.config.env_config import EnvConfig, EnvEntry
from src.logging_config import get_custom_logger


class EventDrivenController:
    def __init__(self):
        env_config = EnvConfig()
        mqtt_config = MQTTConfig(
            broker_url=env_config.get(EnvEntry.MQTT_BROKER_URL),
            broker_port=int(env_config.get(EnvEntry.MQTT_BROKER_PORT)),
            client_id=env_config.get(EnvEntry.MQTT_BROKER_CLIENT_ID)
        )
        self.mqtt_broker = MQTTBrokerAdapter(mqtt_config)
        self.mqtt_broker.set_event_loop(asyncio.get_event_loop())
        self.logger = get_custom_logger(EventDrivenController.__name__)
        self.event_service = EventService()

    async def _handler(self, topic: str, payload: str):
        try:
            payload_dict = json.loads(payload)
            sensor_reading_event = SensorReadingEvent.model_validate(payload_dict)
            await self.event_service.process_sensor_reading(sensor_reading_event)
        except Exception as e:
            self.logger.error(f"Error when handling event: {e}")

    @retry(wait=wait_fixed(60))
    def start(self):
        try:
            self.mqtt_broker.register_handler("waterwise/+", self._handler)
            self.mqtt_broker.connect()
            self.mqtt_broker.start()
        except Exception as e:
            self.logger.error(f"Error when starting MQTT Broker: {e}")
            self.logger.error("Retrying in 60 seconds...")
            raise

    def stop(self):
        self.mqtt_broker.stop()
