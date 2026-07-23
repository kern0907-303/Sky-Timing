# test_feedback_api.py
import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DB_PATH, save_feedback, get_feedback_records, get_all_daily_states

def test_feedback_logic():
    print("Testing feedback database storage...")
    
    # 1. Clean test feedback entries
    test_date = "2026-07-15"
    test_session = "test_session_uuid_12345"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_feedback WHERE date = ? AND anonymous_session_id = ?", (test_date, test_session))
    conn.commit()
    conn.close()
    
    # 2. Save feedback
    success = save_feedback(
        date_str=test_date,
        reaction="resonant",
        observation="今天感覺真的很推進，項目開展很順利！",
        anonymous_session_id=test_session
    )
    assert success is True
    print("  First feedback submission: Success")
    
    # 3. Duplicate check / Update check (allow updating feedback for same date with same session)
    success_dup = save_feedback(
        date_str=test_date,
        reaction="partial",
        observation="已修改為部分有感",
        anonymous_session_id=test_session
    )
    assert success_dup is True
    print("  Feedback update/overwrite: Success")
    
    # 4. Fetch records and verify update
    records = get_feedback_records(days=7)
    assert len(records) > 0
    found_test = False
    for r in records:
        if r["date"] == test_date:
            found_test = True
            assert r["reaction"] == "partial"
            assert r["observation"] == "已修改為部分有感"
            print("  Retrieved updated observation:", r["observation"])
            break
    assert found_test is True
    print("All feedback logic tests passed successfully!")

if __name__ == "__main__":
    test_feedback_logic()
