# social_content_generator.py
import re

def generate_social_post(date_str, timing, vectors, forces, content_dict, daily_url):
    """
    Generates a 250-450 character traditional Chinese social post.
    Structure:
      - Opening: Friendly, intuitive summary of today's state.
      - Middle: Explains key energies, feelings, friction, and rhythm.
      - Ending: Reflection question + Link.
    """
    rhythm = content_dict["daily_rhythm"]
    prim = forces["primary_force"]
    sec = forces["secondary_force"]
    question = content_dict["question"]
    
    # 1. Opening variation based on date & primary energy
    opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n感覺到前進的阻力，或是思緒有些起伏嗎？今天整體的運行律動指向「{rhythm}」。"
    if rhythm == "啟動":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n新秩序的種子正在萌芽。今天天地間有一股適合「{rhythm}」的生氣，非常利於勾勒新的方向與點燃開端。"
    elif rhythm == "推進":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n蓄勢待發的能量正強烈釋放。今天的氣場適合向外「{rhythm}」，是擴大行動規模、跨出邊界的開展時刻。"
    elif rhythm == "穩定":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n天地安靜沉穩，承載力強。今天適合讓腳步落實，以「{rhythm}」為主軸，是默默加固現有基石的絕佳時機。"
    elif rhythm == "整合":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n人際與資訊正在流動對接。今天天地運行有利於「{rhythm}」，是打通協調網絡、交換資源與取得共識的契機。"
    elif rhythm == "收斂":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n潮水正在退去，動能緩緩向內聚合。今天的天時透露出「{rhythm}」的意味，特別適合整理舊物、做項目的盤點與收尾。"
    elif rhythm == "調整":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n氣流處於過渡交接點。今天的天時主軸在於「{rhythm}」，與其頑固地堅持既定軌道，不如順應形勢微調方向。"
    elif rhythm == "轉換":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n天地能量正進行出清重組。今天的運行旋律偏向「{rhythm}」，適合斷捨離、打破不合時宜的舊結構並釋放負擔。"
    elif rhythm == "暫停":
        opening_sentence = f"【Sky Timing 欽天監｜每日天時觀測 — {date_str}】\n能見度降低，氣場波動不定。今天適合主動「{rhythm}」，保留彈性，靜下心來觀察局勢，切忌急躁做出重大決定。"

    # 2. Middle paragraph detailing forces & friction
    has_clash = timing["has_clash"]
    friction_text = "氣場平穩，無顯著阻力摩擦。"
    if has_clash:
        friction_text = "由於本日存在日沖與破缺的氣場，您可能會感到溝通成本增加，或是執行中出現意料外的細節阻礙。"
    elif vectors["uncertainty"] > 0.4:
        friction_text = "因為當前不確定性動能較高，資訊能見度受限，在做判斷時可能會感到猶豫，容錯邊界也會隨之收窄。"
    elif vectors["contraction"] > 0.4:
        friction_text = "受到能量向內收縮的牽引，強行拓展容易感到後繼無力，此時應避免透支體力。"

    middle_paragraph = (
        f"今天主要影響我們的力量為「{prim}」，而輔助的動能是「{sec}」。"
        f"在這樣的氣場組合下，{friction_text}"
        f"最適合的運行節奏是 {content_dict['daily_rhythm_reason']}順應自然界週期，做順向的事務推進，才能獲得天時最大的支持。"
    )

    # 3. Ending
    ending = (
        f"💡 今日天時問事自省：\n「{question}」\n\n"
        f"查看完整今日天時觀測與八維語義圖表：\n{daily_url}"
    )

    post = f"{opening_sentence}\n\n{middle_paragraph}\n\n{ending}"
    
    # Verify word count
    # Remove URL to check core text length
    cleaned_post = post.replace(daily_url, "")
    char_count = len(re.sub(r'\s+', '', cleaned_post))
    
    # Just a print debug or safeguard
    # If too short, we can pad slightly
    if char_count < 250:
        padding = f"\n天地不言，以四時運行彰顯其理。在順應自然背景的流動中，每一步微小的調整都將成為未來的基石。"
        post = post.replace("\n\n💡", f"\n{padding}\n\n💡")
        
    return post

if __name__ == "__main__":
    from timing_calculator import calculate_daily_timing
    from semantic_state_engine import compute_semantic_vectors
    from daily_interpretation import generate_daily_content
    
    timing = calculate_daily_timing("2026-07-15")
    vec, forces = compute_semantic_vectors(timing)
    content = generate_daily_content("2026-07-15", timing, vec, forces)
    post = generate_social_post("2026-07-15", timing, vec, forces, content, "http://127.0.0.1:8000/date/2026-07-15")
    print(post)
    print("Char count without URL:", len(re.sub(r'\s+', '', post.replace("http://127.0.0.1:8000/date/2026-07-15", ""))))
