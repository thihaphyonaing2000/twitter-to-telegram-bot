import os
import requests
from bs4 import BeautifulSoup

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "8604292424:AAGwOl9SBsC-mDgTJcziXjGeSbJvjhYhj0c"
TELEGRAM_CHAT_ID = "@moonlightmenMM"

# Target X (Twitter) Accounts List
TARGET_ACCOUNTS = [
    "Alvin97273292",
    "TO2K879015",
    "50Gyn",
    "ollo_dr2",
    "alejito_bbk",
    "TOMMYGIKKI",
    "naymyooooo",
    "banyar5343",
    "BomberKeo",
    "HungryGay419019",
    "Larryyesid13",
    "realzayren",
    "DiamondHXG",
    "Rhysand112797"
]

# အလုပ်လုပ်နိုင်ချေရှိသော Nitter ဆာဗာစာရင်းများ (Fallback Instances)
NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.catsarch.com",
    "https://nitter.privacydev.net"
]

def send_telegram_video(video_url, caption):
    """Telegram ချန်နယ်သို့ ဗီဒီယို ပို့ပေးရန် function"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "video": video_url,
        "caption": caption
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Successfully sent video to Telegram!")
        else:
            print(f"Failed to send video: {response.text}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def get_latest_twitter_videos():
    """Target Accounts များမှ Nitter ဆာဗာအမျိုးမျိုးကိုသုံး၍ ဗီဒီယိုရှာဖွေရန်"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    for username in TARGET_ACCOUNTS:
        print(f"Checking account: {username}...")
        success = False
        
        # ဆာဗာတစ်ခုချင်းစီကို အလှည့်ကျ စမ်းသပ်ခြင်း
        for base_url in NITTER_INSTANCES:
            nitter_url = f"{base_url}/{username}"
            try:
                response = requests.get(nitter_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tweets = soup.find_all('div', class_='timeline-item')
                    
                    for tweet in tweets:
                        video_elem = tweet.find('video')
                        if video_elem and video_elem.get('src'):
                            video_src = video_elem.get('src')
                            if video_src.startswith('http'):
                                video_url = video_src
                            else:
                                video_url = f"{base_url}{video_src}"
                                
                            tweet_text = tweet.find('div', class_='tweet-content')
                            caption = tweet_text.text.strip() if tweet_text else f"Video from @{username}"
                            caption = f"@{username}: {caption}"
                            
                            print(f"Found video from {username} using {base_url}! Sending...")
                            return video_url, caption
                    
                    success = True
                    break # ဒီအကောင့်အတွက် ဆာဗာအလုပ်လုပ်သဖြင့် ဆက်မစမ်းတော့ပါ
            except Exception as e:
                continue
                
        print(f"No new videos found or failed to reach instances for {username}.")
    
    return None, None

def main():
    print("Bot is running with fallback instances...")
    video_url, caption = get_latest_twitter_videos()
    
    if video_url:
        send_telegram_video(video_url, caption)
    else:
        print("ဗီဒီယို အသစ် မတွေ့ရသေးပါ။")

if __name__ == "__main__":
    main()
