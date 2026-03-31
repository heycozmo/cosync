import requests
import time

def get_weather():
    try:

        time.sleep(5)
        url = "https://api.open-meteo.com/v1/forecast?latitude=29.6&longitude=-90.7&current_weather=true"

        response = requests.get(url)
        data = response.json()

        temp_c = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        temp_f = (temp_c * 9/5) + 32

        return f"it’s about {round(temp_f)}°F right now, with winds around {round(wind)} mph"
    
    except Exception as e:
        return f"error getting weather: {e}"