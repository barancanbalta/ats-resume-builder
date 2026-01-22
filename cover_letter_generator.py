import datetime

TEMPLATE = """
{my_name}
{my_email} | {my_phone}
{today}

Hiring Manager
{company_name}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in {top_skill} and my passion for delivering high-quality results, I am confident in my ability to contribute effectively to your team.

In my previous experience, I have successfully demonstrated my expertise in {skills_list}. I admire {company_name}'s commitment to innovation and am eager to bring my problem-solving skills to help you achieve your goals.

I would welcome the opportunity to discuss how my background, energy, and enthusiasm would be a great match for this role. Thank you for your time and consideration.

Sincerely,

{my_name}
"""

def generate_cover_letter(cv_data, jd_text=""):
    """
    Generates a simple cover letter.
    """
    p = cv_data.get('personal', {})
    skills = cv_data.get('skills', {})
    
    # Extract simple skill list
    skill_list = []
    for k, v in skills.items():
        if v: skill_list.append(v.split(',')[0]) # Take first matched skill
    
    # Try to guess company name from JD (very naive)
    company_name = "[Company Name]"
    job_title = "[Job Title]"
    
    # If user provided short JD, we might not extract much without LLM.
    # We will return the template with placeholders filled as best as possible.
    
    return TEMPLATE.format(
        my_name=p.get('fullName', '[My Name]'),
        my_email=p.get('email', '[Email]'),
        my_phone=p.get('phone', '[Phone]'),
        today=datetime.date.today().strftime("%d %B %Y"),
        company_name=company_name,
        job_title=job_title,
        top_skill=skill_list[0] if skill_list else "[My Top Skill]",
        skills_list=", ".join(skill_list[:3]) if skill_list else "[Key Skills]"
    )
