from telethon import events

def register_topic_system(client):
    @client.on(events.NewMessage(pattern=r'^/topic (.+)'))
    async def handler(event):
        if not event.is_group: return
        topic = event.pattern_match.group(1)
        await event.reply(f"📌 **Topic Set:** {topic}")
