from typing import Optional, List

from pydantic import Field, BaseModel

from src.domain.entities.water_system import WaterSystemType
from src.domain.entities.water_system_sensor import WaterSystemSensor


class WaterSystemCreateUpdateRequest(BaseModel):
    name: str = Field(...)
    location: Optional[str] = Field(None)
    capacity: Optional[float] = Field(None)
    system_type: WaterSystemType = Field(...)
    sensors: List[WaterSystemSensor] = Field(default_factory=lambda: list)
    status: Optional[str] = Field("online")
