# timing_calculator.py
from datetime import datetime
from lunar_python import Lunar, Solar

def calculate_daily_timing(date_str, timezone_str="Asia/Taipei", city_str="Taipei"):
    """
    Computes lunar, solar terms, jianchu, zhishen, xiu, clash, combo, etc. for a given date.
    """
    y, m, d = map(int, date_str.split('-'))
    solar = Solar.fromYmdHms(y, m, d, 12, 0, 0)
    lunar = Lunar.fromSolar(solar)
    
    bazi = lunar.getBaZi()
    bazi_wuxing = lunar.getBaZiWuXing()
    
    year_gz = bazi[0]
    month_gz = bazi[1]
    day_gz = bazi[2]
    hour_gz = bazi[3]
    
    jianchu = lunar.getZhiXing()
    zhishen = lunar.getDayTianShen()
    xiu = lunar.getXiu()
    
    day_chong = lunar.getDayChongDesc()
    has_clash = 1 if "沖" in day_chong or "破" in day_chong else 0
    has_combo = 1 if "合" in day_chong else 0
    
    # Next & Prev Jieqi
    prev_jq = lunar.getPrevJieQi()
    next_jq = lunar.getNextJieQi()
    
    return {
        "solar_date": date_str,
        "lunar_date": lunar.toString(),
        "solar_term": lunar.getJieQi() or (prev_jq.getName() if prev_jq else "None"),
        "prev_jieqi": prev_jq.getName() if prev_jq else "None",
        "next_jieqi": next_jq.getName() if next_jq else "None",
        "month_command": lunar.getSeason() + "月令",
        "year_ganzhi": year_gz,
        "month_ganzhi": month_gz,
        "day_ganzhi": day_gz,
        "hour_ganzhi": hour_gz,
        "jianchu": jianchu,
        "zhishen": zhishen,
        "xiu": xiu,
        "nayin": lunar.getDayNaYin(),
        "wuxing": bazi_wuxing[2],
        "clash": day_chong,
        "has_clash": has_clash,
        "has_combo": has_combo,
        "yueling_wuxing": bazi_wuxing[1],
        "jishen": ", ".join(lunar.getDayJiShen()[:4]),
        "xiongsha": ", ".join(lunar.getDayXiongSha()[:4])
    }

if __name__ == "__main__":
    import json
    res = calculate_daily_timing("2026-07-15")
    print(json.dumps(res, indent=2, ensure_ascii=False))
