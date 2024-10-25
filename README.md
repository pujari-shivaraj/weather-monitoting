# Weather Monitoring System

## Overview
The Weather Monitoring System is a FastAPI-based application that retrieves, stores, and processes real-time weather data for major Indian cities. It utilizes MongoDB for data storage, supports configurable temperature units (Celsius/Fahrenheit), and includes alert functionality for high temperatures.

## Features
- **Real-time Weather Retrieval**: Fetches weather data from OpenWeatherMap API at configurable intervals.
- **Daily Summaries**: Provides daily average, maximum, and minimum temperatures, along with the dominant weather conditions.
- **Alerts**: Sends temperature alerts via email when configured thresholds are exceeded.
- **Docker Support**: The application is containerized, allowing for easy setup and deployment.

## Setup Instructions

### Prerequisites
- Docker (required for containerized deployment)
- Docker Compose (optional, if you choose to use it for managing containers)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_handle/weather-monitoring-system.git
   cd weather-monitoring-system

2. **Environment Variables**:
   MONGODB_URI=<Your MongoDB URI>   API_KEY=<OpenWeatherMap API Key>
   FETCH_INTERVAL_MINUTES=5   
   TEMP_UNIT=Celsius           
   ALERT_THRESHOLD_TEMP=35        

3. **Build the Docker Image**:
    docker build -t weather-monitoring-system .

4. **Run the Docker Container**:
    docker run -p 8000:8000 --env-file .env weather-monitoring-system

5. **Run the Docker Container**:
    Access the API: Once the container is running, you can access the FastAPI application at 
    .

    API Endpoints
    GET / - Returns a welcome message to the Weather Monitoring API.
    GET /weather/{city} - Retrieve real-time weather data for the specified city.
    GET /daily-summary - Retrieve daily weather summaries for all tracked cities.