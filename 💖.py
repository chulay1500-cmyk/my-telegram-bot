import json
import os
import re
import asyncio
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.types import ChannelParticipantsAdmins

# ================= MODULE IMPORTS (ဖွင့်ထားသော Module များ) =================
from welcome_goodbye import register as register_welcome
from topic_system import register_topic_system
from gpt_check import register as gpt_register
from filter_system import register as register_filter
from all import register as all_register
from tiktok_system import register_tiktok_system
from reply_system import register_reply_system

# ================= MODULE IMPORTS (မရှိသေး၍ ခေတ္တပိတ်ထားသော Module များ) =================
# အစ်ကို့ဆီမှာ ဒီဖိုင်တွေ မရှိသေးရင် Bot Run လို့မရမှာစိုးလို့ ပိတ်ထားတာပါ
# from quick import register as quick_register
# from mute import register as mute_register
# from dm_system import register_dm_system
# from file_system import register_file_system
# from groupadm_system import register_groupadm_system
# from sms_system import register_sms_system
# from admin_system import register_admin_system
# from group_only_commands import register_group_only_commands
# from spam import register_spam
# from shop import register_shop
# from translation import register_translation_system
# from city_weather_full_system import register_all_system
# from link import register_link_system
# from clear import register_clear_system

# ================= CONFIG =================
api_id = 38180913
api_hash = "192dcce296fc8607d9828d83bc7b8bb5"
bot_token = "8593935916:AAE-5LFj-0X1SBKZ76TIEj1jsZADZ6KkIns"
OWNER_IDS = [-1003795852457,-1003721025417,7260737562,8597326828]

REPLY_FILE = "replies.json"
COUNTER_FILE = "counter.json"
GROUP_FILE = "groups.json"
AUTO_FILE = "auto_sticker.json"
REACT_FILE = "auto_react.json"

# ================= JSON =================
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

replies = load_json(REPLY_FILE, {})
counter = load_json(COUNTER_FILE, {})
groups = load_json(GROUP_FILE, [])

def save_group(chat_id):
    if chat_id not in groups:
        groups.append(chat_id)
        save_json(GROUP_FILE, groups)

# ================= CLIENT =================
client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# ================= /id COMMAND =================
@client.on(events.NewMessage(pattern=r'^/id$'))
async def id_handler(event):
    if event.is_reply:
        user = (await event.get_reply_message()).sender
    elif len(event.text.split()) == 2:
        user = await event.client.get_entity(event.text.split()[1])
    else:
        user = await event.get_sender()

    await event.reply(
        f"""
<blockquote expandable>
╭────────────────────────────╮
│ Target Name = {user.first_name}
│ Target ID   =      {user.id}
╰────────────────────────────╯
</blockquote>
""",
        parse_mode="html"
    )

PENDING_FILE = "pending.json"
def load_pending(): return load_json(PENDING_FILE, [])
def save_pending(pending): save_json(PENDING_FILE, pending)

# ================= LIVE CLOCK SYSTEM =================
running_tasks = {}
pause_state = {}

@client.on(events.NewMessage(pattern=r'^/time$'))
async def time_now(event):
    user_id = event.sender_id
    if user_id in running_tasks:
        running_tasks[user_id].cancel()

    pause_state[user_id] = False
    msg = await event.reply("⏳ Starting live clock...", buttons=[[Button.inline("⏸ Pause", b"pause"), Button.inline("⏹ Stop", b"stop")]])

    start_date = datetime(2025, 5, 19)

    async def updater():
        while True:
            try:
                if pause_state.get(user_id):
                    await asyncio.sleep(1)
                    continue
                now = datetime.now()
                delta = now - start_date
                total_days = delta.days
                total_months = (now.year - start_date.year) * 12 + (now.month - start_date.month)

                text = f"""
<blockquote>
╭──────────────────────────────────╮
│        A Day Full Of Site Ko Lovers SaNoe
╰──────────────────────────────────╯
╭──────────────────────────────────╮
│ VALENTINE`S DAY   - 19.5.2025
│ MONTHS            - {total_months} Months
│ NUMBER OF DAYS    - {total_days} Days
╰──────────────────────────────────╯
╭──────────────────────────────────╮
│ DATE              = {now.strftime("%d.%m.%Y")}
│ DAY               = {now.strftime("%A")}
│ TIME              = {now.strftime("%I:%M:%S %p")}
╰──────────────────────────────────╯
</blockquote>
"""
                await msg.edit(text, parse_mode="html", buttons=[[Button.inline("⏸ Pause", b"pause"), Button.inline("⏹ Stop", b"stop")]])
                await asyncio.sleep(2)
            except asyncio.CancelledError: break
            except: break

    task = asyncio.create_task(updater())
    running_tasks[user_id] = task

@client.on(events.CallbackQuery)
async def callback_handler(event):
    user_id = event.sender_id
    data = event.data.decode()
    if data == "pause":
        pause_state[user_id] = True
        await event.edit(buttons=[[Button.inline("▶ Resume", b"resume"), Button.inline("⏹ Stop", b"stop")]])
    elif data == "resume":
        pause_state[user_id] = False
        await event.edit(buttons=[[Button.inline("⏸ Pause", b"pause"), Button.inline("⏹ Stop", b"stop")]])
    elif data == "stop":
        if user_id in running_tasks:
            running_tasks[user_id].cancel()
            del running_tasks[user_id]
        await event.edit("<blockquote>⛔ Stopped Clock</blockquote>", buttons=None, parse_mode="html")

# ================= MENU SYSTEM (အစ်ကို့စာသားများ အပြည့်အစုံ) =================
MENU_TEXT = """<blockquote expandable>
Reply Bot Command List ကို ကြည့်ရန် Buttons Open ကိုနှိပ်ပါ။
</blockquote>"""
GROUP_CMDS = """<blockquote expandable>
╔═══════ Group Only Command List  ════════╗

🔇 /mute              → reply + time mute
🔊 /unmute          → mute ရပ်
⛔ /ban                 → user ban
📢 /report             → report user
⚠️ /warn               → warn user
👢 /kip                  → kick user
📌 /pin                  → message pin
📍 /unpin              → unpin message
🛠 /admin             → reply + title admin မြှင့်
📋 /adminlist        → Group Admin List
❌ /rmadmin         → admin ဖြုတ်
⚙️ /groupadm      → group admin tools
🔎 /filter                 → word filter + reply
📑 /filterlist            → filter list
🗑 /rmfilter            → filter ဖျက်
🚫 /quick                → ban text set
📃 /quicklist           → ban list
🧹 /rmquick            → ban ဖျက်
👥 /all                       → mention all
🛑 /stop                   → mention ရပ်
💬 /sms                   → sms spam
🌐 /translation        → translate reply
⏰ /time                   → အချိန်ကြည့်
🌆 /city                    → မြို့ကြည့်
🏠 /mycity               → အိမ်နီးချင်းကြည့်
🤖 /gpt                    → reply AI စာစစ်
🧵 /topic                 → topic set
🎵 /tiktok                 → TikTok Logo Video
📂 /file                      → Group broadcast (1 day limit)
📊 /fileinfo               → file remaining time
╚═════════════════════════════════╝
Channel : @DanGerOus_SKO
Owner   : @DanGerOusSiteKo
</blockquote>"""

@client.on(events.NewMessage(pattern="/help"))
async def show_menu(event):
    await event.reply(MENU_TEXT, parse_mode="html", buttons=[[Button.inline("Open", data="group_cmds"), Button.url("Channel", "https://t.me/DanGerOus_SKO")]])

@client.on(events.CallbackQuery(data=b"group_cmds"))
async def group_cmds(event):
    await event.edit(GROUP_CMDS, parse_mode="html", buttons=[[Button.inline("🔙 Back", data="back_menu")]])

@client.on(events.CallbackQuery(data=b"back_menu"))
async def back_menu(event):
    await event.edit(MENU_TEXT, parse_mode="html", buttons=[[Button.inline("Open", data="group_cmds")]])

# ================= AUTO REACTION & START SYSTEM =================
COUNTER = {}
STICKER_ID = "BAADBQADDBgAAmGO0VbASxrUpkVFRwI"

@client.on(events.NewMessage)
async def main_handler(event):
    if event.is_group:
        save_group(event.chat_id)
        # Auto Reaction Logic
        COUNTER.setdefault(event.chat_id, 0)
        COUNTER[event.chat_id] += 1
        if COUNTER[event.chat_id] >= 20:
            import random
            from telethon.tl.functions.messages import SendReactionRequest
            from telethon.tl.types import ReactionEmoji
            try:
                await client(SendReactionRequest(peer=event.chat_id, msg_id=event.id, reaction=[ReactionEmoji(emoticon=random.choice(["❤️","🔥","✨","😍"]))]))
                COUNTER[event.chat_id] = 0
            except: pass

@client.on(events.NewMessage(pattern=r'^/start$'))
async def start_cmd(event):
    user = await event.get_sender()
    chat_id = event.chat_id
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    async with client.action(chat_id, "typing"):
        msg = await event.reply("𝒲")
        for frame in ["𝒲𝑒", "𝒲𝑒𝓁", "𝒲𝑒𝓁𝒸", "𝒲𝑒𝓁𝒸𝑜", "𝒲𝑒𝓁𝒸𝑜𝓂", "𝒲𝑒𝓁𝒸𝑜𝓂𝑒"]:
            await asyncio.sleep(0.4); await msg.edit(frame)
        await asyncio.sleep(0.5); await msg.delete()

    text = f"<blockquote expandable>💖 𝐇𝐞𝐥𝐥𝐨 {mention}!\n\n𝐈 𝐚𝐦 𝐍𝐠𝐚𝐬𝐚𝐫 က 𝐆𝐫𝐨𝐮𝐩 𝐎𝐧𝐥𝐲 မှာ 𝐎𝐧𝐥𝐢𝐧𝐞 𝐌𝐞မေမေ နဲ့ အတူ 𝐑𝐞𝐩𝐥𝐲 ပြန်ပေးတဲ့ စက်ရုပ်လေးပါ။</blockquote>"
    await event.respond(text, buttons=[[Button.url("➕ Group ထဲထည့်ပါ", "https://t.me/DanGerOusNgaSar_Bot?startgroup=true")]], parse_mode="html")

# ================= OWNER COMMANDS =================
@client.on(events.NewMessage(pattern="/send"))
async def broadcast(event):
    if event.sender_id not in OWNER_IDS: return
    if not event.is_reply: return await event.reply("Reply to message.")
    msg = await event.get_reply_message()
    sent = 0
    for gid in groups:
        try: await msg.forward_to(gid); sent += 1; await asyncio.sleep(0.5)
        except: pass
    await event.reply(f"✅ Sent to {sent} groups")

# ================= REGISTER ALL SYSTEMS =================
# ဖွင့်ထားသော Register များ
register_welcome(client)
register_topic_system(client)
gpt_register(client)
register_filter(client)
all_register(client)
register_tiktok_system(client)
register_reply_system(client)

# ပိတ်ထားသော Register များ (မဖျက်ထားပါ)
# quick_register(client)
# mute_register(client)
# register_dm_system(client)
# register_file_system(client, OWNER_IDS)
# register_groupadm_system(client)
# register_sms_system(client)
# register_admin_system(client)
# register_group_only_commands(client)
# register_spam(client)
# register_shop(client)
# register_translation_system(client)
# register_all_system(client)
# register_link_system(client, OWNER_IDS)
# register_clear_system(client, OWNER_IDS)

print("✅ Bot is running with all texts included!")
client.run_until_disconnected()
