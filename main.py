import os
import aiohttp
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

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
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    await update.message.reply_text("Link received ✅")
                else:
                    await update.message.reply_text(f"Failed to access link. Status code: {response.status} ❌")
    except aiohttp.ClientError as e:
        logging.error(f"Request failed: {e}")
        await update.message.reply_text("Error while processing link ❌")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
        await update.message.reply_text("Error while processing link ❌")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
