from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.config import BOT_TOKEN
from app.database.models import init_db
from app.bot.handlers import handle_forward
from app.bot.commands import start

def main():
    # Initialize database
    init_db()
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    # Handle both text and media messages with captions
    app.add_handler(MessageHandler(
        (filters.FORWARDED & (filters.TEXT | filters.CAPTION)), 
        handle_forward
    ))
    
    # Start the bot
    print("Bot is running...")
    app.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    main()