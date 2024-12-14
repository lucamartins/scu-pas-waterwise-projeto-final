from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.domain.entities.water_system_sensor import WaterSystemSensor


class WaterSystemType(str, Enum):
    RESERVOIR = "reservoir"
    TREATMENT = "treatment"


class WaterSystem(BaseModel):
    """Gêmeo Digital do sistema físico de água."""
    id: str = Field(None, description="Identificador único do gêmeo digital")
    name: str = Field(..., description="Nome do sistema físico representado")
    location: Optional[str] = Field(None, description="Localização do sistema físico")
    capacityCubicMeters: Optional[float] = Field(None, description="Capacidade total (em litros ou metros cúbicos)")
    system_type: WaterSystemType = Field(..., description="Tipo do sistema físico (ex.: reservatório, tratamento)")
    status: str = Field("online", description="Estado atual do sistema (online/offline/manutenção)")
    sensors: List[WaterSystemSensor] = Field(default_factory=lambda: list, description="Lista de sensores atrelados")

    # Simulação e Interatividade
    def add_sensor(self, sensor: WaterSystemSensor):
        """Adiciona um sensor virtual ao gêmeo digital."""
        self.sensors.append(sensor)

    def update_sensor_value(self, sensor_id: str, value: float):
        """Atualiza o valor de um sensor específico."""
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.update_value(value)
                return
