"""
Alternative Summary Versions for Different ATS Systems
Some ATS systems prefer shorter summaries (3-5 sentences)
"""

# Mevcut Summary (Uzun Versiyon - 6 cümle)
ORIGINAL_SUMMARY = """
Endüstri Mühendisliği mezunu (GPA: 3.43/4.00, Bölüm 1., Fakülte 3.) Data Analyst & Data Scientist olarak finansal modelleme, predictive analytics ve business intelligence çözümleri geliştiriyorum. Python ekosisteminde (Pandas, NumPy, Scikit-learn, Streamlit) Time Series Analysis, Feature Engineering ve Ensemble Methods kullanarak SARIMA, LSTM ve hibrit makine öğrenimi modelleri tasarlayıp 300.000+ satırlık veri setlerinde ölçülebilir sonuçlar ürettim. Sigortambudur'da ETL pipeline'ları ve fuzzy matching algoritmaları ile end-to-end otomasyon sistemi inşa ederek raporlama doğruluğunu %100'e çıkardım ve interaktif data visualization platformu geliştirdim. SQL, statistical modeling, data pipeline orchestration ve stakeholder management ile karmaşık iş süreçlerini otomatize ediyor, veri odaklı karar mekanizmalarını güçlendiriyorum.
"""

# Kısa Versiyon 1: 3 Cümle (ATS-Optimized)
SHORT_V1 = """
Data Analyst & Data Scientist with Industrial Engineering background (GPA: 3.43/4.00) specializing in financial modeling, predictive analytics, and business intelligence solutions. Proficient in Python ecosystem (Pandas, NumPy, Scikit-learn, Streamlit) with hands-on experience developing SARIMA, LSTM, and hybrid ML models for 300,000+ record datasets. Built end-to-end ETL pipelines and interactive dashboards, achieving 100% reporting accuracy while automating complex business processes through data-driven decision frameworks.
"""

# Kısa Versiyon 2: 4 Cümle (Balanced)
SHORT_V2 = """
Results-driven Data Analyst with Industrial Engineering degree (GPA: 3.43/4.00, Ranked 1st in Department) and expertise in financial modeling and predictive analytics. Skilled in Python (Pandas, NumPy, Scikit-learn, Streamlit), SQL, and statistical modeling for building Time Series forecasting models (SARIMA, LSTM) and interactive BI dashboards. At Sigortambudur, developed ETL pipelines processing 300,000+ insurance records, implemented fuzzy matching algorithms improving data quality to 99%, and reduced reporting time by 80% through automation. Passionate about transforming complex datasets into actionable insights that drive strategic business decisions.
"""

# Kısa Türkçe Versiyon: 3 Cümle
SHORT_TR = """
Endüstri Mühendisliği mezunu (GPA: 3.43/4.00, Bölüm 1.) Data Analyst olarak finansal modelleme ve predictive analytics alanında uzmanlaştım. Python (Pandas, Scikit-learn, Streamlit), SQL ve statistical modeling ile SARIMA/LSTM tabanlı zaman serisi modelleri ve interaktif BI dashboard'ları geliştiriyorum. 300.000+ kayıtlık veri setlerinde %100 doğruluk sağlayan ETL pipeline'ları kurarak raporlama süresini %80 azalttım ve veri odaklı karar mekanizmalarını güçlendirdim.
"""

# Ultra-Compact Versiyon: 2 Cümle (LinkedIn-Style)
ULTRA_SHORT = """
Data Analyst specializing in predictive analytics and ML-driven business intelligence. Python expert with proven track record in building ETL pipelines, Time Series models (SARIMA/LSTM), and dashboards that delivered 80% efficiency gains on 300K+ datasets.
"""

def get_summary(version='original', language='tr'):
    """
    Get summary based on version and language

    Args:
        version: 'original', 'short_v1', 'short_v2', 'short_tr', 'ultra'
        language: 'tr' or 'en'
    """
    summaries = {
        'original': {
            'tr': ORIGINAL_SUMMARY.strip(),
            'en': SHORT_V1.strip()  # English original is same as short_v1
        },
        'short_v1': {
            'en': SHORT_V1.strip(),
            'tr': SHORT_TR.strip()
        },
        'short_v2': {
            'en': SHORT_V2.strip(),
            'tr': SHORT_TR.strip()
        },
        'ultra': {
            'en': ULTRA_SHORT.strip(),
            'tr': SHORT_TR.strip()
        }
    }

    return summaries.get(version, summaries['original']).get(language, ORIGINAL_SUMMARY.strip())

def print_all_versions():
    """Print all summary versions for comparison"""
    print("=" * 80)
    print("SUMMARY ALTERNATIVES")
    print("=" * 80)
    print()

    print("📝 ORIGINAL (Turkish - Long)")
    print("-" * 80)
    print(ORIGINAL_SUMMARY.strip())
    print(f"\nKarakter Sayısı: {len(ORIGINAL_SUMMARY.strip())}")
    print(f"Kelime Sayısı: {len(ORIGINAL_SUMMARY.split())}")
    print()

    print("📝 SHORT V1 (English - 3 Sentences, ATS-Optimized)")
    print("-" * 80)
    print(SHORT_V1.strip())
    print(f"\nKarakter Sayısı: {len(SHORT_V1.strip())}")
    print(f"Kelime Sayısı: {len(SHORT_V1.split())}")
    print()

    print("📝 SHORT V2 (English - 4 Sentences, Balanced)")
    print("-" * 80)
    print(SHORT_V2.strip())
    print(f"\nKarakter Sayısı: {len(SHORT_V2.strip())}")
    print(f"Kelime Sayısı: {len(SHORT_V2.split())}")
    print()

    print("📝 SHORT TR (Turkish - 3 Sentences)")
    print("-" * 80)
    print(SHORT_TR.strip())
    print(f"\nKarakter Sayısı: {len(SHORT_TR.strip())}")
    print(f"Kelime Sayısı: {len(SHORT_TR.split())}")
    print()

    print("📝 ULTRA SHORT (English - 2 Sentences, LinkedIn-Style)")
    print("-" * 80)
    print(ULTRA_SHORT.strip())
    print(f"\nKarakter Sayısı: {len(ULTRA_SHORT.strip())}")
    print(f"Kelime Sayısı: {len(ULTRA_SHORT.split())}")
    print()

    print("=" * 80)
    print("💡 KULLANIM:")
    print("-" * 80)
    print("• ORIGINAL: Detaylı başvurular, kişisel web sitesi")
    print("• SHORT V1: Çoğu ATS sistemi için ideal (3 cümle)")
    print("• SHORT V2: İnsan okuyucular için daha akıcı (4 cümle)")
    print("• SHORT TR: Türkçe başvurular için (3 cümle)")
    print("• ULTRA SHORT: LinkedIn, online profiller, hızlı tarama")
    print("=" * 80)

if __name__ == "__main__":
    print_all_versions()
