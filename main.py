import os
import time
import requests
from bs4 import BeautifulSoup

# Telegram Bot configuration
TOKEN = "8604292424:AAGwOl9SBsC-mDgTJcziXjGeSbJvjhYhj0c"
CHAT_ID = "@moonlightmenMM"

# Target Twitter User
TARGET_USER = "Alvin97273292"

def send_telegram_video(video_url, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
    payload = {
        "chat_id": CHAT_ID,
        "video": video_url,
        "caption": caption
    }
    requests.post(url, json=payload)

def main():
    print("Bot is running...")
    # ယာယီစမ်းသပ်ရန် လိုအပ်သည်များကို ဆက်လက်ပြင်ဆင်ပါမည်။

if name == "main":
    main()
