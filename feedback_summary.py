# feedback_summary.py
import argparse
import os
from database import get_feedback_records, get_all_daily_states

def generate_feedback_summary(days=7):
    records = get_feedback_records(days)
    all_states = get_all_daily_states()
    
    # Filter states within the last N days
    # Since we generate daily packages, we can calculate how many days are active
    total_states_count = len(all_states)
    
    resonant_cnt = 0
    partial_cnt = 0
    not_resonant_cnt = 0
    observations = []
    
    for r in records:
        rx = r["reaction"]
        if rx == "resonant":
            resonant_cnt += 1
        elif rx == "partial":
            partial_cnt += 1
        elif rx == "not_resonant":
            not_resonant_cnt += 1
            
        if r["observation"]:
            observations.append(r)
            
    total_feedback = len(records)
    
    # Calculate percentages
    res_pct = (resonant_cnt / total_feedback * 100) if total_feedback else 0.0
    par_pct = (partial_cnt / total_feedback * 100) if total_feedback else 0.0
    not_pct = (not_resonant_cnt / total_feedback * 100) if total_feedback else 0.0
    
    # Build feedback ratio (feedbacks / total active states)
    feedback_ratio = (total_feedback / total_states_count * 100) if total_states_count else 0.0
    
    md_content = f"""# 欽天監今日天時反饋審計報告 ({days}天內)

*   **報告生成時間**：{os.popen('date').read().strip()}
*   **總已生成天時數**：{total_states_count}
*   **總提交反饋次數**：{total_feedback}
*   **反饋覆蓋率**：{feedback_ratio:.2f}%

## 1. 狀態反饋統計 (Reaction Statistics)
*   **有感 (Resonant)**：{resonant_cnt} 次 ({res_pct:.1f}%)
*   **部分有感 (Partial)**：{partial_cnt} 次 ({par_pct:.1f}%)
*   **沒有感覺 (Not Resonant)**：{not_resonant_cnt} 次 ({not_pct:.1f}%)

## 2. 使用者匿名文字觀察 (User Observations)
"""
    if observations:
        for idx, obs in enumerate(observations, 1):
            md_content += f"{idx}. **[{obs['date']}]** {obs['observation']}\n"
    else:
        md_content += "_目前無使用者提交文字觀察。_\n"
        
    output_filename = f"feedback_summary_{days}d.md"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"Feedback summary saved to: {output_path}")
    print(f"Total Feedback: {total_feedback}")
    print(f"  - Resonant: {resonant_cnt}")
    print(f"  - Partial: {partial_cnt}")
    print(f"  - Not Resonant: {not_resonant_cnt}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate feedback summary reports")
    parser.add_argument("--days", type=int, default=7, help="Range of days to summarize")
    args = parser.parse_args()
    generate_feedback_summary(args.days)
