import os
import pymongo
from telethon import events


# မရှိရင် Error မတက်အောင် default တစ်ခု ထားပေးထားမယ်
MONGO_URI = os.getenv("MONGO_URL")

if MONGO_URI:
    client_db = pymongo.MongoClient(MONGO_URI)
    db = client_db["bot_database"]
    replies_col = db["replies"]
    pending_col = db["pending_learning"]
else:
    print("❌ Error: MONGO_URL variable ကို Railway မှာ မတွေ့ရပါဘူး!")

def register_reply_system(client):
    @client.on(events.NewMessage)
    async def auto_learn_handler(event):
        if not MONGO_URI or not event.is_group or event.is_bot:
            return

        chat_id = str(event.chat_id)

        # ၁။ အဖြေရှိပြီးသားစာသားလား အရင်စစ်မယ်
        if event.text:
            user_text = event.text.strip().lower()
            found = replies_col.find_one({"question": user_text})
            if found:
                ans = found["answer"]
                if ans.startswith("stk_"):
                    await event.reply(file=ans.replace("stk_", ""))
                else:
                    await event.reply(ans)
                return

        # ၂။ သင်ယူခြင်းအပိုင်း (Learning Logic)
        pending_data = pending_col.find_one({"chat_id": chat_id})
        
        if pending_data:
            question = pending_data["question"]
            answer = None

            if event.text:
                answer = event.text.strip()
            elif event.sticker:
                answer = f"stk_{event.file.id}"

            if answer and question != answer:
                # Database ထဲမှာ သိမ်းမယ်
                replies_col.update_one(
                    {"question": question}, 
                    {"$set": {"answer": answer}}, 
                    upsert=True
                )
                # Pending ကနေ ပြန်ဖျက်မယ်
                pending_col.delete_one({"chat_id": chat_id})
                return

        # ၃။ အဖြေမရှိသေးတဲ့ စာသားအသစ်ကို မေးခွန်းအဖြစ် မှတ်သားမယ်
        if event.text:
            new_question = event.text.strip().lower()
            pending_col.update_one(
                {"chat_id": chat_id}, 
                {"$set": {"question": new_question}}, 
                upsert=True
            )
