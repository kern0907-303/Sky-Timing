# test_content_deduplication.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content_deduplication import jaccard_similarity, find_collision

def test_jaccard():
    print("Testing Jaccard Similarity...")
    s1 = "今日天地運行以【推進】為軸心，天地動能充沛，適合快速拓展。"
    s2 = "今日天地運行以【推進】為軸心，天地動能充實，適合快速拓展。"
    sim = jaccard_similarity(s1, s2)
    assert sim > 0.8
    print(f"  Similarity between highly similar texts: {sim:.4f}")
    
    s3 = "今天氣場穩定守恆，適合鞏固基礎工作。"
    sim_diff = jaccard_similarity(s1, s3)
    assert sim_diff < 0.5
    print(f"  Similarity between different texts: {sim_diff:.4f}")
    
    # Test find_collision
    history = [s1]
    assert find_collision(s2, history, threshold=0.78) is not None
    assert find_collision(s3, history, threshold=0.78) is None
    print("All Jaccard tests passed!")

if __name__ == "__main__":
    test_jaccard()
