import discord
import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN") 

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # respond only in DMs OR mentions
    if isinstance(message.channel, discord.DMChannel) or client.user in message.mentions:

        user_input = message.content.replace(f"<@{client.user.id}>", "").strip()

        try:

            async with message.channel.typing():
                res = requests.post(
                    "http://127.0.0.1:8000/command",
                    json={"input": user_input},
                    stream=True
                )

                content_type = res.headers.get("content-type", "")

                # JSON response (weather/time)
                if "application/json" in content_type:
                    data = res.json()
                    await message.channel.send(data["response"])

                # streaming response (LLM)
                else:
                    response_text = ""

                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk:
                            response_text += chunk.decode()

                    await message.channel.send(response_text)

        except Exception as e:
            print("DISCORD BOT ERROR:", e)
            await message.channel.send("cosync hit an error.")

client.run(TOKEN)