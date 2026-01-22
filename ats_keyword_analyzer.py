"""
ATS Keyword Density Analyzer
Analyzes CV content for keyword frequency and suggests improvements
"""

import re
from collections import Counter

# Data Analyst/Data Scientist için kritik ATS keyword'leri
CRITICAL_KEYWORDS = {
    'Technical Skills': [
        'Python', 'SQL', 'R', 'Machine Learning', 'Data Analysis',
        'Statistical Modeling', 'Data Visualization', 'ETL', 'Data Mining',
        'Time Series', 'Predictive Analytics', 'A/B Testing', 'Feature Engineering',
        'Deep Learning', 'Neural Network', 'Natural Language Processing', 'NLP',
        'Big Data', 'Hadoop', 'Spark', 'TensorFlow', 'PyTorch', 'Scikit-learn',
        'Pandas', 'NumPy', 'Tableau', 'Power BI', 'Excel', 'Git'
    ],
    'Methodologies': [
        'Agile', 'Scrum', 'Waterfall', 'CI/CD', 'DevOps', 'CRISP-DM',
        'Six Sigma', 'Lean', 'Kanban'
    ],
    'Business Skills': [
        'Stakeholder Management', 'Business Intelligence', 'KPI', 'ROI',
        'Data-Driven', 'Dashboard', 'Reporting', 'Analysis', 'Insights',
        'Strategy', 'Optimization', 'Forecasting', 'Problem Solving',
        'Communication', 'Collaboration', 'Leadership', 'Project Management'
    ],
    'Domains': [
        'Finance', 'Healthcare', 'E-commerce', 'Marketing', 'Operations',
        'Supply Chain', 'Insurance', 'Banking', 'Retail'
    ]
}

def extract_text_from_profile(profile):
    """Extract all text content from user profile"""
    text_parts = []

    # Personal summary
    if 'personal' in profile and 'summary' in profile['personal']:
        text_parts.append(profile['personal']['summary'])

    # Experience descriptions
    if 'experience' in profile:
        for exp in profile['experience']:
            if 'title' in exp:
                text_parts.append(exp['title'])
            if 'description' in exp:
                text_parts.append(exp['description'])

    # Education
    if 'education' in profile:
        for edu in profile['education']:
            if 'degree' in edu:
                text_parts.append(edu['degree'])

    # Skills
    if 'skills' in profile:
        for category, items in profile['skills'].items():
            text_parts.append(category)
            text_parts.append(items)

    return ' '.join(text_parts)

def analyze_keywords(profile):
    """Analyze keyword density in CV"""
    text = extract_text_from_profile(profile)

    # Clean and normalize text
    text = text.lower()

    results = {
        'found_keywords': {},
        'missing_keywords': {},
        'keyword_counts': {},
        'total_words': len(text.split()),
        'unique_keywords': 0
    }

    # Analyze each category
    for category, keywords in CRITICAL_KEYWORDS.items():
        results['found_keywords'][category] = []
        results['missing_keywords'][category] = []

        for keyword in keywords:
            # Case-insensitive search
            keyword_lower = keyword.lower()
            count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text))

            if count > 0:
                results['found_keywords'][category].append({
                    'keyword': keyword,
                    'count': count
                })
                results['keyword_counts'][keyword] = count
            else:
                results['missing_keywords'][category].append(keyword)

    results['unique_keywords'] = len(results['keyword_counts'])

    return results

def generate_report(profile):
    """Generate a comprehensive ATS keyword analysis report"""
    results = analyze_keywords(profile)

    report = []
    report.append("=" * 80)
    report.append("ATS KEYWORD DENSITY ANALYSIS")
    report.append("=" * 80)
    report.append("")

    # Summary Stats
    report.append("📊 ÖZET İSTATİSTİKLER")
    report.append("-" * 80)
    report.append(f"Toplam Kelime Sayısı: {results['total_words']}")
    report.append(f"Benzersiz ATS Keyword: {results['unique_keywords']}")
    total_possible = sum(len(keywords) for keywords in CRITICAL_KEYWORDS.values())
    coverage = (results['unique_keywords'] / total_possible) * 100
    report.append(f"Keyword Coverage: {coverage:.1f}% ({results['unique_keywords']}/{total_possible})")
    report.append("")

    # Top Keywords
    report.append("🏆 EN SIKKULLANILAN KEYWORD'LER (Top 15)")
    report.append("-" * 80)
    top_keywords = sorted(results['keyword_counts'].items(), key=lambda x: x[1], reverse=True)[:15]
    for keyword, count in top_keywords:
        bar = "█" * min(count, 20)
        report.append(f"{keyword:35} {bar} {count}x")
    report.append("")

    # Category Analysis
    for category in CRITICAL_KEYWORDS.keys():
        found = results['found_keywords'][category]
        missing = results['missing_keywords'][category]

        if found:
            report.append(f"✅ {category.upper()} - Bulunan ({len(found)})")
            report.append("-" * 80)
            for item in sorted(found, key=lambda x: x['count'], reverse=True)[:10]:
                report.append(f"  • {item['keyword']:30} ({item['count']}x)")
            report.append("")

        if missing and category in ['Technical Skills', 'Business Skills']:
            report.append(f"⚠️  {category.upper()} - Eksik ({len(missing)})")
            report.append("-" * 80)
            report.append(f"  Eklenebilecek keyword'ler: {', '.join(missing[:10])}")
            if len(missing) > 10:
                report.append(f"  ... ve {len(missing) - 10} tane daha")
            report.append("")

    # Recommendations
    report.append("💡 ÖNERİLER")
    report.append("-" * 80)

    if coverage < 30:
        report.append("  🔴 DÜŞÜK: Keyword coverage çok düşük! Daha fazla teknik terim ekleyin.")
    elif coverage < 50:
        report.append("  🟡 ORTA: İyi bir başlangıç, ancak daha fazla keyword eklenebilir.")
    else:
        report.append("  🟢 İYİ: Keyword coverage yeterli seviyede!")

    report.append("")
    report.append("  1. En önemli eksik keyword'leri 'Skills' veya açıklamalara ekleyin")
    report.append("  2. Teknik terimleri açıklamalarda doğal bir şekilde kullanın")
    report.append("  3. Başarılarınızı anlatırken sektör jargonunu kullanın")
    report.append("  4. Her keyword'ü en az 1-2 kez kullanmaya çalışın (spam yapmadan!)")
    report.append("")
    report.append("=" * 80)

    return "\n".join(report)

if __name__ == "__main__":
    from user_data import user_profile
    report = generate_report(user_profile)
    print(report)

    # Save to file
    with open('ATS_Keyword_Analysis.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n📄 Rapor 'ATS_Keyword_Analysis.txt' dosyasına kaydedildi!")
