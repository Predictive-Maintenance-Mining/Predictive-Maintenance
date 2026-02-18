import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(
    page_title="Asset Analysis - Haul Truck HT20002",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Hide default Streamlit multipage navigation */
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# 🔙 Back to Main Dashboard Button (Top Right)
# ============================================================

col_back1, col_back2 = st.columns([6, 1])

if st.button("⬅ Back to Dashboard"):
    st.markdown(
        '<meta http-equiv="refresh" content="0; url=/" />',
        unsafe_allow_html=True,
    )


# Color Theme
BG_PRIMARY = "#0d1117"
BG_SECONDARY = "#161b22"
BG_TERTIARY = "#21262d"
BG_CARD = "#1c2128"
ACCENT_ORANGE = "#ff9800"
ACCENT_BLUE = "#58a6ff"
SUCCESS = "#3fb950"
WARNING = "#d29922"
CRITICAL = "#f85149"
TEXT_PRIMARY = "#c9d1d9"
TEXT_SECONDARY = "#8b949e"
BORDER_COLOR = "#30363d"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }}
    
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;
    }}
    
    .stApp {{
        background-color: {BG_PRIMARY};
        color: {TEXT_PRIMARY};
    }}
    
    * {{
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BG_SECONDARY} 0%, {BG_PRIMARY} 100%);
        border-right: 3px solid {ACCENT_ORANGE};
        box-shadow: 4px 0 20px rgba(0,0,0,0.5);
        min-width: 320px !important;
        max-width: 320px !important;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent;
        padding: 1.5rem 1rem;
    }}
    
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {BG_PRIMARY};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {ACCENT_ORANGE};
        border-radius: 4px;
    }}
    
    .sidebar-header {{
        text-align: center;
        padding: 1.2rem 1rem;
        background: linear-gradient(135deg, {BG_TERTIARY} 0%, {BG_CARD} 100%);
        border-radius: 10px;
        margin-bottom: 1.2rem;
        border: 2px solid {ACCENT_ORANGE};
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.15);
        position: relative;
        overflow: hidden;
    }}
    
    .sidebar-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 152, 0, 0.1), transparent);
        animation: shimmer 3s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    .sidebar-title {{
        font-size: 1.25rem;
        font-weight: 900;
        color: {ACCENT_ORANGE};
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 0 0 20px rgba(255, 152, 0, 0.3);
    }}
    
    .sidebar-subtitle {{
        font-size: 0.75rem;
        color: {TEXT_SECONDARY};
        margin-top: 0.4rem;
        font-weight: 500;
    }}
    
    .sidebar-section {{
        background: linear-gradient(135deg, {BG_SECONDARY} 0%, {BG_TERTIARY} 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid {BORDER_COLOR};
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    .sidebar-section:hover {{
        border-color: rgba(255, 152, 0, 0.5);
    }}
    
    .sidebar-section-title {{
        font-size: 0.85rem;
        font-weight: 800;
        color: {ACCENT_ORANGE};
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        letter-spacing: 0.8px;
        border-bottom: 2px solid {ACCENT_ORANGE};
        padding-bottom: 0.5rem;
    }}
    
    .sidebar-metric {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0;
        border-bottom: 1px solid {BORDER_COLOR};
    }}
    
    .sidebar-metric:last-child {{
        border-bottom: none;
    }}
    
    .sidebar-metric-label {{
        font-size: 0.8rem;
        color: {TEXT_SECONDARY};
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    .sidebar-metric-value {{
        font-size: 0.85rem;
        color: {TEXT_PRIMARY};
        font-weight: 800;
    }}
    
    .status-indicator {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 6px currentColor;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    .status-active {{ background-color: {SUCCESS}; }}
    .status-warning {{ background-color: {WARNING}; }}
    .status-critical {{ background-color: {CRITICAL}; }}
    
    /* Main Header */
    .main-header {{
        background: linear-gradient(135deg, {BG_SECONDARY} 0%, {BG_TERTIARY} 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        border-left: 5px solid {ACCENT_ORANGE};
        margin-bottom: 2rem;
        box-shadow: 0 6px 24px rgba(0,0,0,0.4);
    }}
    
    .main-title {{
        font-size: 1.8rem;
        font-weight: 900;
        color: {TEXT_PRIMARY};
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}
    
    .sub-title {{
        font-size: 0.9rem;
        color: {TEXT_SECONDARY};
        margin-top: 0.5rem;
        font-weight: 500;
    }}
    
    .live-badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: {CRITICAL};
        color: white;
        padding: 3px 10px;
        border-radius: 16px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-left: 12px;
        animation: livePulse 2s infinite;
    }}
    
    @keyframes livePulse {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(244, 81, 73, 0.7); }}
        50% {{ box-shadow: 0 0 0 6px rgba(244, 81, 73, 0); }}
    }}
    
    /* Health Cards */
    .health-card {{
        background: linear-gradient(135deg, {BG_CARD} 0%, {BG_TERTIARY} 100%);
        border-radius: 12px;
        padding: 1.2rem;
        border: 2px solid {BORDER_COLOR};
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        height: 100%;
        min-height: 280px;
        position: relative;
    }}
    
    .health-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {ACCENT_ORANGE}, {ACCENT_BLUE});
    }}
    
    .health-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(0,0,0,0.4);
        border-color: {ACCENT_ORANGE};
    }}
    
    .health-card-title {{
        font-size: 0.8rem;
        color: {TEXT_SECONDARY};
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }}
    
    .health-score {{
        font-size: 3rem;
        font-weight: 900;
        margin: 0.8rem 0;
        line-height: 1;
        text-shadow: 0 0 25px currentColor;
    }}
    
    .health-status {{
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.8rem;
        letter-spacing: 0.5px;
    }}
    
    .status-healthy {{ background: {SUCCESS}; color: #000; }}
    .status-warning-badge {{ background: {WARNING}; color: #000; }}
    .status-critical-badge {{ background: {CRITICAL}; color: #fff; }}
    
    /* Metric Cards */
    .metric-card {{
        background: linear-gradient(135deg, {BG_SECONDARY} 0%, {BG_CARD} 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid {BORDER_COLOR};
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        height: 100%;
        min-height: 90px;
    }}
    
    .metric-card:hover {{
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        border-color: {ACCENT_ORANGE};
    }}
    
    .metric-label {{
        font-size: 0.7rem;
        color: {TEXT_SECONDARY};
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }}
    
    .metric-value {{
        font-size: 1.3rem;
        font-weight: 900;
        color: {TEXT_PRIMARY};
        line-height: 1.2;
    }}
    
    .metric-badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 800;
        margin-top: 0.4rem;
        letter-spacing: 0.3px;
    }}
    
    .badge-running {{ background: {SUCCESS}; color: #000; }}
    
    /* Alert Boxes */
    .alert-box {{
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid;
        font-size: 0.85rem;
        font-weight: 500;
        background: {BG_SECONDARY};
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        cursor: pointer;
    }}
    
    .alert-box:hover {{
        transform: translateX(3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }}
    
    .alert-critical {{
        border-left-color: {CRITICAL};
        background: linear-gradient(90deg, rgba(244, 81, 73, 0.1) 0%, {BG_SECONDARY} 100%);
    }}
    
    .alert-critical strong {{
        color: {CRITICAL};
    }}
    
    .alert-warning {{
        border-left-color: {WARNING};
        background: linear-gradient(90deg, rgba(210, 153, 34, 0.1) 0%, {BG_SECONDARY} 100%);
    }}
    
    .alert-warning strong {{
        color: {WARNING};
    }}
    
    .alert-info {{
        border-left-color: {ACCENT_BLUE};
        background: linear-gradient(90deg, rgba(88, 166, 255, 0.1) 0%, {BG_SECONDARY} 100%);
    }}
    
    .alert-info strong {{
        color: {ACCENT_BLUE};
    }}
    
    /* Action Cards */
    .action-card {{
        background: linear-gradient(135deg, {BG_CARD} 0%, {BG_TERTIARY} 100%);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border: 2px solid {BORDER_COLOR};
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        cursor: pointer;
    }}
    
    .action-card:hover {{
        border-color: {ACCENT_ORANGE};
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.2);
        transform: translateY(-2px);
    }}
    
    .action-priority {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }}
    
    .priority-high {{ background: {CRITICAL}; color: #fff; }}
    .priority-medium {{ background: {WARNING}; color: #000; }}
    .priority-low {{ background: {SUCCESS}; color: #000; }}
    
    .action-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin-bottom: 0.5rem;
    }}
    
    .action-description {{
        font-size: 0.8rem;
        color: {TEXT_SECONDARY};
        line-height: 1.5;
        margin-bottom: 0.8rem;
    }}
    
    .action-meta {{
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: {TEXT_SECONDARY};
        padding-top: 0.8rem;
        border-top: 1px solid {BORDER_COLOR};
    }}
    
    /* Section Headers */
    .section-header {{
        font-size: 1.1rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid {ACCENT_ORANGE};
        position: relative;
        letter-spacing: -0.01em;
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: {ACCENT_BLUE};
    }}
    
    /* Image Container */
    .image-container {{
        background: linear-gradient(135deg, {BG_SECONDARY} 0%, {BG_TERTIARY} 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid {BORDER_COLOR};
        text-align: center;
        box-shadow: 0 6px 24px rgba(0,0,0,0.3);
    }}
    
    .image-container img {{
        border-radius: 10px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }}
    
    /* Buttons */
    .stButton button {{
        background: linear-gradient(135deg, {ACCENT_ORANGE} 0%, #ff6f00 100%);
        color: #000000;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        width: 100%;
        font-size: 0.75rem;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
    }}
    
    .stButton button:hover {{
        background: linear-gradient(135deg, #ff6f00 0%, {ACCENT_ORANGE} 100%);
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.5);
        transform: translateY(-2px);
    }}
    
    /* Progress Bar */
    .progress-bar {{
        width: 100%;
        height: 5px;
        background: {BG_TERTIARY};
        border-radius: 3px;
        overflow: hidden;
        margin: 0.4rem 0;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {ACCENT_ORANGE}, {ACCENT_BLUE});
        border-radius: 3px;
    }}
    
    /* Badge Counter */
    .badge-counter {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 24px;
        height: 24px;
        background: {CRITICAL};
        color: white;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0 6px;
        margin-left: 8px;
    }}
    
    .stVerticalBlock {{
        gap: 1rem;
    }}
    
    .stDataFrame {{
        background-color: {BG_SECONDARY} !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }}
    
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {BORDER_COLOR}, transparent);
        margin: 2rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data(ttl=300)
def load_fleet_data():
    try:
        df = pd.read_csv('output/mining_truck_fleet_cleaned.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return pd.DataFrame()

df = load_fleet_data()

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-title">⚙️ HT-20002</div>
        <div class="sidebar-subtitle">Real-Time Asset Monitoring</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Clock
    st.markdown(f"""
    <div style='text-align: center; padding: 0.8rem; background: {BG_TERTIARY}; border-radius: 8px; margin: 1rem 0; border: 1px solid {BORDER_COLOR};'>
        <div style='font-size: 1.5rem; font-weight: 900; color: {ACCENT_ORANGE}; font-family: monospace;'>
            {datetime.now().strftime('%H:%M:%S')}
        </div>
        <div style='font-size: 0.65rem; color: {TEXT_SECONDARY}; margin-top: 0.3rem;'>
            {datetime.now().strftime('%A, %b %d, %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">📊 STATUS</div>', unsafe_allow_html=True)
    
    overall_health = 87
    st.markdown(f"""
    <div class="sidebar-metric">
        <span class="sidebar-metric-label"><span class="status-indicator status-active"></span>Operational</span>
        <span class="sidebar-metric-value" style="color: {SUCCESS};">ACTIVE</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Health Score</span>
        <span class="sidebar-metric-value" style="color: {WARNING};">{overall_health}%</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {overall_health}%;"></div>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Critical</span>
        <span class="sidebar-metric-value" style="color: {CRITICAL};">2</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Warnings</span>
        <span class="sidebar-metric-value" style="color: {WARNING};">4</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Asset Info
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">🚛 ASSET INFO</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Model</span>
        <span class="sidebar-metric-value">Komatsu 810e</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Site</span>
        <span class="sidebar-metric-value">North Pit</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Year</span>
        <span class="sidebar-metric-value">2018</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Fleet</span>
        <span class="sidebar-metric-value">797</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">📈 PERFORMANCE</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Runtime</span>
        <span class="sidebar-metric-value">2,498 hrs</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Odometer</span>
        <span class="sidebar-metric-value">128K km</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Loads</span>
        <span class="sidebar-metric-value">15,234</span>
    </div>
    <div class="sidebar-metric">
        <span class="sidebar-metric-label">Efficiency</span>
        <span class="sidebar-metric-value" style="color: {SUCCESS};">94.2%</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: 94.2%; background: {SUCCESS};"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Component Health
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">⚡ COMPONENTS</div>', unsafe_allow_html=True)
    
    components = [
        ("Engine", 79, WARNING),
        ("Drive", 85, SUCCESS),
        ("Hydraulic", 91, SUCCESS),
        ("Brakes", 93, SUCCESS),
        ("Tyres", 76, WARNING),
    ]
    
    for name, value, color in components:
        indicator = "status-active" if value >= 85 else "status-warning"
        st.markdown(f"""
        <div class="sidebar-metric">
            <span class="sidebar-metric-label"><span class="status-indicator {indicator}"></span>{name}</span>
            <span class="sidebar-metric-value" style="color: {color};">{value}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {value}%; background: {color};"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Actions
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">⚡ ACTIONS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 REFRESH")
        st.button("🚨 ALERT")
    with col2:
        st.button("📥 EXPORT")
        st.button("🔧 WORK ORDER")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style='text-align: center; color: {TEXT_SECONDARY}; font-size: 0.7rem; margin-top: 1.5rem;'>
        <p style="margin: 3px 0;">🔒 Secure</p>
        <p style="margin: 3px 0; color: {ACCENT_ORANGE}; font-weight: 700;">XMPro v5.3</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown(f"""
<div class="main-header">
    <div class="main-title">
        🚛 Asset Analysis – Haul Truck HT-20002
        <span class="live-badge">
            <span class="status-indicator status-critical"></span>LIVE
        </span>
    </div>
    <div class="sub-title">Real-Time Asset Health Monitoring & Predictive Maintenance Platform</div>
</div>
""", unsafe_allow_html=True)

# Health Scores
st.markdown('<div class="section-header">SYSTEM HEALTH METRICS</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

systems = [
    ("Engine Health", 79, "NEEDS SERVICE", WARNING),
    ("Drive System", 85, "HEALTHY", SUCCESS),
    ("Hydraulic", 91, "HEALTHY", SUCCESS),
    ("Brake System", 93, "HEALTHY", SUCCESS)
]

for col, (title, score, status, color) in zip([col1, col2, col3, col4], systems):
    with col:
        status_class = "status-healthy" if score >= 85 else "status-warning-badge"
        
        st.markdown(f"""
        <div class="health-card">
            <div class="health-card-title">{title}</div>
            <div class="health-score" style="color: {color}">{score}%</div>
            <div class="health-status {status_class}">{status}</div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid {BORDER_COLOR};">
                <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; font-size: 0.8rem;">
                    <span style="color: {TEXT_SECONDARY};">Temp</span>
                    <span style="color: {TEXT_PRIMARY}; font-weight: 700;">{np.random.randint(75, 95)}%</span>
                </div>
                <div class="progress-bar" style="height: 4px;">
                    <div class="progress-fill" style="width: {np.random.randint(75, 95)}%; background: {color};"></div>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; font-size: 0.8rem;">
                    <span style="color: {TEXT_SECONDARY};">Press</span>
                    <span style="color: {TEXT_PRIMARY}; font-weight: 700;">{np.random.randint(70, 90)}%</span>
                </div>
                <div class="progress-bar" style="height: 4px;">
                    <div class="progress-fill" style="width: {np.random.randint(70, 90)}%; background: {color};"></div>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; font-size: 0.8rem;">
                    <span style="color: {TEXT_SECONDARY};">Vibr</span>
                    <span style="color: {TEXT_PRIMARY}; font-weight: 700;">{np.random.randint(80, 95)}%</span>
                </div>
                <div class="progress-bar" style="height: 4px;">
                    <div class="progress-fill" style="width: {np.random.randint(80, 95)}%; background: {color};"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Metadata Strip
col1, col2, col3, col4, col5, col6 = st.columns(6)

metadata = [
    ("STATUS", "RUNNING", "badge-running"),
    ("TYPE", "Haul Truck", ""),
    ("MODEL", "Komatsu 810e", ""),
    ("RUNTIME", "2,498 Hr", ""),
    ("DISTANCE", "128K KM", ""),
    ("CODE", "[Clear]", "badge-running")
]

for col, (label, value, badge_class) in zip([col1, col2, col3, col4, col5, col6], metadata):
    with col:
        badge_html = f'<div class="metric-badge {badge_class}">{value}</div>' if badge_class else value
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="font-size: 1rem;">{badge_html if badge_class else value}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ALERTS AND ACTIONS SECTION
# ============================================================================

st.markdown(f'<div class="section-header">🚨 CRITICAL ALERTS & RECOMMENDED ACTIONS<span class="badge-counter">6</span></div>', unsafe_allow_html=True)

alert_col, action_col = st.columns([1, 1])

with alert_col:
    st.markdown("### ⚠️ Active Alerts")
    
    alerts = [
        {
            "type": "critical",
            "icon": "🔴",
            "title": "Engine Health Critical",
            "description": "Engine oil temperature 92°C (threshold: 85°C). Immediate maintenance recommended.",
            "location": "North Pit, Grid B-12",
            "time": "2 minutes ago",
            "sensor": "Temp-ENG-01"
        },
        {
            "type": "critical",
            "icon": "⚠️",
            "title": "Predicted Failure Alert",
            "description": "AI model predicts engine failure within 48 hours. Health score degrading rapidly.",
            "location": "Predictive Analytics",
            "time": "15 minutes ago",
            "sensor": "ML-PREDICT-01"
        },
        {
            "type": "warning",
            "icon": "🟠",
            "title": "Hydraulic Return Fluid Overtemp",
            "description": "Hydraulic fluid temperature 78°C. Monitor closely to prevent system damage.",
            "location": "Hydraulic System",
            "time": "1 hour ago",
            "sensor": "Temp-HYD-03"
        },
        {
            "type": "warning",
            "icon": "🟡",
            "title": "Tyre Pressure Low",
            "description": "Back right outer tyre pressure 85 PSI (spec: 100 PSI). Risk of blowout.",
            "location": "Rear Axle R-2",
            "time": "2 hours ago",
            "sensor": "Press-TYRE-04"
        },
        {
            "type": "warning",
            "icon": "🟠",
            "title": "High Oil Temperature",
            "description": "Transmission oil 88°C (threshold: 82°C). Cooling system may need inspection.",
            "location": "Drive System",
            "time": "3 hours ago",
            "sensor": "Temp-TRANS-01"
        },
        {
            "type": "warning",
            "icon": "🟡",
            "title": "Load Capacity Exceeded",
            "description": "Current payload 268 tons (max: 250 tons). Inspect payload distribution immediately.",
            "location": "Load Sensors",
            "time": "4 hours ago",
            "sensor": "Load-CELL-02"
        },
    ]
    
    for alert in alerts:
        st.markdown(f"""
        <div class="alert-box alert-{alert['type']}">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                <strong>{alert['icon']} {alert['title']}</strong>
                <span style="font-size: 0.7rem; color: {TEXT_SECONDARY};">{alert['time']}</span>
            </div>
            <div style="color: {TEXT_SECONDARY}; font-size: 0.8rem; line-height: 1.5; margin-bottom: 0.5rem;">
                {alert['description']}
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: {TEXT_SECONDARY}; padding-top: 0.5rem; border-top: 1px solid {BORDER_COLOR};">
                <span>📍 {alert['location']}</span>
                <span>🔧 {alert['sensor']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with action_col:
    st.markdown("### ✅ Next Actions Required")
    
    actions = [
        {
            "priority": "high",
            "priority_label": "URGENT",
            "title": "Emergency Engine Shutdown & Inspection",
            "description": "Stop HT-20002 immediately. Conduct full engine diagnostic. Check oil system, cooling system, and thermal sensors.",
            "assignee": "Maintenance Team A",
            "estimated_time": "4-6 hours",
            "due": "Immediately",
            "work_order": "WO-2024-0456"
        },
        {
            "priority": "high",
            "priority_label": "URGENT",
            "title": "Predictive Maintenance - Engine Overhaul",
            "description": "Schedule complete engine inspection based on AI prediction. Replace worn components, flush oil system, inspect bearings.",
            "assignee": "Senior Mechanic - J. Smith",
            "estimated_time": "8-12 hours",
            "due": "Within 24 hours",
            "work_order": "WO-2024-0457"
        },
        {
            "priority": "medium",
            "priority_label": "HIGH",
            "title": "Hydraulic System Cooling Check",
            "description": "Inspect hydraulic cooling system. Check coolant levels, radiator condition, and fan operation. Clean filters if needed.",
            "assignee": "Maintenance Team B",
            "estimated_time": "2-3 hours",
            "due": "Within 12 hours",
            "work_order": "WO-2024-0458"
        },
        {
            "priority": "medium",
            "priority_label": "MEDIUM",
            "title": "Tyre Pressure Adjustment & Inspection",
            "description": "Inflate back right outer tyre to 100 PSI. Inspect for leaks, valve damage, or punctures. Replace if necessary.",
            "assignee": "Tyre Specialist",
            "estimated_time": "1 hour",
            "due": "Within 24 hours",
            "work_order": "WO-2024-0459"
        },
        {
            "priority": "medium",
            "priority_label": "MEDIUM",
            "title": "Transmission Oil System Service",
            "description": "Check transmission oil cooler. Inspect cooling fans and clean debris. Monitor temperature during operation.",
            "assignee": "Maintenance Team C",
            "estimated_time": "2 hours",
            "due": "Within 48 hours",
            "work_order": "WO-2024-0460"
        },
        {
            "priority": "low",
            "priority_label": "LOW",
            "title": "Load Distribution Review",
            "description": "Review loading procedures with operators. Recalibrate load sensors. Ensure compliance with weight limits.",
            "assignee": "Operations Supervisor",
            "estimated_time": "1 hour",
            "due": "Within 72 hours",
            "work_order": "WO-2024-0461"
        },
    ]
    
    for action in actions:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-priority priority-{action['priority']}">{action['priority_label']}</div>
            <div class="action-title">{action['title']}</div>
            <div class="action-description">{action['description']}</div>
            <div class="action-meta">
                <div>
                    <div style="margin-bottom: 0.3rem;">👤 {action['assignee']}</div>
                    <div>⏱️ Est. Time: {action['estimated_time']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="margin-bottom: 0.3rem;">📅 Due: {action['due']}</div>
                    <div style="color: {ACCENT_ORANGE}; font-weight: 700;">{action['work_order']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ASSET VISUAL AND KPIs
# ============================================================================

st.markdown('<div class="section-header">🚛 ASSET VISUAL & OPERATIONAL KPIs</div>', unsafe_allow_html=True)

visual_col1, visual_col2 = st.columns([3, 2])

with visual_col1:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    try:
        truck_image = Image.open('images/truck.jpeg')
        st.image(truck_image, use_container_width=True)
    except:
        st.info("📷 Place truck.jpeg in directory")
    st.caption("HT-20002 - Komatsu 810e | Real-Time Sensor Monitoring System")
    st.markdown('</div>', unsafe_allow_html=True)

with visual_col2:
    kpi1, kpi2 = st.columns(2)
    
    with kpi1:
        fig_power = go.Figure(go.Indicator(
            mode="gauge+number",
            value=1.9,
            number={"suffix": " MW", "font": {"size": 20, "color": TEXT_PRIMARY}},
            title={"text": "Power Output", "font": {"size": 11, "color": TEXT_SECONDARY}},
            gauge={
                "axis": {"range": [0, 3]},
                "bar": {"color": ACCENT_ORANGE, "thickness": 0.7},
                "bgcolor": BG_TERTIARY,
                "steps": [{"range": [0, 3], "color": BG_SECONDARY}],
            }
        ))
        fig_power.update_layout(
            height=180,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor=BG_SECONDARY,
            font={"color": TEXT_PRIMARY}
        )
        st.plotly_chart(fig_power, use_container_width=True)
    
    with kpi2:
        fig_payload = go.Figure(go.Indicator(
            mode="gauge+number",
            value=250,
            number={"suffix": " T", "font": {"size": 20, "color": TEXT_PRIMARY}},
            title={"text": "Payload", "font": {"size": 11, "color": TEXT_SECONDARY}},
            gauge={
                "axis": {"range": [0, 400]},
                "bar": {"color": SUCCESS, "thickness": 0.7},
                "bgcolor": BG_TERTIARY,
                "steps": [{"range": [0, 400], "color": BG_SECONDARY}],
            }
        ))
        fig_payload.update_layout(
            height=180,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor=BG_SECONDARY,
            font={"color": TEXT_PRIMARY}
        )
        st.plotly_chart(fig_payload, use_container_width=True)
    
    kpi3, kpi4 = st.columns(2)
    
    with kpi3:
        fig_fuel = go.Figure(go.Indicator(
            mode="gauge+number",
            value=92,
            number={"suffix": " L/h", "font": {"size": 20, "color": TEXT_PRIMARY}},
            title={"text": "Fuel", "font": {"size": 11, "color": TEXT_SECONDARY}},
            gauge={
                "axis": {"range": [0, 150]},
                "bar": {"color": WARNING, "thickness": 0.7},
                "bgcolor": BG_TERTIARY,
                "steps": [{"range": [0, 150], "color": BG_SECONDARY}],
            }
        ))
        fig_fuel.update_layout(
            height=180,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor=BG_SECONDARY,
            font={"color": TEXT_PRIMARY}
        )
        st.plotly_chart(fig_fuel, use_container_width=True)
    
    with kpi4:
        fig_uptime = go.Figure(go.Indicator(
            mode="gauge+number",
            value=94.2,
            number={"suffix": "%", "font": {"size": 20, "color": TEXT_PRIMARY}},
            title={"text": "Uptime", "font": {"size": 11, "color": TEXT_SECONDARY}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": SUCCESS, "thickness": 0.7},
                "bgcolor": BG_TERTIARY,
                "steps": [{"range": [0, 100], "color": BG_SECONDARY}],
            }
        ))
        fig_uptime.update_layout(
            height=180,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor=BG_SECONDARY,
            font={"color": TEXT_PRIMARY}
        )
        st.plotly_chart(fig_uptime, use_container_width=True)

# Analytics Charts
st.markdown('<div class="section-header">📊 PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    time_data = pd.DataFrame({
        "State": ["Running", "Idle", "Down"],
        "Hours": [16.85, 1.3, 5.85]
    })
    
    fig_time = go.Figure(go.Bar(
        y=time_data["State"],
        x=time_data["Hours"],
        orientation='h',
        text=time_data["Hours"].apply(lambda x: f"{x:.1f}h"),
        textposition='outside',
        marker=dict(color=[SUCCESS, WARNING, CRITICAL]),
    ))
    
    fig_time.update_layout(
        title="Time Profile (24h)",
        height=250,
        paper_bgcolor=BG_SECONDARY,
        plot_bgcolor=BG_SECONDARY,
        font={"color": TEXT_PRIMARY, "size": 11},
        showlegend=False,
        margin=dict(t=40, b=20, l=20, r=60),
        xaxis=dict(gridcolor=BORDER_COLOR, showgrid=True),
    )
    
    st.plotly_chart(fig_time, use_container_width=True)

with chart_col2:
    cycles = np.arange(0, 400, 20)
    actual = np.linspace(400, 120, len(cycles))
    predicted = actual + np.random.normal(0, 12, len(cycles))
    
    fig_rul = go.Figure()
    fig_rul.add_trace(go.Scatter(
        x=cycles, y=actual, mode="lines+markers",
        name="Actual", line=dict(color=ACCENT_BLUE, width=2)
    ))
    fig_rul.add_trace(go.Scatter(
        x=cycles, y=predicted, mode="lines+markers",
        name="Predicted", line=dict(color=CRITICAL, width=2, dash='dash')
    ))
    
    fig_rul.update_layout(
        title="Remaining Useful Life Prediction",
        height=250,
        paper_bgcolor=BG_SECONDARY,
        plot_bgcolor=BG_SECONDARY,
        font={"color": TEXT_PRIMARY, "size": 11},
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis=dict(gridcolor=BORDER_COLOR, title="Cycle"),
        yaxis=dict(gridcolor=BORDER_COLOR, title="RUL (hrs)"),
        legend=dict(orientation="h", y=1.1)
    )
    
    st.plotly_chart(fig_rul, use_container_width=True)

# Work History
st.markdown('<div class="section-header">📋 MAINTENANCE WORK HISTORY</div>', unsafe_allow_html=True)

work_df = pd.DataFrame({
    "Work Request": ["3453788", "3446268", "3451228", "3450012", "3449876"],
    "Work Order": ["114679", "114900", "114921", "114855", "114821"],
    "Description": [
        "Standard motor inspection - No issues found. Lubrication optimized.",
        "Belt alignment adjusted. Tension verified within normal range.",
        "Vibration analysis performed. Motor and rollers rebalanced.",
        "Hydraulic system pressure test. All values within specification.",
        "Brake pad inspection and replacement. System functioning normally."
    ],
    "Status": ["✓ COMPLETE", "✓ COMPLETE", "✓ COMPLETE", "✓ COMPLETE", "✓ COMPLETE"],
    "Date": ["Nov 9, 2023", "Nov 8, 2023", "Nov 7, 2023", "Nov 5, 2023", "Nov 3, 2023"],
    "Technician": ["J. Smith", "M. Garcia", "R. Johnson", "T. Williams", "S. Anderson"]
})

st.dataframe(work_df, use_container_width=True, hide_index=True, height=220)

# Footer
st.markdown(f"""
<div style='text-align: center; color: {TEXT_SECONDARY}; padding: 1.5rem; background: {BG_SECONDARY}; border-radius: 12px; margin-top: 2rem; border: 1px solid {BORDER_COLOR};'>
    <p style='font-size: 1rem; font-weight: 800; color: {TEXT_PRIMARY}; margin-bottom: 0.5rem;'>
        🚛 Enterprise Asset Intelligence Platform
    </p>
    <p style='font-size: 0.8rem; color: {TEXT_SECONDARY}; margin-bottom: 0.5rem;'>
        Predictive Maintenance • Digital Twin Technology • Real-Time Analytics • AI-Powered Insights
    </p>
    <p style='font-size: 0.75rem; color: {ACCENT_ORANGE}; font-weight: 700;'>
        XMPro Platform v5.3.0 Enterprise Edition
    </p>
    <p style='font-size: 0.7rem; color: {TEXT_SECONDARY}; margin-top: 0.8rem;'>
        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Status: <span style="color: {SUCCESS};">● ONLINE</span> | Latency: 12ms | Uptime: 99.8%
    </p>
</div>
""", unsafe_allow_html=True)


