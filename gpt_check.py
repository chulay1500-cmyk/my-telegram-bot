from telethon import events
import requests

def register(client):
    @client.on(events.NewMessage(pattern=r'^/gpt (.+)'))
    async def handler(event):
        query = event.pattern_match.group(1)
        msg = await event.reply("🤖 AI စဉ်းစားနေပါတယ်...")
        try:
            # Free AI API တစ်ခုခုကို ချိတ်ဆက်အသုံးပြုနိုင်ပါတယ်
            response = requests.get(f"https://api.simsimi.vn/v1/simtalk?text={query}&lc=my").json()
            await msg.edit(f"🤖 **GPT:** {response['message']}")
        except:
            await msg.edit("🤖 အခုလောလောဆယ် AI အလုပ်မလုပ်သေးပါဘူး။")
