from datetime import datetime, timedelta
from collections import defaultdict
from app.database import MongoDBClient

mongodb_client = MongoDBClient()

async def aggregate_daily_weather():
    """Fetch weather data for the current day and prepare it for aggregation."""
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    # Await the async MongoDB operation
    weather_data = await mongodb_client.get_weather_data_by_date_range(start_of_day, end_of_day)
    
    city_weather_data = defaultdict(list)
    for data in weather_data:
        city_weather_data[data["city"]].append(data)
    
    return city_weather_data


def calculate_daily_aggregates(city_weather_data):
    """Calculate daily aggregates for each city."""
    daily_summaries = {}

    for city, weather_list in city_weather_data.items():
        if not weather_list:
            continue
        
        total_temp = 0
        max_temp = float('-inf')
        min_temp = float('inf')
        condition_count = defaultdict(int)

        for data in weather_list:
            temp = data["temp_value"]
            condition = data["main"]
            
            total_temp += temp
            max_temp = max(max_temp, temp)
            min_temp = min(min_temp, temp)
            condition_count[condition] += 1

        avg_temp = total_temp / len(weather_list)
        dominant_condition = max(condition_count, key=condition_count.get)

        daily_summaries[city] = {
            "city": city,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "average_temperature": avg_temp,
            "maximum_temperature": max_temp,
            "minimum_temperature": min_temp,
            "dominant_condition": dominant_condition
        }
    
    return daily_summaries

def store_daily_summaries(city_weather_data):
    """Store the daily summaries into the database."""
    summaries = calculate_daily_aggregates(city_weather_data)
    for city, summary in summaries.items():
        mongodb_client.store_daily_summary(summary)
    return summaries
