import discord
import requests
from bs4 import BeautifulSoup
import asyncio

TOKEN = "MTM2MDg5Njc3MzcxOTA2NDczOA.GducNS.r9EqTpHKcvS6FZhk9NypRCiKzRZ6SFn7R5OxGI"
CHANNEL_ID = 1326619567136706570  # ID канала, куда присылать уведомления
FORUM_URL = "https://forum.gta5rp.com/forums/meroprijatija-na-servere.549/"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

latest_topic = None

async def check_new_topics():
    global latest_topic
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        try:
            response = requests.get(FORUM_URL)
            soup = BeautifulSoup(response.text, "html.parser")
            topics = soup.select("div.structItem--thread")  # Темы на странице

            if topics:
                first_topic = topics[0]
                link = "https://forum.gta5rp.com" + first_topic.find("a", class_="structItem-title").get("href")
                title = first_topic.find("a", class_="structItem-title").text.strip()

                if latest_topic != link:
                    latest_topic = link
                    await channel.send(f"🆕 Новая тема: **{title}**\n{link}")

        except Exception as e:
            print("Ошибка при парсинге:", e)

        await asyncio.sleep(30)  # Проверка каждые 30 секунд

@client.event
async def on_ready():
    print(f"Бот запущен как {client.user}")

client.loop.create_task(check_new_topics())
client.run(TOKEN)
