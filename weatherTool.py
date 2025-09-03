
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_weather(city: str) -> str:
    """Fetches the current weather for a given city."""
    
    #api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": "",
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)        
        response.raise_for_status()
        data = response.json()

        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return f"Current weather in {city}: {description}. Temperature: {temperature}°C, Humidity: {humidity}%"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"
