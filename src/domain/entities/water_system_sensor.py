from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MeasureUnit(str, Enum):
    CELSIUS = "Celcius"
    NTU = "NTU"
    MG_L = "mg/L"
    US_CM = "µS/cm"
    NONE = ""

class SensorType(str, Enum):
    TEMPERATURE = "temperature"
    PH = "ph"
    TURBIDITY = "turbidity"
    DISSOLVED_OXYGEN = "dissolvedOxygen"
    CONDUCTIVITY = "conductivity"


class WaterSystemSensor(BaseModel):
    """Modelo para sensores virtuais associados ao sistema físico."""
    sensor_id: str = Field(..., description="Identificador único do sensor", min_length=1)
    sensor_type: SensorType = Field(..., description="Tipo do sensor (ex.: pH, temperatura)")
    unit: MeasureUnit = Field(..., description="Unidade de medida (ex.: °C, ppm)")
    mean_value: Optional[float] = Field(None, description="Valor médio do sensor dentro intervalo de twinning")
    min_value: Optional[float] = Field(None, description="Valor mínimo registrado pelo sensor dentro do intervalo de twinning")
    max_value: Optional[float] = Field(None, description="Valor máximo registrado pelo sensor dentro do intervalo de twinning")
    last_value: Optional[float] = Field(None, description="Último valor registrado pelo sensor dentro intervalo de twinning")
    last_value_date: Optional[datetime] = Field(None, description="Data/hora do último valor registrado")
    last_updated: Optional[datetime] = Field(None, description="Data/hora da última atualização")

    def update_value(self, value: float):
        """Atualiza o valor do sensor virtual."""
        self.last_value = value
        self.last_updated = datetime.now()
