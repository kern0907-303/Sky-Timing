# test_semantic_state_engine.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from timing_calculator import calculate_daily_timing
from semantic_state_engine import compute_semantic_vectors

def test_vectors():
    print("Running test_vectors...")
    timing = calculate_daily_timing("2026-07-15")
    vec, forces = compute_semantic_vectors(timing)
    
    assert len(vec) == 8
    for k, v in vec.items():
        assert 0.0 <= v <= 1.0
        
    assert "primary_force" in forces
    assert "secondary_force" in forces
    assert "constraint_force" in forces
    assert "inner_contradiction" in forces
    
    print("  Primary Force:", forces["primary_force"])
    print("  Secondary Force:", forces["secondary_force"])
    print("Test semantic vectors passed!")

if __name__ == "__main__":
    test_vectors()
