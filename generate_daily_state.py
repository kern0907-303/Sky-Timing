# generate_daily_state.py
import argparse
from datetime import datetime
import json

# Standard timezone offset helper (simulate local time in Asia/Taipei)
from timing_calculator import calculate_daily_timing
from semantic_state_engine import compute_semantic_vectors
from daily_interpretation import generate_daily_content
from database import save_daily_state

def run_generation(date_str, timezone="Asia/Taipei", city="Taipei"):
    print(f"Generating daily timing state for date={date_str}, timezone={timezone}, city={city}...")
    
    # 1. Compute raw timing
    timing = calculate_daily_timing(date_str, timezone, city)
    
    # 2. Compute semantic vectors & forces
    vectors, forces = compute_semantic_vectors(timing)
    
    # 3. Generate daily report content
    content = generate_daily_content(date_str, timing, vectors, forces)
    
    # 4. Save to SQLite database
    save_daily_state(
        date_str, timezone, city,
        timing, vectors,
        forces["primary_force"], forces["secondary_force"], forces["constraint_force"],
        content["daily_rhythm"], content["summary"], content["question"]
    )
    
    # Write details to file for verification if needed
    print(f"Daily state for {date_str} saved successfully.")
    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate daily timing state for Qin Tian Jian")
    parser.add_argument("--date", type=str, help="ISO Date YYYY-MM-DD (e.g. 2026-07-15)")
    parser.add_argument("--timezone", type=str, default="Asia/Taipei", help="Timezone offset name")
    parser.add_argument("--city", type=str, default="Taipei", help="City name")
    
    args = parser.parse_args()
    
    date_str = args.date
    if not date_str:
        # Default to current date in Taipei timezone (which is current UTC date or local system date)
        # In Taiwan, local time is UTC+8. So we add 8 hours to UTC.
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        
    run_generation(date_str, args.timezone, args.city)
