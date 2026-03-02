import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("Please send a valid link.")
        return

    await update.message.reply_text("Downloading... ⏳")

    try:
        response = requests.get(url, stream=True)
        filename = url.split("/")[-1]

        with open(filename, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        await update.message.reply_document(document=open(filename, "rb"))
        os.remove(filename)

    except Exception:
        await update.message.reply_text("Download failed ❌")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
