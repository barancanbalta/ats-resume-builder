import re

# Dictionary of weak words -> strong alternatives
IMPROVEMENTS = {
    "made": ["Built", "Created", "Constructed", "Formulated"],
    "did": ["Executed", "Performed", "Conducted"],
    "looked after": ["Managed", "Supervised", "Oversaw"],
    "helped": ["Assisted", "Facilitated", "Collaborated with", "Supported"],
    "responsible for": ["Led", "Managed", "In charge of", "Directed"],
    "worked on": ["Contributed to", "Participated in", "Engaged in"],
    "changed": ["Transformed", "Modified", "Improved", "Optimized"],
    "fix": ["Resolve", "Troubleshoot", "Rectify"],
    "use": ["Utilize", "Leverage", "Employ"],
    "talk": ["Negotiate", "Communicate", "Present"]
}

def suggest_improvements(text):
    """
    Analyzes text and returns a list of suggestions.
    Returns: [{'original': 'made', 'suggestions': ['Built', ...]}, ...]
    """
    suggestions = []
    if not text:
        return suggestions
        
    # Simple tokenization by checking presence of keys
    # Use word boundaries to avoid matching substrings
    for weak, strong_list in IMPROVEMENTS.items():
        pattern = r'\b' + re.escape(weak) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            suggestions.append({
                'original': weak,
                'suggestions': strong_list
            })
            
    return suggestions
