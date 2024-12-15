from datetime import datetime

from pydantic import BaseModel, field_validator, Field

from src.domain.entities.water_system_sensor import SensorType, MeasureUnit


class SensorReadingEvent(BaseModel):
    id: str = Field(None)
    sensor: SensorType = Field(...)
    value: float = Field(...)
    measure_unit: MeasureUnit = Field(MeasureUnit.NONE, validation_alias="measureUnit")
    create_date: datetime = Field(..., validation_alias="createDate")
    sensor_id: str = Field(None, validation_alias="sensorId")
    water_system_id: str = Field(None, validation_alias="waterSystemId")

    @classmethod
    @field_validator("measure_unit", mode="after", check_fields=True)
    def validate_measure_unit(cls, unit, values):
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

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
