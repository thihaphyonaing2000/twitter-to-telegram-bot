import os
import requests
from bs4 import BeautifulSoup

# Telegram Bot configuration
TOKEN = "8604292424:AAGwOl9SBsC-mDgTJcziXjGeSbJvjhYhj0c"
CHAT_ID = "@moonlightmenMM"

# Target Twitter User
TARGET_USER = "Alvin97273292"

def get_latest_twitter_video():
    # Twitter ကို Nitter သို့မဟုတ် အများသုံး proxy မှတစ်ဆင့် လှမ်းဆွဲခြင်း
    url = f"https://nitter.poast.org/{TARGET_USER}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Twitter/Nitter မျက်နှာပြင်သို့ ချိတ်ဆက်၍ မရပါ။")
            return None, None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # တွစ်တာပေါ်ရှိ ဗီဒီယို သို့မဟုတ် မီဒီယာလင့်ခ်ကို ရှာဖွေခြင်း
        video_element = soup.find('video')
        if video_element and video_element.find('source'):
            video_url = video_element.find('source')['src']
            if video_url.startswith('/'):
                video_url = f"https://nitter.poast.org{video_url}"
            
            # ပို့စ်ပါ စာသားကို ရယူရန်
            tweet_text = soup.find('div', class_='tweet-content')
            caption = tweet_text.get_text() if tweet_text else "New video from Twitter!"
            
            return video_url, caption
            
    except Exception as e:
        print(f"အမှားအယွင်း ဖြစ်ပေါ်သည်: {e}")
        
    return None, None

def send_telegram_video(video_url, caption):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
    payload = {
        "chat_id": CHAT_ID,
        "video": video_url,
        "caption": caption
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        print("ဗီဒီယိုကို Telegram သို့ အောင်မြင်စွာ ပို့ပြီးပါပြီ။")
    else:
        print(f"ပို့၍မရပါ: {response.text}")

def main():
    print("Bot is running and checking for videos...")
    video_url, caption = get_latest_twitter_video()
    
    if video_url:
        send_telegram_video(video_url, caption)
    else:
        print("ဗီဒီယို အသစ် မတွေ့ရသေးပါ။")

if name == "main":
    main()
