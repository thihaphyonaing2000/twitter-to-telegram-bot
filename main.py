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
    "DiamondHXG"
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
    """Target Accounts များမှ Original နှင့် Retweet ဗီဒီယိုများကို ရှာဖွေရန်"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    for username in TARGET_ACCOUNTS:
        print(f"Checking account: {username}...")
        # Nitter instance ကို အသုံးပြု၍ ဝင်ရောက်ရှာဖွေခြင်း
        nitter_url = f"https://nitter.privacydev.net/{username}"
        
        try:
            response = requests.get(nitter_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Could not reach Nitter for {username}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            tweets = soup.find_all('div', class_='timeline-item')
            
            for tweet in tweets:
                # ဗီဒီယို ပါဝင်သော tweet ဟုတ်မဟုတ် စစ်ဆေးခြင်း (Original နှင့် Retweet နှစ်ခုစလုံး ပါဝင်သည်)
                video_elem = tweet.find('video')
                if video_elem and video_elem.get('src'):
                    video_src = video_elem.get('src')
                    if video_src.startswith('http'):
                        video_url = video_src
                    else:
                        video_url = f"https://nitter.privacydev.net{video_src}"
                        
                    # Caption ရယူရန်
                    tweet_text = tweet.find('div', class_='tweet-content')
                    caption = tweet_text.text.strip() if tweet_text else f"Video from @{username}"
                    caption = f"@{username}: {caption}"
                    
                    print(f"Found video from {username}! Sending...")
                    return video_url, caption
                    
        except Exception as e:
            print(f"Error scraping {username}: {e}")
            
        print(f"No new videos found for {username}.")
    
    return None, None

def main():
    print("Bot is running and checking for videos across all accounts...")
    video_url, caption = get_latest_twitter_videos()
    
    if video_url:
        send_telegram_video(video_url, caption)
    else:
        print("ဗီဒီယို အသစ် မတွေ့ရသေးပါ။")

if __name__ == "__main__":
    main()
