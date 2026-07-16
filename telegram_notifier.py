# telegram_notifier.py
import os
import json
import argparse
import requests

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegram_config.json")
DEFAULT_TOKEN = "8454938807:AAG45XW_ApFyLTdoaA2IhG2Bl6kBoQDTghw"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"bot_token": DEFAULT_TOKEN, "chat_id": None}

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def run_setup():
    print("========================================")
    print(" Sky Timing 欽天監｜每日天時觀測 Telegram 設定")
    print("========================================")
    
    config = load_config()
    token = input(f"請輸入 Telegram Bot Token [{config['bot_token']}]: ").strip()
    if not token:
        token = config['bot_token']
        
    config["bot_token"] = token
    save_config(config)
    
    print("\n[第一步] 請在 Telegram 中搜尋 @EKnotice_bot (或點擊 t.me/EKnotice_bot)")
    print("[第二步] 點擊「Start」或發送隨意一則訊息（例如：Hello！）給機器人。")
    print("正在檢測您向機器人發送的啟用訊息，請於 30 秒內操作...")
    
    # Poll getUpdates
    import time
    chat_id = None
    first_name = "User"
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    for i in range(30): # try for 30 seconds
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                results = data.get("result", [])
                if results:
                    # Get last message chat ID
                    last_msg = results[-1]
                    message = last_msg.get("message") or last_msg.get("channel_post")
                    if message:
                        chat = message.get("chat")
                        if chat:
                            chat_id = chat.get("id")
                            first_name = chat.get("first_name", "User")
                            break
            print(".", end="", flush=True)
            time.sleep(1)
        except Exception as e:
            print(".", end="", flush=True)
            time.sleep(1)
            
    if not chat_id:
        print("\n❌ 逾時未檢測到訊息，請確認您已點擊機器人的 Start，或是 token 是否輸入正確。")
        return False
        
    config["chat_id"] = chat_id
    save_config(config)
    print(f"\n\n✅ 成功偵測到使用者！")
    print(f"   使用者名稱: {first_name}")
    print(f"   Chat ID: {chat_id}")
    print(f"   設定檔已儲存至: {CONFIG_PATH}")
    
    # Send test message
    test_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🎉 恭喜！《Sky Timing 欽天監｜每日天時觀測》通知機器人已綁定成功。今後將為您每日定時發送天時觀測與分享卡。"
    }
    requests.post(test_url, json=payload)
    print("✅ 已發送測試訊息至您的 Telegram 帳號！")
    return True

def notify_daily(date_str):
    config = load_config()
    token = config.get("bot_token")
    chat_id = config.get("chat_id")
    
    if not token or not chat_id:
        print("❌ 錯誤：Telegram 尚未設定。請執行 python telegram_notifier.py --setup 進行設定綁定。")
        return False
        
    # Locate generated package
    day_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_outputs", date_str)
    if not os.path.exists(day_dir):
        print(f"❌ 錯誤：找不到 {date_str} 的 daily_outputs 資料夾。請確認該日期的 Pipeline 已執行。")
        return False
        
    short_msg_path = os.path.join(day_dir, "daily_short_message.txt")
    share_card_path = os.path.join(day_dir, "daily_share_card.png")
    
    if not os.path.exists(short_msg_path):
        print("❌ 錯誤：找不到 daily_short_message.txt")
        return False
        
    with open(short_msg_path, "r", encoding="utf-8") as f:
        message_text = f.read()
        
    # We use the message_text directly as it already contains the correct public GitHub Pages URL
    
    # 1. Send the share card photo with the short message text as the caption!
    photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
    
    sent_photo = False
    if os.path.exists(share_card_path):
        try:
            with open(share_card_path, "rb") as photo_file:
                files = {"photo": photo_file}
                data = {"chat_id": chat_id, "caption": message_text}
                r = requests.post(photo_url, data=data, files=files)
                if r.status_code == 200:
                    print(f"✅ 成功發送 {date_str} 分享圖卡及天時訊息至 Telegram！")
                    sent_photo = True
                else:
                    print(f"⚠️ 發送圖卡失敗，狀態碼：{r.status_code}。將嘗試發送純文字訊息。")
        except Exception as e:
            print(f"⚠️ 發送圖卡發生異常：{e}。將嘗試發送純文字訊息。")
            
    # 2. Fallback to raw text message if photo sending failed
    if not sent_photo:
        text_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message_text}
        r = requests.post(text_url, json=payload)
        if r.status_code == 200:
            print(f"✅ 成功發送 {date_str} 純文字天時訊息至 Telegram！")
        else:
            print(f"❌ 發送純文字訊息失敗，狀態碼：{r.status_code}")
            return False
            
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qin Tian Jian Telegram Notifier")
    parser.add_argument("--setup", action="store_true", help="Run interactive bot chat_id binding setup")
    parser.add_argument("--date", type=str, help="YYYY-MM-DD date to send notification for")
    
    args = parser.parse_args()
    if args.setup:
        run_setup()
    elif args.date:
        notify_daily(args.date)
    else:
        # Default to today
        from datetime import datetime, timedelta
        taipei_today = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d")
        notify_daily(taipei_today)
