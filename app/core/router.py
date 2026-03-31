from app.services.time import get_time
from app.services.weather import get_weather
from app.services.llm import chat_fallback

def route_command(user_input: str):
    original_input = user_input
    user_input = user_input.lower()

    if "light" in user_input:
        return {"type": "text", "content": "lighting command detected"}
    
    elif "weather" in user_input:
        return {"type": "text", "content": get_weather()}
    
    elif "time" in user_input:
        return {"type": "text", "content": get_time()}
    
    else:
        return {"type": "llm", "content": original_input}