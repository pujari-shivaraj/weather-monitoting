import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = "2a6e78468627dcc466790cfc600ac8d5"
    FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", 5))
    FETCH_INTERVAL = FETCH_INTERVAL_MINUTES * 60 

    MONGODB_URI = os.getenv("MONGODB_URI")
    
    TEMP_UNIT = os.getenv("TEMP_UNIT", "Celsius")
    ALERT_THRESHOLD_TEMP = float(os.getenv("ALERT_THRESHOLD_TEMP", 35))
    ALERT_CONSECUTIVE_COUNT = int(os.getenv("ALERT_CONSECUTIVE_COUNT", 2))
