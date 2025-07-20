from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = "7675331377:AAGjh6WPDztxT-FIYkBNpDkrpfyxq1Pk5kc"
OWNER_ID = "1414414216"
WEB_APP_URL = "https://script.google.com/macros/s/your-google-webapp-id/exec"

@app.post("/your_custom_webhook_path")
async def telegram_webhook(req: Request):
    data = await req.json()
    message = data.get("message") or {}
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not text.startswith("http"):
        return {"status": "ignored"}

    # Send to Google Sheet
    try:
        requests.post(WEB_APP_URL, data={"link": text})
    except Exception as e:
        print("Failed to send to WebApp:", e)

    # Reply with the link only
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": chat_id, "text": text}
    )

    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Bot is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
