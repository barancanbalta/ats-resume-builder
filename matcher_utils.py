import re
from collections import Counter

STOP_WORDS_TR = {
    've', 'veya', 'ile', 'için', 'bir', 'bu', 'şu', 'o', 'de', 'da', 'ki', 'mi', 'mu', 'ama', 'fakat', 
    'lakin', 'ancak', 'belki', 'çünkü', 'eğer', 'gibi', 'kadar', 'tümü', 'bazı', 'her', 'şey', 'ben', 'sen', 
    'biz', 'siz', 'onlar', 'bizi', 'sizi', 'onları', 'bize', 'size', 'onlara', 'var', 'yok', 'ol', 'olmak', 
    'yapmak', 'etmek', 'iş', 'çalışma', 'deneyim', 'yıl', 'aranıyor', 'iş', 'tanımı', 'fırsatı', 'hakkında', 
    'genel', 'nitelikler', 'aday', 'başvuru', 'konusunda', 'ilgili', 'üzere', 'tarafından'
}

STOP_WORDS_EN = {
    'and', 'or', 'with', 'for', 'a', 'an', 'the', 'is', 'are', 'was', 'were', 'to', 'in', 'on', 'at', 'by', 
    'this', 'that', 'it', 'be', 'as', 'but', 'if', 'of', 'from', 'so', 'can', 'will', 'my', 'your', 'we', 'they', 
    'job', 'work', 'experience', 'years', 'looking', 'description', 'about', 'qualifications', 'requirements', 
    'candidate', 'apply', 'role', 'team', 'skills', 'ability', 'knowledge', 'proficiency'
}

def clean_text(text):
    text = text.lower()
    # Remove special chars but keep hashtags for things like C# or .NET might use special chars
    # For simplicity, remove non-alphanumeric except + and #
    text = re.sub(r'[^a-z0-9\s\+#üğışçö]', ' ', text)
    return text

def extract_keywords(text, language='tr'):
    cleaned = clean_text(text)
    words = cleaned.split()
    
    stop_words = STOP_WORDS_TR if language == 'tr' else STOP_WORDS_EN
    
    # Filter stopwords and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords

def calculate_match_score(resume_text, job_desc, language='tr'):
    resume_keywords = set(extract_keywords(resume_text, language))
    job_keywords = extract_keywords(job_desc, language)
    
    # Job keywords frequency to determine importance
    job_counts = Counter(job_keywords)
    
    # Analyze
    total_job_terms = len(job_counts)
    if total_job_terms == 0:
        return 0, [], []
        
    matched = []
    missing = []
    
    for term, count in job_counts.most_common(20): # Top 20 most frequent keywords in job desc
        if term in resume_keywords:
            matched.append(term)
        else:
            missing.append(term)
            
    # Simple score: (matched / total_top_20) * 100
    # Actually, let's look at top 20 ONLY for scoring to be meaningful
    relevant_terms_count = len(matched) + len(missing)
    if relevant_terms_count == 0:
        score = 0
    else:
        score = (len(matched) / relevant_terms_count) * 100
        
    return int(score), matched, missing

def get_resume_text(data):
    """
    Converts structured JSON resume data into a single string for analysis.
    """
    text = []
    
    # Personal
    p = data.get('personal', {})
    text.append(p.get('summary', ''))
    
    # Experience
    for exp in data.get('experience', []):
        text.append(exp.get('title', ''))
        text.append(exp.get('description', ''))
        
    # Skills
    for cat, items in data.get('skills', {}).items():
        text.append(items)
        
    # Education
    for edu in data.get('education', []):
        text.append(edu.get('degree', ''))
        text.append(edu.get('school', ''))
        
    return " ".join(text)
