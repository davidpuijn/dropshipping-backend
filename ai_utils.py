import json

def analyze_text(text, keywords):
    score = sum(1 for kw in keywords if kw in text.lower())
    if score >= 3:
        return "dropshipping", score
    elif score == 2:
        return "suspicious", score
    return "safe", score
