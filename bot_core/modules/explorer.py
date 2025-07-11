import os
import re
from telebot.types import Message
from bot_core.config import BOT_ADMIN_ID
from bot_core.utils.escape import escape_markdown

# Start in user's home directory
current_dir = os.path.expanduser("~")

def attach_explorer_handlers(bot):
    @bot.message_handler(commands=['pwd'])
    def handle_pwd(message: Message):
        global current_dir
        if message.from_user.id != BOT_ADMIN_ID:
            return
        escaped_path = escape_markdown(current_dir)
        bot.reply_to(message, f"📍 Current path: `{escaped_path}`", parse_mode='MarkdownV2')

    @bot.message_handler(commands=['ls', 'dir'])
    def handle_ls(message: Message):
        global current_dir
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            entries = os.listdir(current_dir)
            if not entries:
                bot.reply_to(message, "📁 Folder is empty.")
                return

            lines = [f"📂 Contents of: `{escape_markdown(current_dir)}`"]
            for item in entries:
                full_path = os.path.join(current_dir, item)
                if os.path.isdir(full_path):
                    lines.append(f"• {escape_markdown(item)}/ 📁")
                else:
                    lines.append(f"• {escape_markdown(item)}")

            response = "\n".join(lines)
            MAX_LEN = 4000
            for chunk in [response[i:i+MAX_LEN] for i in range(0, len(response), MAX_LEN)]:
                bot.reply_to(message, chunk, parse_mode='MarkdownV2')

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {escape_markdown(str(e))}", parse_mode='MarkdownV2')

    @bot.message_handler(commands=['cd'])
    def handle_cd(message: Message):
        global current_dir
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            target = message.text.split(' ', 1)[1].strip()
            new_path = os.path.abspath(os.path.join(current_dir, target))
            if not os.path.isdir(new_path):
                bot.reply_to(message, "⚠️ Not a valid folder.")
                return
            current_dir = new_path
            bot.reply_to(message, f"✅ Changed directory to: `{escape_markdown(current_dir)}`", parse_mode='MarkdownV2')
        except IndexError:
            bot.reply_to(message, "⚠️ Usage: /cd foldername")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {escape_markdown(str(e))}", parse_mode='MarkdownV2')

    @bot.message_handler(commands=['setpath'])
    def handle_setpath(message: Message):
        global current_dir
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            path = message.text.split(' ', 1)[1].strip()
            if not os.path.isdir(path):
                bot.reply_to(message, "⚠️ Not a valid path.")
                return
            current_dir = os.path.abspath(path)
            bot.reply_to(message, f"✅ Set path to: `{escape_markdown(current_dir)}`", parse_mode='MarkdownV2')
        except Exception as e:
            bot.reply_to(message, f"⚠️ Usage: /setpath full/path/here\nError: {escape_markdown(str(e))}", parse_mode='MarkdownV2')
