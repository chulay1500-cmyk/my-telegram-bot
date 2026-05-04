import requests
from telethon import events

def register_tiktok_system(client):
    @client.on(events.NewMessage(pattern=r'.*tiktok\.com.*'))
    async def handler(event):
        url = event.text
        msg = await event.reply("🔎 TikTok Video ရှာနေပါတယ်...")
        try:
            r = requests.get(f"https://api.reiyuura.me/api/dl/tiktok?url={url}").json()
            if r.get("status"):
                await event.client.send_file(event.chat_id, r['result']['nowm'], caption="✅ Done!")
                await msg.delete()
        except:
            await msg.edit("❌ ဒေါင်းလုဒ်ဆွဲလို့ မရပါဘူး။")
