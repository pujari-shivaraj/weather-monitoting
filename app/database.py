import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBClient:
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client["weather_database"]
            logger.info("Successfully connected to MongoDB.")
        except ServerSelectionTimeoutError as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except OperationFailure as e:
            logger.error(f"MongoDB operation failure: {e}")
            raise

    async def store_weather_data(self, weather_data):
        try:
            await self.db.weather_data.insert_one(weather_data)
            logger.info(f"Weather data for {weather_data['city']} stored successfully.")
        except Exception as e:
            logger.error(f"Error storing weather data: {e}")
            raise

    async def close_connection(self):
        try:
            self.client.close()
            logger.info("MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")

    async def get_weather_data_by_date_range(self, start, end):
        return await self.db.weather_data.find({"timestamp": {"$gte": start, "$lt": end}}).to_list(None)

    async def store_daily_summary(self, summary):
        await self.db.daily_summaries.insert_one(summary)

    async def get_daily_summaries(self, date):
        return await self.db.daily_summaries.find({"date": date}).to_list(None)
