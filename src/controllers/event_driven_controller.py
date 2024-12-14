from src.infrastructure.adapters.mqtt_broker_adapter import MQTTBrokerAdapter, MQTTConfig


class EventDrivenController:
    def __init__(self):
        mqtt_config = MQTTConfig(broker_url="123", broker_port=3030, client_id="123")
        self.mqtt_broker = MQTTBrokerAdapter(mqtt_config)

