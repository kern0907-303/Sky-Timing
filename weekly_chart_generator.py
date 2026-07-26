# weekly_chart_generator.py
import os
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from jinja2 import Template
from database import get_daily_state
from app import get_or_create_state

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "weekly_chart.html")
OUTPUTS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_outputs")

def get_week_dates(start_date_str):
    """
    Returns list of 7 dates (YYYY-MM-DD) starting from start_date_str
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def compute_energy_score(vectors):
    """
    Computes an energy score (0-100) based on outward active vs inward stabilizing energies.
    """
    active = vectors.get("expansion", 0.0) + vectors.get("generation", 0.0) + vectors.get("circulation", 0.0)
    stable = vectors.get("stabilization", 0.0) + vectors.get("contraction", 0.0)
    volatile = vectors.get("disruption", 0.0) + vectors.get("uncertainty", 0.0)
    
    score = 50 + (active - stable - volatile * 0.5) * 35
    return max(10, min(95, round(score)))

def generate_weekly_report_text(start_date_str):
    """
    Generates an engaging, high-curiosity traditional Chinese weekly summary message
    based on the calculated daily states of the upcoming week.
    """
    week_dates = get_week_dates(start_date_str)
    week_data = []
    
    day_names_cn = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
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
    
    for i, d_str in enumerate(week_dates):
        state = get_or_create_state(d_str)
        timing = state["raw_timing_data"]
        vectors = state["semantic_vectors"]
        score = compute_energy_score(vectors)
        
        # Check clash/transition
        is_transition = timing.get("is_transition_day", 0) == 1
        is_year_day_clash = timing.get("is_year_day_clash", 0) == 1
        has_clash = timing.get("has_clash", 0) == 1
        
        d_obj = datetime.strptime(d_str, "%Y-%m-%d")
        date_short = d_obj.strftime("%m/%d")
        
        week_data.append({
            "date": d_str,
            "date_short": date_short,
            "day_name": day_names_cn[i],
            "rhythm": state["daily_rhythm"],
            "score": score,
            "is_transition": is_transition,
            "is_year_day_clash": is_year_day_clash,
            "has_clash": has_clash,
            "solar_term": timing.get("solar_term", "")
        })
        
    # 1. Find energy peak and valley
    peak_day = max(week_data, key=lambda x: x["score"])
    valley_day = min(week_data, key=lambda x: x["score"])
    
    # 2. Find any warning or transition day
    transition_days = [x for x in week_data if x["is_transition"]]
    clash_days = [x for x in week_data if x["is_year_day_clash"] or x["has_clash"]]
    
    # 3. Construct 3 key highlights
    highlights = []
    
    # Highlight 1: Peak
    h_rhythm_emoji = rhythm_emojis.get(peak_day["rhythm"], "✨")
    highlights.append(
        f"📈 【能量頂峰 • {peak_day['day_name']}（{peak_day['date_short']}）】\n"
        f"👉 本週天時能量最高點（指數達 {peak_day['score']}%），氣場朝向「{peak_day['rhythm']} {h_rhythm_emoji}」。\n"
        f"💡 欽天監建議：適合全速推進、擴展行動邊界，或執行最核心的關鍵計畫！"
    )
    
    # Highlight 2: Valley or Clash
    if clash_days:
        clash_day = clash_days[0]
        c_rhythm_emoji = rhythm_emojis.get(clash_day["rhythm"], "✨")
        clash_type = "歲破大沖" if clash_day["is_year_day_clash"] else "地支相沖"
        highlights.append(
            f"⚡ 【波動預警 • {clash_day['day_name']}（{clash_day['date_short']}）】\n"
            f"👉 今日逢「{clash_type}」，能量指數僅 {clash_day['score']}%，氣場朝向「{clash_day['rhythm']} {c_rhythm_emoji}」。\n"
            f"💡 欽天監建議：天地磁場正面相沖，行事易有變數或情緒起伏，宜保守靜守，忌強行推進。"
        )
    else:
        v_rhythm_emoji = rhythm_emojis.get(valley_day["rhythm"], "✨")
        highlights.append(
            f"📉 【能量谷底 • {valley_day['day_name']}（{valley_day['date_short']}）】\n"
            f"👉 本週天時能量最低點（指數僅 {valley_day['score']}%），氣場朝向「{valley_day['rhythm']} {v_rhythm_emoji}」。\n"
            f"💡 欽天監建議：今日宜休養生息、重整內部，防禦大於進攻，靜待轉機。"
        )
        
    # Highlight 3: Transition or Volatility
    if transition_days:
        t_day = transition_days[0]
        t_rhythm_emoji = rhythm_emojis.get(t_day["rhythm"], "✨")
        term_name = t_day["solar_term"]
        highlights.append(
            f"🔄 【氣場轉換 • {t_day['day_name']}（{t_day['date_short']}）】\n"
            f"👉 今日逢節氣【{term_name}】，氣場朝向「{t_day['rhythm']} {t_rhythm_emoji}」。\n"
            f"💡 欽天監建議：節氣交替天地能量轉換劇烈，人心易浮躁，適合梳理節奏，順應能量自然過渡。"
        )
    else:
        # Fallback highlight
        second_highest = sorted(week_data, key=lambda x: x["score"], reverse=True)[1]
        sh_rhythm_emoji = rhythm_emojis.get(second_highest["rhythm"], "✨")
        highlights.append(
            f"🤝 【和諧對接 • {second_highest['day_name']}（{second_highest['date_short']}）】\n"
            f"👉 本週次佳推進日（能量指數 {second_highest['score']}%），氣場朝向「{second_highest['rhythm']} {sh_rhythm_emoji}」。\n"
            f"💡 欽天監建議：適合商務會面、溝通對接或整理規劃，多方借力合作。"
        )

    # 4. Construct Calendar Timeline
    calendar_lines = []
    for day in week_data:
        r_emoji = rhythm_emojis.get(day["rhythm"], "✨")
        alert_flag = " ⚠️" if (day["is_year_day_clash"] or day["has_clash"] or day["is_transition"]) else ""
        calendar_lines.append(f"{r_emoji} {day['day_name']}（{day['date_short']}）：{day['rhythm']}{alert_flag}")
        
    start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=6)
    end_date_str = end_date_obj.strftime("%Y-%m-%d")
    
    text = (
        f"🌌【Sky Timing 欽天監｜本週天時天氣預報 — {start_date_str} ~ {end_date_str}】🌌\n\n"
        f"📊 本週能量波動頻率已繪製完成！大氣局勢充滿轉折起伏。以下為您整理「本週三大天時關鍵狀態」：\n\n"
        + "\n\n".join(highlights) + "\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📅 本週天時運行快報：\n"
        + "\n".join(calendar_lines) + "\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"❓ 想知道自己本週的各項計畫如何借力天時？\n"
        f"👉 點擊下方圖片或連結，查看完整的「本週天時能量波動折線圖」與每日詳細觀測！\n\n"
        f"🌐 完整天時週報與每日詳細觀測：\n"
        f"🔗 https://kern0907-303.github.io/Sky-Timing/\n"
    )
    return text

def generate_weekly_chart(start_date_str):
    """
    Queries/generates the 7 days of the week starting from start_date_str,
    renders weekly_chart.html, and screenshots it to a PNG. Also generates a rich report text.
    """
    week_dates = get_week_dates(start_date_str)
    week_data = []
    scores = []
    y_coords = []
    
    day_names_cn = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    
    print(f"Gathering weekly timing states starting from {start_date_str}...")
    for i, d_str in enumerate(week_dates):
        # Retrieve or auto-generate state
        state = get_or_create_state(d_str)
        timing = state["raw_timing_data"]
        vectors = state["semantic_vectors"]
        
        score = compute_energy_score(vectors)
        scores.append(score)
        # Map score 0-100 to SVG Y coordinates 50-250: y = 250 - (score * 2.0)
        y_val = 250 - (score * 2.0)
        y_coords.append(round(y_val, 1))
        
        # Format dates for column cards
        d_obj = datetime.strptime(d_str, "%Y-%m-%d")
        date_short = d_obj.strftime("%m/%d")
        
        # Check clash
        has_clash = timing.get("has_clash", 0)
        is_year_day_clash = timing.get("is_year_day_clash", 0)
        
        week_data.append({
            "date": d_str,
            "date_short": date_short,
            "day_name": day_names_cn[i],
            "rhythm": state["daily_rhythm"],
            "primary_force": state["primary_force"].split("、")[0].split("（")[0].strip(),
            "summary": state["daily_summary"],
            "has_clash": has_clash,
            "is_year_day_clash": is_year_day_clash
        })
        
    # Render template
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Weekly chart template not found at {TEMPLATE_PATH}")
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()
        
    date_range_str = f"{week_dates[0]} ~ {week_dates[6]}"
    
    template = Template(html_template)
    rendered_html = template.render(
        date_range=date_range_str,
        scores=scores,
        y_coords=y_coords,
        week_data=week_data
    )
    
    # Save temp html file
    output_dir = os.path.join(OUTPUTS_ROOT, "weekly_charts")
    os.makedirs(output_dir, exist_ok=True)
    
    temp_html_path = os.path.join(output_dir, f"temp_weekly_chart_{start_date_str}.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    # Generate and save rich report text message
    weekly_text = generate_weekly_report_text(start_date_str)
    weekly_text_path = os.path.join(output_dir, f"weekly_report_text_{start_date_str}.txt")
    with open(weekly_text_path, "w", encoding="utf-8") as f:
        f.write(weekly_text)
    print(f"Weekly rich report text generated at: {weekly_text_path}")
        
    # Output PNG path
    output_png_path = os.path.join(output_dir, f"weekly_chart_{start_date_str}.png")
    
    # Execute Chrome Headless screenshot
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.exists(chrome_path):
        print("Warning: Google Chrome not found at standard path. PNG generation may fail.")
        return None
        
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--screenshot={output_png_path}",
        "--window-size=1080,1350",
        f"file://{os.path.abspath(temp_html_path)}"
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Clean up temporary html
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        print(f"Weekly celestial chart generated successfully: {output_png_path}")
        return output_png_path
    except subprocess.CalledProcessError as e:
        print("Chrome screenshot failed for weekly chart:", e.stderr.decode('utf-8', errors='ignore'))
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weekly Celestial Wave Chart Generator")
    parser.add_argument("--start-date", type=str, help="Monday start date (YYYY-MM-DD)")
    args = parser.parse_args()
    
    start_date = args.start_date
    if not start_date:
        # Default to current or upcoming Monday
        today = datetime.utcnow() + timedelta(hours=8)
        # Get Monday of this week
        monday = today - timedelta(days=today.weekday())
        start_date = monday.strftime("%Y-%m-%d")
        
    generate_weekly_chart(start_date)
