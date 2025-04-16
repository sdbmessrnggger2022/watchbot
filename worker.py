from telethon import TelegramClient, events
import json
import asyncio

async def run_account(api_id, api_hash, session_name):
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    @client.on(events.NewMessage)
    async def handler(event):
        print(f"[{session_name}] رسالة جديدة في {event.chat.title if event.chat else 'خاص'}: {event.text}")

    print(f"✅ [{session_name}] الحساب شغال...")
    await client.run_until_disconnected()

async def main():
    with open("accounts.json", "r") as f:
        accounts = json.load(f)

    tasks = []
    for acc in accounts:
        tasks.append(run_account(acc["api_id"], acc["api_hash"], acc["session"]))

    await asyncio.gather(*tasks)

asyncio.run(main())
