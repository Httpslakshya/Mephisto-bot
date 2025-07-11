import os
from telebot.types import Message, Document
from bot_core.config import BOT_ADMIN_ID

# Dictionary to map file_id to actual file info
pending_files = {}

def attach_file_receive_handlers(bot):
    @bot.message_handler(content_types=['document'])
    def handle_document(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        # Store document message ID for reply reference
        pending_files[message.message_id] = message.document
        bot.reply_to(message, "📎 File received. Now reply to this message with:\n`/save location=your/path/`", parse_mode='Markdown')

    @bot.message_handler(commands=['save'])
    def handle_save(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        if not message.reply_to_message or message.reply_to_message.message_id not in pending_files:
            bot.reply_to(message, "⚠️ Please reply to the file you sent earlier with the /save command.")
            return

        document: Document = pending_files[message.reply_to_message.message_id]
        try:
            location = message.text.split("location=", 1)[1].strip('" ')
            if not os.path.isdir(location):
                bot.reply_to(message, "❌ Invalid path. Make sure the folder exists.")
                return

            file_info = bot.get_file(document.file_id)
            downloaded = bot.download_file(file_info.file_path)

            save_path = os.path.join(location, document.file_name)
            with open(save_path, "wb") as f:
                f.write(downloaded)

            bot.reply_to(message, f"✅ Saved to:\n`{save_path}`", parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"❌ Failed to save file:\n{e}")
