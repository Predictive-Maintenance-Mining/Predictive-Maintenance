import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from typing import Dict, List, Tuple
import plotly.figure_factory as ff
import datetime
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image
import time

st.markdown("""
<style>
/* Hide default Streamlit multipage navigation */
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Mining Industry Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Enterprise Mining Operations Dashboard v2.0"
    }
)

# =====================================================
# LOADING CLOCK ANIMATION CSS
# =====================================================
LOADING_CSS = """
<style>
/* ── Loading Overlay ────────────────────────────── */
.loading-overlay {
    position: fixed;
    inset: 0;
    background: rgba(10, 15, 30, 0.88);
    backdrop-filter: blur(6px);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: overlayFadeIn 0.25s ease;
}

@keyframes overlayFadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* ── Clock Face ─────────────────────────────────── */
.clock-loader {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #1e3a5f, #0d1b2e);
    border: 3px solid #2563eb;
    box-shadow:
        0 0 0 6px rgba(37, 99, 235, 0.15),
        0 0 30px rgba(37, 99, 235, 0.4),
        inset 0 0 20px rgba(0,0,0,0.6);
    position: relative;
    margin-bottom: 24px;
}

/* tick marks */
.clock-loader::before {
    content: '';
    position: absolute;
    inset: 6px;
    border-radius: 50%;
    background: repeating-conic-gradient(
        rgba(255,255,255,0.15) 0deg 2deg,
        transparent 2deg 30deg
    );
}

/* center dot */
.clock-loader::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 8px; height: 8px;
    background: #60a5fa;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 8px #60a5fa;
    z-index: 4;
}

/* Hour hand */
.clock-hour {
    position: absolute;
    bottom: 50%; left: 50%;
    width: 3px;
    height: 26px;
    background: linear-gradient(to top, #93c5fd, #dbeafe);
    transform-origin: bottom center;
    transform: translateX(-50%);
    border-radius: 3px 3px 0 0;
    animation: rotateHour 8s linear infinite;
    z-index: 3;
    box-shadow: 0 0 6px rgba(147,197,253,0.6);
}

/* Minute hand */
.clock-minute {
    position: absolute;
    bottom: 50%; left: 50%;
    width: 2px;
    height: 34px;
    background: linear-gradient(to top, #2563eb, #60a5fa);
    transform-origin: bottom center;
    transform: translateX(-50%);
    border-radius: 2px 2px 0 0;
    animation: rotateMinute 2s linear infinite;
    z-index: 3;
    box-shadow: 0 0 8px rgba(37,99,235,0.8);
}

/* Second hand */
.clock-second {
    position: absolute;
    bottom: 50%; left: 50%;
    width: 1.5px;
    height: 38px;
    background: linear-gradient(to top, #f59e0b, #fcd34d);
    transform-origin: bottom center;
    transform: translateX(-50%);
    border-radius: 1px;
    animation: rotateSecond 0.6s linear infinite;
    z-index: 3;
    box-shadow: 0 0 6px rgba(245,158,11,0.9);
}

/* Tail of second hand */
.clock-second-tail {
    position: absolute;
    top: 50%; left: 50%;
    width: 1.5px;
    height: 12px;
    background: rgba(245,158,11,0.6);
    transform-origin: top center;
    transform: translateX(-50%);
    border-radius: 1px;
    animation: rotateSecond 0.6s linear infinite;
    z-index: 3;
}

@keyframes rotateHour   { from { transform: translateX(-50%) rotate(0deg);   } to { transform: translateX(-50%) rotate(360deg);   } }
@keyframes rotateMinute { from { transform: translateX(-50%) rotate(0deg);   } to { transform: translateX(-50%) rotate(360deg);   } }
@keyframes rotateSecond { from { transform: translateX(-50%) rotate(0deg);   } to { transform: translateX(-50%) rotate(360deg);   } }

/* ── Loading Text ───────────────────────────────── */
.loading-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.loading-subtitle {
    font-family: 'Segoe UI', sans-serif;
    font-size: 0.8rem;
    color: #64748b;
    letter-spacing: 0.04em;
    margin-bottom: 20px;
}

/* ── Dot pulse ──────────────────────────────────── */
.dot-pulse {
    display: flex;
    gap: 6px;
}

.dot-pulse span {
    width: 7px; height: 7px;
    background: #2563eb;
    border-radius: 50%;
    animation: dotBounce 1.1s ease-in-out infinite;
    box-shadow: 0 0 6px #2563eb;
}

.dot-pulse span:nth-child(1) { animation-delay: 0s; }
.dot-pulse span:nth-child(2) { animation-delay: 0.18s; }
.dot-pulse span:nth-child(3) { animation-delay: 0.36s; }

@keyframes dotBounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40%           { transform: scale(1.1); opacity: 1;   }
}

/* ── Progress bar ───────────────────────────────── */
.loading-bar-track {
    width: 200px;
    height: 3px;
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 16px;
}

.loading-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #1d4ed8, #2563eb, #60a5fa, #2563eb, #1d4ed8);
    background-size: 400% 100%;
    border-radius: 2px;
    animation: shimmerBar 1.5s ease-in-out infinite;
}

@keyframes shimmerBar {
    0%   { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}

/* ── Inline spinner (for buttons/small actions) ─── */
.spin-ring {
    display: inline-block;
    width: 18px; height: 18px;
    border: 2px solid rgba(37,99,235,0.2);
    border-top-color: #2563eb;
    border-radius: 50%;
    animation: spinRing 0.7s linear infinite;
    vertical-align: middle;
    margin-right: 6px;
}

@keyframes spinRing {
    to { transform: rotate(360deg); }
}

/* ── Skeleton shimmer ───────────────────────────── */
.skeleton {
    background: linear-gradient(90deg,
        rgba(255,255,255,0.04) 25%,
        rgba(255,255,255,0.10) 50%,
        rgba(255,255,255,0.04) 75%
    );
    background-size: 400% 100%;
    animation: skeletonShimmer 1.4s ease infinite;
    border-radius: 6px;
}

@keyframes skeletonShimmer {
    0%   { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}

.skeleton-card {
    height: 120px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.skeleton-chart {
    height: 300px;
    border-radius: 12px;
}
</style>
"""


# =====================================================
# REUSABLE CLOCK LOADER HELPER
# =====================================================

CLOCK_HTML = """
{css}
<div class="loading-overlay">
    <div class="clock-loader">
        <div class="clock-hour"></div>
        <div class="clock-minute"></div>
        <div class="clock-second"></div>
        <div class="clock-second-tail"></div>
    </div>
    <div class="loading-title">{title}</div>
    <div class="loading-subtitle">{subtitle}</div>
    <div class="dot-pulse"><span></span><span></span><span></span></div>
    <div class="loading-bar-track"><div class="loading-bar-fill"></div></div>
</div>
"""


def show_clock(title: str = "Please Wait…", subtitle: str = "Processing your request…"):
    """Show full-screen clock overlay. Returns the placeholder so caller can clear it."""
    ph = st.empty()
    ph.markdown(
        CLOCK_HTML.format(css=LOADING_CSS, title=title, subtitle=subtitle),
        unsafe_allow_html=True,
    )
    return ph


def with_clock(title: str, subtitle: str, delay: float = 0.8):
    """
    Context manager: shows clock on enter, hides on exit.

    Usage:
        with with_clock("Loading…", "Fetching data…"):
            do_heavy_work()
    """
    class _ClockCtx:
        def __enter__(self):
            self._ph = show_clock(title, subtitle)
            return self
        def __exit__(self, *_):
            self._ph.empty()
    return _ClockCtx()


def show_loading_clock(
    message: str = "Please wait…",
    subtitle: str = "We are analysing plant data and preparing your dashboard. This may take a few seconds."
):
    """Legacy helper kept for backward compatibility."""
    return show_clock(message, subtitle)


def show_skeleton_cards(n: int = 3):
    cols = st.columns(n)
    for col in cols:
        with col:
            st.markdown(f"{LOADING_CSS}<div class='skeleton skeleton-card'></div>", unsafe_allow_html=True)


def show_skeleton_chart():
    st.markdown(f"{LOADING_CSS}<div class='skeleton skeleton-chart'></div>", unsafe_allow_html=True)


# Inject CSS globally once
st.markdown(LOADING_CSS, unsafe_allow_html=True)

# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================
if "issues" not in st.session_state:
    st.session_state.issues = []
if "theme" not in st.session_state:
    st.session_state.theme = False
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "loading" not in st.session_state:
    st.session_state.loading = False

# Track previous selections so we can fire the loader on change
if "_prev_plant" not in st.session_state:
    st.session_state._prev_plant = None
if "_prev_tab" not in st.session_state:
    st.session_state._prev_tab = None
if "_prev_view" not in st.session_state:
    st.session_state._prev_view = None
if "_prev_subplant" not in st.session_state:
    st.session_state._prev_subplant = None
if "_prev_asset" not in st.session_state:
    st.session_state._prev_asset = None
if "_prev_subplant_drilldown" not in st.session_state:
    st.session_state._prev_subplant_drilldown = None
if "_prev_component" not in st.session_state:
    st.session_state._prev_component = None

# =====================================================
# DATA LOADING — cached with TTL for latency
# =====================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        df = pd.read_csv('output/mining_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['due_date']  = pd.to_datetime(df['due_date'])
        df['_status_label'] = df['health_score'].apply(
            lambda s: 'Healthy' if s >= 85 else ('Warning' if s >= 70 else 'Critical')
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


@st.cache_data(ttl=300, show_spinner=False)
def get_plant_data(plant_id: str):
    return df_raw[df_raw['plant_id'] == plant_id].copy() if df_raw is not None else pd.DataFrame()


@st.cache_data(ttl=300, show_spinner=False)
def get_sub_plant_data(plant_id: str, sub_plant: str):
    return df_raw[
        (df_raw['plant_id'] == plant_id) &
        (df_raw['sub_plant'] == sub_plant)
    ].copy() if df_raw is not None else pd.DataFrame()


# ── Initial data load with clock overlay ─────────────
_loading_placeholder = show_clock("Initialising Dashboard", "Connecting to mining data streams…")
df_raw = load_data()
_loading_placeholder.empty()

# =====================================================
# CONSTANTS & DATA STRUCTURES
# =====================================================
PLANTS = [f"Plant-{i}" for i in range(1, 6)]

PLANT_STRUCTURE = {
    "Crushing Plant": {
        "Jaw Crusher": ["Bearing", "Motor"],
        "Cone Crusher": ["Bearing", "Gearbox"]
    },
    "Grinding Plant": {
        "Ball Mill": ["Bearing", "Gearbox", "Motor"],
        "SAG Mill": ["Bearing", "Motor"]
    },
    "Separation / Beneficiation Plant": {
        "Flotation Pump": ["Pump", "Motor"],
        "Magnetic Separator": ["Coil", "Bearing"]
    },
    "Dewatering Plant": {
        "Thickener": ["Hydraulic", "Motor"],
        "Filter Press": ["Hydraulic", "Pump"]
    },
    "Conveyor & Material Handling": {
        "Conveyor Belt": ["Belt", "Roller"],
        "Drive Pulley": ["Bearing", "Motor"]
    },
    "Utilities (Power, Water, Compressors)": {
        "Air Compressor": ["Motor", "Valve"],
        "Power Transformer": ["Coil", "Cooling"]
    }
}

SENSOR_MAP = {
    "Bearing": ["Vibration", "Temperature"],
    "Motor": ["Temperature", "Power"],
    "Gearbox": ["Vibration", "Temperature"],
    "Pump": ["Pressure", "Vibration"],
    "Hydraulic": ["Pressure", "Temperature"],
    "Belt": ["Speed", "Wear"],
    "Roller": ["Vibration"],
    "Valve": ["Pressure"],
    "Coil": ["Temperature"],
    "Cooling": ["Temperature"]
}

# =====================================================
# ENHANCED THEME SYSTEM
# =====================================================
DARK_THEME = {
    "bg_primary": "#0f172a",
    "bg_secondary": "#020617",
    "text_primary": "#e5e7eb",
    "text_secondary": "#94a3b8",
    "border": "#1e293b",
    "accent": "#2563eb",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "card_bg": "#1e293b"
}

LIGHT_THEME = {
    "bg_primary": "#ffffff",
    "bg_secondary": "#f8fafc",
    "text_primary": "#0f172a",
    "text_secondary": "#64748b",
    "border": "#e5e7eb",
    "accent": "#2563eb",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "card_bg": "#f1f5f9"
}

def apply_theme(is_dark: bool) -> None:
    theme = DARK_THEME if is_dark else LIGHT_THEME
    st.markdown(f"""
    <style>
    .block-container {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {theme['text_primary']};
    }}
    [data-testid="stSidebar"] {{
        background-color: {theme['bg_secondary']};
        border-right: 1px solid {theme['border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {theme['text_primary']};
    }}
    .stButton > button {{
        background-color: {theme['accent']} !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .streamlit-expanderHeader {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        font-weight: 500;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 700;
        color: {theme['accent']};
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.875rem;
        font-weight: 500;
        color: {theme['text_secondary']};
    }}
    .dataframe {{
        border: 1px solid {theme['border']} !important;
        border-radius: 8px;
    }}
    hr {{
        margin: 2rem 0;
        border-color: {theme['border']};
    }}
    .element-container {{
        transition: all 0.2s ease;
    }}
    .stSelectbox > div > div {{
        border-radius: 8px;
    }}
    .stDateInput > div > div {{
        border-radius: 8px;
    }}
    .caption {{
        color: {theme['text_secondary']};
        font-size: 0.875rem;
    }}
    .stCodeBlock {{
        border-radius: 8px;
        border: 1px solid {theme['border']};
    }}
    .stSuccess {{
        background-color: rgba(34, 197, 94, 0.1);
        border-left: 4px solid {theme['success']};
    }}
    .stWarning {{
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid {theme['warning']};
    }}
    .stError {{
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid {theme['danger']};
    }}
    .hierarchy-card {{
        background: {theme['card_bg']};
        border: 2px solid {theme['border']};
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .hierarchy-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .hierarchy-icon {{ font-size: 2.5rem; margin-bottom: 10px; }}
    .hierarchy-title {{
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: {theme['text_primary']};
    }}
    .hierarchy-description {{
        font-size: 0.9rem;
        color: {theme['text_secondary']};
        line-height: 1.5;
    }}
    .status-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }}
    .status-healthy  {{ background: rgba(34,197,94,0.2); color:#22c55e; border:1px solid #22c55e; }}
    .status-warning  {{ background: rgba(245,158,11,0.2); color:#f59e0b; border:1px solid #f59e0b; }}
    .status-critical {{ background: rgba(239,68,68,0.2);  color:#ef4444; border:1px solid #ef4444; }}
    .flow-arrow {{ text-align: center; font-size: 2rem; color: {theme['accent']}; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# UTILITY FUNCTIONS (CSV-based)
# =====================================================
@st.cache_data(ttl=300, show_spinner=False)
def get_health_score(plant_id: str, sub_plant: str, equipment: str, component: str) -> int:
    if df_raw is None:
        return 85
    filtered = df_raw[
        (df_raw['plant_id'] == plant_id) &
        (df_raw['sub_plant'] == sub_plant) &
        (df_raw['equipment'] == equipment) &
        (df_raw['component'] == component)
    ]
    return int(filtered['health_score'].iloc[0]) if not filtered.empty else 85


def status(score: int) -> str:
    if score >= 85: return "🟢 Healthy"
    elif score >= 70: return "🟠 Warning"
    return "🔴 Critical"

def maintenance(score: int) -> str:
    if score >= 85: return "Proactive"
    elif score >= 70: return "Preventive"
    return "Predictive"

def action(score: int) -> str:
    if score >= 85: return "Continue monitoring"
    elif score >= 70: return "Plan inspection"
    return "Immediate inspection & shutdown planning"

def ml_risk_prediction(score: int) -> str:
    if score < 65: return "🔴 High Failure Risk"
    elif score < 80: return "🟠 Medium Failure Risk"
    return "🟢 Low Failure Risk"

def countdown_text(due_text: str) -> str:
    if "24" in due_text: return "⏱ Less than 24 hours remaining"
    elif "7" in due_text: return "⏱ 3–7 days remaining"
    return "⏱ Monitor"

# =====================================================
# ENHANCED VISUALIZATION FUNCTIONS
# =====================================================
@st.cache_data(ttl=300, show_spinner=False)
def create_donut_chart(value: int, title: str, success: str, danger: str) -> go.Figure:
    fig = go.Figure(data=[go.Pie(
        values=[value, 100 - value],
        hole=0.7,
        marker=dict(colors=[success, danger], line=dict(color='rgba(0,0,0,0)', width=0)),
        textinfo='none',
        hoverinfo='skip'
    )])
    fig.update_layout(
        title=dict(text=title, font=dict(size=14), x=0.5, xanchor='center'),
        showlegend=False,
        annotations=[dict(text=f"{value}%", x=0.5, y=0.5, font=dict(size=28), showarrow=False)],
        height=220,
        margin=dict(t=40, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

@st.cache_data(ttl=300, show_spinner=False)
def _build_bar_chart(x_data: tuple, y_data: tuple, x_label: str, y_label: str, title: str) -> go.Figure:
    df = pd.DataFrame({x_label: list(x_data), y_label: list(y_data)})
    fig = px.bar(df, x=x_label, y=y_label, color=y_label,
                 color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e'], title=title)
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)')
    )
    return fig

def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    return _build_bar_chart(tuple(df[x]), tuple(df[y]), x, y, title)

@st.cache_data(ttl=300, show_spinner=False)
def _build_pie_chart(names: tuple, title: str) -> go.Figure:
    df = pd.DataFrame({'name': list(names)})
    fig = px.pie(df, names='name', title=title,
                 color_discrete_sequence=['#22c55e', '#f59e0b', '#ef4444'])
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_pie_chart(df: pd.DataFrame, names: str, title: str) -> go.Figure:
    return _build_pie_chart(tuple(df[names]), title)

# =====================================================
# HIERARCHY VISUALIZATION FUNCTIONS
# =====================================================
@st.cache_data(ttl=600, show_spinner=False)
def create_hierarchy_flowchart(is_dark: bool) -> go.Figure:
    node_labels = [
        "🏭 Mine Site","🏗️ Sub-Plant","⚙️ Equipment","🔧 Component",
        "📡 Sensor","📊 Health Score","🟢 Proactive","🟠 Preventive","🔴 Predictive"
    ]
    node_colors = ["#2563eb","#3b82f6","#60a5fa","#93c5fd","#dbeafe","#fbbf24","#22c55e","#f59e0b","#ef4444"]
    links = [(0,1,20),(1,2,20),(2,3,20),(3,4,20),(4,5,20),(5,6,7),(5,7,7),(5,8,6)]
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20, thickness=30,
            line=dict(color="white", width=2),
            label=node_labels, color=node_colors,
            customdata=[
                "Starting point","Crushing, Grinding, Separation…","Crushers, Mills, Pumps…",
                "Bearings, Motors, Gearbox…","Vibration, Temperature, Pressure",
                "Real-time condition","Equipment healthy - Monitor",
                "Early warning - Plan inspection","High risk - Immediate action"
            ],
            hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>'
        ),
        link=dict(source=[l[0] for l in links], target=[l[1] for l in links],
                  value=[l[2] for l in links], color='rgba(37,99,235,0.3)')
    )])
    bg = "#0f172a" if is_dark else "#ffffff"
    tc = "#e5e7eb" if is_dark else "#0f172a"
    fig.update_layout(
        title={'text':"Mining Operations Monitoring Hierarchy",'x':0.5,'xanchor':'center',
               'font':{'size':24,'color':tc,'family':'Arial'}},
        font=dict(size=12, color=tc, family='Arial'),
        plot_bgcolor=bg, paper_bgcolor=bg,
        height=600, margin=dict(t=80,b=20,l=20,r=20)
    )
    return fig


def render_subplant_asset_insights(selected_plant, selected_subplant, selected_asset, theme_colors):
    st.subheader(f"🚛 Asset Intelligence – {selected_asset}")

    with with_clock("Loading Asset Data", f"Fetching intelligence for {selected_asset}…"):
        df_filtered = df_raw[
            (df_raw["plant_id"] == selected_plant) &
            (df_raw["sub_plant"] == selected_subplant) &
            (df_raw["equipment"] == selected_asset)
        ].copy()

    if df_filtered.empty:
        st.warning("No data available for this asset")
        return

    asset_health = int(df_filtered["health_score"].mean())
    k1, k2, k3 = st.columns(3)
    k1.metric("Asset Health", f"{asset_health}%")
    k2.metric("Status", status(asset_health))
    k3.metric("Maintenance Mode", maintenance(asset_health))

    st.plotly_chart(
        create_donut_chart(asset_health, "Asset Health", theme_colors['success'], theme_colors['danger']),
        use_container_width=True, config={'displayModeBar': False}
    )

    st.markdown("### 🔩 Component Health Overview")
    comp_df = (
        df_filtered.groupby("component")["health_score"].mean()
        .reset_index().rename(columns={"health_score": "Health (%)"})
    )
    comp_df["Health (%)"] = comp_df["Health (%)"].astype(int)
    comp_df["Status"] = comp_df["Health (%)"].apply(status)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    st.plotly_chart(
        create_bar_chart(comp_df, "component", "Health (%)", "Component Health Distribution"),
        use_container_width=True, config={'displayModeBar': False}
    )

    avg_comp_health = comp_df["Health (%)"].mean()
    st.markdown("### 🧠 Component Intelligence Insight")
    if avg_comp_health >= 85:
        st.success("All components operating in stable condition.")
    elif 70 <= avg_comp_health < 85:
        st.warning("Moderate wear detected. Preventive maintenance recommended.")
    else:
        st.error("Critical component degradation detected. Immediate action required.")

    st.markdown("### 📡 Sensor-Level Intelligence")
    selected_component = st.selectbox("Select Component", comp_df["component"], key="asset_component_select")

    # Show clock when component changes
    if st.session_state.get("_prev_asset_comp") != selected_component:
        _prev = st.session_state.get("_prev_asset_comp")
        st.session_state["_prev_asset_comp"] = selected_component
        if _prev is not None:
            ph = show_clock("Loading Sensor Data", f"Fetching readings for {selected_component}…")
            time.sleep(0.7)
            ph.empty()

    sensor_df = df_filtered[df_filtered["component"] == selected_component]
    if sensor_df.empty:
        st.info("No sensor data available")
        return

    sensor_display = sensor_df[["sensor_type","health_score"]].copy()
    sensor_display.columns = ["Sensor","Health (%)"]
    sensor_display["Health (%)"] = sensor_display["Health (%)"].astype(int)
    sensor_display["Status"] = sensor_display["Health (%)"].apply(status)
    st.dataframe(sensor_display, use_container_width=True, hide_index=True)

    worst_sensor = sensor_display.sort_values("Health (%)").iloc[0]
    avg_sensor_health = sensor_display["Health (%)"].mean()
    st.markdown("### 🚨 Sensor Risk Insight")
    if avg_sensor_health >= 85:
        st.success(f"All sensors stable. Lowest: {worst_sensor['Sensor']} ({worst_sensor['Health (%)']}%)")
    elif 70 <= avg_sensor_health < 85:
        st.warning(f"Sensor degradation. Monitor {worst_sensor['Sensor']} ({worst_sensor['Health (%)']}%)")
    else:
        st.error(f"Critical! {worst_sensor['Sensor']} at {worst_sensor['Health (%)']}%. Immediate maintenance.")

    st.markdown("### 📈 Remaining Useful Life Prediction")
    cycles = np.arange(0, 400, 20)
    actual = np.linspace(400, 120, len(cycles))
    predicted = actual + np.random.normal(0, 12, len(cycles))
    fig_rul = go.Figure()
    fig_rul.add_trace(go.Scatter(x=cycles, y=actual, mode="lines", name="Actual"))
    fig_rul.add_trace(go.Scatter(x=cycles, y=predicted, mode="lines", name="Predicted", line=dict(dash="dash")))
    fig_rul.update_layout(title="Remaining Useful Life (RUL)", xaxis_title="Cycle", yaxis_title="Remaining Hours", height=350)
    st.plotly_chart(fig_rul, use_container_width=True)


def render_hierarchy_cards():
    hierarchy_data = [
        {"icon":"🏭","title":"LEVEL 1: Mine Site","description":"Main mining facility containing all operational units","examples":["Plant-1","Plant-2","Plant-3"],"color":"#2563eb"},
        {"icon":"🏗️","title":"LEVEL 2: Sub-Plant","description":"Specialized processing units within the mine site","examples":["Crushing Plant","Grinding Plant","Separation Plant"],"color":"#3b82f6"},
        {"icon":"⚙️","title":"LEVEL 3: Equipment","description":"Heavy machinery and systems that perform operations","examples":["Jaw Crusher","Ball Mill","Flotation Pump"],"color":"#60a5fa"},
        {"icon":"🔧","title":"LEVEL 4: Component","description":"Critical parts of equipment that require monitoring","examples":["Bearing","Motor","Gearbox","Pump"],"color":"#93c5fd"},
        {"icon":"📡","title":"LEVEL 5: Sensor","description":"IoT devices measuring real-time conditions","examples":["Vibration","Temperature","Pressure","Power"],"color":"#38bdf8"},
        {"icon":"📊","title":"LEVEL 6: Health Score","description":"AI-calculated condition score (0-100%)","examples":["85-100% Healthy","70-84% Warning","0-69% Critical"],"color":"#fbbf24"},
        {"icon":"🎯","title":"LEVEL 7: Maintenance Decision","description":"Automated recommendation based on health score","examples":[],"color":"#8b5cf6"}
    ]
    for i, level in enumerate(hierarchy_data):
        st.markdown(f"""
        <div class="hierarchy-card">
            <div class="hierarchy-icon">{level['icon']}</div>
            <div class="hierarchy-title">{level['title']}</div>
            <div class="hierarchy-description">{level['description']}</div>
            <div style="margin-top:12px;">
                {''.join([f'<span style="background:rgba(37,99,235,0.1);padding:4px 10px;border-radius:6px;margin:3px;display:inline-block;font-size:0.85rem;">{ex}</span>' for ex in level['examples']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if i < len(hierarchy_data) - 1:
            st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:15px;margin-top:20px;">
        <div class="hierarchy-card" style="flex:1;border-left:4px solid #22c55e;">
            <div class="hierarchy-icon">🟢</div>
            <div class="hierarchy-title">PROACTIVE</div>
            <div class="hierarchy-description"><strong>Health: 85-100%</strong><br>Equipment is healthy<br>✓ Continue normal monitoring</div>
        </div>
        <div class="hierarchy-card" style="flex:1;border-left:4px solid #f59e0b;">
            <div class="hierarchy-icon">🟠</div>
            <div class="hierarchy-title">PREVENTIVE</div>
            <div class="hierarchy-description"><strong>Health: 70-84%</strong><br>Early warning signs detected<br>⚠️ Plan inspection within 7 days</div>
        </div>
        <div class="hierarchy-card" style="flex:1;border-left:4px solid #ef4444;">
            <div class="hierarchy-icon">🔴</div>
            <div class="hierarchy-title">PREDICTIVE</div>
            <div class="hierarchy-description"><strong>Health: 0-69%</strong><br>High failure risk<br>🚨 Immediate action required (24hrs)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=300, show_spinner=False)
def create_treemap_visualization(is_dark: bool, plant_id: str) -> go.Figure:
    df_plant = df_raw[df_raw['plant_id'] == plant_id].copy()
    labels = [plant_id]; parents = [""]; values = [100]
    health_scores = [int(df_plant['health_score'].mean())]
    for sp in df_plant['sub_plant'].unique():
        labels.append(sp); parents.append(plant_id)
        sp_data = df_plant[df_plant['sub_plant'] == sp]
        values.append(len(sp_data)); health_scores.append(int(sp_data['health_score'].mean()))
        for eq in sp_data['equipment'].unique():
            labels.append(eq[:15]); parents.append(sp)
            eq_data = sp_data[sp_data['equipment'] == eq]
            values.append(len(eq_data)); health_scores.append(int(eq_data['health_score'].mean()))
    colors = ['#22c55e' if s >= 85 else ('#f59e0b' if s >= 70 else '#ef4444') for s in health_scores]
    fig = go.Figure(go.Treemap(
        labels=labels, parents=parents, values=values,
        marker=dict(colors=colors, line=dict(width=2, color='white')),
        text=[f"{l}<br>Health: {s}%" for l, s in zip(labels, health_scores)],
        hovertemplate='<b>%{label}</b><br>Health Score: %{customdata}%<extra></extra>',
        customdata=health_scores, textposition='middle center'
    ))
    bg = "#0f172a" if is_dark else "#ffffff"
    tc = "#e5e7eb" if is_dark else "#0f172a"
    fig.update_layout(
        title={'text':f"Hierarchical Health Map - {plant_id}",'x':0.5,'xanchor':'center','font':{'size':20,'color':tc}},
        paper_bgcolor=bg, plot_bgcolor=bg, height=600, margin=dict(t=60,b=20,l=20,r=20)
    )
    return fig


@st.cache_data(ttl=600, show_spinner=False)
def create_network_diagram(is_dark: bool) -> go.Figure:
    node_x = [0.5,0.2,0.5,0.8,0.1,0.3,0.5,0.7,0.9,0.5]
    node_y = [1.0,0.75,0.75,0.75,0.5,0.5,0.5,0.5,0.5,0.25]
    node_labels = ["Mine Site","Crushing","Grinding","Separation","Crusher-1","Mill-1","Pump-1","Crusher-2","Mill-2","Maintenance Hub"]
    node_colors = ['#2563eb','#3b82f6','#3b82f6','#3b82f6','#22c55e','#f59e0b','#ef4444','#22c55e','#22c55e','#8b5cf6']
    node_sizes = [60,40,40,40,30,30,30,30,30,50]
    edges = [(0,1),(0,2),(0,3),(1,4),(1,7),(2,5),(2,8),(3,6),(4,9),(5,9),(6,9),(7,9),(8,9)]
    edge_x, edge_y = [], []
    for e in edges:
        edge_x += [node_x[e[0]], node_x[e[1]], None]
        edge_y += [node_y[e[0]], node_y[e[1]], None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2,color='#94a3b8'), hoverinfo='none', mode='lines')
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', hoverinfo='text',
        marker=dict(size=node_sizes, color=node_colors, line=dict(width=2,color='white')),
        text=node_labels, textposition="bottom center",
        textfont=dict(size=10, family='Arial'),
        hovertext=[f"<b>{l}</b>" for l in node_labels]
    )
    bg = "#0f172a" if is_dark else "#ffffff"
    tc = "#e5e7eb" if is_dark else "#0f172a"
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title={'text':"Mining Operations Network View",'x':0.5,'xanchor':'center','font':{'size':20,'color':tc}},
        showlegend=False, hovermode='closest',
        paper_bgcolor=bg, plot_bgcolor=bg, height=500,
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        margin=dict(t=60,b=20,l=20,r=20)
    )
    return fig

# =====================================================
# INITIALIZE ISSUES FROM CSV
# =====================================================
def initialize_issues_from_csv() -> None:
    if not st.session_state.data_loaded and df_raw is not None:
        st.session_state.issues = []
        df_issues = df_raw[df_raw['completed'] == False].copy()
        severity_map = {'Critical':'🔴 Critical','Warning':'🟠 Attention','Normal':'🟢 Normal'}
        for _, row in df_issues.iterrows():
            st.session_state.issues.append({
                "Sub-Plant": row['sub_plant'], "Equipment": row['equipment'],
                "Component": row['component'], "Health": int(row['health_score']),
                "Severity": severity_map.get(row['severity'], '🟠 Attention'),
                "Action Type": row['maintenance_type'], "Due": row['action_required'],
                "Done": bool(row['completed']), "Owner": row['owner'],
            })
        st.session_state.data_loaded = True

# =====================================================
# MAIN APPLICATION
# =====================================================
def main():
    if df_raw is None:
        st.error("⚠️ Unable to load data. Please ensure 'mining_data.csv' is in output/ directory.")
        return

    theme_toggle = st.sidebar.toggle("🌗 Dark Mode", value=st.session_state.theme)

    # Show clock when theme changes
    if theme_toggle != st.session_state.theme:
        ph = show_clock("Applying Theme", "Updating dashboard appearance…")
        time.sleep(0.6)
        ph.empty()

    st.session_state.theme = theme_toggle
    theme_colors = DARK_THEME if theme_toggle else LIGHT_THEME
    apply_theme(theme_toggle)

    initialize_issues_from_csv()

    st.markdown("## ⛏️ Mining Industry – Plant Health Dashboard")

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        selected_plant = st.selectbox("🏭 Select Plant", PLANTS, key="plant_select")
    with c2:
        from_date = st.date_input("📅 From", date.today() - timedelta(days=7), key="from_date")
    with c3:
        to_date = st.date_input("📅 To", date.today(), key="to_date")

    # Show clock when plant changes
    if st.session_state._prev_plant is not None and st.session_state._prev_plant != selected_plant:
        ph = show_clock("Loading Plant Data", f"Fetching health metrics for {selected_plant}…")
        time.sleep(0.9)
        ph.empty()
    st.session_state._prev_plant = selected_plant

    st.caption(f"Plant: **{selected_plant}** | Period: **{from_date} → {to_date}**")
    st.markdown("---")

    st.sidebar.title("📂 Navigation")
    tab = st.sidebar.radio("Select Section", ["📊 Overview","🏗️ Hierarchy Visualization","🚨 Alerts","🛠️ Maintenance"], key="tab_select")

    # Show clock when tab changes
    if st.session_state._prev_tab is not None and st.session_state._prev_tab != tab:
        tab_titles = {
            "📊 Overview": ("Loading Overview", "Preparing plant health summary…"),
            "🏗️ Hierarchy Visualization": ("Loading Hierarchy", "Building visualisation layers…"),
            "🚨 Alerts": ("Loading Alerts", "Scanning for critical conditions…"),
            "🛠️ Maintenance": ("Loading Maintenance", "Fetching maintenance schedule…"),
        }
        title, subtitle = tab_titles.get(tab, ("Loading…", "Please wait…"))
        ph = show_clock(title, subtitle)
        time.sleep(0.9)
        ph.empty()
    st.session_state._prev_tab = tab

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Detailed Insights")
    view_mode = st.sidebar.radio("Select View", ["🏭 Plant Overview","🚛 Sub-Plant / Asset Insights","Truck Insights"], key="view_mode")

    # Show clock when view changes
    if st.session_state._prev_view is not None and st.session_state._prev_view != view_mode:
        ph = show_clock("Switching View", "Loading new dashboard panel…")
        time.sleep(0.8)
        ph.empty()
    st.session_state._prev_view = view_mode

    selected_subplant_insight = None
    selected_asset = None

    if view_mode == "Truck Insights":
        selected_truck = st.sidebar.selectbox("Select Truck", ["Truck-1","Truck-2","Truck-3"], key="truck_select")
        ph = show_clock(f"Loading {selected_truck} Dashboard", "Fetching real-time truck telemetry…")
        st.session_state.selected_truck = selected_truck
        st.switch_page("pages/truck1.py")

    if view_mode == "🚛 Sub-Plant / Asset Insights":
        selected_subplant_insight = st.sidebar.selectbox("Select Sub-Plant", list(PLANT_STRUCTURE.keys()), key="subplant_insight")
        selected_asset = st.sidebar.selectbox("Select Asset", list(PLANT_STRUCTURE[selected_subplant_insight].keys()), key="asset_select")

        # Clock on sub-plant change
        if st.session_state._prev_subplant != selected_subplant_insight and st.session_state._prev_subplant is not None:
            ph = show_clock("Loading Sub-Plant", f"Fetching data for {selected_subplant_insight}…")
            time.sleep(0.8)
            ph.empty()
        st.session_state._prev_subplant = selected_subplant_insight

        # Clock on asset change
        if st.session_state._prev_asset != selected_asset and st.session_state._prev_asset is not None:
            ph = show_clock("Loading Asset", f"Fetching intelligence for {selected_asset}…")
            time.sleep(0.8)
            ph.empty()
        st.session_state._prev_asset = selected_asset

        render_subplant_asset_insights(selected_plant, selected_subplant_insight, selected_asset, theme_colors)

    render_operations_panel()

    if tab == "📊 Overview":
        render_overview_tab(selected_plant, to_date, theme_colors)
    elif tab == "🏗️ Hierarchy Visualization":
        render_hierarchy_tab(theme_toggle, selected_plant)
    elif tab == "🚨 Alerts":
        render_alerts_tab(selected_plant, to_date)
    else:
        render_maintenance_tab(selected_plant, to_date)

    st.markdown("---")
    st.caption("Industry-ready mining dashboard designed for Plant Heads, Operations Managers, and Maintenance Teams.")

# =====================================================
# OPERATIONS CONTROL PANEL
# =====================================================
def render_operations_panel() -> None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🚦 Operations Control Panel")
    st.sidebar.caption("Live view of plant issues, required actions, and completion status")

    open_issues = [i for i in st.session_state.issues if not i["Done"]]
    critical_issues = [i for i in open_issues if i["Severity"] == "🔴 Critical"]

    col1, col2 = st.sidebar.columns(2)
    col1.metric("🔴 Critical", len(critical_issues))
    col2.metric("📋 Open", len(open_issues))

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧾 Issues Requiring Action")

    if not open_issues:
        st.sidebar.success("✅ All issues under control")
    else:
        for idx, issue in enumerate(open_issues):
            header = f"{issue['Severity']} | {issue['Component']} ({issue['Action Type']})"
            with st.sidebar.expander(header):
                st.markdown(f"""
**Sub-Plant:** {issue['Sub-Plant']}  
**Equipment:** {issue['Equipment']}  
**Component:** {issue['Component']}  
**Maintenance Type:** {issue['Action Type']}  
**Action Needed:** {issue['Due']}  
**Action Deadline:** {'Within 24 hours' if issue['Action Type'] == 'Predictive' else 'Within 7 days'}  
{countdown_text('24' if issue['Action Type'] == 'Predictive' else '7')}
""")
                if st.button("✔ Mark Completed", key=f"complete_{idx}"):
                    # Show clock while marking complete
                    ph = show_clock("Updating Status", "Saving completion record…")
                    time.sleep(1.0)
                    ph.empty()

                    for i in range(len(st.session_state.issues)):
                        if st.session_state.issues[i] == issue:
                            st.session_state.issues[i]["Done"] = True
                            break
                    st.rerun()

    st.sidebar.markdown("### 🧭 Priority Guide")
    st.sidebar.markdown("""
🟢 **Proactive**  Equipment healthy - Monitor  
🟠 **Preventive**  Early warning - Plan within **7 days**  
🔴 **Predictive**  High risk - Handle **immediately**
""")

# =====================================================
# HIERARCHY VISUALIZATION TAB
# =====================================================
def render_hierarchy_tab(is_dark: bool, plant_id: str) -> None:
    st.markdown("## 🏗️ Mining Operations Monitoring Hierarchy")
    st.markdown("### Understanding How Your Plant is Monitored from Top to Bottom")

    viz_type = st.radio(
        "Select Visualization Type:",
        ["📊 Interactive Flow Diagram","🎴 Detailed Level Cards","🗺️ Hierarchical Health Map","🔗 Network View"],
        horizontal=True
    )
    st.markdown("---")

    if viz_type == "📊 Interactive Flow Diagram":
        st.markdown("### Interactive Flow: From Mine Site to Maintenance Decision")
        st.info("👆 **Hover over each node** to see details.")
        with with_clock("Rendering Flow Diagram", "Building interactive hierarchy…"):
            fig = create_hierarchy_flowchart(is_dark)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("---")
        st.markdown("#### 🎨 Color Guide")
        c1, c2, c3 = st.columns(3)
        c1.markdown("🟢 **Green** = Proactive (Healthy)")
        c2.markdown("🟠 **Amber** = Preventive (Warning)")
        c3.markdown("🔴 **Red** = Predictive (Critical)")

    elif viz_type == "🎴 Detailed Level Cards":
        st.markdown("### 7-Level Monitoring System Explained")
        st.info("📚 Each card represents one level. Follow the flow from top to bottom.")
        render_hierarchy_cards()

    elif viz_type == "🗺️ Hierarchical Health Map":
        st.markdown("### Real-Time Health Status Across All Levels")
        st.info("🔍 **Larger boxes** = higher level. **Colors** show health status.")
        with with_clock("Building Health Map", f"Computing live health scores for {plant_id}…"):
            fig = create_treemap_visualization(is_dark, plant_id)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        df_plant = df_raw[df_raw['plant_id'] == plant_id]
        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Healthy Assets", len(df_plant[df_plant['health_score'] >= 85]), "85-100%")
        c2.metric("🟠 Warning Assets", len(df_plant[(df_plant['health_score'] >= 70) & (df_plant['health_score'] < 85)]), "70-84%")
        c3.metric("🔴 Critical Assets", len(df_plant[df_plant['health_score'] < 70]), "< 70%")

    else:
        st.markdown("### Network Topology - How Systems Connect")
        st.info("🔗 Shows **relationships** between parts of your mining operation.")
        with with_clock("Building Network Diagram", "Mapping equipment relationships…"):
            fig = create_network_diagram(is_dark)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown("🔵 **Blue** = Site/Sub-Plant")
        c2.markdown("🟢 **Green** = Healthy")
        c3.markdown("🟠 **Amber** = Warning")
        c4.markdown("🔴 **Red** = Critical")

    st.markdown("---")
    st.markdown("### 📖 How to Use This Information")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""#### For Plant Managers\n- **Monitor** overall health\n- **Identify** Sub-Plants needing attention\n- **Plan** resources\n- **Track** improvement""")
    with c2:
        st.markdown("""#### For Maintenance Teams\n- **Drill down** to equipment issues\n- **Review** sensor readings\n- **Prioritize** by health score\n- **Execute** maintenance proactively""")

    st.markdown("---")
    st.markdown("### 🔄 Complete Monitoring Workflow")
    st.code("""
STEP 1: Sensors collect real-time data (Vibration, Temperature, Pressure)
       ↓
STEP 2: Data analyzed → Health Score (0-100%)
       ↓
STEP 3: AI categorizes condition:
       • 85-100% = 🟢 Healthy (Proactive)
       • 70-84%  = 🟠 Warning (Preventive)
       • 0-69%   = 🔴 Critical (Predictive)
       ↓
STEP 4: Maintenance recommendations generated
       ↓
STEP 5: Alerts sent to relevant teams
       ↓
STEP 6: Actions tracked in Operations Control Panel
""", language="text")

    st.markdown("---")
    st.markdown("### 🎮 Try It Yourself")
    c1, c2, c3 = st.columns(3)
    with c1:
        selected_subplant = st.selectbox("Sub-Plant", list(PLANT_STRUCTURE.keys()), key="hier_subplant")
    with c2:
        selected_equipment = st.selectbox("Equipment", list(PLANT_STRUCTURE[selected_subplant].keys()), key="hier_equipment")
    with c3:
        selected_component = st.selectbox("Component", PLANT_STRUCTURE[selected_subplant][selected_equipment], key="hier_component")

    # Clock on hierarchy drilldown changes
    combo = f"{selected_subplant}|{selected_equipment}|{selected_component}"
    if st.session_state.get("_prev_hier_combo") and st.session_state["_prev_hier_combo"] != combo:
        ph = show_clock("Computing Health Score", "Running sensor analysis…")
        time.sleep(0.6)
        ph.empty()
    st.session_state["_prev_hier_combo"] = combo

    sample_health = get_health_score(plant_id, selected_subplant, selected_equipment, selected_component)
    sample_status = status(sample_health)
    sample_maintenance = maintenance(sample_health)
    sample_sensors = SENSOR_MAP.get(selected_component, ["General"])

    st.markdown("---")
    st.markdown("#### 🎯 Complete Hierarchy Path for Your Selection:")
    st.markdown(f"""
    <div class="hierarchy-card">
        <h3>🏭 Mine Site → 🏗️ {selected_subplant} → ⚙️ {selected_equipment} → 🔧 {selected_component}</h3>
        <hr>
        <p><strong>📡 Monitored Sensors:</strong> {', '.join(sample_sensors)}</p>
        <p><strong>📊 Current Health Score:</strong> <span class="status-badge status-{'healthy' if sample_health >= 85 else 'warning' if sample_health >= 70 else 'critical'}">{sample_health}%</span></p>
        <p><strong>🎯 Status:</strong> {sample_status}</p>
        <p><strong>🛠️ Maintenance Type:</strong> {sample_maintenance}</p>
        <p><strong>⚡ Recommended Action:</strong> {action(sample_health)}</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# TAB RENDERERS
# =====================================================
def render_overview_tab(selected_plant: str, to_date: date, theme_colors: Dict) -> None:
    st.subheader("🏭 Overall Plant Health")

    with with_clock("Loading Plant Overview", f"Calculating health metrics for {selected_plant}…"):
        df_plant = get_plant_data(selected_plant)
        sub_scores = {}
        for sp in PLANT_STRUCTURE.keys():
            sp_data = df_plant[df_plant['sub_plant'] == sp]
            sub_scores[sp] = int(sp_data['health_score'].mean()) if not sp_data.empty else 85

    plant_health = int(df_plant['health_score'].mean()) if not df_plant.empty else 85
    open_issues = [i for i in st.session_state.issues if not i["Done"]]
    critical_issues = [i for i in open_issues if i["Severity"] == "🔴 Critical"]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Plant Health", f"{plant_health}%")
    k2.metric("Status", status(plant_health))
    k3.metric("Maintenance Mode", maintenance(plant_health))
    k4.metric("Critical Areas", sum(1 for v in sub_scores.values() if v < 70))

    st.markdown("### 📊 Visual Health Indicators")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.plotly_chart(create_donut_chart(plant_health, "Overall Plant Health", theme_colors['success'], theme_colors['danger']), use_container_width=True, config={'displayModeBar': False})
    with d2:
        st.plotly_chart(create_donut_chart(max(30, 100 - len(critical_issues)*10), "Risk Buffer", theme_colors['success'], theme_colors['danger']), use_container_width=True, config={'displayModeBar': False})
    with d3:
        st.plotly_chart(create_donut_chart(max(40, 100 - len(open_issues)*5), "Operational Stability", theme_colors['success'], theme_colors['danger']), use_container_width=True, config={'displayModeBar': False})

    df_sub = pd.DataFrame({"Sub-Plant": sub_scores.keys(), "Health (%)": sub_scores.values()})
    st.plotly_chart(create_bar_chart(df_sub, "Sub-Plant", "Health (%)", "Sub-Plant Health"), use_container_width=True, config={'displayModeBar': False})

    st.markdown("### 🏗️ Sub-Plant → Components")
    selected_subplant = st.selectbox("Select Sub-Plant", list(PLANT_STRUCTURE.keys()), key="subplant_drilldown")

    # Clock on sub-plant drilldown change
    if st.session_state._prev_subplant_drilldown is not None and st.session_state._prev_subplant_drilldown != selected_subplant:
        ph = show_clock("Drilling Down", f"Loading component data for {selected_subplant}…")
        time.sleep(0.7)
        ph.empty()
    st.session_state._prev_subplant_drilldown = selected_subplant

    rows = []
    for eq, comps in PLANT_STRUCTURE[selected_subplant].items():
        for comp in comps:
            score = get_health_score(selected_plant, selected_subplant, eq, comp)
            rows.append({"Equipment": eq, "Component": comp, "Health (%)": score, "Status": status(score)})
    df_comp = pd.DataFrame(rows)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

    st.markdown("### 🔩 Component → Sensors")
    selected_component = st.selectbox("Select Component", df_comp["Component"].unique(), key="component_select")

    # Clock on component change
    if st.session_state._prev_component is not None and st.session_state._prev_component != selected_component:
        ph = show_clock("Loading Sensor Data", f"Fetching readings for {selected_component}…")
        time.sleep(0.6)
        ph.empty()
    st.session_state._prev_component = selected_component

    sensor_rows = []
    comp_data = df_plant[(df_plant['sub_plant'] == selected_subplant) & (df_plant['component'] == selected_component)]
    for _, row in comp_data.iterrows():
        sensor_rows.append({"Sensor": row['sensor_type'], "Health (%)": int(row['health_score']), "Status": status(int(row['health_score']))})
    if sensor_rows:
        st.dataframe(pd.DataFrame(sensor_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No sensor data available for this component")

    st.markdown("### ⚠️ Top Risk Areas (Quick View)")
    if open_issues:
        st.dataframe(pd.DataFrame(open_issues)[["Sub-Plant","Equipment","Component","Severity","Action Type","Due"]], use_container_width=True, hide_index=True)
    else:
        st.success("✅ No high-risk areas identified")

    st.markdown("### 🏭 Mining Operations Snapshot")
    try:
        st.image("images/img1.jpg", caption="Mining plant operations monitored through real-time systems", use_container_width=True)
    except:
        st.info("📷 Add 'images/img1.jpg' to show operations photo")


def render_alerts_tab(selected_plant: str, to_date: date) -> None:
    st.subheader("🚨 Plant → Sub-Plant → Component → Sensor Alerts")

    with with_clock("Scanning for Alerts", f"Checking critical conditions in {selected_plant}…"):
        df_alerts = df_raw[(df_raw['plant_id'] == selected_plant) & (df_raw['health_score'] < 75)].copy()

    if not df_alerts.empty:
        alert_display = df_alerts[['plant_id','sub_plant','equipment','component','sensor_type','status','maintenance_type','action_required']].copy()
        alert_display.columns = ['Plant','Sub-Plant','Equipment','Component','Sensor','Severity','Maintenance','Action']
        alert_display['Severity'] = alert_display['Severity'].apply(
            lambda x: f"🟢 {x}" if x == 'Healthy' else (f"🟠 {x}" if x == 'Warning' else f"🔴 {x}")
        )
        st.dataframe(alert_display, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No active alerts")


def render_maintenance_tab(selected_plant: str, to_date: date) -> None:
    st.subheader("🛠️ Maintenance Planning (Industry View)")

    with with_clock("Loading Maintenance Schedule", "Fetching planned maintenance records…"):
        df_maint = get_plant_data(selected_plant)

    if not df_maint.empty:
        maint_display = df_maint[['sub_plant','equipment','component','health_score','maintenance_type','priority','due_date']].copy()
        maint_display.columns = ['Sub-Plant','Equipment','Component','Health (%)','Maintenance Type','Priority','Planned Date']
        maint_display['Planned Date'] = pd.to_datetime(maint_display['Planned Date']).dt.date
        st.dataframe(maint_display, use_container_width=True, hide_index=True)

        maint_counts = df_maint['maintenance_type'].value_counts()
        maint_df = pd.DataFrame({'Maintenance Type': maint_counts.index, 'Count': maint_counts.values})
        st.plotly_chart(create_pie_chart(maint_df, "Maintenance Type", "Maintenance Strategy Distribution"), use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No maintenance data available for this plant")

    st.success("📌 Predictive maintenance should be prioritized for LOW health assets to avoid unplanned downtime.")


if __name__ == "__main__":
    main()
