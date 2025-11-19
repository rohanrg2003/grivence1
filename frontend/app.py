import streamlit as st
import requests
from datetime import datetime
import time

API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")

# Ultra-aesthetic CSS with beautiful color palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Outfit', -apple-system, sans-serif;
    }
    
    /* Aesthetic dark base with warm undertones */
    .main {
        background: linear-gradient(135deg, #1a1625 0%, #2d1b3d 50%, #1a1625 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Aesthetic color palette: Lavender, Coral, Mint, Peach */
    :root {
        --lavender: #b4a5ff;
        --coral: #ff8a9b;
        --mint: #7fffd4;
        --peach: #ffb38a;
        --cream: #fff5e6;
        --dark-purple: #2d1b3d;
        --soft-purple: #4a3b5c;
    }
    
    /* Dreamy glassmorphism cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.08) 0%, rgba(255, 138, 155, 0.06) 100%);
        backdrop-filter: blur(30px) saturate(200%);
        border: 1.5px solid rgba(180, 165, 255, 0.2);
        border-radius: 28px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px rgba(180, 165, 255, 0.15),
                    0 0 0 1px rgba(255, 255, 255, 0.02) inset,
                    0 20px 60px rgba(45, 27, 61, 0.5);
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(180, 165, 255, 0.1), transparent);
        transition: left 0.7s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(180, 165, 255, 0.4);
        box-shadow: 0 16px 48px rgba(180, 165, 255, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.05) inset,
                    0 30px 90px rgba(45, 27, 61, 0.6);
    }
    
    /* Gradient text with aesthetic colors */
    .gradient-text {
        background: linear-gradient(135deg, #b4a5ff 0%, #ff8a9b 50%, #7fffd4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Soft glow effect */
    .soft-glow {
        text-shadow: 0 0 20px rgba(180, 165, 255, 0.6),
                     0 0 40px rgba(255, 138, 155, 0.3),
                     0 0 60px rgba(127, 255, 212, 0.2);
        animation: glowPulse 3s ease-in-out infinite;
    }
    
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 20px rgba(180, 165, 255, 0.6); }
        50% { text-shadow: 0 0 30px rgba(255, 138, 155, 0.8); }
    }
    
    /* Aesthetic buttons with soft gradients */
    .stButton>button {
        background: linear-gradient(135deg, #b4a5ff 0%, #ff8a9b 100%);
        color: #1a1625;
        border: none;
        border-radius: 18px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        box-shadow: 0 6px 24px rgba(180, 165, 255, 0.35),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 12px 36px rgba(180, 165, 255, 0.5),
                    0 0 0 1px rgba(255, 255, 255, 0.2) inset;
        background: linear-gradient(135deg, #c7b8ff 0%, #ffaab8 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Dreamy tabs with soft colors */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background: rgba(180, 165, 255, 0.05);
        border-radius: 24px;
        padding: 10px;
        border: 1px solid rgba(180, 165, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 18px;
        color: #b4a5ff;
        font-weight: 600;
        padding: 16px 32px;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        border: 1px solid transparent;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(180, 165, 255, 0.15);
        border-color: rgba(180, 165, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.25) 0%, rgba(255, 138, 155, 0.25) 100%) !important;
        color: #fff5e6 !important;
        border-color: rgba(180, 165, 255, 0.4) !important;
        box-shadow: 0 4px 20px rgba(180, 165, 255, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
    }
    
    /* Soft input fields */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        background: rgba(180, 165, 255, 0.05) !important;
        border: 1.5px solid rgba(180, 165, 255, 0.2) !important;
        border-radius: 18px !important;
        padding: 16px 20px !important;
        color: #fff5e6 !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        border-color: #b4a5ff !important;
        box-shadow: 0 0 0 4px rgba(180, 165, 255, 0.15) !important;
        background: rgba(180, 165, 255, 0.08) !important;
        transform: translateY(-2px);
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(180, 165, 255, 0.4) !important;
    }
    
    /* Aesthetic metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #b4a5ff 0%, #ff8a9b 50%, #7fffd4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(180, 165, 255, 0.7) !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Dreamy sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d1b3d 0%, #3d2550 50%, #2d1b3d 100%);
        border-right: 1px solid rgba(180, 165, 255, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #fff5e6 !important;
    }
    
    /* Soft alerts */
    .stSuccess {
        background: linear-gradient(135deg, rgba(127, 255, 212, 0.15) 0%, rgba(180, 165, 255, 0.1) 100%) !important;
        border: 1.5px solid rgba(127, 255, 212, 0.4) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        color: #7fffd4 !important;
        animation: slideInUp 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 138, 155, 0.15) 0%, rgba(180, 165, 255, 0.1) 100%) !important;
        border: 1.5px solid rgba(255, 138, 155, 0.4) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        color: #ff8a9b !important;
        animation: slideInUp 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.15) 0%, rgba(255, 179, 138, 0.1) 100%) !important;
        border: 1.5px solid rgba(180, 165, 255, 0.4) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        color: #b4a5ff !important;
        animation: slideInUp 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 179, 138, 0.15) 0%, rgba(180, 165, 255, 0.1) 100%) !important;
        border: 1.5px solid rgba(255, 179, 138, 0.4) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        color: #ffb38a !important;
        animation: slideInUp 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Soft expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.08) 0%, rgba(255, 138, 155, 0.06) 100%) !important;
        border-radius: 18px !important;
        border: 1.5px solid rgba(180, 165, 255, 0.2) !important;
        color: #fff5e6 !important;
        font-weight: 700 !important;
        padding: 1.25rem 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.15) 0%, rgba(255, 138, 155, 0.12) 100%) !important;
        border-color: rgba(180, 165, 255, 0.4) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(180, 165, 255, 0.2);
    }
    
    /* Dreamy file uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.05) 0%, rgba(255, 138, 155, 0.03) 100%);
        border: 2px dashed rgba(180, 165, 255, 0.4);
        border-radius: 22px;
        padding: 3rem;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    [data-testid="stFileUploader"]:hover {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.1) 0%, rgba(255, 138, 155, 0.08) 100%);
        border-color: rgba(180, 165, 255, 0.6);
        transform: scale(1.02);
    }
    
    /* Beautiful headers */
    h1 {
        color: #fff5e6 !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    h2, h3 {
        color: #fff5e6 !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    p {
        color: rgba(255, 245, 230, 0.8) !important;
        line-height: 1.8 !important;
    }
    
    /* Aesthetic progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #b4a5ff 0%, #ff8a9b 50%, #7fffd4 100%);
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(180, 165, 255, 0.5);
    }
    
    /* Custom scrollbar with aesthetic colors */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(180, 165, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.4) 0%, rgba(255, 138, 155, 0.4) 100%);
        border-radius: 10px;
        border: 2px solid transparent;
        background-clip: padding-box;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, rgba(180, 165, 255, 0.6) 0%, rgba(255, 138, 155, 0.6) 100%);
        background-clip: padding-box;
    }
    
    /* Floating particles background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 15% 15%, rgba(180, 165, 255, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 85% 85%, rgba(255, 138, 155, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(127, 255, 212, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: floatingParticles 20s ease-in-out infinite;
    }
    
    @keyframes floatingParticles {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        33% {
            transform: translate(30px, -30px) scale(1.1);
        }
        66% {
            transform: translate(-20px, 20px) scale(0.9);
        }
    }
    
    /* Smooth transitions for everything */
    * {
        transition: color 0.3s ease, background 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Grievance Portal",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dreamy Hero Header
st.markdown("""
    <div style='text-align: center; padding: 4rem 0 3rem 0;'>
        <div style='font-size: 0.95rem; color: #b4a5ff; font-weight: 700; letter-spacing: 3px; 
                    margin-bottom: 1.5rem; text-transform: uppercase;'>
            ✨ Powered by Intelligence
        </div>
        <h1 class='gradient-text soft-glow' style='font-size: 5rem; margin: 0; line-height: 1;'>
            Grievance Portal
        </h1>
        <p style='font-size: 1.35rem; color: rgba(180, 165, 255, 0.7); margin-top: 1.5rem; 
                  max-width: 700px; margin-left: auto; margin-right: auto; font-weight: 500; line-height: 1.6;'>
            Your voice shapes change. Experience seamless grievance management with our intelligent platform.
        </p>
    </div>
""", unsafe_allow_html=True)

# Aesthetic Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1.5rem 0;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>✨</div>
            <h3 style='margin: 0; font-family: Space Grotesk;'>USER PORTAL</h3>
        </div>
    """, unsafe_allow_html=True)
    
    user_id = st.number_input("Your User ID", min_value=1, value=1, help="Your unique identifier")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Dashboard with aesthetic colors
    st.markdown("### 📊 Your Dashboard")
    
    try:
        stats_response = requests.get(f"{API_BASE}/grievances", timeout=3)
        if stats_response.status_code == 200:
            all_grievances = stats_response.json()
            if isinstance(all_grievances, list):
                total = len(all_grievances)
                user_grievances = [g for g in all_grievances if g.get('user_id') == user_id]
                pending = len([g for g in user_grievances if g.get('status') == 'Pending'])
                resolved = len([g for g in user_grievances if g.get('status') == 'Resolved'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌐 Total", total)
                    st.metric("⏳ Pending", pending)
                with col2:
                    st.metric("👤 Yours", len(user_grievances))
                    st.metric("✨ Resolved", resolved)
    except:
        st.metric("Status", "Connecting...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Actions")
    if st.button("✨ New Grievance", use_container_width=True):
        st.session_state.active_tab = 0
    if st.button("🔍 Track Status", use_container_width=True):
        st.session_state.active_tab = 1
    if st.button("📊 View Dashboard", use_container_width=True):
        st.session_state.active_tab = 2
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 💎 Platform Features")
    st.markdown("""
    <div style='font-size: 0.9rem; line-height: 2; color: rgba(255, 245, 230, 0.8);'>
    ⚡ Lightning-fast Processing<br>
    🔐 Bank-level Security<br>
    🤖 AI Smart Categorization<br>
    📱 Instant Notifications<br>
    📈 Real-time Analytics<br>
    🌍 Available 24/7
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 💬 Need Help?")
    st.markdown("""
    <div style='font-size: 0.88rem; color: rgba(180, 165, 255, 0.8); line-height: 1.8;'>
    📧 help@portal.com<br>
    📱 +1 (800) 123-4567<br>
    💬 Live Chat: Available
    </div>
    """, unsafe_allow_html=True)

# Main Content Tabs
tab1, tab2, tab3 = st.tabs(["✨ SUBMIT", "🔍 TRACK", "📊 DASHBOARD"])

# TAB 1: Submit Grievance
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.markdown("## ✨ Submit Your Grievance")
        st.markdown("""
            <p style='font-size: 1.1rem; color: rgba(180, 165, 255, 0.7); line-height: 1.7;'>
                Our intelligent system will analyze and route your grievance to the appropriate department within minutes.
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(180, 165, 255, 0.12) 0%, rgba(255, 138, 155, 0.08) 100%);
                    padding: 2rem; border-radius: 22px; border: 1.5px solid rgba(180, 165, 255, 0.25);'>
            <div style='font-size: 0.9rem; color: #b4a5ff; font-weight: 700; margin-bottom: 1rem; letter-spacing: 1px;'>
                💡 SUBMISSION TIPS
            </div>
            <div style='font-size: 0.9rem; color: rgba(255, 245, 230, 0.85); line-height: 2;'>
            • Clear and specific title<br>
            • Detailed description<br>
            • Relevant documentation<br>
            • Professional language
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.form("grievance_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            title = st.text_input(
                "📌 Grievance Title",
                placeholder="e.g., Delayed salary payment for October 2024",
                help="Provide a clear, concise title"
            )
            
            description = st.text_area(
                "📝 Detailed Description",
                height=300,
                placeholder="Describe your grievance comprehensively...\n\n• What happened?\n• When did it occur?\n• Who was involved?\n• What outcome do you expect?",
                help="More details help us resolve faster"
            )
            
            col1a, col1b = st.columns(2)
            with col1a:
                category = st.selectbox(
                    "🏷️ Category",
                    ["Select Category", "💼 HR & Payroll", "🏢 Infrastructure", "⚠️ Harassment", 
                     "📋 Policy Issues", "🔧 Technical", "💰 Financial", "✨ Other"],
                )
            
            with col1b:
                priority = st.select_slider(
                    "⚡ Priority Level",
                    options=["🟢 Low", "🟡 Medium", "🟠 High", "🔴 Urgent"],
                    value="🟡 Medium",
                )
        
        with col2:
            st.markdown("#### 📎 Attachments")
            uploaded_file = st.file_uploader(
                "Drag files here or click to browse",
                type=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xlsx'],
                help="Maximum 10MB per file",
                label_visibility="collapsed"
            )
            
            if uploaded_file:
                file_size = len(uploaded_file.getvalue()) / 1024
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(127, 255, 212, 0.15) 0%, rgba(180, 165, 255, 0.1) 100%);
                            padding: 1.25rem; border-radius: 16px; margin-top: 1rem;
                            border: 1.5px solid rgba(127, 255, 212, 0.4);'>
                    <div style='color: #7fffd4; font-weight: 700; font-size: 0.95rem;'>✅ {uploaded_file.name}</div>
                    <div style='color: rgba(180, 165, 255, 0.7); font-size: 0.85rem; margin-top: 0.5rem;'>
                        {file_size:.1f} KB • {uploaded_file.type}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("#### 🔔 Notifications")
            email_notify = st.checkbox("📧 Email updates", value=True)
            sms_notify = st.checkbox("📱 SMS alerts", value=False)
            push_notify = st.checkbox("🔔 Push notifications", value=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            anonymous = st.checkbox("🕶️ Submit anonymously", help="Your identity will remain confidential")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1.2, 1, 1.8])
        with col1:
            submitted = st.form_submit_button("✨ SUBMIT", use_container_width=True, type="primary")
        with col2:
            st.form_submit_button("💾 SAVE DRAFT", use_container_width=True)
    
    if submitted:
        if not title or not description:
            st.error("⚠️ Please complete all required fields")
        elif category == "Select Category":
            st.error("⚠️ Please select a category")
        else:
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    ("🔐 Securing your data...", 20),
                    ("🤖 AI analysis in progress...", 40),]