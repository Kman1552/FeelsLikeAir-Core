from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import List, Optional, Literal

class coordinateModel(BaseModel):
    # Field handles the range check automatically!
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class paramModel(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    units: str  
    display_name: str = Field(..., alias="displayName")

    @model_validator(mode='after')
    def validate_units(self):
        allowed = ["µg/m³", "ppm", "particles/cm³", "\u00b5g/m\u00b3"]
        if self.units not in allowed:
            raise ValueError(f"Unit {self.units} not in {allowed}")
        return self

class sensorModel(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    parameter: paramModel

class Date_timeModel(BaseModel):
    utc: datetime
    local: str #V3 of openAq returns as a string


class locationModel(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    coordinates: coordinateModel
    sensors: List[sensorModel] # Use capital 'L' List for better compatibility
    isMobile: bool
    datetime_last: Date_timeModel = Field(..., alias="datetimeLast")

    @model_validator(mode='after')
    def validate_logic(self):
        if not self.sensors:
            raise ValueError("Location must have at least one sensor.")
        return self
    


# OpenAQ API response model
class OpenAQResponse(BaseModel):
    results: List[locationModel]