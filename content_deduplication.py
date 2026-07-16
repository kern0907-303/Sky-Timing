# content_deduplication.py
import re

def jaccard_similarity(str1, str2):
    """
    Computes character-level Jaccard similarity between two strings.
    Filters out spaces and punctuation.
    """
    if not str1 or not str2:
        return 0.0
    
    # Filter out non-alphanumeric/non-Chinese characters
    s1 = re.sub(r'[^\w]', '', str1)
    s2 = re.sub(r'[^\w]', '', str2)
    
    if not s1 or not s2:
        return 0.0
        
    set1 = set(s1)
    set2 = set(s2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return len(intersection) / len(union) if union else 0.0

def find_collision(candidate, history_list, threshold=0.78):
    """
    Checks if the candidate text has a similarity >= threshold with any item in history_list.
    Returns the colliding item if found, otherwise None.
    """
    for hist in history_list:
        if not hist:
            continue
        sim = jaccard_similarity(candidate, hist)
        if sim >= threshold:
            return hist
    return None

def deduplicate_text(field_name, primary_key, original_text, history_list, alternatives_func, threshold=0.78, max_attempts=5):
    """
    Attempts to generate a non-colliding version of a text using the alternatives_func.
    """
    attempt = 0
    candidate = original_text
    while find_collision(candidate, history_list, threshold) is not None and attempt < max_attempts:
        candidate = alternatives_func(primary_key, attempt)
        attempt += 1
    return candidate

if __name__ == "__main__":
    s1 = "今日天地運行以【推進】為軸心，天地動能充沛，適合快速拓展。"
    s2 = "今日天地運行以【推進】為軸心，天地動能充足，適合快速擴張。"
    sim = jaccard_similarity(s1, s2)
    print(f"Similarity: {sim:.4f} (Expected to be high)")
