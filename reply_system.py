import json
import os
from telethon import events

REPLY_FILE = "replies.json"
PENDING_FILE = "pending_learning.json"

def load_data(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return default
    return default

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def register_reply_system(client):
    @client.on(events.NewMessage)
    async def auto_learn_handler(event):
        # Bot ကိုယ်တိုင်ပို့တဲ့စာ သို့မဟုတ် Private Chat ဆိုရင် မမှတ်ဘူး
        if not event.is_group or event.is_bot:
            return

        replies = load_data(REPLY_FILE, {})
        pending = load_data(PENDING_FILE, {})
        chat_id = str(event.chat_id)

        # ၁။ အဖြေရှိပြီးသားစာသားလား အရင်စစ်မယ်
        if event.text:
            user_text = event.text.strip().lower()
            if user_text in replies:
                ans = replies[user_text]
                # အဖြေက Sticker ID ဖြစ်နေရင် Sticker အဖြစ်ပို့မယ်
                if ans.startswith("stk_"):
                    await event.reply(file=ans.replace("stk_", ""))
                else:
                    await event.reply(ans)
                return

        # ၂။ သင်ယူခြင်းအပိုင်း (Learning Logic)
        if chat_id in pending:
            question = pending[chat_id]
            answer = None

            # အဖြေက စာသားဆိုရင်
            if event.text:
                answer = event.text.strip()
            # အဖြေက Sticker ဆိုရင်
            elif event.sticker:
                # Sticker ID ကို ခွဲခြားရအောင် ရှေ့မှာ stk_ ခံပြီး သိမ်းမယ်
                answer = f"stk_{event.file.id}"

            if answer and question != answer:
                replies[question] = answer
                save_data(REPLY_FILE, replies)
                del pending[chat_id]
                save_data(PENDING_FILE, pending)
                return

        # ၃။ အဖြေမရှိသေးတဲ့ စာသားအသစ်ကို မေးခွန်းအဖြစ် မှတ်သားမယ်
        if event.text:
            new_question = event.text.strip().lower()
            pending[chat_id] = new_question
            save_data(PENDING_FILE, pending)
