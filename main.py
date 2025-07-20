from flask import Flask, request
import requests
import re

app = Flask(__name__)

# 🔐 টেলিগ্রাম বট টোকেন
BOT_TOKEN = "7675331377:AAGjh6WPDztxT-FIYkBNpDkrpfyxq1Pk5kc"  # এখানে আপনার বট টোকেন বসবে
BOT_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ✅ অথরাইজড ইউজার আইডি (OWNER_LIST)
OWNER_IDS = [1414414216, 7728185213]  # এখানে আপনার বা ওনার ইউজার আইডি বসবে

# 📤 গুগল শিট ওয়েবহুক URL
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbwkMMe401QPlBeOsypfnxu_qXcJB5qjq5Y_P7q3WXASj8FdCjHAtq3ZWRt-6_hJMiCsvQ/exec"
# উপরে আপনার গুগল শিট অ্যাপ স্ক্রিপ্ট URL বসান

# 🔍 লিংক এক্সট্রাক্ট করার ফাংশন
def extract_url(text):
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else None

# 📦 মেসেজ পাঠানোর ফাংশন
def send_message(chat_id, text):
    url = f"{BOT_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# ❌ মেসেজ ডিলিট করার ফাংশন
def delete_message(chat_id, message_id):
    url = f"{BOT_API_URL}/deleteMessage"
    payload = {"chat_id": chat_id, "message_id": message_id}
    requests.post(url, json=payload)

# 🌐 টেলিগ্রাম বটের ওয়েবহুক হ্যান্ডলার
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        message_id = message.get("message_id")

        if chat_id in OWNER_IDS:
            # ✅ Owner Commands
            if text == "/start":
                send_message(chat_id, "*👋 Welcome boss! আমি আপনার জন্য প্রস্তুত 😎*")
            else:
                url = extract_url(text)
                if url:
                    # ➕ Reply link only
                    send_message(chat_id, url)

                    # ➕ Send to Google Sheet
                    requests.post(GOOGLE_SHEET_WEBHOOK, json={"url": url})

                    # ❌ Delete original message
                    delete_message(chat_id, message_id)
        else:
            # ❌ Unauthorized User
            send_message(chat_id, "*❌ দুঃখিত! আমি আপনার জন্য কাজ করতে পারবো না 🥱*")

    return "ok", 200

# ✅ Bot running check route
@app.route('/', methods=['GET'])
def home():
    return "✅ Bot is running!", 200

# 🔁 অ্যাপ চালু রাখার জন্য
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
