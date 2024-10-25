from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeatherData(BaseModel):
    city: str = Field(..., description="Name of the city")
    temp_value: float = Field(..., description="Temperature value in the preferred unit (Celsius or Fahrenheit)")
    feels_like: float = Field(..., description="Perceived temperature value")
    unit: str = Field(..., description="Unit of temperature measurement (Celsius or Fahrenheit)")
    main: str = Field(..., description="Main weather condition (e.g., Rain, Clear, Snow)")
    timestamp: datetime = Field(..., description="Timestamp of the weather data")

class DailySummary(BaseModel):
    city: str = Field(..., description="Name of the city")
    date: str = Field(..., description="Date of the weather data summary (YYYY-MM-DD)")
    average_temperature: float = Field(..., description="Average temperature for the day")
    maximum_temperature: float = Field(..., description="Maximum temperature for the day")
    minimum_temperature: float = Field(..., description="Minimum temperature for the day")
    dominant_condition: str = Field(..., description="Dominant weather condition for the day")

class AlertData(BaseModel):
    city: str = Field(..., description="Name of the city")
    triggered_at: datetime = Field(..., description="When the alert was triggered")
    alert_type: str = Field(..., description="Type of the alert (e.g., temperature, weather condition)")
    alert_message: str = Field(..., description="Detailed message about the alert")
    current_value: float = Field(..., description="Current temperature or condition value that triggered the alert")
    threshold_value: Optional[float] = Field(None, description="Threshold value for temperature alerts")
