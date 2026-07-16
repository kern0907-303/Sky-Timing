# daily_publish_pipeline.py
import argparse
import os
import json
from datetime import datetime, timedelta

from timing_calculator import calculate_daily_timing
from semantic_state_engine import compute_semantic_vectors
from daily_interpretation import generate_daily_content
from social_content_generator import generate_social_post
from short_message_generator import generate_short_message
from share_card_generator import generate_share_card_png
from content_deduplication import find_collision
from database import save_daily_state, get_past_states_summaries
from telegram_notifier import notify_daily, CONFIG_PATH

OUTPUTS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_outputs")

def run_publish_pipeline(date_str, timezone="Asia/Taipei", city="Taipei"):
    print(f"\n--- Running Daily Publish Pipeline for date={date_str} ---")
    
    # 1. Compute raw timing
    timing = calculate_daily_timing(date_str, timezone, city)
    
    # 2. Compute semantic vectors & forces
    vectors, forces = compute_semantic_vectors(timing)
    
    # 3. Retrieve past 14 days history summaries for deduplication
    past_history = get_past_states_summaries(limit=14)
    past_summaries = [h["daily_summary"] for h in past_history]
    past_questions = [h["reflection_question"] for h in past_history]
    
    # 4. Generate content with deduplication loop
    attempt = 0
    max_attempts = 5
    content = None
    
    while attempt < max_attempts:
        content = generate_daily_content(date_str, timing, vectors, forces, attempt=attempt)
        
        # Check collision on summary & question
        colliding_summary = find_collision(content["summary"], past_summaries, threshold=0.78)
        colliding_question = find_collision(content["question"], past_questions, threshold=0.78)
        
        if not colliding_summary and not colliding_question:
            print(f"Content accepted at attempt {attempt} (No collision).")
            break
        else:
            print(f"Collision detected at attempt {attempt}. summary_collision={bool(colliding_summary)}, question_collision={bool(colliding_question)}. Regenerating...")
            attempt += 1
            
    # 5. Save state to SQLite Database
    save_daily_state(
        date_str, timezone, city,
        timing, vectors,
        forces["primary_force"], forces["secondary_force"], forces["constraint_force"],
        content["daily_rhythm"], content["summary"], content["question"]
    )
    
    # 6. Generate Outputs folder
    day_dir = os.path.join(OUTPUTS_ROOT, date_str)
    os.makedirs(day_dir, exist_ok=True)
    
    # 6a. daily_state.json
    state_json_path = os.path.join(day_dir, "daily_state.json")
    full_state_payload = {
        "date": date_str,
        "timezone": timezone,
        "city": city,
        "raw_timing_data": timing,
        "semantic_vectors": vectors,
        "primary_force": forces["primary_force"],
        "secondary_force": forces["secondary_force"],
        "constraint_force": forces["constraint_force"],
        "daily_rhythm": content["daily_rhythm"],
        "daily_summary": content["summary"],
        "reflection_question": content["question"],
        "content_details": content
    }
    with open(state_json_path, "w", encoding="utf-8") as f:
        json.dump(full_state_payload, f, ensure_ascii=False, indent=2)
        
    # 6b. daily_web.md
    web_md_path = os.path.join(day_dir, "daily_web.md")
    web_md_content = f"""# Sky Timing 欽天監｜每日天時觀測報告 — {date_str}

## 今日主題：{', '.join(content['keywords'])}
## 今日天時一句話：
> {content['one_liner']}

### 一、天時能量分佈 (Semantic Vectors)
*   建立 (generation): {vectors['generation']}
*   擴張 (expansion): {vectors['expansion']}
*   穩定 (stabilization): {vectors['stabilization']}
*   流動 (circulation): {vectors['circulation']}
*   收斂 (contraction): {vectors['contraction']}
*   轉換 (transformation): {vectors['transformation']}
*   瓦解 (disruption): {vectors['disruption']}
*   不確定 (uncertainty): {vectors['uncertainty']}

### 二、天地運行主軸
*   核心推動力量：{forces['primary_force']}
*   次要支持力量：{forces['secondary_force']}
*   潛在限制條件：{forces['constraint_force']}
*   當日運行節奏：{content['daily_rhythm']} ({content['daily_rhythm_reason']})

### 三、三層觀察
*   **天地層**：{content['tian_obs']}
*   **群體層**：{content['group_obs']}
*   **個人層**：{content['person_obs']}

### 四、今日觀察問題
*   {content['question']}
"""
    with open(web_md_path, "w", encoding="utf-8") as f:
        f.write(web_md_content)
        
    # 6c. daily_social_post.txt
    social_url = f"http://127.0.0.1:8000/date/{date_str}"
    social_post = generate_social_post(date_str, timing, vectors, forces, content, social_url)
    social_post_path = os.path.join(day_dir, "daily_social_post.txt")
    with open(social_post_path, "w", encoding="utf-8") as f:
        f.write(social_post)
        
    # 6d. daily_short_message.txt
    short_msg = generate_short_message(date_str, timing, vectors, forces, content, social_url)
    short_msg_path = os.path.join(day_dir, "daily_short_message.txt")
    with open(short_msg_path, "w", encoding="utf-8") as f:
        f.write(short_msg)
        
    # 6e. daily_share_card.png
    share_png_path = os.path.join(day_dir, "daily_share_card.png")
    png_success = generate_share_card_png(
        date_str=date_str,
        lunar_date=timing["lunar_date"],
        solar_term=timing["solar_term"],
        one_liner=content["one_liner"],
        keywords=content["keywords"],
        daily_rhythm=content["daily_rhythm"],
        output_png_path=share_png_path
    )
    
    print(f"Daily Package generated at: {day_dir}")
    print(f"  - daily_state.json (Saved)")
    print(f"  - daily_web.md (Saved)")
    print(f"  - daily_social_post.txt (Saved, length={len(social_post)})")
    print(f"  - daily_short_message.txt (Saved, length={len(short_msg)})")
    print(f"  - daily_share_card.png (Success={png_success})")
    
    # 7. Automatically notify Telegram if configured
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if cfg.get("chat_id"):
                    print("Dispatching notification to Telegram...")
                    notify_daily(date_str)
        except Exception as e:
            print(f"Failed to load Telegram config for notification: {e}")
    else:
        print("[Info] Telegram is not configured yet. Run 'python telegram_notifier.py --setup' to bind it.")
        
    return full_state_payload

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qin Tian Jian Daily Publish Pipeline")
    parser.add_argument("--date", type=str, help="ISO Date YYYY-MM-DD")
    parser.add_argument("--timezone", type=str, default="Asia/Taipei", help="Timezone offset name")
    parser.add_argument("--city", type=str, default="Taipei", help="City name")
    
    args = parser.parse_args()
    
    date_str = args.date
    if not date_str:
        # Default to current date in Asia/Taipei (+8 hours)
        date_str = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d")
        
    run_publish_pipeline(date_str, args.timezone, args.city)
