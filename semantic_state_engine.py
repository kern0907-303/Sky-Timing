# semantic_state_engine.py

def compute_semantic_vectors(timing_data):
    """
    Computes the 8 semantic vectors based on lunar timing calculations.
    Returns:
        vectors: dict with 8 keys, values float in [0.0, 1.0]
        interpretation: dict with primary, secondary, constraint, and contradiction.
    """
    # 8 Dimensions init
    vec = {
        "generation": 0.3,
        "expansion": 0.3,
        "stabilization": 0.3,
        "circulation": 0.3,
        "contraction": 0.3,
        "transformation": 0.3,
        "disruption": 0.3,
        "uncertainty": 0.3
    }
    
    jc = timing_data["jianchu"]
    zs = timing_data["zhishen"]
    has_clash = timing_data["has_clash"]
    has_combo = timing_data["has_combo"]
    
    # 1. Jianchu adjustments
    if jc == "建":
        vec["generation"] += 0.4
        vec["stabilization"] += 0.2
    elif jc == "除":
        vec["disruption"] += 0.3
        vec["transformation"] += 0.2
    elif jc == "滿":
        vec["expansion"] += 0.4
        vec["circulation"] += 0.2
    elif jc == "平":
        vec["stabilization"] += 0.4
    elif jc == "定":
        vec["stabilization"] += 0.5
        vec["generation"] += 0.1
    elif jc == "執":
        vec["stabilization"] += 0.4
        vec["contraction"] += 0.2
    elif jc == "破":
        vec["disruption"] += 0.5
        vec["transformation"] += 0.2
    elif jc == "危":
        vec["uncertainty"] += 0.5
        vec["transformation"] += 0.2
    elif jc == "成":
        vec["generation"] += 0.5
        vec["stabilization"] += 0.2
    elif jc == "收":
        vec["contraction"] += 0.5
        vec["stabilization"] += 0.2
    elif jc == "開":
        vec["expansion"] += 0.5
        vec["circulation"] += 0.3
    elif jc == "閉":
        vec["contraction"] += 0.5
        vec["stabilization"] += 0.3
        vec["expansion"] -= 0.2
        
    # 2. Zhishen adjustments
    if zs in ["青龍", "金匱", "司命"]:
        vec["generation"] += 0.15
        vec["stabilization"] += 0.15
    elif zs in ["明堂", "天德", "玉堂"]:
        vec["circulation"] += 0.2
        vec["expansion"] += 0.1
    elif zs in ["天刑", "白虎"]:
        vec["disruption"] += 0.2
    elif zs in ["朱雀", "勾陳"]:
        vec["uncertainty"] += 0.2
    elif zs in ["天牢", "玄武"]:
        vec["contraction"] += 0.2
        
    # 3. Clash / Combo adjustments
    if has_clash:
        vec["disruption"] += 0.3
        vec["uncertainty"] += 0.15
        vec["stabilization"] -= 0.2
    if has_combo:
        vec["circulation"] += 0.2
        vec["stabilization"] += 0.1
        
    # Standardize/cap values between 0.0 and 1.0
    for k in vec:
        vec[k] = round(max(0.0, min(1.0, vec[k])), 2)
        
    # Determine forces
    sorted_vec = sorted(vec.items(), key=lambda x: x[1], reverse=True)
    prim = sorted_vec[0][0]
    sec = sorted_vec[1][0]
    
    # Potential constraints
    constraint = "uncertainty" if vec["uncertainty"] > 0.4 else "stabilization"
    if vec["disruption"] > 0.5:
        constraint = "disruption"
        
    # Inner Contradiction (e.g. high generation/expansion but high disruption/uncertainty)
    contradiction = "力量分布平緩，天地動能和諧。"
    if vec["expansion"] > 0.5 and vec["contraction"] > 0.5:
        contradiction = "擴張推進與收斂保守的力量同時並存，面臨執行張力。"
    elif vec["generation"] > 0.5 and vec["disruption"] > 0.5:
        contradiction = "一方面急於建立新秩序，另一方面面臨結構性瓦解的摩擦。"
    elif vec["stabilization"] > 0.5 and vec["transformation"] > 0.5:
        contradiction = "維持現狀的慣性與尋求變革的力量相互拉扯。"
        
    # Translate forces to user-friendly terms
    force_labels = {
        "generation": "建立、形成、定位",
        "expansion": "擴散、開放、向外推動",
        "stabilization": "穩定、固定、承載、維持",
        "circulation": "流動、交換、連結、傳遞",
        "contraction": "收斂、回收、沉澱、保存",
        "transformation": "架構調整、系統重組、軌道過渡",
        "disruption": "切割、瓦解、衝突、解除",
        "uncertainty": "模糊、變動、資訊不足、容錯降低"
    }
    
    return vec, {
        "primary_force": force_labels[prim],
        "secondary_force": force_labels[sec],
        "constraint_force": force_labels[constraint],
        "inner_contradiction": contradiction
    }

if __name__ == "__main__":
    from timing_calculator import calculate_daily_timing
    import json
    timing = calculate_daily_timing("2026-07-15")
    vec, interp = compute_semantic_vectors(timing)
    print(json.dumps(vec, indent=2))
    print(json.dumps(interp, indent=2, ensure_ascii=False))
