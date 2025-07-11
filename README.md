# 💀 Mephisto_bot — Telegram-Based C2 Bot

![Python](https://img.shields.io/badge/language-python-blue?style=flat&logo=python)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-critical?logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/Development-Active-brightgreen)
![Author](https://img.shields.io/badge/Made%20By-Httpslakshya-red)

**Mephisto_Killer** is a stealthy, modular, Telegram-controlled C2 (Command & Control) bot built using Python. Designed and developed by [Httpslakshya](https://github.com/Httpslakshya), it enables **remote file control, surveillance, system execution, anti-forensics**, and **system monitoring** functionalities — all through your **Telegram** chat.

> ⚠️ Built with an **educational mindset** — Meant to demonstrate real-world system control automation and bot architecture.

---

## 🧱 Feature Breakdown (Phases ✅)

| Phase | Description |
|-------|-------------|
| ✅ **Phase 1: Base Setup & Connection** | Machine ID lock, admin-only access, Telegram bot setup |
| ✅ **Phase 2: File Control Tools** | `getfile`, `sendfile`, `cd`, `pwd`, `ls`, `setpath`, file info |
| ✅ **Phase 3: Surveillance & Spy Modules** | Screenshot, camera/mic/screen recording, keylogger, active window spy |
| ✅ **Phase 4: Execution & System Control** | Shell command execution, shutdown, restart, logoff |
| ✅ **Phase 5: Self-Destruct & Anti-Forensics** | File deletion, clear traces, trap trigger, watchdog mechanism |
<!--
| 🚧 **Phase 6: Advanced Logging & Watchers** | Process list, uptime, CPU/RAM status, file watchers |
| 🚧 **Phase 7: Multi-PC & Logging** | Remote config, scaling support, machine tags |
-->

---

## 🛠 Setup Instructions

### 1️⃣ Install Requirements

Clone this repository and install dependencies:

```bash
git clone https://github.com/Httpslakshya/Mephisto-bot.git
cd Mephisto-bot
pip install -r requirements.txt
```
### 2️⃣ Install Requirements
```bash

pip install -r requirements.txt
```
### 3️⃣ Configure Your Bot
Create the config file:
```bash
bot_core/config.py
```
Paste your bot credentials:
```bash
BOT_TOKEN = "your-telegram-bot-token"
BOT_ADMIN_ID = your-telegram-user-id
```
### 4️⃣ Run the Bot
```bash
python main.py
```
Your Telegram bot is now live and listening.
Send /help in your Telegram to see available commands.

### Supported commands
| Category                 | Example Commands                                                    |
| ------------------------ | ------------------------------------------------------------------- |
| 📁 **File Control**      | `getfile`, `sendfile`, `cd`, `pwd`, `ls`, `setpath`                 |
| 🕵️ **Surveillance**     | `screenshot`, `recordmic`, `recordscreen`, `keylogger`, `spywindow` |
| 🧪 **Execution**         | `shell <command>`, `shutdown`, `restart`, `logoff`                  |
| 🧹 **Self-Destruct**     | `deletefile`, `cleardata`, `traptrigger`, `killwatchdog`            |
| 🔍 **Spy & System Info** | `activewindow`, `getprocesses`, `uptime`                            |


### ⚠️ Disclaimer
* This project is for educational and ethical testing only. 

* Do NOT use it on devices you do not own or have explicit permission to access.

* Misuse of this tool can lead to criminal charges under cybercrime laws.

* The developer Httpslakshya is not responsible for any misuse, damage, or legal issues arising from this project.

### ⭐ Support
 If you found this tool useful or cool, consider giving it a ⭐ on GitHub.
It motivates me to build even more powerful & practical tools for learners and builders like you.

Built for knowledge. Run with caution. ⚙️

