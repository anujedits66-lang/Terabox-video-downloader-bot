import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found! Set it in Environment Variables.")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running ✅\nSend me any link.")

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid link.")
        return

    await update.message.reply_text("Downloading... ⏳")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            await update.message.reply_text("Link received ✅")
        else:
            await update.message.reply_text("Failed to access link ❌")

    except Exception:
        await update.message.reply_text("Error while processing link ❌")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
