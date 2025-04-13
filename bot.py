import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
FORUM_URL = "https://forum.gta5rp.com/forums/meroprijatija-na-servere.549/"

intents = discord.Intents.default()

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.latest_topic = None

    async def on_ready(self):
        print(f"Бот запущен как {self.user}")
        self.bg_task = asyncio.create_task(self.check_new_topics())

    async def check_new_topics(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)

        while not self.is_closed():
            try:
                response = requests.get(FORUM_URL)
                soup = BeautifulSoup(response.text, "html.parser")
                topics = soup.select("div.structItem--thread")

                if topics:
                    first_topic = topics[0]
                    link = "https://forum.gta5rp.com" + first_topic.find("a", class_="structItem-title").get("href")
                    title = first_topic.find("a", class_="structItem-title").text.strip()

                    if self.latest_topic != link:
                        self.latest_topic = link
                        await channel.send(f"🆕 Новая тема: **{title}**\n{link}")

            except Exception as e:
                print("Ошибка при парсинге:", e)

            await asyncio.sleep(30)  # Проверка каждые 30 секунд

client = MyClient(intents=intents)
client.run(TOKEN)
