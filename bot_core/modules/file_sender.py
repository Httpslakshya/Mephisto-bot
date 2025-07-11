import os
import zipfile


def zip_folder(folder_path):
    folder_path = folder_path.rstrip("/\\")
    zip_filename = os.path.basename(folder_path) + ".zip"
    zip_path = os.path.join(os.path.dirname(folder_path), zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)

    return zip_path

# 🔧 Handler attachment function
def attach_file_sender_handlers(bot):
    from bot_core.config import BOT_ADMIN_ID

    @bot.message_handler(commands=['sendfile'])
    def send_file(message):
        if message.from_user.id != BOT_ADMIN_ID:
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
