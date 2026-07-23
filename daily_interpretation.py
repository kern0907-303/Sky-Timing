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
            "大氣處於系統軌道切換點，適合進行底層架構的微調與重組以保持彈性。",
            "系統動能正進行結構性過渡，此時宜主動調整底層規則與方向以適應變化。",
            "運行軌道正面臨結構性切換，應順應系統發展趨勢，彈性優化底層架構。"
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
    group_obs = f"環境層：環境表現出「{prim_force}」的普遍張力。容易感到溝通成本{('增加' if vectors['uncertainty'] > 0.4 or vectors['disruption'] > 0.4 else '平緩')}，適合透過「{rhythm}」的節奏來對接外部環境。"
    if contradiction == "力量分布平緩，天地動能和諧。":
        person_obs = f"個人層：注意力將聚焦在「{sec_force}」相關事務。當前能量運作和諧，無顯著阻力與拉扯感，適合順勢推進既定計劃。"
    else:
        person_obs = f"個人層：注意力容易集中在「{sec_force}」相關事務。可能會感覺到自己被兩種力量拉扯（{contradiction}），應學會順勢借力，不急於強行推進。"
    
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
    
    # 7. Resolve Contradictions (Tension Resolver)
    synthesis_text = "【天時解構】天地能量運作和諧，無顯著阻力與摩擦。適合順勢而為，按部就班推進各項既定計劃。"
    u = vectors.get("uncertainty", 0.0)
    g = vectors.get("generation", 0.0)
    t = vectors.get("transformation", 0.0)
    s = vectors.get("stabilization", 0.0)
    e = vectors.get("expansion", 0.0)
    c = vectors.get("contraction", 0.0)
    d = vectors.get("disruption", 0.0)
    
    if g > 0.4 and u > 0.4:
        synthesis_text = "【天時解構】「建立」與「模糊」並存：在此模糊局勢下，不宜強行建構大型、剛性、不可逆的系統；相反，此時特別適合「小步快跑、靈活試錯」的實驗性建立，先以輕量框架測試環境，隨時保持調整空間。"
    elif s > 0.4 and t > 0.4:
        synthesis_text = "【天時解構】「穩定」與「調整」拉扯：即「核心不變，邊緣靈活」。應堅守底層的基本盤與核心原則，但對於具體的執行路徑與戰術方法，則應保持高度彈性，隨形勢主動微調。"
    elif e > 0.4 and (c > 0.4 or u > 0.4):
        synthesis_text = "【天時解構】「推進」與「收斂/模糊」並存：提示「定向突破」。此時切忌全線鋪開盲目衝刺，而應將資源收束，集中於局部安全地帶進行精準突破，其餘大部分領域則應收緊邊界、作防禦保留。"
    elif g > 0.4 and d > 0.4:
        synthesis_text = "【天時解構】「建立」與「瓦解」交織：即「破舊立新」。新結構的誕生必須建立在對陳舊阻礙的果斷切割之上，主動清理失效關係與累贅，才能釋放出真正有生命力的新秩序空間。"
    elif t > 0.4 and u > 0.4:
        synthesis_text = "【天時解構】「調整」與「模糊」重疊：此時大氣處於深度的過渡交接點。暫時缺乏清晰的方向信號，所有的調整都應以「保留彈性與容錯」為第一考量，切忌在此時鎖定剛性決策。"

    # 8. Summary (keep under 250 characters)
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
        "summary": summary_text,
        "synthesis": synthesis_text
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
    
    # Determine suitability and advice based on energy and event type
    suitability = "平順中立"
    advice = "適合按部就班推進。"
    
    # Group categories
    expansion_actions = ["啟動", "合約", "情感約會", "大宗交易", "移徙入宅", "靈感企劃"]
    consensus_actions = ["關係溝通", "商談"]
    contraction_actions = ["關係斷捨離", "收尾", "大掃除"]
    reflective_actions = ["冥想修行", "讀書學習", "調整", "靈感寫作", "收支結算"]
    
    if clash:
        if event_type in expansion_actions:
            suitability = "面臨阻力與考驗"
            advice = f"今日日值歲破或能量衝突強烈，對於需要和諧共識或重大投入的「{event_type}」變數極多，建議放緩推進節奏，避免強求結果。"
        elif event_type in consensus_actions or event_type == "靈感企劃":
            suitability = "溝通變數增多"
            advice = f"今日氣場存在交戰與沖煞，在「{event_type}」中容易出現意見分歧或思緒被打斷，建議抱持包容心，多聽少說，避免在此時做出硬性承諾。"
        elif event_type in contraction_actions:
            suitability = "阻力偏大且易耗能"
            advice = f"天時能量波動劇烈，進行「{event_type}」時可能遇到拖延或突發枝節，且體力消耗較快，建議量力而行，不宜過度勉強。"
        elif event_type in reflective_actions:
            suitability = "心神易受干擾"
            advice = f"今日外界干擾氣場較強，進行「{event_type}」時可能感到心神不寧或財務數據混亂。建議以小規模微調、記錄零散靈感或複習舊知識為主，避免做重大定案。"
        else:
            suitability = "變數與波動較多"
            advice = "天時能量存在交戰或沖煞，各類事務進展易生突發枝節，建議以彈性防禦為主，避免做重大定案。"
            
    elif jc in ["建", "成", "開"]:
        if event_type in expansion_actions:
            suitability = "深受天時支持"
            advice = f"當前建除十二神氣場生機勃勃，主建立與擴充。對於向外開展、注入新生動能的「{event_type}」非常有利，能獲得強勁的順向推動力。"
        elif event_type in consensus_actions or event_type == "讀書學習":
            suitability = "有利拓展與交流"
            advice = f"氣場開放，有利於「{event_type}」中的思想碰撞與秩序建立，容易達成共識或快速吸收新知識，是向外連結的極佳時機。"
        elif event_type in contraction_actions or event_type == "收支結算":
            suitability = "收斂阻力稍大"
            advice = f"今日天時偏向擴張與建立，對於「{event_type}」等收尾或收納事宜容易產生拖延，建議先做評估與整理，暫緩強硬切斷。"
        elif event_type in ["冥想修行", "調整", "靈感寫作"]:
            suitability = "宜開啟新方向"
            advice = f"今日適合為「{event_type}」規劃全新架構或開啟新篇章。適合冥想未來藍圖，或動筆寫下全新靈感的大綱框架。"
        else:
            suitability = "天時平順支持"
            advice = "天地氣流順暢，適合積極推動各項事務。"
            
    elif jc in ["收", "閉", "執"]:
        if event_type in contraction_actions or event_type == "收支結算":
            suitability = "極利於收斂與歸檔"
            advice = f"本日能量主軸為收存與閉藏，最適合將多餘、耗能的事務收尾，或為不健康的關係/空間進行「{event_type}」整理，能獲得極佳的清明與安定力。"
        elif event_type in ["冥想修行", "讀書學習", "靈感寫作"]:
            suitability = "深受天時支持"
            advice = f"天時氣流趨向內斂收攏，是進行「{event_type}」的黃金時機。此時心靈平靜、注意力容易集中，極易進入深度思考或靈感整理狀態。"
        elif event_type in consensus_actions or event_type == "調整":
            suitability = "偏向保守內省"
            advice = f"大氣動能主收攏，在此氣流下進行「{event_type}」應避免過度強求對方的讓步，建議多從內部架構或底層邏輯進行微調，以守代攻。"
        elif event_type in expansion_actions:
            suitability = "拓展受限"
            advice = f"大氣動能處於收斂封閉階段，此時若強行推動「{event_type}」等擴張性計劃，容易感到進展緩慢或反響冷淡，建議改採低調儲備與非公開測試策略。"
        else:
            suitability = "保守穩健為宜"
            advice = "能量趨於收縮，適合內部整理、補足細節，不宜盲目擴張。"
            
    elif jc in ["破", "危", "除"]:
        if event_type in contraction_actions or event_type in ["調整", "收支結算"]:
            suitability = "極佳的破舊立新時機"
            advice = f"今日建除氣場帶有「破除、清除舊疾」的強大動能，若要進行「{event_type}」，能順應天時快速排除障礙、重獲新生，是除舊迎新的最佳時機。"
        elif event_type in ["冥想修行", "讀書學習", "靈感寫作"]:
            suitability = "適合打破瓶頸"
            advice = f"今日適合打破思維定勢。在進行「{event_type}」時，若能主動挑戰難關、顛覆舊有認知或清除心靈毒素，將有突破性的收穫。"
        elif event_type in consensus_actions or event_type == "靈感企劃":
            suitability = "意見易生分歧"
            advice = f"大氣中帶有碰撞與破裂的動能，進行「{event_type}」時容易因觀點不同而引發摩擦，建議保持彈性與冷靜，多加聆聽，避免情緒化爭執。"
        elif event_type in expansion_actions:
            suitability = "變數與衝突較多"
            advice = f"大氣動能帶有波動與破裂之意，在此氣流下強行推動「{event_type}」等剛性契約或關係建立，容易因誤解而留下隱患，建議壓後或保持高度謹慎。"
        else:
            suitability = "變革與重組期"
            advice = "氣場較為波動，適合清理舊包袱，不宜草率做出重大承諾。"
            
    response = (
        f"【天時關聯分析】：您所問的「{question}」（類型：{event_type}），在今日天時背景下，"
        f"整體狀態呈現「{suitability}」。\n"
        f"今日天時的主軸能量為「{prim}」。\n"
        f"針對您提及的限制「{constraint}」：{advice}\n"
        f"【個人建議節奏】：穩健且順勢而為，不盲目逆氣場強求。"
    )
    return response

