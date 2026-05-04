from telethon import events

BAD_WORDS = ["ဆဲစာသား၁", "ဆဲစာသား၂"] # ဒီမှာ စကားလုံးတွေ ထည့်ပါ

def register(client):
    @client.on(events.NewMessage)
    async def handler(event):
        for word in BAD_WORDS:
            if word in event.text.lower():
                await event.delete()
                await event.respond("⚠️ မသင့်တော်တဲ့ စကားလုံး သုံးနှုန်းလို့ ဖျက်လိုက်ပါပြီ။")
                break
