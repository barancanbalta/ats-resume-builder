import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
/* Main Font and Background */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Primary Button Styling */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #4F46E5 0%, #3B82F6 100%);
    color: white;
    border: none;
    padding: 0.5rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

/* Secondary Button (Outline) */
div.stButton > button.secondary {
    background: transparent;
    border: 1px solid #E5E7EB;
    color: #374151;
}

/* Text Inputs / Text Areas */
div[data-baseweb="input"] > div {
    background-color: #F9FAFB !important;
    border-radius: 8px !important;
    border: 1px solid #E5E7EB !important;
}

div[data-baseweb="input"]:focus-within > div {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 1px #4F46E5 !important;
}

/* Cards / Containers */
.stExpander {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #F3F4F6;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Progress Bar Container */
.progress-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    position: relative;
}

.progress-step {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #E5E7EB;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    color: #6B7280;
    z-index: 10;
    position: relative;
}

.progress-step.active {
    background-color: #4F46E5;
    color: white;
    box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.2);
}

.progress-line {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #E5E7EB;
    transform: translateY(-50%);
    z-index: 0;
}

.progress-line-fill {
    height: 100%;
    background-color: #4F46E5;
    transition: width 0.3s ease;
}

/* Header */
.header-container {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
    padding: 2rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 2rem;
    text-align: center;
}

.header-title {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(90deg, #818CF8, #C7D2FE);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

</style>
    """, unsafe_allow_html=True)

def render_header(user_name="User"):
    st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">ATS Resume Builder</h1>
        <p style="opacity: 0.8; margin-top: 0.5rem;">Profesyonel Kariyer Asistanınız</p>
        <div style="margin-top: 1rem; font-size: 0.9rem; background: rgba(255,255,255,0.1); display: inline-block; padding: 4px 12px; border-radius: 20px;">
            Hoşgeldin, {user_name}
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_progress_bar_html(current_step, total_steps, current_step_name):
    fill_percent = (current_step / (total_steps - 1)) * 100
    
    steps_html = ""
    for i in range(total_steps):
        is_active = "active" if i <= current_step else ""
        steps_html += f'<div class="progress-step {is_active}">{i+1}</div>'
    
    return f"""
    <div class="progress-container">
        <div class="progress-line">
            <div class="progress-line-fill" style="width: {fill_percent}%;"></div>
        </div>
        {steps_html}
    </div>
    <div style="text-align: center; font-weight: 600; color: #4F46E5; margin-bottom: 2rem;">Adım {current_step + 1}: {current_step_name}</div>
    """

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🛠 Araçlar")
        st.info("💡 **İpucu:** Verileriniz tarayıcınızda saklanır. Oturumu kapatmadan önce PDF'inizi indirmeyi unutmayın.")
        
        st.markdown("---")
        st.markdown("Developed by **Baran**")
        st.caption("v2.1.0 • ATS Optimized")

def get_job_matcher_results_html(results):
    missing_badges = "".join([f'<span style="background:#FEE2E2; color:#B91C1C; padding:4px 8px; border-radius:4px; margin:2px; font-size:0.85em;">{w}</span>' for w in results.get('missing', [])])
    matched_badges = "".join([f'<span style="background:#D1FAE5; color:#047857; padding:4px 8px; border-radius:4px; margin:2px; font-size:0.85em;">{w}</span>' for w in results.get('matched', [])])
    
    return f"""
    <div style="display:flex; gap:1rem; flex-wrap:wrap;">
        <div style="flex:1; min-width:300px; background:white; padding:1rem; border-radius:8px; border:1px solid #E5E7EB;">
            <h4 style="margin:0 0 0.5rem 0; color:#B91C1C;">Lütfen Ekleyin ({len(results.get('missing', []))})</h4>
            <div style="display:flex; flex-wrap:wrap;">{missing_badges}</div>
        </div>
        <div style="flex:1; min-width:300px; background:white; padding:1rem; border-radius:8px; border:1px solid #E5E7EB;">
            <h4 style="margin:0 0 0.5rem 0; color:#047857;">Mevcut ({len(results.get('matched', []))})</h4>
            <div style="display:flex; flex-wrap:wrap;">{matched_badges}</div>
        </div>
    </div>
    """
