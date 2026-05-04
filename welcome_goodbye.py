from telethon import events

def register(client):
    @client.on(events.ChatAction)
    async def handler(event):
        if event.user_joined or event.user_added:
            user = await event.get_user()
            await event.reply(f"💖 **Welcome {user.first_name}!**\nGroup ကနေ နွေးထွေးစွာ ကြိုဆိုပါတယ်ဗျ။")
        elif event.user_left or event.user_kicked:
            user = await event.get_user()
            await event.reply(f"👋 **Bye Bye {user.first_name}!**\nနောက်မှ ပြန်ဆုံကြမယ်။")
