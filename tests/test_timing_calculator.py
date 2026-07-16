# test_timing_calculator.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from timing_calculator import calculate_daily_timing

def test_timing_calculation():
    print("Running test_timing_calculation...")
    res = calculate_daily_timing("2026-07-15")
    
    # Assertions
    assert "solar_date" in res
    assert res["solar_date"] == "2026-07-15"
    assert "lunar_date" in res
    assert "jianchu" in res
    assert "zhishen" in res
    assert "xiu" in res
    assert "clash" in res
    
    print("  lunar_date:", res["lunar_date"])
    assert len(res["lunar_date"]) > 0
    print("Test timing calculation passed!")

if __name__ == "__main__":
    test_timing_calculation()
