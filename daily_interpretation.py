# daily_interpretation.py
import os
import json

def generate_daily_content(date_str, timing, vectors, forces, attempt=0):
    """
    Generates structured Chinese content for the daily timing report.
    Supports rule-based templates by default, with alternative phrasings
    guided by the 'attempt' parameter to support content deduplication.
    """
    prim_force = forces["primary_force"]
    sec_force = forces["secondary_force"]
    constraint_force = forces["constraint_force"]
    contradiction = forces["inner_contradiction"]
    
    # 1. Determine Rhythm
    rhythm_mapping = {
        "generation": ("啟動", [
            "今日氣場有利於新結構的成形，適合宣告起點與勾勒方向。",
            "今日氣運聚焦於奠基與開端，有利於確立新項目的起點。",
            "今日能量偏向凝聚成形，是宣告新計畫啟程的理想時機。"
        ]),
        "expansion": ("推進", [
            "天地動能充沛，適合快速拓展，放大行動規模。",
            "今日氣場積極擴散，有利於資源輸出與業務版圖開拓。",
            "外部動能正盛，適合順勢放大行動規模，向外取得突破。"
        ]),
        "stabilization": ("穩定", [
            "能量處於承載期，比起急躁推進，更適合鞏固現有基礎。",
            "今日天地氣場以守恆承載為主，建議鞏固成果以蓄積後勁。",
            "當前動能收斂於內部結構，宜加固基礎，不宜盲目躁進。"
        ]),
        "circulation": ("整合", [
            "資訊與關係正在加速流動，適合溝通協調與對接資源。",
            "今日能量利於多方連結，適合資訊交換、商務談判與資源整合。",
            "今日流動氣場暢通，是打通關鍵環節、促進社群交流的好時機。"
        ]),
        "contraction": ("收斂", [
            "氣場趨於內省與沉澱，適合整理歷史遺留問題，做好結構收尾。",
            "今日大氣能量向內聚合，宜進行覆盤整理與項目結案收尾。",
            "天地動能放緩，適合將注意力收回，進行內部盤點與減法整理。"
        ]),
        "transformation": ("調整", [
            "舊秩序正在過渡，比起盲目固守，更適合小幅修正方向。",
            "今日氣流處於過渡交接點，適宜主動微調架構以應對外部變化。",
            "能量軌道正在切換，宜順應趨勢進行彈性調整，切忌頑固執念。"
        ]),
        "disruption": ("轉換", [
            "面臨清理與瓦解，適合打破不合時宜的舊架構，釋放包袱。",
            "今日氣場帶有破舊迎新的力量，適合清理累贅、解除舊合約。",
            "結構面臨摩擦與破缺，利於斷捨離，打破瓶頸以釋放隱形負擔。"
        ]),
        "uncertainty": ("暫停", [
            "資訊能見度低，適合放慢速度，觀察環境變化再做定奪。",
            "天地能量波動較大，能見度受限，宜放慢腳步、冷靜觀察。",
            "當前局勢不明朗，資訊缺口多，建議暫緩決策以保全容錯空間。"
        ])
    }
    
    # Identify primary vector key
    max_key = max(vectors, key=vectors.get)
    rhythm_data = rhythm_mapping.get(max_key, ("穩定", ["鞏固現有基礎。"]))
    rhythm = rhythm_data[0]
    
    # Select rhythm reason based on attempt
    reasons_list = rhythm_data[1]
    rhythm_reason = reasons_list[attempt % len(reasons_list)]
    
    # 2. Keywords mapping (Select top 3 based on vectors)
    keyword_mapping = {
        "generation": ["建立", "定位", "凝聚"],
        "expansion": ["擴展", "發布", "前進"],
        "stabilization": ["穩固", "承載", "守恆"],
        "circulation": ["流動", "傳遞", "對接"],
        "contraction": ["收斂", "保存", "沉澱"],
        "transformation": ["調整", "轉換", "過渡"],
        "disruption": ["瓦解", "打破", "釋放"],
        "uncertainty": ["模糊", "觀察", "容錯"]
    }
    
    sorted_vec = sorted(vectors.items(), key=lambda x: x[1], reverse=True)
    keywords = []
    for k, _ in sorted_vec[:3]:
        # If attempt > 0, we can slightly rotate keyword pool if available
        pool = keyword_mapping[k]
        kw_idx = attempt % len(pool)
        keywords.append(pool[kw_idx])
    keywords = keywords[:3]
    
    # 3. One line description alternative phrasings
    one_liner_templates = [
        f"今日天地運行以【{rhythm}】為軸心，{rhythm_reason} {contradiction}",
        f"今日大氣氣場轉向【{rhythm}】律動，{rhythm_reason} {contradiction}",
        f"今日天地動能以【{rhythm}】為主導，應順勢而為，{rhythm_reason} {contradiction}"
    ]
    one_liner = one_liner_templates[attempt % len(one_liner_templates)]
    
    # 4. Support and constraint points
    support_options = {
        "generation": [
            "新秩序與架構正迎來初步建立時機。",
            "結構正在成形，適合勾勒藍圖與確立起點。",
            "凝聚力提升，有利於確立核心方向與定位。"
        ],
        "expansion": [
            "天地動能利於擴張和資源輸出。",
            "外部動能充沛，推廣與版圖擴展阻力較小。",
            "向外拓展的推動力強大，適合宣告與發布。"
        ],
        "stabilization": [
            "穩定承載的條件到位，利於長線規劃。",
            "核心底座穩固，防守與加固基礎的效率極高。",
            "氣場平穩，承載力強，適合執行高複雜度底層工作。"
        ],
        "circulation": [
            "資訊、流通與社群交流暢通無阻。",
            "多方對接與溝通順暢，利於打通合作管道。",
            "資源流動加速，交易與資訊共享條件極佳。"
        ]
    }
    
    risk_options = {
        "disruption": [
            "面臨局部結構的摩擦、破缺或舊物瓦解。",
            "舊包袱與過時架構面臨出清摩擦，需注意解約風險。",
            "面臨局部的斷裂或重組挑戰，不宜強求關係完整。"
        ],
        "uncertainty": [
            "資訊缺口較大，容錯空間可能收窄。",
            "環境波動信號增加，局勢明朗前切忌孤注一擲。",
            "能見度受限，需多備預案以防突發狀況。"
        ],
        "contraction": [
            "外在推力減弱，面臨推進緩慢的收縮阻力。",
            "天地動能減慢，過度擴張易導致內部防線空虛。",
            "面臨成長減速或資源回收壓力，宜保本守成。"
        ]
    }
    
    support_points = []
    risk_points = []
    
    # Choose support point based on vector & attempt
    if vectors["generation"] > 0.4:
        opts = support_options["generation"]
        support_points.append(opts[attempt % len(opts)])
    if vectors["expansion"] > 0.4:
        opts = support_options["expansion"]
        support_points.append(opts[attempt % len(opts)])
    if vectors["stabilization"] > 0.4:
        opts = support_options["stabilization"]
        support_points.append(opts[attempt % len(opts)])
    if vectors["circulation"] > 0.4:
        opts = support_options["circulation"]
        support_points.append(opts[attempt % len(opts)])
        
    # Choose risk point based on vector & attempt
    if vectors["disruption"] > 0.4:
        opts = risk_options["disruption"]
        risk_points.append(opts[attempt % len(opts)])
    if vectors["uncertainty"] > 0.4:
        opts = risk_options["uncertainty"]
        risk_points.append(opts[attempt % len(opts)])
    if vectors["contraction"] > 0.4:
        opts = risk_options["contraction"]
        risk_points.append(opts[attempt % len(opts)])
        
    if not support_points:
        support_points.append("天地能量均衡，利於例行事務推進。")
    if not risk_points:
        risk_points.append("氣場平穩，無顯著阻力，但需防範鬆懈。")
        
    # 5. Three tiers observation
    tianshen = timing["zhishen"]
    jianchu = timing["jianchu"]
    tian_obs = f"天地層：當前運行至{timing['solar_term']}節氣，月令以【{timing['yueling_wuxing']}】氣場主導，本日值神為【{tianshen}】、建除十二神為【{jianchu}】。這代表自然界處於「{rhythm_reason[:-1]}」的背景週期中。"
    group_obs = f"群體層：群體活動表現出「{prim_force}」的普遍張力。成員容易感到溝通成本{('增加' if vectors['uncertainty'] > 0.4 or vectors['disruption'] > 0.4 else '平緩')}，適合透過「{rhythm}」的節奏取得團隊共識。"
    person_obs = f"個人層：注意力容易集中在「{sec_force}」相關事務。可能會感覺到自己被兩種力量拉扯（{contradiction}），應學會順應天時節奏，不急於強行求成。"
    
    # 6. Reflection question
    questions_map = {
        "generation": [
            "今天真正需要建立的，是新的行動，還是能夠承載行動的結構？",
            "當你著手建構新項目時，核心的定位與方向是否已經足夠清晰？",
            "今日的建立，是為了解決眼前的問題，還是為了打下長遠的基石？"
        ],
        "expansion": [
            "在快速推動的同時，你的後方防禦與邊界是否同樣做好了準備？",
            "盲目擴展規模的背後，核心的交付能力能否跟上擴張的速度？",
            "此時的外向突破，是顺應時機的借力，還是強行消耗的透支？"
        ],
        "stabilization": [
            "當下的等待與鞏固，是停滯不前，還是為了下一次躍升在積蓄能量？",
            "在不變的日常中，你是否能看見穩定底座下悄然累積的動能？",
            "守成雖然安全，但有哪些底層的安全感是阻礙你跨出腳步的包袱？"
        ],
        "circulation": [
            "此時的對外連結，是源於內在的充沛，還是為了掩蓋核心的空白？",
            "資訊的加速流動中，你聽到的是有價值的共鳴，還是無意義的雜訊？",
            "與他人的對接中，你在交換的是真實的資源，還是口頭上的防禦？"
        ],
        "contraction": [
            "有哪些已經不再適用的習慣與包袱，值得你在今天優雅地放下？",
            "收尾與沉澱的過程中，你是在遺憾失去，還是在為新種子騰出空間？",
            "當前局部的收縮，是暫時的妥協，還是戰略性撤退的必要智慧？"
        ],
        "transformation": [
            "面對變革，你是在抗拒變化，還是在主動順應新規則的誕生？",
            "方向微調的背後，你是否看清了那股推動你不得不變的底層趨勢？",
            "過渡期的模糊與動盪，是失去控制的危機，還是重新洗牌的契機？"
        ],
        "disruption": [
            "今天所發生的破缺，是偶然的打擊，還是結構重組的必然序曲？",
            "當舊架構被迫崩解時，你是否做好了迎接新生事物的心理準備？",
            "清理舊關係與舊負擔，到底是在割捨痛楚，還是在釋放重生的空間？"
        ],
        "uncertainty": [
            "在能見度極低的時刻，盲目做出決定，真的比停下來觀察更有價值嗎？",
            "面對未知，你的焦慮是源於局勢的不明，還是源於對失去掌控的抗拒？",
            "如何在重重迷霧中，找到一個可以安心容錯的最小立足點？"
        ]
    }
    q_list = questions_map.get(max_key, ["今日你最需要覺察的，是前進的速度，還是維持穩定的基石？"])
    question = q_list[attempt % len(q_list)]
    
    # 7. Summary (keep under 250 characters)
    summary_text = (
        f"今日主要方向：{rhythm}。支持力量：{prim_force}。限制力量：{constraint_force}。"
        f"運行節奏：{rhythm_reason}。天地層面呈現「{rhythm}」大氣，建議順應此運行節律，"
        f"關注「{question[:15]}...」之自省，避免逆勢強求。"
    )[:248]
    
    content = {
        "one_liner": one_liner,
        "keywords": keywords[:3],
        "support_points": support_points[:4],
        "risk_points": risk_points[:4],
        "daily_rhythm": rhythm,
        "daily_rhythm_reason": rhythm_reason,
        "tian_obs": tian_obs,
        "group_obs": group_obs,
        "person_obs": person_obs,
        "question": question,
        "summary": summary_text
    }
    
    return content

# "Ask daily timing" function (次要附屬功能)
def ask_daily_timing_relation(timing_data, vectors, forces, question, event_type, constraint):
    """
    Answers user question about timing relation for a specific action.
    """
    jc = timing_data["jianchu"]
    clash = timing_data["has_clash"]
    prim = forces["primary_force"]
    
    # Simple rule-based logic mapping
    suitability = "平順中立"
    advice = "適合按部就班推進。"
    
    if clash and event_type in ["簽約", "上線", "發布"]:
        suitability = "面臨阻力與變數"
        advice = "本日日沖氣場較強，且有衝突能量，建議將重要行動（如發布/簽約）改為內部檢查或非公開的局部推進，以化解摩擦。"
    elif jc in ["建", "成", "開"] and event_type in ["啟動", "課程開班", "合作"]:
        suitability = "深受天時支持"
        advice = "今日天時利於建立與擴充新秩序，適合高調啟動或舉行儀式，能獲得最大順向推進力。"
    elif jc in ["破", "危", "收", "閉"]:
        suitability = "適合收縮與防禦"
        advice = "本日建除氣場為收斂或清理瓦解，不太適合強行對外拓展。適合做覆盤、除舊迎新或補充細節。"
        
    response = (
        f"【天時關聯分析】：您所問的「{question}」（類型：{event_type}），在今日天時背景下，"
        f"整體狀態呈現「{suitability}」。"
        f"今日的天時主軸力量為「{prim}」。"
        f"對於您提到的限制「{constraint}」，{advice}"
        f"\n建議今日採取的個人節奏：穩健且順勢而為，不盲目逆氣場強求。"
    )
    return response
