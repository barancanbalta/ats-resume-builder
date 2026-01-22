import re
from collections import Counter

# Common stopwords to ignore (Turkish & English mix for safety)
STOPWORDS = set([
    "ve", "ile", "için", "bir", "bu", "şu", "o", "ama", "fakat", "lakin",
    "the", "and", "or", "for", "in", "to", "a", "an", "of", "with",
    "deneyim", "yıl", "tecrübe", "bilgisi", "yetkinliği", "sahip",
    "iş", "tanımı", "sorumluluklar", "aranan", "nitelikler", "aday",
    "experience", "years", "knowledge", "skills", "qualifications",
    "job", "description", "candidate", "work", "looking", "we", "are"
])

def extract_keywords(text: str, top_n: int = 20) -> list:
    """
    Extracts most frequent relevant words from text.
    """
    text = text.lower()
    # Remove special chars
    text = re.sub(r'[^a-zA-ZğüşıöçĞÜŞİÖÇ\s]', ' ', text)
    
    words = text.split()
    # Filter stopwords and short words
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    
    counts = Counter(filtered_words)
    return [item[0] for item in counts.most_common(top_n)]

def compare_keywords(jd_text: str, cv_data: dict) -> dict:
    """
    Compares JD text with CV content.
    Returns: {
        'jd_keywords': [],
        'matches': [],
        'missing': [],
        'match_score': int
    }
    """
    # 1. Analyze JD
    jd_kw = set(extract_keywords(jd_text, top_n=30))
    
    # 2. Analyze CV
    cv_text = ""
    # Personal Summary
    cv_text += cv_data.get('personal', {}).get('summary', '') + " "
    # Experience
    for exp in cv_data.get('experience', []):
        cv_text += f"{exp.get('title','')} {exp.get('company','')} {exp.get('description','')} "
    # Education
    for edu in cv_data.get('education', []):
        cv_text += f"{edu.get('school','')} {edu.get('degree','')} "
    # Skills
    for items in cv_data.get('skills', {}).values():
        cv_text += f"{items} "
        
    cv_kw = set(extract_keywords(cv_text, top_n=100))
    
    # 3. Compare
    matches = jd_kw.intersection(cv_kw)
    missing = jd_kw.difference(cv_kw)
    
    score = 0
    if jd_kw:
        score = int((len(matches) / len(jd_kw)) * 100)
    
    return {
        'jd_keywords': sorted(list(jd_kw)),
        'matches': sorted(list(matches)),
        'missing': sorted(list(missing)),
        'match_score': score
    }
