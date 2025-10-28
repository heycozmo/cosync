import platform
import psutil  # you'll need to install this one

def get_system_status():
    """
    returns a summary of basic system info.
    later you can make this way deeper (gpu temp, ram %, etc.)
    """
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


def handle_command(user_text: str):
    """
    checks if the user_text is a known local command.
    if yes -> run it here and return a response string.
    if no  -> return None so main code knows to call the llm instead.
    """

    text = user_text.lower().strip()

    # system status command
    if "system status" in text or "cpu temp" in text or "how's my pc" in text:
        return get_system_status()

    # sleep / shutdown / etc could go here later
    # if "sleep mode" in text:
    #     return run_sleep_mode_scene()

    # smart home stuff will live here too later:
    # if "focus mode" in text or "focus scene" in text:
    #     return set_scene("focus")

    # not a command we handle locally
    return None