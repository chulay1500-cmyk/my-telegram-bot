from telethon import events

def register_reply_system(client):
    @client.on(events.NewMessage)
    async def handler(event):
        text = event.text.lower()
        if text == "hi":
            await event.reply("Hello ဗျာ! ဘာကူညီပေးရမလဲ?")
        elif text == "bot":
            await event.reply("ကျွန်တော် ရှိပါတယ်ခင်ဗျ။")
