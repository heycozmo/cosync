from datetime import datetime

def get_time():
    now = datetime.now()
    time_str = now.strftime('%I:%M %p').lstrip('0')
    return f"it’s {time_str}"