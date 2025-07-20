from flask import Flask, request
import requests

app = Flask(__name__)

# 🔐 টেলিগ্রাম বট টোকেন
BOT_TOKEN = "7675331377:AAGjh6WPDztxT-FIYkBNpDkrpfyxq1Pk5kc"

# ✅ একাধিক অথরাইজড ইউজার আইডি (OWNER_LIST)
OWNER_IDS = [1414414216, 7728185213]

# 📦 মেসেজ পাঠানোর ফাংশন
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

# 🌐 ওয়েবহুক রিসিভ করার রুট
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            if chat_id in OWNER_IDS:
                send_message(chat_id, "👋 Welcome boss! আমি আপনার জন্য প্রস্তুত 😊")
            else:
                send_message(chat_id, "⚠️ দুঃখিত! আপনার জন্য আমি কাজ করতে পারবো না।")
    return "ok"

# 🟢 চেক করার জন্য রুট
@app.route("/")
def home():
    return "✅ Bot is running!"

# 🔁 অ্যাপ চালু রাখার জন্য
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
