import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, logger
from app.config import Config
from app.database import MongoDBClient
from app.services.weather_services import fetch_weather_data
from app.services.data_processing import aggregate_daily_weather, store_daily_summaries
from app.schemas.weather import WeatherData, DailySummary
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

mongodb_client = MongoDBClient()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Create the task for periodic weather fetching
    interval = Config.FETCH_INTERVAL  # Fetch interval in seconds from config
    weather_task = asyncio.create_task(fetch_weather_for_cities(interval))
    
    yield  # Application will run while suspended here

    # Shutdown logic: Cancel the weather task when the app stops
    weather_task.cancel()
    await weather_task  # Ensure the task has finished

# Assign lifespan to the FastAPI app
app = FastAPI(lifespan=lifespan)


async def fetch_weather_for_cities(interval: int):
    """
    Fetch weather data for predefined cities at regular intervals.
    """
    while True:
        logger.info("Fetching weather data for Indian metros...")
        for city in cities:
            weather_data = await fetch_weather_data(city)
            if weather_data:
                await mongodb_client.store_weather_data(weather_data)
            else:
                logger.error(f"Failed to fetch weather data for {city}.")
        
        logger.info(f"Waiting for {interval} seconds before the next update.")
        await asyncio.sleep(interval)


cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather Monitoring API"}


@app.get("/weather/{city}", response_model=WeatherData)
async def get_weather(city: str):
    weather_data = await fetch_weather_data(city)
    if weather_data:
        await mongodb_client.store_weather_data(weather_data)
        return weather_data
    raise HTTPException(status_code=404, detail="City not found")

@app.get("/daily-summary", response_model=dict)
async def get_daily_summary():
    city_weather_data = await aggregate_daily_weather()  # Await the async function
    daily_summaries = store_daily_summaries(city_weather_data)  # Await the async function
    return daily_summaries
