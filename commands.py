import platform
import psutil # type: ignore
import re

# import spotify helpers
import spotify_control


def get_system_status():
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        ram_used_gb = ram.used / (1024**3)
        ram_total_gb = ram.total / (1024**3)
        ram_percent = ram.percent

        os_name = platform.system()
        os_version = platform.release()

        return (
            f"system status:\n"
            f"- os: {os_name} {os_version}\n"
            f"- cpu load: {cpu_percent:.1f}%\n"
            f"- memory: {ram_used_gb:.1f}gb / {ram_total_gb:.1f}gb "
            f"({ram_percent:.1f}%)"
        )
    except Exception as e:
        return f"couldn't read system status yet ({e})"


def handle_spotify_command(text: str):
    # pause / resume
    if ("pause" in text and "spotify" in text) or ("pause the music" in text):
        return spotify_control.spotify_pause(), "spotify_pause"

    if (("resume" in text or "play again" in text or "continue" in text) and
        ("spotify" in text or "music" in text)):
        return spotify_control.spotify_resume(), "spotify_resume"

    # next song
    if "next song" in text or "skip" in text:
        return spotify_control.spotify_next(), "spotify_next"

    # what's playing
    if "what's playing" in text or "what song is this" in text or "current track" in text:
        return spotify_control.spotify_current_track(), "spotify_current_track"

    # play something specific
    # ex: "play travis scott", "play drake", "play my chill playlist"
    m = re.match(r"play (.+)", text)
    if m:
        query = m.group(1)
        return spotify_control.spotify_play_search(query), "spotify_play_search"

    return None, None


def handle_command(user_text: str):
    text = user_text.lower().strip()

    # system level stuff
    if "system status" in text or "cpu temp" in text or "how's my pc" in text:
        return get_system_status(), "system_status"

    # spotify
    spotify_result, handler_name = handle_spotify_command(text)
    if spotify_result is not None:
        return spotify_result, handler_name

    # not a known direct command
    return None, None