import os
import logging
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from threading import Thread

# ================== Flask Web Server ==================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))  # Dynamically fetch the port if running on a cloud provider
    app.run(host="0.0.0.0", port=port)

# Flask ko background thread me start karo
def start_flask():
    thread = Thread(target=run_web)
    thread.daemon = True
    thread.start()

# ================== Telegram Bot ==================

TOKEN = "8755130382:AAF9jzZEYZkoBiKTFFcqIQUaZO3GFL7QL_A"  # Your Telegram Bot Token directly added here
MAX_SIZE = 50 * 1024 * 1024  # 50MB limit for Telegram file uploads

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
            update.message.reply_text("File larger than 50MB ❌ Telegram limit.")
            return

        file_name = url.split("/")[-1] or "file"

        with open(file_name, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):  # 1MB chunks
                if chunk:
                    f.write(chunk)

        update.message.reply_text("Uploading... 🚀")

        with open(file_name, "rb") as f:
            update.message.reply_document(f, timeout=600)

        os.remove(file_name)

        update.message.reply_text("Done ✅")

    except Exception as e:
        update.message.reply_text("Error occurred ❌")
        logging.error(f"Error: {e}")

def main():
    start_flask()  # Flask app ko start karo

    # Telegram bot setup
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
