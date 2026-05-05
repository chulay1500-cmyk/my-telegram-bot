# ၁။ Python ရဲ့ ပတ်ဝန်းကျင်ကို တည်ဆောက်ခြင်း
FROM python:3.13-slim

# ၂။ အလုပ်လုပ်မယ့် ပတ်ဝန်းကျင် (Directory) သတ်မှတ်ခြင်း
WORKDIR /app

# ၃။ Library စာရင်း (requirements.txt) ကို container ထဲ ကူးထည့်ခြင်း
COPY requirements.txt .

# ၄။ requests library အပါအဝင် လိုအပ်တာတွေကို install လုပ်ခြင်း
RUN pip install --no-cache-dir -r requirements.txt

# ၅။ သင့်ရဲ့ Python code တွေအားလုံးကို container ထဲ ကူးထည့်ခြင်း
COPY . .

# ၆။ Application ကို စတင် run ခိုင်းခြင်း
CMD ["python", "💖.py"]
