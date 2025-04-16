import os
from telethon import TelegramClient, events

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    print(f"New message from {event.chat_id}: {event.raw_text}")

print("Starting client...")
client.start()
client.run_until_disconnected()
