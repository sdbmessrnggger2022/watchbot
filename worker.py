import os, json, time, requests, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ——— إعدادات من متغيرات البيئة ———
api_id     = int(os.environ['API_ID'])
api_hash   = os.environ['API_HASH']
config_url = os.environ['CONFIG_URL']  # https://yourdomain.com/watchmassage/config.json?token=XYZ

# ——— دالة لجلب الإعدادات ———
def get_cfg():
    return requests.get(config_url).json()

# ——— إعداد كافة العملاء ———
clients = []
for cl in get_cfg().get('clients', []):
    ss = cl['session']
    client = TelegramClient(StringSession(ss), api_id, api_hash)
    clients.append(client)

# ——— معالجات الرسائل لكل عميل ———
for client in clients:
    @client.on(events.NewMessage)
    async def handler(event):
        cfg = get_cfg()
        text = (event.raw_text or "").lower()
        # استبعاد المحظورات
        if any(b in text for b in cfg.get('banned', [])):
            return
        # مطابقة الكلمات المفتاحية
        for w in cfg.get('trigger', []):
            if w in text:
                link = await event.message.get_link()
                await client.send_message(
                    cfg['target'],
                    f"📬 {event.raw_text}\n🔗 {link}"
                )
                break

# ——— تشغيل جميع العملاء ———
async def main():
    # بدء كل عميل
    for c in clients:
        await c.start()
    # انتظر حتى يفصل الجميع (سيبهم شغالين)
    await asyncio.gather(*(c.run_until_disconnected() for c in clients))

if __name__ == '__main__':
    asyncio.run(main())
