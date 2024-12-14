from typing import Callable, Any

import paho.mqtt.client as mqtt
import paho.mqtt.enums as mqtt_enums
from pydantic import BaseModel, Field

from src.logging_config import get_custom_logger


class MQTTConfig(BaseModel):
    broker_url: str = Field(..., description="URL do broker MQTT")
    broker_port: int = Field(..., gt=0, description="Porta do broker MQTT")
    client_id: str = Field(..., description="ID único do cliente MQTT")


class MQTTBrokerAdapter:
    def __init__(self, config: MQTTConfig):
        """
        Inicializa o adaptador MQTT.
        :param config: Configuração para o MQTT.
        """
        self.logger = get_custom_logger("MQTTBrokerAdapter")
        self.config = config
        self.client = mqtt.Client(mqtt_enums.CallbackAPIVersion(2))

        # Dicionário para armazenar handlers associados a tópicos
        self.handlers = {}

        # Configura os callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc, properties):
        """Callback chamado ao conectar ao broker."""
        if rc == 0:
            self.logger.info("Conectado ao broker com sucesso!")
            # Assina todos os tópicos previamente registrados
            for topic in self.handlers.keys():
                self.client.subscribe(topic)
                self.logger.info(f"Tópico registrado automaticamente: {topic}")
        else:
            self.logger.info(f"Erro ao conectar ao broker, código: {rc}")

    def _on_message(self, client, userdata, msg):
        """Callback chamado quando uma mensagem é recebida."""
        handler = self.handlers.get(msg.topic)
        if handler:
            # Chama o handler associado ao tópico
            handler(msg.topic, msg.payload.decode())
        else:
            self.logger.warning(f"Mensagem recebida sem handler associado: {msg.topic}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback chamado ao desconectar do broker."""
        self.logger.info("Desconectado do broker MQTT.")

    def register_handler(self, topic: str, handler: Callable[[str, Any], None]):
        """
        Registra um handler para um tópico específico.
        :param topic: O tópico para o qual o handler será associado.
        :param handler: Uma função que processará as mensagens do tópico.
        """
        self.handlers[topic] = handler
        self.logger.info(f"Handler registrado para o tópico: {topic}")
        if self.client.is_connected():
            self.client.subscribe(topic)
            self.logger.info(f"Tópico {topic} assinado.")

    def connect(self):
        """
        Conecta ao broker MQTT.
        """
        self.client.connect(self.config.broker_url, self.config.broker_port)
        self.logger.info("Conectando ao broker MQTT...")

    def start(self):
        """
        Inicia o loop para processar mensagens.
        """
        self.client.loop_start()
        self.logger.info("Loop MQTT iniciado.")

    def stop(self):
        """
        Para o loop e desconecta do broker.
        """
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Loop MQTT parado e cliente desconectado.")
