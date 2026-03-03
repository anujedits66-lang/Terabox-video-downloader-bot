import aiohttp
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

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
                    logging.error(f"Failed to access {url}. Status code: {response.status}")
    except aiohttp.ClientError as e:
        logging.error(f"Request failed for {url}: {e}")
        await update.message.reply_text(f"Error while processing link ❌. Error: {e}")
