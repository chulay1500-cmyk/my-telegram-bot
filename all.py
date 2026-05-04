from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'^/all'))
    async def handler(event):
        if not event.is_group: return
        chat = await event.get_input_chat()
        async for user in event.client.iter_participants(chat):
            if not user.bot:
                await event.client.send_message(event.chat_id, f"Hey {user.first_name}!", reply_to=event.id)
