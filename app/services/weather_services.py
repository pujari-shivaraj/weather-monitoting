import httpx
from datetime import datetime
from app.config import Config
from app.temperature_utils import convert_temperature

async def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.API_KEY}"

    print(f"Fetching data from: {url}")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temp_value": convert_temperature(data['main']['temp']),
            "feels_like": convert_temperature(data['main']['feels_like']),
            "unit": Config.TEMP_UNIT,
            "main": data['weather'][0]['main'],
            "timestamp": datetime.fromtimestamp(data['dt']),
        }
    else:
        # Better error handling
        print(f"Error fetching data for {city}: {response.status_code}")
        return None
