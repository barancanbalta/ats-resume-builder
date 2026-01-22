from fpdf import FPDF
import os

class BaseResumePDF(FPDF):
    def __init__(self, language='tr'):
        super().__init__()
        self.language = language
        # For English, use tighter layout to prevent text overflow
        margin = 12 if language == 'en' else 15
        self.set_auto_page_break(auto=True, margin=margin)
        
        # Localized Headers
        self.labels = {
            'tr': {
                'SUMMARY': "ÖZET",
                'EXPERIENCE': "İŞ DENEYİMİ",
                'EDUCATION': "EĞİTİM",
                'SKILLS': "TEKNİK BECERİLER",
                'EXPERIENCE_ACADEMIC': "PROFESYONEL DENEYİM",
                'EDUCATION_ACADEMIC': "EĞİTİM GEÇMİŞİ",
                'SKILLS_ACADEMIC': "YETKİNLİKLER",
                'EXPERIENCE_MODERN': "DENEYİM",
                'EDUCATION_MODERN': "EĞİTİM",
                'SKILLS_MODERN': "YETENEKLER",
                'PROJECTS': "PROJELER",
                'CERTIFICATES': "SERTİFİKALAR ve EĞİTİMLER"
            },
            'en': {
                'SUMMARY': "SUMMARY",
                'EXPERIENCE': "EXPERIENCE",
                'EDUCATION': "EDUCATION",
                'SKILLS': "TECHNICAL SKILLS",
                'EXPERIENCE_ACADEMIC': "PROFESSIONAL EXPERIENCE",
                'EDUCATION_ACADEMIC': "EDUCATION HISTORY",
                'SKILLS_ACADEMIC': "COMPETENCIES",
                'EXPERIENCE_MODERN': "EXPERIENCE",
                'EDUCATION_MODERN': "EDUCATION",
                'SKILLS_MODERN': "SKILLS",
                'PROJECTS': "PROJECTS",
                'CERTIFICATES': "CERTIFICATIONS & TRAINING"
            }
        }
        
        # Font setup
        font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
        
        # Prefer Roboto if available (better for TR)
        regular_font = os.path.join(font_dir, 'Roboto-Regular.ttf')
        bold_font = os.path.join(font_dir, 'Roboto-Bold.ttf')
        italic_font = os.path.join(font_dir, 'Roboto-Italic.ttf')
        
        # Fallback to DejaVu if Roboto missing
        if not os.path.exists(regular_font):
             regular_font = os.path.join(font_dir, 'DejaVuSans.ttf')
             bold_font = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
             italic_font = os.path.join(font_dir, 'DejaVuSans-Oblique.ttf')

        if os.path.exists(regular_font):
            self.add_font('DejaVu', '', regular_font, uni=True)
            
            # Bold Logic
            if os.path.exists(bold_font):
                self.add_font('DejaVu', 'B', bold_font, uni=True)
            else:
                self.add_font('DejaVu', 'B', regular_font, uni=True)
            
            # Italic Logic
            if os.path.exists(italic_font):
                self.add_font('DejaVu', 'I', italic_font, uni=True)

            self.main_font = 'DejaVu'
            self.set_font(self.main_font, '', 11)
        else:
            # System fallback
            self.main_font = "Arial"
            self.set_font(self.main_font, size=11)
            
        # Initial bold set for testing (optional, removed to avoid error if bold missing)
        # self.set_font(self.main_font, 'B', 12)

    def header(self):
        pass

    def add_section_title(self, title):
        raise NotImplementedError

    def add_personal_info(self, data):
        raise NotImplementedError
        
    def add_experience(self, experience_list):
        raise NotImplementedError
        
    def add_education(self, education_list):
        raise NotImplementedError
        
    def add_skills(self, skills_dict):
        raise NotImplementedError

    def add_projects(self, projects_list):
        raise NotImplementedError

    def add_certificates(self, certificates_list):
        raise NotImplementedError

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def generate(self, data, theme_color="#19375f"):
        # Set Theme Color
        self.primary_color = self._hex_to_rgb(theme_color)
        
        # Set Metadata for ATS
        p = data.get('personal', {})
        full_name = p.get('fullName', 'Resume')
        self.set_title(f"{full_name} - CV")
        self.set_author(full_name)
        self.set_creator("ATS Resume Builder")
        self.set_subject(f"Resume / CV of {full_name}")
        
        # Inject Keywords for ATS
        keywords = []
        if data.get('skills'):
            for cat, items in data['skills'].items():
                if items:
                    keywords.append(f"{cat}: {items}")
        
        if keywords:
            self.set_keywords(", ".join(keywords))
        
        self.add_page()
        self.add_personal_info(p)
        
        if data.get('experience'):
            self.add_experience(data['experience'])
            
        if data.get('education'):
            self.add_education(data['education'])

        if data.get('projects'):
            self.add_projects(data['projects'])
            
        if data.get('certificates'):
            self.add_certificates(data['certificates'])
            
        if data.get('skills'):
            self.add_skills(data['skills'])

        return self.output(dest='S')

    def get_pdf_bytes(self):
        return self.output(dest='S')

class ClassicTemplate(BaseResumePDF):
    """
    Optimized ATS-friendly template with modern aesthetics.
    Centered header, professional spacing, clean design.
    """
    def add_section_title(self, title):
        # Orphan protection
        if self.get_y() > 250:
            self.add_page()

        # Improved spacing before section
        self.ln(5 if self.language == 'en' else 6)

        # Professional font size for section titles
        title_size = 12 if self.language == 'en' else 13
        self.set_font('DejaVu', 'B', title_size)

        # Add subtle color to section titles (Dynamic Brand Color)
        r, g, b = self.primary_color
        self.set_text_color(r, g, b)

        # Clean thin border bottom instead of thick border
        self.cell(0, 7, title.upper(), ln=True, align='L')

        # Reset color to black for body text
        self.set_text_color(0, 0, 0)

        # Draw a professional thin line
        self.set_draw_color(r, g, b)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())

        # Reset line width
        self.set_line_width(0.2)
        self.ln(4)

    def add_personal_info(self, p):
        # Optimized name size (adjust for English)
        name_size = 18 if self.language == 'en' else 20
        contact_size = 9 if self.language == 'en' else 10
        summary_size = 9 if self.language == 'en' else 10
        summary_line_height = 5.2 if self.language == 'en' else 5.5

        self.set_font('DejaVu', 'B', name_size)

        # Dynamic Name Color
        r, g, b = self.primary_color
        self.set_text_color(r, g, b)

        self.cell(0, 10, p.get('fullName', ''), ln=True, align='C')
        self.set_text_color(0, 0, 0)  # Reset to black

        # Improved spacing after name
        self.ln(2)

        # Contact info with better formatting
        self.set_font('DejaVu', '', contact_size)
        contact_parts = []
        if p.get('email'): contact_parts.append(p.get('email'))
        if p.get('phone'): contact_parts.append(p.get('phone'))
        
        country = p.get('country', '')
        if self.language == 'en': country = country.replace('Türkiye', 'Turkey')
        
        if p.get('city') and country: contact_parts.append(f"{p.get('city')}, {country}")

        if contact_parts:
            self.cell(0, 5, "  •  ".join(contact_parts), ln=True, align='C')

        # Links with bullet separator
        links = []
        if p.get('linkedin'): links.append(p.get('linkedin'))
        if p.get('github'): links.append(p.get('github'))
        if links:
            self.ln(1)
            self.set_font('DejaVu', '', 8)
            self.set_text_color(60, 60, 60)  # Subtle gray for links
            self.cell(0, 5, "  •  ".join(links), ln=True, align='C')
            self.set_text_color(0, 0, 0)

        # Professional summary with improved spacing
        if p.get('summary'):
            self.ln(2)
            self.add_section_title(self.labels[self.language]['SUMMARY'])
            self.set_font('DejaVu', '', summary_size)
            # Improved line height for better readability
            self.multi_cell(0, summary_line_height, p.get('summary'))

    def add_experience(self, experience_list):
        self.add_section_title(self.labels[self.language]['EXPERIENCE'])
        # Adjust font sizes for English to prevent overflow
        title_size = 10 if self.language == 'en' else 11
        desc_size = 9 if self.language == 'en' else 10
        line_height = 4.8 if self.language == 'en' else 5.2

        for i, exp in enumerate(experience_list):
            self.set_font('DejaVu', 'B', title_size)
            
            # Title (Left) | Date (Right)
            date_str = f"{exp.get('startDate', '')} - {exp.get('endDate', '')}"
            
            y_start = self.get_y()
            self.multi_cell(135, 6, exp.get('title', ''))
            y_end = self.get_y()
            
            # Date
            self.set_xy(145, y_start)
            self.set_font('DejaVu', '', 9)
            self.set_text_color(60, 60, 60)
            self.cell(0, 6, date_str, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            # Reset Y
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            # Company | Location
            self.set_font('DejaVu', '', 10)
            parts = []
            if exp.get('company'): parts.append(exp.get('company'))
            
            loc = exp.get('location', '')
            if self.language == 'en': loc = loc.replace('Türkiye', 'Turkey')
            
            if loc: parts.append(loc)
            
            if parts:
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, " | ".join(parts), ln=True)
                self.set_text_color(0, 0, 0)

            # Description
            self.ln(1)
            self.set_font('DejaVu', '', desc_size)
            self.multi_cell(0, line_height, exp.get('description', ''))

            # Better spacing
            if i < len(experience_list) - 1:
                self.ln(4)
            else:
                self.ln(2)

    def add_education(self, education_list):
        self.add_section_title(self.labels[self.language]['EDUCATION'])
        for edu in education_list:
            self.set_font(self.main_font, 'B', 11)
            line = f"{edu.get('degree', '')}, {edu.get('school', '')}"
            year = edu.get('year', '')
            
            y_start = self.get_y()
            self.multi_cell(145, 6, line)
            y_end = self.get_y()
            
            # Year on Right
            self.set_xy(155, y_start)
            self.set_font(self.main_font, '', 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, year, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())

            # GPA & Rank Line
            extras = []
            if edu.get('gpa'): extras.append(f"GPA: {edu.get('gpa')}")
            if edu.get('rank'): extras.append(edu.get('rank'))
            
            if extras:
                self.set_font(self.main_font, '', 10)
                self.set_text_color(50, 50, 50)
                self.cell(0, 5, " | ".join(extras), ln=True)
                self.set_text_color(0, 0, 0)
            
            self.ln(3)

    def add_skills(self, skills_dict):
        self.add_section_title(self.labels[self.language]['SKILLS'])
        skill_size = 9 if self.language == 'en' else 10
        self.set_font('DejaVu', '', skill_size)

        for cat, items in skills_dict.items():
            if items:
                # Category name in dark blue
                self.set_font('DejaVu', 'B', skill_size)
                self.set_text_color(25, 55, 95)
                self.write(5.2, f"{cat}: ")

                # Items in black
                self.set_font('DejaVu', '', skill_size)
                self.set_text_color(0, 0, 0)
                self.write(5.2, f"{items}\n")
                self.ln(1)

    def add_projects(self, projects_list):
        self.add_section_title(self.labels[self.language]['PROJECTS'])
        title_size = 10 if self.language == 'en' else 11
        desc_size = 9 if self.language == 'en' else 10
        
        for i, proj in enumerate(projects_list):
            self.set_font('DejaVu', 'B', title_size)
            self.cell(0, 6, proj.get('name', ''), ln=True)
            
            p_tech = proj.get('tech', '')
            if p_tech:
                self.set_font('DejaVu', 'I', 9)
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, p_tech, ln=True)
                self.set_text_color(0, 0, 0)

            if proj.get('description'):
                self.set_font('DejaVu', '', desc_size)
                self.multi_cell(0, 5, proj.get('description', ''))
            
            if i < len(projects_list) - 1:
                self.ln(3)
            else:
                self.ln(2)

    def add_certificates(self, certificates_list):
        self.add_section_title(self.labels[self.language]['CERTIFICATES'])
        # Sort/Reverse logic: Show newest first (assuming input is chronological)
        # Simple reverse is usually what users expect if they added 2020 then 2025
        sorted_certs = list(reversed(certificates_list))
        
        for cert in sorted_certs:
            self.set_font(self.main_font, 'B', 10)
            line = cert.get('name', '')
            if cert.get('authority'): line += f" - {cert.get('authority')}"
            
            y_start = self.get_y()
            self.multi_cell(145, 5, line)
            y_end = self.get_y()
            
            if cert.get('date'):
                self.set_xy(155, y_start)
                self.set_font(self.main_font, '', 9)
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, cert.get('date'), align='R', ln=True)
                self.set_text_color(0, 0, 0)
            
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            self.ln(2)

    def add_personal_info(self, p):
        # Optimized name size (adjust for English)
        name_size = 18 if self.language == 'en' else 20
        contact_size = 9 if self.language == 'en' else 10
        summary_size = 9 if self.language == 'en' else 10
        summary_line_height = 5.2 if self.language == 'en' else 5.5

        self.set_font('DejaVu', 'B', name_size)

        # Dynamic Name Color
        r, g, b = self.primary_color
        self.set_text_color(r, g, b)

        self.cell(0, 10, p.get('fullName', ''), ln=True, align='C')
        self.set_text_color(0, 0, 0)  # Reset to black

        # Improved spacing after name
        self.ln(2)

        # Contact info with better formatting
        self.set_font('DejaVu', '', contact_size)
        contact_parts = []
        if p.get('email'): contact_parts.append(p.get('email'))
        if p.get('phone'): contact_parts.append(p.get('phone'))
        if p.get('city') and p.get('country'): contact_parts.append(f"{p.get('city')}, {p.get('country')}")

        if contact_parts:
            self.cell(0, 5, "  •  ".join(contact_parts), ln=True, align='C')

        # Links with bullet separator
        links = []
        if p.get('linkedin'): links.append(p.get('linkedin'))
        if p.get('github'): links.append(p.get('github'))
        if links:
            self.ln(1)
            self.set_font('DejaVu', '', 8)
            self.set_text_color(60, 60, 60)  # Subtle gray for links
            self.cell(0, 5, "  •  ".join(links), ln=True, align='C')
            self.set_text_color(0, 0, 0)

        # Professional summary with improved spacing
        if p.get('summary'):
            self.ln(2)
            self.add_section_title(self.labels[self.language]['SUMMARY'])
            self.set_font('DejaVu', '', summary_size)
            # Improved line height for better readability
            self.multi_cell(0, summary_line_height, p.get('summary'))

    def add_experience(self, experience_list):
        self.add_section_title(self.labels[self.language]['EXPERIENCE'])
        # Adjust font sizes for English to prevent overflow
        title_size = 10 if self.language == 'en' else 11
        desc_size = 9 if self.language == 'en' else 10
        line_height = 4.8 if self.language == 'en' else 5.2

        for i, exp in enumerate(experience_list):
            self.set_font('DejaVu', 'B', title_size)
            
            # Title (Left) with Wrapping
            y_start = self.get_y()
            self.multi_cell(135, 6, exp.get('title', ''))
            y_end = self.get_y()
            
            # Date (Right) aligned to top
            start_d = exp.get('startDate', '')
            end_d = exp.get('endDate', '')
            
            # Dynamic Translation for Date
            if self.language == 'en':
                if end_d == 'Devam Ediyor': end_d = 'Present'
            else:
                if end_d == 'Present': end_d = 'Devam Ediyor'
                
            date_str = f"{start_d} - {end_d}"
            self.set_xy(145, y_start)
            self.set_font('DejaVu', '', 9)
            self.set_text_color(60, 60, 60)
            self.cell(0, 6, date_str, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            # Reset Y to below title (or date, whichever is lower)
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            # Company | Location
            self.set_font('DejaVu', '', 10)
            parts = []
            if exp.get('company'): parts.append(exp.get('company'))
            
            loc = exp.get('location', '')
            if self.language == 'en': loc = loc.replace('Türkiye', 'Turkey')
            
            if loc: parts.append(loc)
            
            if parts:
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, " | ".join(parts), ln=True)
                self.set_text_color(0, 0, 0)

            # Description
            self.ln(1)
            self.set_font('DejaVu', '', desc_size)
            self.multi_cell(0, line_height, exp.get('description', ''))

            # Better spacing between experiences
            if i < len(experience_list) - 1:
                self.ln(4)
            else:
                self.ln(2)

    def add_education(self, education_list):
        self.add_section_title(self.labels[self.language]['EDUCATION'])
        for edu in education_list:
            # Row 1: School Name | Year
            self.set_font(self.main_font, 'B', 11)
            y_start = self.get_y()
            self.multi_cell(145, 6, edu.get('school', '')) # Support School wrapping
            y_end = self.get_y()
            
            # Year on Right (Aligned with School top)
            year = edu.get('year', '')
            self.set_xy(155, y_start)
            self.set_font(self.main_font, '', 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, year, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            # Reset Y
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())

            # Row 2: Degree (Italic/Regular)
            self.set_font(self.main_font, 'I' if self.language == 'en' else '', 11) # Italic looks nice for degree
            self.multi_cell(0, 6, edu.get('degree', ''))

            # Row 3: GPA & Rank
            extras = []
            gpa = edu.get('gpa', '').strip()
            rank = edu.get('rank', '').strip()
            
            if gpa: extras.append(f"GPA: {gpa}")
            if rank: extras.append(rank)
            
            if extras:
                self.set_x(self.l_margin) # Force reset X
                self.set_font(self.main_font, '', 10)
                self.set_text_color(50, 50, 50)
                self.cell(0, 5, " | ".join(extras), ln=True, align='L') # Force Left
                self.set_text_color(0, 0, 0)
            
            self.ln(2)

    def add_skills(self, skills_dict):
        self.add_section_title(self.labels[self.language]['SKILLS'])
        skill_size = 9 if self.language == 'en' else 10
        self.set_font('DejaVu', '', skill_size)
        
        # Translation Map
        cat_map = {
            'Programlama': 'Programming',
            'Frameworks': 'Frameworks',
            'Araçlar': 'Tools',
            'Diller': 'Languages'
        } if self.language == 'en' else {}

        for cat, items in skills_dict.items():
            if items:
                display_cat = cat_map.get(cat, cat)
                
                # Auto-append Turkish if English resume and Languages category
                if self.language == 'en' and display_cat == 'Languages':
                    if 'Turkish' not in items and 'Türkçe' not in items:
                         items += ", Turkish (Native)"
                
                # Category name in dark blue
                self.set_font('DejaVu', 'B', skill_size)
                self.set_text_color(25, 55, 95)
                self.write(5.2, f"{display_cat}: ")

                # Items in black
                self.set_font('DejaVu', '', skill_size)
                self.set_text_color(0, 0, 0)
                self.write(5.2, f"{items}\n")
                self.ln(1)  # Small spacing between skill categories

    def add_projects(self, projects_list):
        self.add_section_title(self.labels[self.language]['PROJECTS'])
        title_size = 10 if self.language == 'en' else 11
        desc_size = 9 if self.language == 'en' else 10
        
        for i, proj in enumerate(projects_list):
            self.set_font('DejaVu', 'B', title_size)
            self.cell(0, 6, proj.get('name', ''), ln=True)
            
            p_tech = proj.get('tech', '')
            if p_tech:
                self.set_font('DejaVu', 'I', 9)
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, p_tech, ln=True)
                self.set_text_color(0, 0, 0)

            if proj.get('description'):
                self.set_font('DejaVu', '', desc_size)
                self.multi_cell(0, 5, proj.get('description', ''))
            
            if i < len(projects_list) - 1:
                self.ln(3)
            else:
                self.ln(2)

    def add_certificates(self, certificates_list):
        self.add_section_title(self.labels[self.language]['CERTIFICATES'])
        # Sort/Reverse logic: Show newest first (assuming input is chronological)
        # Simple reverse is usually what users expect if they added 2020 then 2025
        sorted_certs = list(reversed(certificates_list))
        
        for cert in sorted_certs:
            self.set_font(self.main_font, 'B', 10)
            
            line = cert.get('name', '')
            if cert.get('authority'): line += f" - {cert.get('authority')}"
            
            y_start = self.get_y()
            self.multi_cell(145, 5, line) # Wrap long text
            y_end = self.get_y()
            
            # Date on right
            if cert.get('date'):
                self.set_xy(155, y_start)
                self.set_font(self.main_font, '', 9)
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, cert.get('date'), align='R', ln=True)
                self.set_text_color(0, 0, 0)
            
            # Reset Y
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            self.ln(2)


class ModernTemplate(BaseResumePDF):
    """
    Optimized modern template with clean aesthetics.
    Left-aligned header, minimal borders, efficient space usage.
    """
    def add_section_title(self, title):
        # Orphan protection: If near bottom, add page
        if self.get_y() > 250:
            self.add_page()
            
        # Improved spacing before section
        self.ln(6)

        # Professional font size
        self.set_font('DejaVu', 'B', 13)

        # Dark blue color for section titles
        self.set_text_color(25, 55, 95)
        self.cell(0, 8, title.upper(), ln=True, align='L')

        # Reset color
        self.set_text_color(0, 0, 0)

        # Draw a professional thin line
        self.set_draw_color(25, 55, 95)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
        self.set_line_width(0.2)
        self.ln(4)

    def add_personal_info(self, p):
        # Optimized name size (20pt instead of 26pt)
        self.set_font('DejaVu', 'B', 20)
        self.set_text_color(25, 55, 95)
        self.cell(0, 10, p.get('fullName', ''), ln=True, align='L')
        self.set_text_color(0, 0, 0)

        # Improved spacing
        self.ln(3)

        self.set_font('DejaVu', '', 10)
        # Contact info with bullet separators
        info_lines = []
        if p.get('email'): info_lines.append(p.get('email'))
        if p.get('phone'): info_lines.append(p.get('phone'))
        
        country = p.get('country', '')
        if self.language == 'en': country = country.replace('Türkiye', 'Turkey')
        
        if p.get('city') and country: info_lines.append(f"{p.get('city')}, {country}")

        if info_lines:
            self.cell(0, 5, "  •  ".join(info_lines), ln=True, align='L')

        # Links with gray color
        if p.get('linkedin') or p.get('github'):
            self.ln(2)
            links = []
            if p.get('linkedin'): links.append(p.get('linkedin'))
            if p.get('github'): links.append(p.get('github'))
            self.set_font('DejaVu', '', 9)
            self.set_text_color(60, 60, 60)
            self.cell(0, 5, "  •  ".join(links), ln=True, align='L')
            self.set_text_color(0, 0, 0)

        if p.get('summary'):
            self.ln(2)
            self.add_section_title(self.labels[self.language]['SUMMARY'])
            self.set_font('DejaVu', '', 10)
            self.multi_cell(0, 5.5, p.get('summary'))

    def add_experience(self, experience_list):
        self.add_section_title(self.labels[self.language]['EXPERIENCE_MODERN'])
        for i, exp in enumerate(experience_list):
            self.set_font('DejaVu', 'B', 11)
            
            title_company = f"{exp.get('title', '')} - {exp.get('company', '')}"
            
            loc = exp.get('location', '')
            if self.language == 'en': loc = loc.replace('Türkiye', 'Turkey')
            
            if loc: title_company += f", {loc}"
            
            start_d = exp.get('startDate', '')
            end_d = exp.get('endDate', '')
            
            # Dynamic Translation for Date
            if self.language == 'en':
                if end_d == 'Devam Ediyor': end_d = 'Present'
            else:
                if end_d == 'Present': end_d = 'Devam Ediyor'

            date_str = f"{start_d} - {end_d}"
            
            # Layout: Title (Left) | Date (Right)
            y_start = self.get_y()
            self.multi_cell(135, 6, title_company)
            y_end = self.get_y()
            
            # Date
            self.set_xy(145, y_start)
            self.set_font('DejaVu', '', 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, date_str, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            # Reset Y
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                 self.set_xy(self.l_margin, self.get_y())

            # Description
            self.set_font('DejaVu', '', 10)
            self.multi_cell(0, 5.2, exp.get('description', ''))

            # Better spacing
            if i < len(experience_list) - 1:
                self.ln(4)
            else:
                self.ln(2)

    def add_education(self, education_list):
        self.add_section_title(self.labels[self.language]['EDUCATION_MODERN'])
        for edu in education_list:
            # Row 1: School | Date
            self.set_font(self.main_font, 'B', 11)
            y_start = self.get_y()
            self.multi_cell(145, 6, edu.get('school', ''))
            y_end = self.get_y()

            # Year on right
            year = edu.get('year', '')
            self.set_xy(155, y_start)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, year, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())

            # Row 2: Degree
            self.set_font(self.main_font, '', 11)
            self.multi_cell(0, 6, edu.get('degree', ''))

            # GPA & Rank Line
            extras = []
            gpa = edu.get('gpa', '').strip()
            rank = edu.get('rank', '').strip()
            
            if gpa: extras.append(f"GPA: {gpa}")
            if rank: extras.append(rank)
            
            if extras:
                self.set_x(self.l_margin) # Force reset X
                self.set_font(self.main_font, '', 10)
                self.set_text_color(25, 55, 95) # Dark Blue
                self.cell(0, 5, " • ".join(extras), ln=True, align='L') # Force Left
                self.set_text_color(0, 0, 0)
            
            self.ln(2)

    def add_skills(self, skills_dict):
        self.add_section_title(self.labels[self.language]['SKILLS_MODERN'])
        self.set_font('DejaVu', '', 10)
        
        # Translation Map
        cat_map = {
            'Programlama': 'Programming',
            'Frameworks': 'Frameworks',
            'Araçlar': 'Tools',
            'Diller': 'Languages'
        } if self.language == 'en' else {}

        for cat, items in skills_dict.items():
            if items:
                display_cat = cat_map.get(cat, cat)
                
                # Auto-append Turkish if English resume and Languages category
                if self.language == 'en' and display_cat == 'Languages':
                    if 'Turkish' not in items and 'Türkçe' not in items:
                         items += ", Turkish (Native)"
                
                # Category in dark blue
                self.set_font('DejaVu', 'B', 10)
                self.set_text_color(25, 55, 95)
                self.write(5.5, f"{display_cat}: ")

                # Items in black
                self.set_font('DejaVu', '', 10)
                self.set_text_color(0, 0, 0)
                self.write(5.5, f"{items}\n")
                self.ln(1)
    
    def add_projects(self, projects_list):
        self.add_section_title(self.labels[self.language]['PROJECTS'])
        for i, proj in enumerate(projects_list):
            self.set_font('DejaVu', 'B', 10)
            self.cell(0, 5, proj.get('name', ''), ln=True)
            
            p_tech = proj.get('tech', '')
            if p_tech:
                self.set_font('DejaVu', 'I', 9)
                self.set_text_color(25, 55, 95)
                self.cell(0, 4, p_tech, ln=True)
                self.set_text_color(0, 0, 0)

            if proj.get('description'):
                self.set_font('DejaVu', '', 9)
                self.multi_cell(0, 4.3, proj.get('description', ''))
            
            if i < len(projects_list) - 1:
                self.ln(2)
            else:
                self.ln(1)

    def add_certificates(self, certificates_list):
        self.add_section_title(self.labels[self.language]['CERTIFICATES'])
        # Sort/Reverse logic: Show newest first (assuming input is chronological)
        # Simple reverse is usually what users expect if they added 2020 then 2025
        sorted_certs = list(reversed(certificates_list))
        
        for cert in sorted_certs:
            self.set_font(self.main_font, 'B', 10)
            line = cert.get('name', '')
            
            if cert.get('authority'):
                line += f" - {cert.get('authority')}"
            
            y_start = self.get_y()
            self.multi_cell(145, 5, line)
            y_end = self.get_y()
            
            if cert.get('date'):
                self.set_xy(155, y_start)
                self.set_text_color(80, 80, 80)
                self.cell(0, 5, cert.get('date'), align='R', ln=True)
                self.set_text_color(0, 0, 0)
            
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            self.ln(1)

    def add_personal_info(self, p):
        # Optimized name size (20pt instead of 26pt)
        self.set_font('DejaVu', 'B', 20)
        self.set_text_color(25, 55, 95)
        self.cell(0, 10, p.get('fullName', ''), ln=True, align='L')
        self.set_text_color(0, 0, 0)

        # Improved spacing
        self.ln(3)

        self.set_font('DejaVu', '', 10)
        # Contact info with bullet separators
        info_lines = []
        if p.get('email'): info_lines.append(p.get('email'))
        if p.get('phone'): info_lines.append(p.get('phone'))
        
        country = p.get('country', '')
        if self.language == 'en': country = country.replace('Türkiye', 'Turkey')
        
        if p.get('city') and country: info_lines.append(f"{p.get('city')}, {country}")

        if info_lines:
            self.cell(0, 5, "  •  ".join(info_lines), ln=True, align='L')

        # Links with gray color
        if p.get('linkedin') or p.get('github'):
            self.ln(2)
            links = []
            if p.get('linkedin'): links.append(p.get('linkedin'))
            if p.get('github'): links.append(p.get('github'))
            self.set_font('DejaVu', '', 9)
            self.set_text_color(60, 60, 60)
            self.cell(0, 5, "  •  ".join(links), ln=True, align='L')
            self.set_text_color(0, 0, 0)

        if p.get('summary'):
            self.ln(2)
            self.add_section_title(self.labels[self.language]['SUMMARY'])
            self.set_font('DejaVu', '', 10)
            self.multi_cell(0, 5.5, p.get('summary'))

    def add_experience(self, experience_list):
        self.add_section_title(self.labels[self.language]['EXPERIENCE_MODERN'])
        for i, exp in enumerate(experience_list):
            # Title
            self.set_font('DejaVu', 'B', 11)
            self.cell(0, 6, exp.get('title', ''), ln=True)

            # Company | Date | Location
            self.set_font('DejaVu', '', 9)
            self.set_text_color(80, 80, 80)
            
            parts = [exp.get('company', '')]
            date_str = f"{exp.get('startDate', '')} - {exp.get('endDate', '')}"
            parts.append(date_str)
            if exp.get('location'): parts.append(exp.get('location'))
            
            self.cell(0, 5, " | ".join(parts), ln=True)
            self.set_text_color(0, 0, 0)

            # Description
            self.ln(1)
            self.set_font('DejaVu', '', 10)
            self.multi_cell(0, 5.2, exp.get('description', ''))

            # Better spacing
            if i < len(experience_list) - 1:
                self.ln(4)
            else:
                self.ln(2)

    def add_education(self, education_list):
        self.add_section_title(self.labels[self.language]['EDUCATION_MODERN'])
        for edu in education_list:
            self.set_font(self.main_font, 'B', 11)
            self.multi_cell(0, 6, f"{edu.get('degree', '')}, {edu.get('school', '')}")

            # GPA & Rank Line
            extras = []
            if edu.get('gpa'): extras.append(f"GPA: {edu.get('gpa')}")
            if edu.get('rank'): extras.append(edu.get('rank'))
            
            if extras:
                self.set_font(self.main_font, '', 10)
                self.set_text_color(25, 55, 95) # Dark Blue info
                self.cell(0, 5, " • ".join(extras), ln=True)
                self.set_text_color(0, 0, 0)
            
            self.set_font(self.main_font, '', 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 5, edu.get('year', ''), ln=True)
            self.set_text_color(0, 0, 0)
            self.ln(3)

    def add_skills(self, skills_dict):
        self.add_section_title(self.labels[self.language]['SKILLS_MODERN'])
        self.set_font('DejaVu', '', 10)
        
        # Translation Map
        cat_map = {
            'Programlama': 'Programming',
            'Frameworks': 'Frameworks',
            'Araçlar': 'Tools',
            'Diller': 'Languages'
        } if self.language == 'en' else {}

        for cat, items in skills_dict.items():
            if items:
                display_cat = cat_map.get(cat, cat)
                
                # Auto-append Turkish if English resume and Languages category
                if self.language == 'en' and display_cat == 'Languages':
                    if 'Turkish' not in items and 'Türkçe' not in items:
                         items += ", Turkish (Native)"
                
                # Category in dark blue
                self.set_font('DejaVu', 'B', 10)
                self.set_text_color(25, 55, 95)
                self.write(5.5, f"{display_cat}: ")

                # Items in black
                self.set_font('DejaVu', '', 10)
                self.set_text_color(0, 0, 0)
                self.write(5.5, f"{items}\n")
                self.ln(1)

    def add_projects(self, projects_list):
        self.add_section_title(self.labels[self.language]['PROJECTS'])
        for i, proj in enumerate(projects_list):
            self.set_font('DejaVu', 'B', 10)
            self.cell(0, 5, proj.get('name', ''), ln=True)
            
            p_tech = proj.get('tech', '')
            if p_tech:
                self.set_font('DejaVu', 'I', 9)
                self.set_text_color(25, 55, 95)
                self.cell(0, 4, p_tech, ln=True)
                self.set_text_color(0, 0, 0)

            if proj.get('description'):
                self.set_font('DejaVu', '', 9)
                self.multi_cell(0, 4.3, proj.get('description', ''))
            
            if i < len(projects_list) - 1:
                self.ln(2)
            else:
                self.ln(1)

    def add_certificates(self, certificates_list):
        self.add_section_title(self.labels[self.language]['CERTIFICATES'])
        # Sort/Reverse logic: Show newest first (assuming input is chronological)
        # Simple reverse is usually what users expect if they added 2020 then 2025
        sorted_certs = list(reversed(certificates_list))
        
        for cert in sorted_certs:
            self.set_font(self.main_font, 'B', 10)
            line = cert.get('name', '')
            
            if cert.get('authority'):
                line += f" - {cert.get('authority')}"
                
            y = self.get_y()
            # Use multi_cell with width limit
            self.multi_cell(145, 5, line)
            
            # If multi_cell increased height, we need to capture new Y
            new_y = self.get_y()
            
            # Restore Y for the right column date (but careful if date also wraps? Date usually short)
            # We align Date to the top line of the entry
            self.set_xy(155, y)
            
            if cert.get('date'):
                self.set_xy(155, y)
                self.set_text_color(80, 80, 80)
                self.cell(0, 5, cert.get('date'), align='R', ln=True)
                self.set_text_color(0, 0, 0)
            else:
                self.ln(5)
            
            self.ln(1)

class AcademicTemplate(BaseResumePDF):
    """
    Optimized dense template with professional aesthetics.
    Minimal margins, maximum content, clean design.
    """
    def __init__(self, language='tr'):
        super().__init__(language)
        # Smaller margins for academic
        self.set_margins(12, 12, 12)

    def add_section_title(self, title):
        self.ln(4)
        self.set_font(self.main_font, 'B', 12)

        # Dark blue color for sections
        self.set_text_color(25, 55, 95)
        self.cell(0, 6, title.upper(), ln=True)

        # Reset color
        self.set_text_color(0, 0, 0)

        # Clean thin line
        self.set_draw_color(25, 55, 95)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
        self.set_line_width(0.2)
        self.ln(2)

    def add_personal_info(self, p):
        # Optimized name size (18pt for academic - balanced)
        self.set_font('DejaVu', 'B', 18)
        self.set_text_color(25, 55, 95)
        self.cell(0, 8, p.get('fullName', ''), ln=True, align='C')
        self.set_text_color(0, 0, 0)

        self.ln(2)

        # Dense contact line with bullet separators
        self.set_font('DejaVu', '', 9)
        parts = []
        if p.get('email'): parts.append(p.get('email'))
        if p.get('phone'): parts.append(p.get('phone'))
        if p.get('city') and p.get('country'): parts.append(f"{p.get('city')}, {p.get('country')}")

        if parts:
            self.cell(0, 5, "  •  ".join(parts), ln=True, align='C')

        # Links
        if p.get('linkedin') or p.get('github'):
            links = []
            if p.get('linkedin'): links.append(p.get('linkedin'))
            if p.get('github'): links.append(p.get('github'))
            self.set_text_color(60, 60, 60)
            self.cell(0, 5, "  •  ".join(links), ln=True, align='C')
            self.set_text_color(0, 0, 0)

        if p.get('summary'):
            self.ln(2)
            self.add_section_title(self.labels[self.language]['SUMMARY'])
            self.set_font('DejaVu', '', 9)
            self.multi_cell(0, 4.5, p.get('summary'))

    def add_experience(self, experience_list):
        self.add_section_title(self.labels[self.language]['EXPERIENCE_ACADEMIC'])
        for i, exp in enumerate(experience_list):
            self.set_font('DejaVu', 'B', 10)

            title_company = f"{exp.get('title', '')} - {exp.get('company', '')}"
            
            loc = exp.get('location', '')
            if self.language == 'en': loc = loc.replace('Türkiye', 'Turkey')
            
            if loc: title_company += f", {loc}"
            date_str = f"{exp.get('startDate', '')} - {exp.get('endDate', '')}"

            # Two-column layout with wrapping support
            y_start = self.get_y()
            self.multi_cell(135, 5, title_company)
            y_end = self.get_y()

            # Date on right in gray (aligned to top line)
            self.set_xy(145, y_start)
            self.set_font('DejaVu', '', 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 5, date_str, align='R', ln=True)
            self.set_text_color(0, 0, 0)

            # Move cursor to below the lowest point (either text or date)
            # Usually text is taller. If date wrapped (unlikely), self.get_y() would be updated.
            # But we used cell() for date which doesn't wrap. 
            # So we set Y to y_end (bottom of text) if y_end > current Y.
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                 self.set_xy(self.l_margin, self.get_y())

            # Description
            self.set_font('DejaVu', '', 9)
            self.multi_cell(0, 4.3, exp.get('description', ''))

            if i < len(experience_list) - 1:
                self.ln(2)
            else:
                self.ln(1)

    def add_education(self, education_list):
        self.add_section_title(self.labels[self.language]['EDUCATION_ACADEMIC'])
        for edu in education_list:
            self.set_font(self.main_font, 'B', 10)
            line = f"{edu.get('degree', '')}, {edu.get('school', '')}"
            year = edu.get('year', '')

            y_start = self.get_y()
            self.multi_cell(145, 5, line)
            y_end = self.get_y()

            # Year in gray on right
            self.set_xy(155, y_start)
            self.set_text_color(80, 80, 80)
            self.cell(0, 5, year, align='R', ln=True)
            self.set_text_color(0, 0, 0)
            
            # Reset Y to bottom of school name
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            # GPA & Rank (Below line)
            extras = []
            if edu.get('gpa'): extras.append(f"GPA: {edu.get('gpa')}")
            if edu.get('rank'): extras.append(edu.get('rank'))
            
            if extras:
                self.set_font(self.main_font, 'I', 9) # Italic for emphasis
                self.cell(0, 4, "  " + " | ".join(extras), ln=True)
                self.set_font(self.main_font, '', 9)

            self.ln(1)

    def add_skills(self, skills_dict):
        self.add_section_title(self.labels[self.language]['SKILLS_ACADEMIC'])
        self.set_font('DejaVu', '', 9)
        for cat, items in skills_dict.items():
            if items:
                # Category in dark blue
                self.set_font('DejaVu', 'B', 9)
                self.set_text_color(25, 55, 95)
                self.cell(45, 5, f"{cat}:")

                # Items in black
                self.set_font('DejaVu', '', 9)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 5, items) # multi_cell to wrap skills
                self.ln(1)

    def add_projects(self, projects_list):
        self.add_section_title(self.labels[self.language]['PROJECTS'])
        for i, proj in enumerate(projects_list):
            self.set_font('DejaVu', 'B', 10)
            self.cell(0, 5, proj.get('name', ''), ln=True)
            
            p_tech = proj.get('tech', '')
            if p_tech:
                self.set_font('DejaVu', 'I', 9)
                self.set_text_color(25, 55, 95)
                self.cell(0, 4, p_tech, ln=True)
                self.set_text_color(0, 0, 0)

            if proj.get('description'):
                self.set_font('DejaVu', '', 9)
                self.multi_cell(0, 4.3, proj.get('description', ''))
            
            if i < len(projects_list) - 1:
                self.ln(2)
            else:
                self.ln(1)

    def add_certificates(self, certificates_list):
        self.add_section_title(self.labels[self.language]['CERTIFICATES'])
        # Sort/Reverse logic: Show newest first (assuming input is chronological)
        # Simple reverse is usually what users expect if they added 2020 then 2025
        sorted_certs = list(reversed(certificates_list))
        
        for cert in sorted_certs:
            self.set_font(self.main_font, 'B', 10)
            line = cert.get('name', '')
            
            if cert.get('authority'):
                line += f" - {cert.get('authority')}"
            
            y_start = self.get_y()
            self.multi_cell(145, 5, line)
            y_end = self.get_y()
            
            if cert.get('date'):
                self.set_xy(155, y_start)
                self.set_text_color(80, 80, 80)
                self.cell(0, 5, cert.get('date'), align='R', ln=True)
                self.set_text_color(0, 0, 0)
            
            if y_end > self.get_y():
                self.set_xy(self.l_margin, y_end)
            else:
                self.set_xy(self.l_margin, self.get_y())
            
            self.ln(1)

def get_generator(template_name, language='tr'):
    if template_name == "Modern":
        return ModernTemplate(language)
    elif template_name == "Akademik":
        return AcademicTemplate(language)
    else:
        return ClassicTemplate(language)

class CoverLetterPDF(BaseResumePDF):
    def generate_cover_letter_pdf(self, person_data, cover_body):
        self.add_page()
        p = person_data.get('personal', {})
        
        # Header (Use Modern Style for Header)
        self.set_font('DejaVu', 'B', 22)
        self.cell(0, 10, p.get('fullName', ''), ln=True, align='L')
        self.set_font('DejaVu', '', 10)
        
        info = []
        if p.get('email'): info.append(p.get('email'))
        if p.get('phone'): info.append(p.get('phone'))
        
        self.cell(0, 6, " | ".join(info), ln=True, align='L')
        self.ln(10)
        
        # Date
        # self.cell(0, 6, "Date: ...", ln=True) # Optional
        
        # Body
        self.set_font('DejaVu', '', 11)
        self.multi_cell(0, 6, cover_body)
        
        self.ln(20)
        self.cell(0, 6, "Saygılarımla,", ln=True)
        self.ln(5)
        self.cell(0, 6, p.get('fullName', ''), ln=True)
        
        return self.output()
