# test_daily_generation.py
import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate_daily_state import run_generation
from database import DB_PATH, get_daily_state

def test_generation():
    print("Running test_generation...")
    # Clean up test entry if exists
    test_date = "2026-12-25"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_states WHERE date = ?", (test_date,))
    conn.commit()
    conn.close()
    
    # Run generation
    run_generation(test_date)
    
    # Assert DB has it
    res = get_daily_state(test_date)
    assert res is not None
    assert res["date"] == test_date
    assert res["primary_force"] != ""
    assert res["daily_rhythm"] != ""
    assert len(res["daily_summary"]) > 0
    
    print("  Saved state summary:", res["daily_summary"])
    print("Test daily generation passed!")

if __name__ == "__main__":
    test_generation()
