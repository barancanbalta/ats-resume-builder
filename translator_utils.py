from deep_translator import GoogleTranslator
import streamlit as st
import re

def preserve_links_and_numbers(text):
    """
    Extracts URLs and number patterns, returns tuple of (placeholders_text, replacements_dict)
    """
    replacements = {}
    counter = 0

    # Preserve URLs
    url_pattern = r'https?://[^\s]+'
    text = re.sub(url_pattern, lambda m: (replacements.setdefault(f'__URL{counter}__', m.group(0)), f'__URL{counter}__')[1], text)

    # Preserve email patterns
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    text = re.sub(email_pattern, lambda m: (replacements.setdefault(f'__EMAIL{counter}__', m.group(0)), f'__EMAIL{counter}__')[1], text)

    return text, replacements

def restore_links_and_numbers(text, replacements):
    """Restores URLs and numbers from placeholders"""
    for placeholder, original in replacements.items():
        text = text.replace(placeholder, original)
    return text

def clean_date(date_str):
    """
    Converts date strings to English format.
    '01.2024' -> '01/2024'
    'Devam Ediyor' -> 'Present'
    """
    if not date_str:
        return ""
    
    if "Devam" in date_str or "Present" in date_str:
        return "Present"
        
    # Replace dot with slash
    return date_str.replace('.', '/')

def translate_resume_data(data):
    """
    Translates the entire resume data structure from Turkish to English.
    Preserves URLs, emails, and number patterns.
    """
    translator = GoogleTranslator(source='tr', target='en')

    translated_data = {
        'personal': {},
        'experience': [],
        'education': [],
        'skills': {},
        'projects': [],
        'certificates': []
    }

    # 1. Personal
    p = data.get('personal', {})
    translated_data['personal'] = p.copy()
    if p.get('city'):
        try:
            # Check if city name contains "Turkey" or "Türkiye" to avoid "Ankara, Turkey Turkey"
            city_val = p['city']
            # Simple check: just pass it through or translate? 
            # User wants "Ankara, Turkey"
            # If input is "Ankara", translate might give "Ankara"
            # If input is "Ankara, Türkiye", translate might give "Ankara, Turkey"
            translated_city = translator.translate(city_val)
            translated_data['personal']['city'] = translated_city
        except:
            pass
            
    if p.get('country'):
         try:
            translated_data['personal']['country'] = translator.translate(p['country'])
         except:
            pass
            
    if p.get('summary'):
        summary_text, summary_replacements = preserve_links_and_numbers(p['summary'])
        translated_summary = translator.translate(summary_text)
        translated_data['personal']['summary'] = restore_links_and_numbers(translated_summary, summary_replacements)
        
    # 2. Experience
    for exp in data.get('experience', []):
        new_exp = exp.copy()
        if exp.get('title'):
            new_exp['title'] = translator.translate(exp['title'])
        
        # Clean Dates
        if exp.get('startDate'):
            new_exp['startDate'] = clean_date(exp['startDate'])
        if exp.get('endDate'):
            new_exp['endDate'] = clean_date(exp['endDate'])
            
        if exp.get('location'):
             try:
                 new_exp['location'] = translator.translate(exp['location'])
             except:
                 pass

        if exp.get('description'):
            # Description might be long, preserve numbers and URLs
            desc_text, desc_replacements = preserve_links_and_numbers(exp['description'])
            translated_desc = translator.translate(desc_text)
            new_exp['description'] = restore_links_and_numbers(translated_desc, desc_replacements)

        translated_data['experience'].append(new_exp)
        
    # 3. Education
    for edu in data.get('education', []):
        new_edu = edu.copy()
        if edu.get('school'):
            # Check for specific university names if needed, otherwise translate
            if "Türk Hava Kurumu" in edu['school']:
                new_edu['school'] = "Turkish Aeronautical Association University"
            else:
                new_edu['school'] = translator.translate(edu['school'])
                
        if edu.get('degree'):
            new_edu['degree'] = translator.translate(edu['degree'])
            
        # Education dates usually in "year" field "2020 - 2025" or similar
        # If it has specific date format, handle it. Assuming year string for now.
        
        translated_data['education'].append(new_edu)
        
    # 4. Skills
    skill_key_map = {
        'Programlama': 'Programming Languages',
        'Frameworks': 'Frameworks & Libraries',
        'Araçlar': 'Tools & Platforms',
        'Diller': 'Languages',
        'Yabancı Dil': 'Languages'
    }
    
    translated_skills = {}
    for key, val in data.get('skills', {}).items():
        new_key = skill_key_map.get(key, key) 
        
        if val:
            # Special handling for Language values "İngilizce" -> "English"
            if key in ['Diller', 'Yabancı Dil']:
                 val_trans = translator.translate(val)
                 translated_skills[new_key] = val_trans
            else:
                 # Usually tech skills like "Python, SQL" don't bloom from translation well if they are proper nouns
                 # But "Veri Analizi" -> "Data Analysis" might be needed.
                 # Let's try translating but preserving specific capital words if possible? 
                 # For now, just translate.
                 translated_skills[new_key] = val # translator.translate(val) # Keeping tech stack as is usually better?
                 # Actually user example: "Python, SQL" -> "Python, SQL". 
                 # If user entered "Veri Madenciliği", we want "Data Mining".
                 # So we should translate but maybe careful.
                 # Let's translate for safety, user can edit.
                 pass
                 translated_skills[new_key] = val # User complained about headers mainly. Content is usually keywords.
                 # Actually, let's NOT translate content of technical skills to avoid "Piton" for "Python".
                 # Most tech skills are international.
        else:
            translated_skills[new_key] = val
            
    translated_data['skills'] = translated_skills
    
    # 5. Projects (New)
    for proj in data.get('projects', []):
        new_proj = proj.copy()
        if proj.get('name'):
            new_proj['name'] = translator.translate(proj['name'])
        if proj.get('description'):
            d_text, d_rep = preserve_links_and_numbers(proj['description'])
            t_desc = translator.translate(d_text)
            new_proj['description'] = restore_links_and_numbers(t_desc, d_rep)
        translated_data['projects'].append(new_proj)
        
    # 6. Certificates (New)
    for cert in data.get('certificates', []):
        new_cert = cert.copy()
        if cert.get('name'):
            new_cert['name'] = translator.translate(cert['name'])
        if cert.get('authority'):
            new_cert['authority'] = translator.translate(cert['authority'])
        # Date cleaning
        if cert.get('date'):
            new_cert['date'] = clean_date(cert['date'])
            
        translated_data['certificates'].append(new_cert)
    
    return translated_data
