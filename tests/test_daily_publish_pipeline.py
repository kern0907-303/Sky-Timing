# test_daily_publish_pipeline.py
import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daily_publish_pipeline import run_publish_pipeline, OUTPUTS_ROOT

def test_pipeline():
    print("Testing Daily Publish Pipeline...")
    test_date = "2026-07-22"
    
    # 1. Clean output directory if exists
    target_dir = os.path.join(OUTPUTS_ROOT, test_date)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        
    # 2. Run pipeline
    payload = run_publish_pipeline(test_date)
    
    # 3. Assertions
    assert payload["date"] == test_date
    assert os.path.exists(target_dir)
    assert os.path.exists(os.path.join(target_dir, "daily_state.json"))
    assert os.path.exists(os.path.join(target_dir, "daily_web.md"))
    assert os.path.exists(os.path.join(target_dir, "daily_social_post.txt"))
    assert os.path.exists(os.path.join(target_dir, "daily_short_message.txt"))
    assert os.path.exists(os.path.join(target_dir, "daily_share_card.png"))
    
    print("  Successfully generated all outputs including share card PNG!")
    print("Test daily publish pipeline passed!")

if __name__ == "__main__":
    test_pipeline()
