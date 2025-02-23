from telegram import Update
from telegram.ext import ContextTypes
from app.utils.parser import parse_airdrop_message
from app.database.operations import AirdropDB
import re

async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Debug print untuk melihat pesan yang masuk
    print("Received message:", update.message.text)
    print("Message caption:", update.message.caption)
    print("Is forwarded:", update.message.forward_date is not None)
    print("Message type:", update.message.effective_attachment)
    
    # Get text from either message text or caption
    message_text = None
    if update.message.text:
        message_text = update.message.text
    elif update.message.caption:
        # Add AIRDROP ASC header for caption messages
        message_text = f"AIRDROP ASC, [09/02/2025]\n{update.message.caption}"
    
    if not message_text:
        await update.message.reply_text("Please forward text messages from airdrop channels.")
        return
    
    print("Processing text:", message_text)
    
    if not update.message.forward_date:
        await update.message.reply_text("Please forward messages from airdrop channels.")
        return
        
    parsed_data = parse_airdrop_message(message_text)
    if not parsed_data:
        # Debug print untuk melihat hasil parsing
        print("Failed to parse message")
        await update.message.reply_text("Couldn't parse the airdrop information. Make sure it's from AIRDROP ASC channel.")
        return
    
    print("Parsed data:", parsed_data)
    if AirdropDB.save_airdrop(parsed_data):
        # Filter and clean tasks
        tasks_list = []
        for task in parsed_data.get('tasks', '').split('\n'):
            task = task.strip('➡️🟢➖ ')
            # Skip unwanted tasks
            if any(x in task.lower() for x in [
                'done', 'complete all', 'before end', 'register', 'join now',
                'details:', 'collect your', 'tutorial:', '🪂', '🗓', '📖'
            ]):
                continue
            # Skip empty or URL-only tasks
            if not task or task.startswith('http') or 'https://' in task:
                continue
            # Clean up the task text
            task = re.sub(r'^(➖|➡️|•|\-)\s*', '', task).strip()
            if task:
                tasks_list.append(task)
        
        # Remove duplicates while preserving order
        cleaned_tasks = list(dict.fromkeys(tasks_list))
        
        tasks_formatted = '\n'.join(f"  - {task}" for task in cleaned_tasks)
        
        message = (
            "✓ Airdrop saved successfully!\n"
            "─────────────────────\n"
            f"✦ Project: {parsed_data['project_name']}\n"
            f"✦ Project Link: [Click Here]({parsed_data['link']})\n"
            "─────────────────────\n"
            "✦ Tasks:\n"
            f"{tasks_formatted}\n"
            "─────────────────────\n"
            f"ⓘ Added on {parsed_data['date_posted']}"
        )
        
        await update.message.reply_text(
            message,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text("❌ Error saving airdrop data.")