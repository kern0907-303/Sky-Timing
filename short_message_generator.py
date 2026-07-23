# short_message_generator.py
import re

def generate_short_message(date_str, timing, vectors, forces, content_dict, daily_url):
    """
    Generates a 120-180 character traditional Chinese short message.
    Format:
      【今日天時｜日期】
      今日主題：
      三個詞
      今日狀態：
      兩至三句。
      今日提醒：
      一句。
      今日觀察：
      一個問題。
      完整內容：
      {daily_url}
    """
    rhythm = content_dict["daily_rhythm"]
    reason = content_dict["daily_rhythm_reason"]
    question = content_dict["question"]
    
    rhythm_emojis = {
        "啟動": "🌱",
        "推進": "🚀",
        "穩定": "🛡️",
        "整合": "🤝",
        "收斂": "🍂",
        "調整": "⚙️",
        "轉換": "🔄",
        "暫停": "🛑"
    }
    r_emoji = rhythm_emojis.get(rhythm, "✨")
    
    # Format keywords to be spaced
    spaced_keywords = " ｜ ".join(content_dict["keywords"])
    
    # Construct status sentences
    prim = forces["primary_force"]
    status_sentences = (
        f"天地氣場主軸朝向「{rhythm} {r_emoji}」，大氣動能表現為「{prim}」。\n"
        f"👉 建議順應「{reason[:-1]}」的自然規律運行。"
    )
    
    # Construct reminder
    reminder = "穩健推進，不宜躁進逆勢強求。"
    if rhythm == "啟動":
        reminder = "適合確立起點與規畫新藍圖。"
    elif rhythm == "推進":
        reminder = "乘勝追擊，放手擴展行動邊界。"
    elif rhythm == "穩定":
        reminder = "加固內部結構，防禦大於進攻。"
    elif rhythm == "整合":
        reminder = "多方聯絡對接，積極促成合作契機。"
    elif rhythm == "收斂":
        reminder = "做好結案整理，放下不再適用的包袱。"
    elif rhythm == "調整":
        reminder = "保持彈性隨時微調，切忌固步自封。"
    elif rhythm == "轉換":
        reminder = "主動斷捨離，清除陳舊累贅。"
    elif rhythm == "暫停":
        reminder = "資訊不足時宜放慢步伐，靜待轉機。"
        
    msg = (
        f"🌌【Sky Timing 欽天監｜每日天時觀測 — {date_str}】🌌\n\n"
        f"🏷️ 今日主題：\n{spaced_keywords}\n\n"
        f"🌀 今日狀態：\n{status_sentences}\n\n"
        f"💡 今日提醒：\n📌 {reminder}\n\n"
        f"💭 當日深度思考：\n❓ {question}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🌐 完整天時分析與能動走勢：\n"
        f"🔗 {daily_url}"
    )
    
    # Adjust character count limit (120 to 180 words excluding URL)
    cleaned_msg = msg.replace(daily_url, "")
    char_count = len(re.sub(r'\s+', '', cleaned_msg))
    
    if char_count < 120:
        # Pad with a small poetic sentence
        msg = msg.replace("━━━━━━━━━━━━━━━━", f"天地運行自有其規律，順向借力方得圓滿。\n\n━━━━━━━━━━━━━━━━")
        
    return msg

if __name__ == "__main__":
    from timing_calculator import calculate_daily_timing
    from semantic_state_engine import compute_semantic_vectors
    from daily_interpretation import generate_daily_content
    
    timing = calculate_daily_timing("2026-07-15")
    vec, forces = compute_semantic_vectors(timing)
    content = generate_daily_content("2026-07-15", timing, vec, forces)
    msg = generate_short_message("2026-07-15", timing, vec, forces, content, "http://127.0.0.1:8000/date/2026-07-15")
    print(msg)
    print("Char count without URL:", len(re.sub(r'\s+', '', msg.replace("http://127.0.0.1:8000/date/2026-07-15", ""))))
