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
    display_name: str = Field(..., min_length=1)

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
    local: datetime

    @model_validator(mode='after')
    def validate_tz(self):
        # Pydantic already guaranteed they are datetimes, 
        # so we only check the timezone!
        if self.local.tzinfo is None:
            raise ValueError("Local time must be timezone-aware.")
        return self

class locationModel(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    coordinates: coordinateModel
    sensors: List[sensorModel] # Use capital 'L' List for better compatibility
    is_mobile: bool
    datetime_last: Date_timeModel

    @model_validator(mode='after')
    def validate_logic(self):
        if not self.sensors:
            raise ValueError("Location must have at least one sensor.")
        return self
    


# OpenAQ API response model
class OpenAQResponse(BaseModel):
    results: List[locationModel]