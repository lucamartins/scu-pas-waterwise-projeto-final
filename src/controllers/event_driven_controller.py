from src.infrastructure.adapters.mqtt_broker_adapter import MQTTBrokerAdapter, MQTTConfig
from src.logging_config import get_custom_logger


class EventDrivenController:
    def __init__(self):
        mqtt_config = MQTTConfig(broker_url="localhost", broker_port=1883, client_id="1")
        self.mqtt_broker = MQTTBrokerAdapter(mqtt_config)
        self.logger = get_custom_logger("EventDrivenController")

    def _handler(self, topic: str, payload: str):
        self.logger.info(f"Received message on topic {topic}: {payload}")

    def start(self):
        self.mqtt_broker.register_handler("waterwise/temperature", self._handler)
        self.mqtt_broker.connect()
        self.mqtt_broker.start()

    def stop(self):
        self.mqtt_broker.stop()
