# line_notifier.py
import os
import json
import argparse
import requests
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "line_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"channel_access_token": None, "user_id": None}

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def run_setup():
    print("========================================")
    print(" Sky Timing 欽天監｜Line Official Account 設定")
    print("========================================")
    
    config = load_config()
    token = input(f"請輸入 Line OA Channel Access Token [{config.get('channel_access_token')}]: ").strip()
    if not token and config.get('channel_access_token'):
        token = config['channel_access_token']
        
    user_id = input(f"請輸入您的 Line User ID [{config.get('user_id')}]: ").strip()
    if not user_id and config.get('user_id'):
        user_id = config['user_id']
        
    if not token or not user_id:
        print("❌ 設定失敗：Token 與 User ID 為必填欄位。")
        return False
        
    config["channel_access_token"] = token
    config["user_id"] = user_id
    save_config(config)
    
    print("\n✅ 設定檔已儲存！正在發送測試訊息...")
    
    # Send test message
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "🎉 恭喜！《Sky Timing 欽天監｜每日天時觀測》Line 官方帳號通知已綁定成功！今後將在此為您推送每週氣候圖與天時預警。"
            }
        ]
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print("✅ 測試訊息發送成功！請檢查您的 Line。")
            return True
        else:
            print(f"❌ 測試訊息發送失敗，狀態碼：{r.status_code}，錯誤訊息：{r.text}")
            return False
    except Exception as e:
        print(f"❌ 發送測試訊息發生異常：{e}")
        return False

def notify_line_daily(date_str):
    config = load_config()
    token = config.get("channel_access_token")
    user_id = config.get("user_id")
    
    if not token or not user_id:
        print("[Info] Line OA 未設定，跳過 Line 推送。")
        return False
        
    # Locate daily outputs
    day_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_outputs", date_str)
    short_msg_path = os.path.join(day_dir, "daily_short_message.txt")
    
    if not os.path.exists(short_msg_path):
        print(f"❌ 錯誤：找不到 {date_str} 的 daily_short_message.txt")
        return False
        
    with open(short_msg_path, "r", encoding="utf-8") as f:
        message_text = f.read()
        
    # Construct image URL based on raw GitHub User Content to bypass GitHub Pages build propagation delay
    image_url = f"https://raw.githubusercontent.com/kern0907-303/Sky-Timing/main/daily_outputs/{date_str}/daily_share_card.png"
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # We send both the text message and the image card
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message_text
            },
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url
            }
        ]
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"✅ 成功發送 {date_str} 觀測與圖卡至 Line OA！")
            return True
        else:
            print(f"⚠️ 發送 Line 失敗，狀態碼：{r.status_code}，回傳內容：{r.text}。嘗試僅發送文字...")
            # Fallback to text only
            fallback_payload = {
                "to": user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message_text
                    }
                ]
            }
            r_fallback = requests.post(url, json=fallback_payload, headers=headers, timeout=10)
            if r_fallback.status_code == 200:
                print("✅ 成功以純文字發送 Line 訊息。")
                return True
            else:
                print(f"❌ 僅發送 Line 文字也失敗，狀態碼：{r_fallback.status_code}")
                return False
    except Exception as e:
        print(f"❌ 發送 Line 發生異常：{e}")
        return False

def notify_line_weekly(start_date_str):
    config = load_config()
    token = config.get("channel_access_token")
    user_id = config.get("user_id")
    
    if not token or not user_id:
        return False
        
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = start_date + timedelta(days=6)
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    message_text = (
        f"【Sky Timing 欽天監｜本週天時天氣預報 — {start_date_str} ~ {end_date_str}】\n\n"
        "📊 本週天時能量走勢與波動預報已繪製完成！\n"
        "請點擊下方圖片或連結查看「本週天時天氣圖」卡片。\n\n"
        "宜依氣場起伏合理調整起居作息與事務佈局。\n\n"
        "🌐 完整天時週報與每日詳細觀測：\n"
        "https://kern0907-303.github.io/Sky-Timing/\n"
    )
    
    # Construct weekly chart image URL based on raw GitHub User Content to bypass GitHub Pages build propagation delay
    image_url = f"https://raw.githubusercontent.com/kern0907-303/Sky-Timing/main/daily_outputs/weekly_charts/weekly_chart_{start_date_str}.png"
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message_text
            },
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url
            }
        ]
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print("✅ 成功發送週報天氣圖卡至 Line OA！")
            return True
        else:
            print(f"❌ 發送 Line 週報圖卡失敗，狀態碼：{r.status_code}，回傳內容：{r.text}")
            # Fallback to text
            fallback_payload = {
                "to": user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message_text
                    }
                ]
            }
            requests.post(url, json=fallback_payload, headers=headers, timeout=10)
            return False
    except Exception as e:
        print(f"❌ 發送 Line 週報圖卡發生異常：{e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qin Tian Jian Line OA Notifier")
    parser.add_argument("--setup", action="store_true", help="Run interactive Line OA credentials setup")
    parser.add_argument("--date", type=str, help="YYYY-MM-DD date to send daily notification for")
    parser.add_argument("--weekly", type=str, help="YYYY-MM-DD Monday start date to send weekly notification for")
    
    args = parser.parse_args()
    if args.setup:
        run_setup()
    elif args.weekly:
        notify_line_weekly(args.weekly)
    elif args.date:
        notify_line_daily(args.date)
    else:
        # Default to today
        taipei_today = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d")
        notify_line_daily(taipei_today)
