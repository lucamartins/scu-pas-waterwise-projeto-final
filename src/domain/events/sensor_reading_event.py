from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator, Field

from src.domain.entities.water_system_sensor import SensorType, MeasureUnit


class SensorReadingEvent(BaseModel):
    sensor: SensorType = Field(...)
    value: float = Field(...)
    measure_unit: MeasureUnit = Field(MeasureUnit.NONE)
    create_date: datetime = Field(...)
    sensor_id: UUID = Field(None)

    @field_validator("measure_unit", mode="after", check_fields=True)
    def validate_measure_unit(self, unit, values):
        sensor = values.get("sensor")
        if sensor:
            sensor_units = {
                SensorType.TEMPERATURE: MeasureUnit.CELSIUS,
                SensorType.PH: MeasureUnit.NONE,
                SensorType.TURBIDITY: MeasureUnit.NTU,
                SensorType.DISSOLVED_OXYGEN: MeasureUnit.MG_L,
                SensorType.CONDUCTIVITY: MeasureUnit.US_CM,
            }
            expected_unit = sensor_units.get(sensor)
            if unit != expected_unit and unit != MeasureUnit.NONE:
                raise ValueError(
                    f"Invalid measure unit '{unit}' for sensor type '{sensor}'. Expected: '{expected_unit}'."
                )
        return unit
