from pyrogram import Client, filters
import json
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("BOT_API_ID"))
API_HASH = os.environ.get("BOT_API_HASH")

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("add_account"))
async def add_account(client, message):
    parts = message.text.split()
    if len(parts) != 4:
        await message.reply("❗ استخدم الأمر كالتالي:\n`/add_account api_id api_hash session_name`", quote=True)
        return

    _, api_id, api_hash, session = parts

    new_account = {
        "api_id": int(api_id),
        "api_hash": api_hash,
        "session": session
    }

    accounts = []
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            accounts = json.load(f)

    accounts.append(new_account)

    with open("accounts.json", "w") as f:
        json.dump(accounts, f, indent=4)

    await message.reply("✅ تم إضافة الحساب بنجاح!")

bot.run()
