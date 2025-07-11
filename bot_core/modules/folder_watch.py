# import os
# import time
# import win32file
# import win32con
# import threading
# from bot_core.spybot import bot
# from bot_core.config import BOT_ADMIN_ID

# WATCHED_FOLDER = r"D:\Codes\my code\Mephisto_killer"
# FILE_LIST_DIRECTORY = 0x0001
# FILE_NOTIFY_CHANGE_LAST_ACCESS = 0x00000020  # 👈 Manually added

# def watch_folder_open():
#     folder_handle = win32file.CreateFile(
#         WATCHED_FOLDER,
#         FILE_LIST_DIRECTORY,
#         win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
#         None,
#         win32con.OPEN_EXISTING,
#         win32con.FILE_FLAG_BACKUP_SEMANTICS,
#         None,
#     )

#     while True:
#         results = win32file.ReadDirectoryChangesW(
#             folder_handle,
#             1024,
#             True,
#             FILE_NOTIFY_CHANGE_LAST_ACCESS,  # ✅ Use defined constant here
#             None,
#             None
#         )
#         for action, file in results:
#             if action == 3:  # 3 = FILE_ACTION_MODIFIED (often triggered on access)
#                 bot.send_message(BOT_ADMIN_ID, f"🚨 Folder '{WATCHED_FOLDER}' was opened or accessed!")
#                 time.sleep(5)

# def start_folder_watch():
#     thread = threading.Thread(target=watch_folder_open, daemon=True)
#     thread.start()
