from flask import Flask, request
import requests

app = Flask(__name__)

# 🔐 এখানে আপনার টেলিগ্রাম বট টোকেন বসানো হয়েছে
BOT_TOKEN = "7675331377:AAGjh6WPDztxT-FIYkBNpDkrpfyxq1Pk5kc"

# ✅ এখানে আপনার টেলিগ্রাম ইউজার আইডি বসানো হয়েছে (আপনি যিনি বট চালাতে পারবেন)
OWNER_ID = 1414414216

# 📦 টেলিগ্রাম মেসেজ পাঠানোর জন্য ফাংশন
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

# 🌐 ওয়েবহুকের মাধ্যমে আপডেট রিসিভ করার রুট
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            # 🧔 যদি আপনি স্টার্ট করেন
            if chat_id == OWNER_ID:
                send_message(chat_id, "👋 Welcome boss! আমি আপনার জন্য প্রস্তুত 😊")
            else:
                # ❌ যদি অন্য কেউ স্টার্ট করে
                send_message(chat_id, "⚠️ দুঃখিত! আপনার জন্য আমি কাজ করতে পারবো না।")
    return "ok"

# 🟢 রুট "/" শুধু সার্ভার চেক করার জন্য
@app.route("/")
def home():
    return "✅ Bot is running!"

# 🔁 Render সার্ভারে অ্যাপ চালু রাখার জন্য
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
