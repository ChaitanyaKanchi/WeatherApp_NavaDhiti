"""
Weather API Utility

This module provides a function to fetch weather information for a given city
using the OpenWeatherMap API.

Tech stack:
- Python
- Requests
- dotenv for environment variables
"""

import os
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException, Timeout

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


def get_weather(city: str) -> dict:
    """
    Fetch weather data for a given city.

    Args:
        city (str): The name of the city to fetch weather for.

    Returns:
        dict: Weather details if successful, or error message.
            Example (success):
            {
                "city": "Guntur",
                "temperature": 18.5,
                "humidity": 65,
                "condition": "Clear Sky"
            }

            Example (error):
            {
                "error": "City not found"
            }
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        # Send request to weather API
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        # Success response
        if response.status_code == 200:
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"].title(),
            }

        # Error from API
        return {"error": data.get("message", "Unable to fetch weather.")}

    except (RequestException, Timeout) as e:
        # Handle request or connection errors
        return {"error": str(e)}
