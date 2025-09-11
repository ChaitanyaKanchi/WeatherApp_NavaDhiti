import requests
from config import API_KEY, BASE_URL

def get_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()
        if response.status_code == 200:
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"].title()
            }
        else:
            return {"error": data.get("message", "Unable to fetch weather.")}
    except Exception as e:
        return {"error": str(e)}
