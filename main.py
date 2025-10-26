import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is Running on Render!"

@app.route('/health')
def health():
    return "OK", 200

# Get token from environment variable
TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n"
        f"✅ Bot is running 24/7 on Render!\n"
        f"🚀 Free hosting activated!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

def main():
    # Check if token is available
    if not TOKEN:
        logging.error("❌ BOT_TOKEN not found in environment variables!")
        return
    
    # Create Bot Application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    logging.info("🤖 Starting Telegram Bot...")
    
    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    # Start Flask for health checks
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run bot
    main()
