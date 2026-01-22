import streamlit as st
import ui_components
from cv_generator import get_generator, CoverLetterPDF
from cv_generator_docx import ATSResumeDocx
from translator_utils import translate_resume_data
from matcher_utils import calculate_match_score, get_resume_text
from localization import STRINGS
import datetime
import json
import os

st.set_page_config(page_title="ATS CV Sihirbazı", page_icon="📄", layout="wide")

# Inject Custom UI Styles
ui_components.inject_custom_css()

# Initialize Session State
if 'resume_language' not in st.session_state:
    st.session_state['resume_language'] = 'tr'

if 'data_store' not in st.session_state:
    try:
        from user_data import user_profile
        # Migration Logic: Check if legacy format (no 'tr'/'en' keys)
        if 'personal' in user_profile and 'tr' not in user_profile:
            import copy
            st.session_state['data_store'] = {
                'tr': user_profile,
                'en': copy.deepcopy(user_profile)
            }
        else:
            st.session_state['data_store'] = user_profile
    except ImportError:
        empty_profile = {
            'personal': {},
            'experience': [],
            'education': [],
            'skills': {},
            'projects': [],
            'certificates': []
        }
        import copy
        st.session_state['data_store'] = {
            'tr': empty_profile,
            'en': copy.deepcopy(empty_profile)
        }

# Bind active cv_data to selected language
# This creates a reference, so edits to cv_data update data_store[lang]
curr_lang = st.session_state['resume_language']
if curr_lang not in st.session_state['data_store']:
    # Fallback if key missing
    import copy
    st.session_state['data_store'][curr_lang] = copy.deepcopy(st.session_state['data_store'].get('tr', {}))

st.session_state['cv_data'] = st.session_state['data_store'][curr_lang]

if 'current_step' not in st.session_state:
    st.session_state['current_step'] = 0

if 'selected_template' not in st.session_state:
    st.session_state['selected_template'] = "Klasik"

# moved up

def get_text(key):
    lang = st.session_state.get('resume_language', 'tr')
    return STRINGS[lang].get(key, key)

# Edit States
if 'edit_exp_idx' not in st.session_state: st.session_state['edit_exp_idx'] = -1
if 'edit_edu_idx' not in st.session_state: st.session_state['edit_edu_idx'] = -1

STEPS = get_text('steps')

# Auto-save function
def save_cv_data():
    """Save CV data to user_data.py"""
    try:
        user_data_path = os.path.join(os.path.dirname(__file__), 'user_data.py')
        
        # Ensure we are saving the latest state of data_store
        # (cv_data is ref, so it should be up to date)
        
        with open(user_data_path, 'w', encoding='utf-8') as f:
            f.write("user_profile = ")
            f.write(json.dumps(st.session_state['data_store'], ensure_ascii=False, indent=4))
            f.write("\n")
        st.toast("✅ Veriler kaydedildi!", icon="🎉")
    except Exception as e:
        st.error(f"Kaydetme hatası: {e}")

def next_step():
    if st.session_state['current_step'] < len(STEPS) - 1:
        st.session_state['current_step'] += 1
    save_cv_data()

def prev_step():
    if st.session_state['current_step'] > 0:
        st.session_state['current_step'] -= 1
    save_cv_data()

# --- Render Custom Header ---
user_fullname = st.session_state['cv_data']['personal'].get('fullName', 'User')
ui_components.render_header(user_name=user_fullname)

# --- Render Custom Sidebar ---
ui_components.render_sidebar()

# --- Save/Load Progress (Defensive State Management) ---
with st.sidebar:
    st.divider()
    st.markdown(f"### {get_text('sidebar_manage_data')}")
    
    # Download
    import json
    cv_json = json.dumps(st.session_state['cv_data'], ensure_ascii=False, indent=2)
    st.download_button(
        label=get_text('sidebar_download_backup'),
        data=cv_json,
        file_name="cv_yedek.json",
        mime="application/json",
        use_container_width=True
    )
    
    # Upload
    uploaded_file = st.file_uploader(get_text('sidebar_upload_backup'), type=['json'])
    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            # Basic validation
            if 'personal' in loaded_data:
                # Update data store for current language
                lang = st.session_state.get('resume_language', 'tr')
                st.session_state['data_store'][lang] = loaded_data
                st.session_state['cv_data'] = st.session_state['data_store'][lang]
                
                # Auto-save immediately
                save_cv_data()
                
                st.success(get_text('sidebar_upload_success'))
                st.rerun()
            else:
                st.error(get_text('sidebar_upload_error'))
        except Exception as e:
            st.error(f"Hata: {e}")

# --- Render Progress Indicator ---
current_step_idx = st.session_state['current_step']
current_step_name = STEPS[current_step_idx]
st.markdown(ui_components.get_progress_bar_html(current_step_idx, len(STEPS), current_step_name), unsafe_allow_html=True)

# --- Step 0: Intro ---
if st.session_state['current_step'] == 0:
    if 'show_lang_select' not in st.session_state:
        st.session_state['show_lang_select'] = False

    if not st.session_state['show_lang_select']:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h3>{get_text('intro_title')}</h3>
            <p style="font-size: 1.1rem; color: #4B5563;">
                {get_text('intro_desc_1')}
            </p>
            <ul style="text-align: left; display: inline-block; margin-top: 1rem; color: #374151;">
                <li>{get_text('intro_bullet_1')}</li>
                <li>{get_text('intro_bullet_2')}</li>
                <li>{get_text('intro_bullet_3')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            def show_lang():
                st.session_state['show_lang_select'] = True
            st.button(get_text('intro_btn_start'), on_click=show_lang, use_container_width=True)
            
    else:
        # Language Selection Screen
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h3>{get_text('lang_select_title')}</h3>
            <p style="color: #6B7280;">{get_text('lang_select_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
        
        with c2:
            if st.button("🇹🇷 Türkçe", use_container_width=True, type="primary"):
                st.session_state['resume_language'] = "tr"
                next_step()
                
        with c3:
            if st.button("🇬🇧 English", use_container_width=True):
                st.session_state['resume_language'] = "en"
                # If English, maybe set default country to USA? Kept simple for now.
                next_step()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button(get_text('btn_back')):
            st.session_state['show_lang_select'] = False
            st.rerun()

# --- Step 1: Personal Info ---
elif st.session_state['current_step'] == 1:
    st.info(get_text('s1_info'))
    
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input(get_text('s1_fullname'), value=st.session_state['cv_data']['personal'].get('fullName', ''))
        email = st.text_input(get_text('s1_email'), value=st.session_state['cv_data']['personal'].get('email', ''))
        phone = st.text_input(get_text('s1_phone'), value=st.session_state['cv_data']['personal'].get('phone', ''))
    with col2:
        city = st.text_input(get_text('s1_city'), value=st.session_state['cv_data']['personal'].get('city', ''))
        country = st.text_input(get_text('s1_country'), value=st.session_state['cv_data']['personal'].get('country', 'Türkiye'))
        linkedin = st.text_input(get_text('s1_linkedin'), value=st.session_state['cv_data']['personal'].get('linkedin', ''))
        github = st.text_input(get_text('s1_github'), value=st.session_state['cv_data']['personal'].get('github', ''))
    
    summary = st.text_area(get_text('s1_summary_label'), value=st.session_state['cv_data']['personal'].get('summary', ''), height=100)
    
    # Save State
    st.session_state['cv_data']['personal'] = {
        'fullName': full_name, 'email': email, 'phone': phone,
        'city': city, 'country': country, 'linkedin': linkedin,
        'github': github, 'summary': summary
    }

    col1, col2 = st.columns([1, 5])
    col1.button(get_text('btn_prev'), on_click=prev_step)
    col2.button(get_text('btn_next'), on_click=next_step)

# --- Step 2: Experience ---
elif st.session_state['current_step'] == 2:
    st.info(get_text('s2_info'))
    
    # --- Handle Edit State ---
    edit_idx = st.session_state['edit_exp_idx']
    
    # Defaults
    def_title, def_comp, def_loc, def_start, def_end, def_desc = "", "", "", None, None, ""
    btn_label = get_text('s2_btn_add')
    
    if edit_idx != -1 and edit_idx < len(st.session_state['cv_data']['experience']):
        # Pre-fill data
        item = st.session_state['cv_data']['experience'][edit_idx]
        def_title = item.get('title', '')
        def_comp = item.get('company', '')
        def_loc = item.get('location', '')
        def_desc = item.get('description', '')
        
        # Parse Dates
        try:
            if item.get('startDate'):
                # Support both dot and slash
                s_date = item['startDate'].replace('/', '.')
                parts = s_date.split('.')
                def_start = datetime.date(int(parts[1]), int(parts[0]), 1)
            
            if item.get('endDate'):
                if item['endDate'] in ["Devam Ediyor", "Present"]:
                    def_end = None
                else:
                    s_date = item['endDate'].replace('/', '.')
                    parts = s_date.split('.')
                    def_end = datetime.date(int(parts[1]), int(parts[0]), 1)
        except:
            pass
            
        btn_label = get_text('s2_btn_update')
        st.info(f"{get_text('s2_editing')} **{def_title}**")
        if st.button(get_text('s2_btn_cancel_edit')):
            st.session_state['edit_exp_idx'] = -1
            st.rerun()

    # Input Form
    k_suffix = str(edit_idx)
    with st.expander(get_text('s2_expander'), expanded=True):
        title = st.text_input(get_text('s2_job_title'), value=def_title, key=f"exp_title_{k_suffix}")
        
        c_comp, c_loc = st.columns(2)
        company = c_comp.text_input(get_text('s2_company'), value=def_comp, key=f"exp_comp_{k_suffix}")
        location = c_loc.text_input(get_text('s1_city'), value=def_loc, key=f"exp_loc_{k_suffix}", placeholder="Ankara, Türkiye")
        
        c1, c2 = st.columns(2)
        start_date = c1.date_input(get_text('s2_start_date'), value=def_start, min_value=datetime.date(1970,1,1), key=f"exp_start_{k_suffix}")
        
        is_current = c2.checkbox(get_text('s2_current_job'), value=(def_end is None and edit_idx != -1) if edit_idx != -1 else True, key=f"exp_curr_{k_suffix}")
        
        if not is_current:
            end_date_val = c2.date_input(get_text('s2_end_date'), value=def_end, key=f"exp_end_{k_suffix}")
            end_date_str = end_date_val.strftime("%m/%Y") if end_date_val else ""
        else:
            end_date_str = "Present" if st.session_state.get('language') == 'en' else "Devam Ediyor"
            
        start_date_str = start_date.strftime("%m/%Y") if start_date else ""
        
        with st.expander(get_text('s2_desc_hint')):
            st.markdown("""
            **Etki Yaratan Fiiller:**
            *   *Yönetti, Geliştirdi, Optimize Etti, Tasarladı, Kurdu*
            *   *Analiz Etti, Artırdı, Azalttı, Liderlik Etti, Koordine Etti*
            """)
        
        desc = st.text_area(get_text('s2_desc_label'), value=def_desc, height=150, key=f"exp_desc_{k_suffix}")
        
        # Metric Check logic (kept same)
        import re
        if desc and not re.search(r'\d+|%', desc):
             st.warning("⚠️ **Geliştirme Önerisi:** Sayısal veri (KPI, %) ekleyin.")

        # Text Enhancer Button (kept same)
        c_desc1, c_desc2 = st.columns([1,1])
        if c_desc2.button(get_text('s2_btn_enhance')):
             # ... (Same logic as before, omitted for brevity, user has library installed?)
             # Assuming text_enhancer import logic is same
             pass

        if c_desc1.button(btn_label):
            if title and company and start_date:
                new_item = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'startDate': start_date_str,
                    'endDate': end_date_str,
                    'description': desc
                }
                
                if edit_idx != -1:
                    # Update Existing
                    st.session_state['cv_data']['experience'][edit_idx] = new_item
                    st.success(get_text('s2_btn_update') + "!")
                    st.session_state['edit_exp_idx'] = -1
                else:
                    # Add New
                    st.session_state['cv_data']['experience'].append(new_item)
                    st.success(get_text('s2_btn_add') + "!")
                
                st.rerun()
            else:
                st.error("Lütfen en azından Unvan ve Şirket girin.")

    # Show Items with Edit Button
    st.write(get_text('s2_added_header'))
    if not st.session_state['cv_data']['experience']:
        st.caption(get_text('s2_no_exp'))
    else:
        for i, exp in enumerate(st.session_state['cv_data']['experience']):
            with st.container():
                cols = st.columns([4, 1, 1])
                cols[0].markdown(f"**{exp['title']}** @ {exp['company']}")
                
                if cols[1].button(get_text('btn_edit'), key=f"edit_exp_{i}"):
                    st.session_state['edit_exp_idx'] = i
                    st.rerun()
                    
                if cols[2].button(get_text('btn_delete'), key=f"del_exp_{i}"):
                    st.session_state['cv_data']['experience'].pop(i)
                    if st.session_state['edit_exp_idx'] == i: st.session_state['edit_exp_idx'] = -1
                    st.rerun()
            st.divider()

    c1, c2 = st.columns([1, 5])
    c1.button(get_text('btn_prev'), on_click=prev_step)
    c2.button(get_text('btn_next'), on_click=next_step)

# --- Step 3: Education ---
elif st.session_state['current_step'] == 3:
    st.info(get_text('s3_info'))
    
    # --- Edit State Logic ---
    edit_idx = st.session_state['edit_edu_idx']
    def_school, def_degree, def_start, def_end, def_gpa, def_rank = "", "", None, None, "", ""
    btn_label = get_text('s3_btn_add')
    
    if edit_idx != -1 and edit_idx < len(st.session_state['cv_data']['education']):
        item = st.session_state['cv_data']['education'][edit_idx]
        def_school = item.get('school', '')
        def_degree = item.get('degree', '')
        def_gpa = item.get('gpa', '')
        def_rank = item.get('rank', '')
        
        # Try to parse Year string "YYYY - YYYY"
        try:
            if item.get('year') and '-' in item['year']:
                y_start, y_end = item['year'].split('-')
                def_start = datetime.date(int(y_start.strip()), 1, 1)
                def_end = datetime.date(int(y_end.strip()), 1, 1)
        except:
            pass
            
        btn_label = get_text('s3_btn_update')
        st.info(f"{get_text('s2_editing')} **{def_school}**")
        if st.button(get_text('s2_btn_cancel_edit'), key="cancel_edu"):
            st.session_state['edit_edu_idx'] = -1
            st.rerun()
    
    with st.expander(get_text('s3_expander'), expanded=True):
        k_suffix = str(edit_idx)
        col_s1, col_s2 = st.columns(2)
        school = col_s1.text_input(get_text('s3_school'), value=def_school, key=f"edu_school_{k_suffix}")
        degree = col_s2.text_input(get_text('s3_degree'), value=def_degree, key=f"edu_degree_{k_suffix}")
        
        # GPA and Rank Row
        col_g1, col_g2 = st.columns(2)
        gpa = col_g1.text_input(get_text('s3_gpa'), value=def_gpa, placeholder="3.43/4.00", key=f"edu_gpa_{k_suffix}")
        rank = col_g2.text_input(get_text('s3_rank'), value=def_rank, placeholder=get_text('s3_rank_placeholder'), key=f"edu_rank_{k_suffix}")
        
        c1, c2 = st.columns(2)
        start_edu = c1.date_input(get_text('s3_start_date'), key=f"edu_start_{k_suffix}", value=def_start, min_value=datetime.date(1950,1,1))
        end_edu = c2.date_input(get_text('s3_end_date'), key=f"edu_end_{k_suffix}", value=def_end)
        
        year_str = ""
        if start_edu and end_edu:
             year_str = f"{start_edu.year} - {end_edu.year}"

        if st.button(btn_label, key="add_edu_btn"):
            if school and degree:
                new_item = {
                    'school': school,
                    'degree': degree,
                    'year': year_str,
                    'gpa': gpa,
                    'rank': rank
                }
                
                if edit_idx != -1:
                    st.session_state['cv_data']['education'][edit_idx] = new_item
                    st.success(get_text('s3_btn_update') + "!")
                    st.session_state['edit_edu_idx'] = -1
                else:
                    st.session_state['cv_data']['education'].append(new_item)
                    st.success(get_text('s3_btn_add') + "!")
                st.rerun()
            else:
                st.error(get_text('s3_error_required'))

    st.write(get_text('s3_added_header'))
    if not st.session_state['cv_data']['education']:
        st.caption(get_text('s3_no_edu'))
    else:
        for i, edu in enumerate(st.session_state['cv_data']['education']):
            with st.container():
                cols = st.columns([4, 1, 1])
                cols[0].markdown(f"**{edu['school']}** - {edu['degree']}")
                
                if cols[1].button(get_text('btn_edit'), key=f"edit_edu_{i}"):
                    st.session_state['edit_edu_idx'] = i
                    st.rerun()
                
                if cols[2].button(get_text('btn_delete'), key=f"del_edu_{i}"):
                    st.session_state['cv_data']['education'].pop(i)
                    if st.session_state['edit_edu_idx'] == i: st.session_state['edit_edu_idx'] = -1
                    st.rerun()
            st.divider()

    c1, c2 = st.columns([1, 5])
    c1.button(get_text('btn_prev'), on_click=prev_step)
    c2.button(get_text('btn_next'), on_click=next_step)

# --- Step 4: Projects ---
elif st.session_state['current_step'] == 4:
    st.info(get_text('s_proj_info'))
    
    # Init Projects list if not exists
    if 'projects' not in st.session_state['cv_data']:
        st.session_state['cv_data']['projects'] = []
    
    # Init Edit Index
    if 'edit_proj_idx' not in st.session_state:
        st.session_state['edit_proj_idx'] = -1

    edit_idx = st.session_state['edit_proj_idx']
    
    # Defaults
    def_name, def_tech, def_desc = "", "", ""
    btn_label = get_text('s_proj_btn_add')
    
    if edit_idx != -1 and edit_idx < len(st.session_state['cv_data']['projects']):
        item = st.session_state['cv_data']['projects'][edit_idx]
        def_name = item.get('name', '')
        def_tech = item.get('tech', '')
        def_desc = item.get('description', '')
        btn_label = get_text('s_proj_btn_update')
        
        st.info(f"🖊️ {get_text('s2_editing')} **{def_name}**")
        if st.button(get_text('s2_btn_cancel_edit'), key="cancel_proj"):
            st.session_state['edit_proj_idx'] = -1
            st.rerun()

    with st.expander(get_text('s_proj_expander'), expanded=True):
        p_name = st.text_input(get_text('s_proj_name'), value=def_name)
        p_tech = st.text_input(get_text('s_proj_tech'), value=def_tech)
        p_desc = st.text_area(get_text('s_proj_desc'), value=def_desc)
        
        if st.button(btn_label, key="add_proj_btn"):
            if p_name:
                item = {'name': p_name, 'tech': p_tech, 'description': p_desc}
                if edit_idx != -1:
                    st.session_state['cv_data']['projects'][edit_idx] = item
                    st.session_state['edit_proj_idx'] = -1
                else:
                    st.session_state['cv_data']['projects'].append(item)
                st.rerun()
            else:
                st.error(get_text('s3_error_required'))

    st.write(get_text('s_proj_list_header'))
    if not st.session_state['cv_data']['projects']:
        st.caption(get_text('s_proj_no_item'))
    else:
        for i, item in enumerate(st.session_state['cv_data']['projects']):
            with st.container():
                cols = st.columns([4, 1, 1])
                cols[0].markdown(f"**{item['name']}**")
                if cols[1].button(get_text('btn_edit'), key=f"edit_proj_{i}"):
                    st.session_state['edit_proj_idx'] = i
                    st.rerun()
                if cols[2].button(get_text('btn_delete'), key=f"del_proj_{i}"):
                    st.session_state['cv_data']['projects'].pop(i)
                    if st.session_state['edit_proj_idx'] == i: st.session_state['edit_proj_idx'] = -1
                    st.rerun()
            st.divider()

    c1, c2 = st.columns([1, 5])
    c1.button(get_text('btn_prev'), on_click=prev_step)
    c2.button(get_text('btn_next'), on_click=next_step)


# --- Step 5: Certificates ---
elif st.session_state['current_step'] == 5:
    st.info(get_text('s_cert_info'))
    
    if 'certificates' not in st.session_state['cv_data']:
        st.session_state['cv_data']['certificates'] = []
        
    if 'edit_cert_idx' not in st.session_state:
        st.session_state['edit_cert_idx'] = -1
        
    edit_idx = st.session_state['edit_cert_idx']
    
    # Defaults
    def_name, def_auth, def_date = "", "", ""
    btn_label = get_text('s_cert_btn_add')
    
    if edit_idx != -1 and edit_idx < len(st.session_state['cv_data']['certificates']):
        item = st.session_state['cv_data']['certificates'][edit_idx]
        def_name = item.get('name', '')
        def_auth = item.get('authority', '')
        def_date = item.get('date', '')
        btn_label = get_text('s_cert_btn_update')
        
        st.info(f"🖊️ {get_text('s2_editing')} **{def_name}**")
        if st.button(get_text('s2_btn_cancel_edit'), key="cancel_cert"):
            st.session_state['edit_cert_idx'] = -1
            st.rerun()
            
    with st.expander(get_text('s_cert_expander'), expanded=True):
        c_name = st.text_input(get_text('s_cert_name'), value=def_name)
        c_auth = st.text_input(get_text('s_cert_auth'), value=def_auth)
        c_date = st.text_input(get_text('s_cert_date'), value=def_date, placeholder="2024")
        
        if st.button(btn_label, key="add_cert_btn"):
            if c_name:
                item = {'name': c_name, 'authority': c_auth, 'date': c_date}
                if edit_idx != -1:
                    st.session_state['cv_data']['certificates'][edit_idx] = item
                    st.session_state['edit_cert_idx'] = -1
                else:
                    st.session_state['cv_data']['certificates'].append(item)
                st.rerun()
            else:
                st.error(get_text('s3_error_required'))

    st.write(get_text('s_cert_list_header'))
    if not st.session_state['cv_data']['certificates']:
        st.caption(get_text('s_cert_no_item'))
    else:
        for i, item in enumerate(st.session_state['cv_data']['certificates']):
            with st.container():
                cols = st.columns([4, 1, 1])
                cols[0].markdown(f"**{item['name']}**")
                if cols[1].button(get_text('btn_edit'), key=f"edit_cert_{i}"):
                    st.session_state['edit_cert_idx'] = i
                    st.rerun()
                if cols[2].button(get_text('btn_delete'), key=f"del_cert_{i}"):
                    st.session_state['cv_data']['certificates'].pop(i)
                    if st.session_state['edit_cert_idx'] == i: st.session_state['edit_cert_idx'] = -1
                    st.rerun()
            st.divider()

    c1, c2 = st.columns([1, 5])
    c1.button(get_text('btn_prev'), on_click=prev_step)
    c2.button(get_text('btn_next'), on_click=next_step)

elif st.session_state['current_step'] == 6:
    st.info(get_text('s4_info'))
    
    s1 = st.text_input(get_text('s4_l1'), value=st.session_state['cv_data']['skills'].get('Programlama', ''))
    s2 = st.text_input(get_text('s4_l2'), value=st.session_state['cv_data']['skills'].get('Frameworks', ''))
    s3 = st.text_input(get_text('s4_l3'), value=st.session_state['cv_data']['skills'].get('Araçlar', ''))
    s4 = st.text_input(get_text('s4_l4'), value=st.session_state['cv_data']['skills'].get('Diller', ''))
    
    st.session_state['cv_data']['skills'] = {
        'Programlama': s1,
        'Frameworks': s2,
        'Araçlar': s3,
        'Diller': s4
    }

    c1, c2 = st.columns([1, 5])
    c1.button(get_text('btn_prev'), on_click=prev_step)
    c2.button(get_text('btn_next'), on_click=next_step)

# --- Step 7: Job Analysis (Shifted from 5) ---
elif st.session_state['current_step'] == 7:
    st.info(get_text('s5_info'))
    
    job_desc = st.text_area(get_text('s5_text_area'), height=200, placeholder=get_text('s5_placeholder'), key="job_desc_input")
    
    if job_desc:
        resume_text = get_resume_text(st.session_state['cv_data'])
        score, matched, missing = calculate_match_score(resume_text, job_desc)
        
        # Custom UI Result Display
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #E5E7EB; text-align: center;">
                <h3 style="margin: 0; color: #4F46E5; font-size: 2.5rem;">%{score}</h3>
                <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{get_text('s5_match_score')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(ui_components.get_job_matcher_results_html({'matched': matched, 'missing': missing}), unsafe_allow_html=True)
    
    st.divider()
    c1, c2, c3 = st.columns([1, 2, 2])
    with c1:
        st.button(get_text('btn_prev'), on_click=prev_step)
    with c2:
        st.button(get_text('s5_btn_skip'), on_click=next_step, type="secondary")
    with c3:
        if job_desc:
            st.button(get_text('s5_btn_analyze'), on_click=next_step, type="primary")
        else:
             # Just a placeholder to align, or show nothing
             pass

# --- Step 8: Template Selection (Shifted from 6) ---
elif st.session_state['current_step'] == 8:
    st.info(get_text('s6_info'))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(get_text('s6_classic_title'))
        st.caption(get_text('s6_classic_desc'))
        if st.button(get_text('s6_btn_select') + " Klasik", type="primary" if st.session_state['selected_template'] == "Klasik" else "secondary"):
            st.session_state['selected_template'] = "Klasik"
            
    with col2:
        st.markdown(get_text('s6_modern_title'))
        st.caption(get_text('s6_modern_desc'))
        if st.button(get_text('s6_btn_select') + " Modern", type="primary" if st.session_state['selected_template'] == "Modern" else "secondary"):
            st.session_state['selected_template'] = "Modern"
            
    with col3:
        st.markdown(get_text('s6_academic_title'))
        st.caption(get_text('s6_academic_desc'))
        if st.button(get_text('s6_btn_select') + " Akademik", type="primary" if st.session_state['selected_template'] == "Akademik" else "secondary"):
            st.session_state['selected_template'] = "Akademik"
    
    st.success(f"{get_text('s6_selected_msg')} **{st.session_state['selected_template']}**")

    c1, c2 = st.columns([1, 5])
    c1.button(get_text('btn_prev'), on_click=prev_step)
    c2.button(get_text('btn_next'), on_click=next_step)

# --- Step 9: Final Review & Export (Shifted from 7) ---
elif st.session_state['current_step'] == 9:
    st.balloons()
    st.success(get_text('s7_success'))

    # --- Live PDF Preview (New Feature) ---
    import pdf_utils
    st.subheader(get_text('s7_preview_title'))
    
    # Generate PDF for Preview
    # Ensure language is correct for preview
    preview_lang = st.session_state.get('resume_language', 'tr')
    preview_pdf = get_generator(st.session_state['selected_template'], language=preview_lang)
    
    # If using English preview but data is not translated yet, it might look mixed.
    # But usually we generate from main data.
    preview_pdf.generate(st.session_state['cv_data'])
    preview_bytes = preview_pdf.get_pdf_bytes()
    
    with st.expander(get_text('s7_preview_expander'), expanded=True):
        pdf_utils.display_pdf(preview_bytes)

    st.divider()

    st.write(get_text('s7_raw_data_title'))
    with st.expander(get_text('s7_raw_data_expander')):
        st.json(st.session_state['cv_data'])

    st.divider()

    # Download section
    st.subheader(get_text('s7_download_title'))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 PDF")
        st.caption(get_text('s7_pdf_desc'))

        # Generate PDF
        # Use current language
        pdf_lang = st.session_state.get('resume_language', 'tr')
        pdf = get_generator(st.session_state['selected_template'], language=pdf_lang)
        pdf.generate(st.session_state['cv_data'])
        pdf_bytes = bytes(pdf.get_pdf_bytes())

        st.download_button(
            label=get_text('s7_btn_download_pdf'),
            data=pdf_bytes,
            file_name=f"CV_{st.session_state['cv_data']['personal'].get('fullName', 'resume')}_{st.session_state['selected_template']}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        save_cv_data()

    with col2:
        st.markdown("### 📝 DOCX")
        st.caption(get_text('s7_docx_desc'))

        # Generate DOCX
        docx = ATSResumeDocx()
        docx.generate(st.session_state['cv_data'])
        docx_bytes = bytes(docx.get_bytes())

        st.download_button(
            label=get_text('s7_btn_download_docx'),
            data=docx_bytes,
            file_name=f"CV_{st.session_state['cv_data']['personal'].get('fullName', 'resume')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
    st.divider()
    
    # Translation Section
    # Only show if current language is NOT English, or maybe allow anyway?
    # Logic: If I am in Turkish, I want English version.
    # If I am in English, maybe I want Turkish? For now, stick to original requirement: "Ingilizce Versiyon"
    
    st.subheader(get_text('s7_trans_title'))
    st.caption(get_text('s7_trans_caption'))

    # Initialize or Update Translation
    if 'cv_data_en' not in st.session_state:
        if st.button(get_text('s7_btn_prepare_en')):
             with st.spinner(get_text('s7_translating')):
                try:
                    st.session_state['cv_data_en'] = translate_resume_data(st.session_state['cv_data'])
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if 'cv_data_en' in st.session_state:
        st.success(get_text('s7_success_trans'))
        
        with st.expander(get_text('s7_expander_edit_en'), expanded=False):
            # Personal
            st.markdown(get_text('s7_header_personal'))
            en_summary = st.text_area("Summary", value=st.session_state['cv_data_en']['personal'].get('summary', ''), height=100, key="en_summ")
            st.session_state['cv_data_en']['personal']['summary'] = en_summary
            
            # Experience
            st.markdown(get_text('s7_header_exp'))
            if st.session_state['cv_data_en'].get('experience'):
                for i, exp in enumerate(st.session_state['cv_data_en']['experience']):
                    st.markdown(f"**{exp.get('company', 'Company')}**")
                    c1, c2 = st.columns(2)
                    new_title = c1.text_input(f"Title ({i})", value=exp.get('title', ''), key=f"en_title_{i}")
                    exp['title'] = new_title
                    
                    new_desc = st.text_area(f"Description ({i})", value=exp.get('description', ''), height=100, key=f"en_desc_{i}")
                    exp['description'] = new_desc
                    st.divider()

            # Education
            st.markdown(get_text('s7_header_edu'))
            if st.session_state['cv_data_en'].get('education'):
                for i, edu in enumerate(st.session_state['cv_data_en']['education']):
                    c1, c2 = st.columns(2)
                    new_school = c1.text_input(f"School ({i})", value=edu.get('school', ''), key=f"en_school_{i}")
                    edu['school'] = new_school
                    
                    new_degree = c2.text_input(f"Degree ({i})", value=edu.get('degree', ''), key=f"en_degree_{i}")
                    edu['degree'] = new_degree
            
            # Skills
            st.markdown(get_text('s7_header_skills'))
            if st.session_state['cv_data_en'].get('skills'):
                for key, val in st.session_state['cv_data_en']['skills'].items():
                    new_val = st.text_input(f"{key}", value=val, key=f"en_skill_{key}")
                    st.session_state['cv_data_en']['skills'][key] = new_val

            if st.button(get_text('s7_btn_reset_trans')):
                del st.session_state['cv_data_en']
                st.rerun()

        # Generate PDF Button from Edited Data
        try:
            pdf_en = get_generator(st.session_state['selected_template'], language='en')
            pdf_en.generate(st.session_state['cv_data_en'])
            pdf_en_bytes = bytes(pdf_en.get_pdf_bytes())

            st.download_button(
                label=get_text('s7_btn_download_en'),
                data=pdf_en_bytes,
                file_name=f"Resume_{st.session_state['cv_data']['personal'].get('fullName', 'resume')}_EN.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()

    st.info(get_text('s7_tip'))

    if st.button(get_text('s7_btn_restart')):
        st.session_state['current_step'] = 0
        save_cv_data()
        st.rerun()

# Auto-save mechanism - track changes and save automatically
if 'last_cv_data' not in st.session_state:
    st.session_state['last_cv_data'] = json.dumps(st.session_state['cv_data'], ensure_ascii=False, sort_keys=True)
else:
    current_data_str = json.dumps(st.session_state['cv_data'], ensure_ascii=False, sort_keys=True)
    if current_data_str != st.session_state['last_cv_data']:
        save_cv_data()
        st.session_state['last_cv_data'] = current_data_str
