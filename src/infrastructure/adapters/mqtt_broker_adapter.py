import asyncio
from typing import Callable, Any, Coroutine

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
        self.logger = get_custom_logger(MQTTBrokerAdapter.__name__)
        self.config = config
        self.client = mqtt.Client(mqtt_enums.CallbackAPIVersion(2))

        # Dicionário para armazenar handlers associados a tópicos
        self.handlers = {}
        self.event_loop = None

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
        self.logger.info(f"New message received on topic {msg.topic}")
        matched = False
        for pattern, handler in self.handlers.items():
            if self.matches_topic(pattern, msg.topic):
                try:
                    asyncio.run_coroutine_threadsafe(handler(msg.topic, msg.payload.decode()), self.event_loop)
                except Exception as e:
                    self.logger.error(f"Failure when sending message from MQTT thread to event loop: {e}")
                matched = True
                break

        if not matched:
            self.logger.warning(f"Received message with no related handler on topic {msg.topic}: {msg.payload.decode()}")

    def _on_disconnect(self, client, userdata, df, rc, p):
        """Callback chamado ao desconectar do broker."""
        self.logger.info("Desconectado do broker MQTT.")

    def set_event_loop(self, event_loop):
        """
        Define o event loop para o adaptador.
        :param event_loop: Event loop a ser definido.
        """
        self.event_loop = event_loop

    def register_handler(self, topic: str, handler: Callable[[str, str], Coroutine[Any, Any, None]]):
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

    @staticmethod
    def matches_topic(pattern, topic):
        """
        Verifica se o tópico recebido corresponde ao padrão MQTT.
        :param pattern: Padrão MQTT (pode incluir + e #)
        :param topic: Tópico recebido
        :return: True se corresponder, False caso contrário
        """
        pattern_parts = pattern.split('/')
        topic_parts = topic.split('/')

        for i, part in enumerate(pattern_parts):
            if part == '#':
                # '#' corresponde a todos os níveis restantes
                return True
            if part == '+':
                # '+' corresponde exatamente a um nível
                if i >= len(topic_parts):
                    return False
            elif i >= len(topic_parts) or part != topic_parts[i]:
                return False

        return len(pattern_parts) == len(topic_parts)
