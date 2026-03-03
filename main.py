import os
import logging
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# ================== Flask Web Server ==================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Flask ko background thread me start karo
threading.Thread(target=run_web).start()

# ================== Telegram Bot ==================

TOKEN = os.environ.get("8755130382:AAGPcpzPYTmuBHew5bJE55Adqv46cWhx3Qc")
MAX_SIZE = 2 * 1024 * 1024 * 1024  # 2GB limit

logging.basicConfig(level=logging.INFO)

def handle(update: Update, context: CallbackContext):
    url = update.message.text.strip()

    if not url.startswith("http"):
        update.message.reply_text("Send a valid direct download link.")
        return

    try:
        update.message.reply_text("Downloading... ⏳")

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, stream=True, headers=headers, timeout=60)

        if r.status_code != 200:
            update.message.reply_text("Download failed ❌")
            return

        file_size = int(r.headers.get("content-length", 0))

        if file_size > MAX_SIZE:
            update.message.reply_text("File larger than 2GB ❌ Telegram limit.")
            return

        file_name = url.split("/")[-1] or "file"

        with open(file_name, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

        update.message.reply_text("Uploading... 🚀")

        with open(file_name, "rb") as f:
            update.message.reply_document(f, timeout=600)

        os.remove(file_name)

        update.message.reply_text("Done ✅")

    except Exception as e:
        update.message.reply_text("Error occurred ❌")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
