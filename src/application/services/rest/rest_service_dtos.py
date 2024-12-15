from typing import Optional, List

from pydantic import Field, BaseModel, field_validator

from src.domain.entities.water_system import WaterSystemType
from src.domain.entities.water_system_sensor import WaterSystemSensor


class WaterSystemCreateUpdateRequest(BaseModel):
    name: str = Field(...)
    location: Optional[str] = Field(None)
    capacity: Optional[float] = Field(None)
    system_type: WaterSystemType = Field(...)
    sensors: List[WaterSystemSensor] = Field(default_factory=lambda: list)
    status: Optional[str] = Field("online")
    twinning_rate_seconds: Optional[int] = Field(60)

    @classmethod
    @field_validator("twinning_rate_seconds", mode="after", check_fields=True)
    def validate_measure_unit(cls, twinning_rate_seconds, values):
        if twinning_rate_seconds < 60:
            raise ValueError("Twinning rate must be at least 60.")
        return twinning_rate_seconds
