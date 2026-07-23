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

def generate_weekly_chart(start_date_str):
    """
    Queries/generates the 7 days of the week starting from start_date_str,
    renders weekly_chart.html, and screenshots it to a PNG.
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
