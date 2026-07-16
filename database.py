# database.py
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_states.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create daily_states table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            timezone TEXT NOT NULL,
            city TEXT NOT NULL,
            raw_timing_data TEXT NOT NULL,
            semantic_vectors TEXT NOT NULL,
            primary_force TEXT NOT NULL,
            secondary_force TEXT NOT NULL,
            constraint_force TEXT NOT NULL,
            daily_rhythm TEXT NOT NULL,
            daily_summary TEXT NOT NULL,
            reflection_question TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(date, timezone, city)
        )
    """)
    # Create daily_feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_state_id INTEGER,
            date TEXT NOT NULL,
            reaction TEXT NOT NULL,
            observation TEXT,
            created_at TEXT NOT NULL,
            anonymous_session_id TEXT NOT NULL,
            UNIQUE(date, anonymous_session_id)
        )
    """)
    conn.commit()
    conn.close()

def save_daily_state(date_str, timezone, city, raw_timing, vectors, prim, sec, constr, rhythm, summary, question):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Use REPLACE to handle duplicate inserts for the same date/timezone/city
    cursor.execute("""
        INSERT OR REPLACE INTO daily_states (
            date, timezone, city, raw_timing_data, semantic_vectors,
            primary_force, secondary_force, constraint_force, daily_rhythm,
            daily_summary, reflection_question, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        date_str, timezone, city,
        json.dumps(raw_timing, ensure_ascii=False),
        json.dumps(vectors, ensure_ascii=False),
        prim, sec, constr, rhythm, summary, question, created_at
    ))
    conn.commit()
    conn.close()

def get_daily_state(date_str, timezone="Asia/Taipei", city="Taipei"):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, timezone, city, raw_timing_data, semantic_vectors,
               primary_force, secondary_force, constraint_force, daily_rhythm,
               daily_summary, reflection_question, created_at
        FROM daily_states
        WHERE date = ? AND timezone = ? AND city = ?
    """, (date_str, timezone, city))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "date": row[0],
            "timezone": row[1],
            "city": row[2],
            "raw_timing_data": json.loads(row[3]),
            "semantic_vectors": json.loads(row[4]),
            "primary_force": row[5],
            "secondary_force": row[6],
            "constraint_force": row[7],
            "daily_rhythm": row[8],
            "daily_summary": row[9],
            "reflection_question": row[10],
            "created_at": row[11]
        }
    return None

def get_all_daily_states():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, timezone, city, daily_summary, daily_rhythm, created_at
        FROM daily_states
        ORDER BY date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    states = []
    for r in rows:
        states.append({
            "date": r[0],
            "timezone": r[1],
            "city": r[2],
            "daily_summary": r[3],
            "daily_rhythm": r[4],
            "created_at": r[5]
        })
    return states

def save_feedback(date_str, reaction, observation, anonymous_session_id):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Try to find corresponding daily_state_id
    cursor.execute("SELECT id FROM daily_states WHERE date = ?", (date_str,))
    row = cursor.fetchone()
    state_id = row[0] if row else None
    
    try:
        cursor.execute("""
            INSERT INTO daily_feedback (
                daily_state_id, date, reaction, observation, created_at, anonymous_session_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (state_id, date_str, reaction, observation, created_at, anonymous_session_id))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # Already submitted feedback for this date with this session
        success = False
    conn.close()
    return success

def get_feedback_records(days=7):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, reaction, observation, created_at
        FROM daily_feedback
        WHERE date >= date('now', ?)
        ORDER BY date DESC, created_at DESC
    """, (f"-{days} days",))
    rows = cursor.fetchall()
    conn.close()
    return [{"date": r[0], "reaction": r[1], "observation": r[2], "created_at": r[3]} for r in rows]

def get_past_states_summaries(limit=14):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, daily_summary, reflection_question
        FROM daily_states
        ORDER BY date DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"date": r[0], "daily_summary": r[1], "reflection_question": r[2]} for r in rows]

if __name__ == "__main__":
    init_db()
    print("Database schema successfully initialized at", DB_PATH)
