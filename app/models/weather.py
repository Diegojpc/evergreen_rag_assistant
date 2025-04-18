from pydantic import BaseModel
import datetime as dt
from typing import List


class WeatherDailyForecast(BaseModel):
    """
    Represents a daily weather forecast for a specific date.

    Attributes:
        date: The date for which the forecast is valid
        max_temperature_c: Maximum temperature in Celsius
        min_temperature_c: Minimum temperature in Celsius
        precipitation_mm: Amount of precipitation in millimeters
        precipitation_prob: Probability of precipitation as a decimal (0.0 to 1.0)
        humidity_relative_avg: Average relative humidity as a decimal (0.0 to 1.0)
        wind_speed_kmh: Wind speed in kilometers per hour
    """

    date: dt.date
    max_temperature_c: float
    min_temperature_c: float
    precipitation_mm: float
    precipitation_prob: float
    humidity_relative_avg: float
    wind_speed_kmh: float

    def to_prompt_string(self) -> str:
        """Convert the weather daily forecast into a formatted string suitable for use in prompts.

        This method formats all the weather daily forecast data into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all weather daily forecast data, with each field on a new line.
                 The string includes date, max temperature, min temperature, precipitation, precipitation probability, humidity, and wind speed.
        """

        return f"""
            - Date: {self.date}
                * Max Temp: {self.max_temperature_c}°C
                * Min Temp: {self.min_temperature_c}°C
                * Precipitation: {self.precipitation_mm} mm
                * Precipitation Prob: {self.precipitation_prob * 100}%
                * Humidity: {self.humidity_relative_avg}%
                * Wind Speed: {self.wind_speed_kmh} km/h
        """


class WeatherForecast(BaseModel):
    """
    Represents weather forecast information for a specific location, including a list of daily forecasts.

    Attributes:
        created_at: Timestamp when the weather information was created/fetched
        location: Name or identifier of the location
        daily: List of daily weather forecasts for the location
    """

    created_at: dt.datetime
    location: str
    daily: List[WeatherDailyForecast]

    def to_prompt_string(self) -> str:
        """Convert the weather forecast into a formatted string suitable for use in prompts.

        This method formats all the weather forecast data into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all weather forecast data, with each field on a new line.
                 The string includes created at, location, and daily forecasts.
        """

        if len(self.daily) == 0:
            daily_forecasts_str: str = "No daily weather forecast data available"
        else:
            daily_forecasts_str = """
            """.join([forecast.to_prompt_string() for forecast in self.daily])

        return f"""
        - Created At: {self.created_at}
        - Location: {self.location}
        - Daily Forecasts:
        {daily_forecasts_str}
        """
