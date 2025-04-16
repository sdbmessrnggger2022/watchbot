from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from pyrogram import Client, filters
import asyncio

API_BOT_TOKEN = "ضع هنا توكن البوت"

# قائمة الحسابات المراقِبة
accounts = []

bot = Client("watcher_bot", bot_token=API_BOT_TOKEN, api_id=12345, api_hash="your_api_hash")


@bot.on_message(filters.command("add"))
async def add_account(client, message):
    args = message.text.split()
    if len(args) != 4:
        await message.reply("❌ استخدم الصيغة التالية:\n`/add API_ID API_HASH SESSION_STRING`")
        return

    _, api_id, api_hash, session_string = args

    try:
        account = TelegramClient(StringSession(session_string), int(api_id), api_hash)
        await account.start()
        me = await account.get_me()
        accounts.append(account)
        await message.reply(f"✅ تم إضافة الحساب: {me.first_name}")
        await start_monitoring(account, message.chat.id)
    except Exception as e:
        await message.reply(f"❌ خطأ: {e}")


async def start_monitoring(account, notify_chat_id):
    @account.on(events.NewMessage)
    async def handler(event):
        try:
            sender = await event.get_sender()
            await bot.send_message(
                notify_chat_id,
                f"📩 رسالة جديدة من جروب:\n\n👤 {sender.first_name}\n💬 {event.message.message}"
            )
        except Exception as e:
            print("Error sending message to bot:", e)

    await account.run_until_disconnected()


bot.run()
