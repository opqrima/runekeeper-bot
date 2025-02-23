from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '✧ Welcome to Rune Keeper ✧\n\n'
        'I transform airdrop messages into organized knowledge.\n\n'
        '⚡ Commands:\n'
        '• /start - Awaken the keeper\n'
        '• /list - View your collection\n'
        '📜 Forward messages to begin the transformation.'
    )