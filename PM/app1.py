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
# SESSION STATE INITIALIZATION
# =====================================================
if "issues" not in st.session_state:
    st.session_state.issues = []
if "theme" not in st.session_state:
    st.session_state.theme = False
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# =====================================================
# DATA LOADING
# =====================================================
@st.cache_data
def load_data():
    """Load data from CSV file"""
    try:
        df = pd.read_csv('output/mining_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df_raw = load_data()

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
    """Apply comprehensive theme styling"""
    theme = DARK_THEME if is_dark else LIGHT_THEME
    
    st.markdown(f"""
    <style>
    /* Global Styles */
    .block-container {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {theme['text_primary']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {theme['bg_secondary']};
        border-right: 1px solid {theme['border']};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {theme['text_primary']};
    }}
    
    /* Buttons */
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
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        font-weight: 500;
    }}
    
    /* Metrics */
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
    
    /* DataFrames */
    .dataframe {{
        border: 1px solid {theme['border']} !important;
        border-radius: 8px;
    }}
    
    /* Dividers */
    hr {{
        margin: 2rem 0;
        border-color: {theme['border']};
    }}
    
    /* Cards */
    .element-container {{
        transition: all 0.2s ease;
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        border-radius: 8px;
    }}
    
    /* Date Input */
    .stDateInput > div > div {{
        border-radius: 8px;
    }}
    
    /* Caption */
    .caption {{
        color: {theme['text_secondary']};
        font-size: 0.875rem;
    }}
    
    /* Code Block */
    .stCodeBlock {{
        border-radius: 8px;
        border: 1px solid {theme['border']};
    }}
    
    /* Success/Warning/Error */
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
    
    /* Hierarchy Card Styles */
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
    
    .hierarchy-icon {{
        font-size: 2.5rem;
        margin-bottom: 10px;
    }}
    
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
    
    .status-healthy {{
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid #22c55e;
    }}
    
    .status-warning {{
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid #f59e0b;
    }}
    
    .status-critical {{
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }}
    
    .flow-arrow {{
        text-align: center;
        font-size: 2rem;
        color: {theme['accent']};
        margin: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# UTILITY FUNCTIONS (CSV-based)
# =====================================================
def get_health_score(plant_id: str, sub_plant: str, equipment: str, component: str) -> int:
    """Get health score from CSV data"""
    filtered = df_raw[
        (df_raw['plant_id'] == plant_id) &
        (df_raw['sub_plant'] == sub_plant) &
        (df_raw['equipment'] == equipment) &
        (df_raw['component'] == component)
    ]
    if not filtered.empty:
        return int(filtered['health_score'].iloc[0])
    return 85  # Default healthy

def status(score: int) -> str:
    """Determine status based on health score"""
    if score >= 85:
        return "🟢 Healthy"
    elif score >= 70:
        return "🟠 Warning"
    else:
        return "🔴 Critical"

def maintenance(score: int) -> str:
    """Determine maintenance type"""
    if score >= 85:
        return "Proactive"
    elif score >= 70:
        return "Preventive"
    else:
        return "Predictive"

def action(score: int) -> str:
    """Determine required action"""
    if score >= 85:
        return "Continue monitoring"
    elif score >= 70:
        return "Plan inspection"
    else:
        return "Immediate inspection & shutdown planning"

def ml_risk_prediction(score: int) -> str:
    """ML-based failure risk prediction"""
    if score < 65:
        return "🔴 High Failure Risk"
    elif score < 80:
        return "🟠 Medium Failure Risk"
    else:
        return "🟢 Low Failure Risk"

def countdown_text(due_text: str) -> str:
    """Convert due date to countdown text"""
    if "24" in due_text:
        return "⏱ Less than 24 hours remaining"
    elif "7" in due_text:
        return "⏱ 3–7 days remaining"
    else:
        return "⏱ Monitor"

# =====================================================
# ENHANCED VISUALIZATION FUNCTIONS - FIXED
# =====================================================
def create_donut_chart(value: int, title: str, theme_colors: Dict) -> go.Figure:
    """Create enhanced donut chart with theme support - FIXED"""
    fig = go.Figure(data=[go.Pie(
        values=[value, 100 - value],
        hole=0.7,
        marker=dict(
            colors=[theme_colors['success'], theme_colors['danger']],
            line=dict(color='rgba(0,0,0,0)', width=0)
        ),
        textinfo='none',
        hoverinfo='skip'
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14),  # FIXED: Removed 'weight' parameter
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        annotations=[dict(
            text=f"{value}%",
            x=0.5, y=0.5,
            font=dict(size=28),  # FIXED: Removed 'weight' parameter
            showarrow=False
        )],
        height=220,
        margin=dict(t=40, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    """Create enhanced bar chart"""
    fig = px.bar(
        df, x=x, y=y,
        color=y,
        color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e'],
        title=title
    )
    
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

def create_pie_chart(df: pd.DataFrame, names: str, title: str) -> go.Figure:
    """Create enhanced pie chart"""
    fig = px.pie(
        df,
        names=names,
        title=title,
        color_discrete_sequence=['#22c55e', '#f59e0b', '#ef4444']
    )
    
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# =====================================================
# HIERARCHY VISUALIZATION FUNCTIONS - FIXED
# =====================================================
def create_hierarchy_flowchart(is_dark: bool) -> go.Figure:
    """Create interactive hierarchy flowchart using Plotly Sankey diagram - FIXED"""
    
    node_labels = [
        "🏭 Mine Site",
        "🏗️ Sub-Plant",
        "⚙️ Equipment",
        "🔧 Component",
        "📡 Sensor",
        "📊 Health Score",
        "🟢 Proactive",
        "🟠 Preventive",
        "🔴 Predictive"
    ]
    
    node_colors = [
        "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#dbeafe",
        "#fbbf24", "#22c55e", "#f59e0b", "#ef4444"
    ]
    
    links = [
        (0, 1, 20), (1, 2, 20), (2, 3, 20), (3, 4, 20), (4, 5, 20),
        (5, 6, 7), (5, 7, 7), (5, 8, 6),
    ]
    
    source = [link[0] for link in links]
    target = [link[1] for link in links]
    value = [link[2] for link in links]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=30,
            line=dict(color="white", width=2),
            label=node_labels,
            color=node_colors,
            customdata=[
                "Starting point of monitoring",
                "Crushing, Grinding, Separation, etc.",
                "Crushers, Mills, Pumps, etc.",
                "Bearings, Motors, Gearbox, etc.",
                "Vibration, Temperature, Pressure",
                "Real-time condition assessment",
                "Equipment healthy - Monitor",
                "Early warning - Plan inspection",
                "High risk - Immediate action"
            ],
            hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>'
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(37, 99, 235, 0.3)'
        )
    )])
    
    bg_color = "#0f172a" if is_dark else "#ffffff"
    text_color = "#e5e7eb" if is_dark else "#0f172a"
    
    fig.update_layout(
        title={
            'text': "Mining Operations Monitoring Hierarchy",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': text_color, 'family': 'Arial'}  # FIXED: Changed from 'Arial Black' to 'Arial'
        },
        font=dict(size=12, color=text_color, family='Arial'),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        height=600,
        margin=dict(t=80, b=20, l=20, r=20)
    )
    
    return fig

def render_subplant_asset_insights(
    selected_plant: str,
    selected_subplant: str,
    selected_asset: str,
    theme_colors: Dict
) -> None:

    st.subheader(f"🚛 Asset Intelligence – {selected_asset}")

    df_filtered = df_raw[
        (df_raw["plant_id"] == selected_plant) &
        (df_raw["sub_plant"] == selected_subplant) &
        (df_raw["equipment"] == selected_asset)
    ].copy()

    if df_filtered.empty:
        st.warning("No data available for this asset")
        return

    # ===================================================
    # 1️⃣ OVERALL ASSET HEALTH
    # ===================================================

    asset_health = int(df_filtered["health_score"].mean())

    k1, k2, k3 = st.columns(3)
    k1.metric("Asset Health", f"{asset_health}%")
    k2.metric("Status", status(asset_health))
    k3.metric("Maintenance Mode", maintenance(asset_health))

    st.plotly_chart(
        create_donut_chart(asset_health, "Asset Health", theme_colors),
        use_container_width=True,
        config={'displayModeBar': False}
    )

    # ===================================================
    # 2️⃣ COMPONENT HEALTH BREAKDOWN
    # ===================================================

    st.markdown("### 🔩 Component Health Overview")

    comp_df = (
        df_filtered
        .groupby("component")["health_score"]
        .mean()
        .reset_index()
        .rename(columns={"health_score": "Health (%)"})
    )

    comp_df["Health (%)"] = comp_df["Health (%)"].astype(int)
    comp_df["Status"] = comp_df["Health (%)"].apply(status)

    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    st.plotly_chart(
        create_bar_chart(
            comp_df,
            "component",
            "Health (%)",
            "Component Health Distribution"
        ),
        use_container_width=True,
        config={'displayModeBar': False}
    )

    # ===================================================
    # 3️⃣ COMPONENT LEVEL INTELLIGENCE
    # ===================================================

    avg_comp_health = comp_df["Health (%)"].mean()

    st.markdown("### 🧠 Component Intelligence Insight")

    if avg_comp_health >= 85:
        st.success("All components operating in stable condition.")
    elif 70 <= avg_comp_health < 85:
        st.warning("Moderate wear detected. Preventive maintenance recommended.")
    else:
        st.error("Critical component degradation detected. Immediate action required.")

    # ===================================================
    # 4️⃣ SENSOR DRILLDOWN
    # ===================================================

    st.markdown("### 📡 Sensor-Level Intelligence")

    selected_component = st.selectbox(
        "Select Component",
        comp_df["component"],
        key="asset_component_select"
    )

    sensor_df = df_filtered[df_filtered["component"] == selected_component]

    if sensor_df.empty:
        st.info("No sensor data available")
        return

    sensor_display = sensor_df[["sensor_type", "health_score"]].copy()
    sensor_display.columns = ["Sensor", "Health (%)"]
    sensor_display["Health (%)"] = sensor_display["Health (%)"].astype(int)
    sensor_display["Status"] = sensor_display["Health (%)"].apply(status)

    st.dataframe(sensor_display, use_container_width=True, hide_index=True)

    # ===================================================
    # 5️⃣ SENSOR RISK INSIGHT
    # ===================================================

    worst_sensor = sensor_display.sort_values("Health (%)").iloc[0]
    avg_sensor_health = sensor_display["Health (%)"].mean()

    st.markdown("### 🚨 Sensor Risk Insight")

    if avg_sensor_health >= 85:
        st.success(
            f"All sensors stable. Lowest sensor: "
            f"{worst_sensor['Sensor']} ({worst_sensor['Health (%)']}%)"
        )

    elif 70 <= avg_sensor_health < 85:
        st.warning(
            f"Sensor degradation detected. Monitor "
            f"{worst_sensor['Sensor']} ({worst_sensor['Health (%)']}%)"
        )

    else:
        st.error(
            f"Critical sensor risk detected! "
            f"{worst_sensor['Sensor']} at "
            f"{worst_sensor['Health (%)']}%. Immediate maintenance required."
        )

    # ===================================================
    # 6️⃣ SIMULATED RUL GRAPH
    # ===================================================

    st.markdown("### 📈 Remaining Useful Life Prediction")

    cycles = np.arange(0, 400, 20)
    actual = np.linspace(400, 120, len(cycles))
    predicted = actual + np.random.normal(0, 12, len(cycles))

    fig_rul = go.Figure()
    fig_rul.add_trace(go.Scatter(
        x=cycles, y=actual,
        mode="lines",
        name="Actual"
    ))
    fig_rul.add_trace(go.Scatter(
        x=cycles, y=predicted,
        mode="lines",
        name="Predicted",
        line=dict(dash="dash")
    ))

    fig_rul.update_layout(
        title="Remaining Useful Life (RUL)",
        xaxis_title="Cycle",
        yaxis_title="Remaining Hours",
        height=350
    )

    st.plotly_chart(fig_rul, use_container_width=True)


def render_hierarchy_cards():
    """Render hierarchy as interactive cards with visual flow"""
    
    hierarchy_data = [
        {
            "icon": "🏭",
            "title": "LEVEL 1: Mine Site",
            "description": "Main mining facility containing all operational units",
            "examples": ["Plant-1", "Plant-2", "Plant-3"],
            "color": "#2563eb"
        },
        {
            "icon": "🏗️",
            "title": "LEVEL 2: Sub-Plant",
            "description": "Specialized processing units within the mine site",
            "examples": ["Crushing Plant", "Grinding Plant", "Separation Plant"],
            "color": "#3b82f6"
        },
        {
            "icon": "⚙️",
            "title": "LEVEL 3: Equipment",
            "description": "Heavy machinery and systems that perform operations",
            "examples": ["Jaw Crusher", "Ball Mill", "Flotation Pump"],
            "color": "#60a5fa"
        },
        {
            "icon": "🔧",
            "title": "LEVEL 4: Component",
            "description": "Critical parts of equipment that require monitoring",
            "examples": ["Bearing", "Motor", "Gearbox", "Pump"],
            "color": "#93c5fd"
        },
        {
            "icon": "📡",
            "title": "LEVEL 5: Sensor",
            "description": "IoT devices measuring real-time conditions",
            "examples": ["Vibration", "Temperature", "Pressure", "Power"],
            "color": "#38bdf8"
        },
        {
            "icon": "📊",
            "title": "LEVEL 6: Health Score",
            "description": "AI-calculated condition score (0-100%)",
            "examples": ["85-100% Healthy", "70-84% Warning", "0-69% Critical"],
            "color": "#fbbf24"
        },
        {
            "icon": "🎯",
            "title": "LEVEL 7: Maintenance Decision",
            "description": "Automated recommendation based on health score",
            "examples": [],
            "color": "#8b5cf6"
        }
    ]
    
    for i, level in enumerate(hierarchy_data):
        st.markdown(f"""
        <div class="hierarchy-card">
            <div class="hierarchy-icon">{level['icon']}</div>
            <div class="hierarchy-title">{level['title']}</div>
            <div class="hierarchy-description">{level['description']}</div>
            <div style="margin-top: 12px;">
                {''.join([f'<span style="background: rgba(37, 99, 235, 0.1); padding: 4px 10px; border-radius: 6px; margin: 3px; display: inline-block; font-size: 0.85rem;">{ex}</span>' for ex in level['examples']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if i < len(hierarchy_data) - 1:
            st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: flex; gap: 15px; margin-top: 20px;">
        <div class="hierarchy-card" style="flex: 1; border-left: 4px solid #22c55e;">
            <div class="hierarchy-icon">🟢</div>
            <div class="hierarchy-title">PROACTIVE</div>
            <div class="hierarchy-description">
                <strong>Health: 85-100%</strong><br>
                Equipment is healthy<br>
                ✓ Continue normal monitoring
            </div>
        </div>
        <div class="hierarchy-card" style="flex: 1; border-left: 4px solid #f59e0b;">
            <div class="hierarchy-icon">🟠</div>
            <div class="hierarchy-title">PREVENTIVE</div>
            <div class="hierarchy-description">
                <strong>Health: 70-84%</strong><br>
                Early warning signs detected<br>
                ⚠️ Plan inspection within 7 days
            </div>
        </div>
        <div class="hierarchy-card" style="flex: 1; border-left: 4px solid #ef4444;">
            <div class="hierarchy-icon">🔴</div>
            <div class="hierarchy-title">PREDICTIVE</div>
            <div class="hierarchy-description">
                <strong>Health: 0-69%</strong><br>
                High failure risk<br>
                🚨 Immediate action required (24hrs)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_treemap_visualization(is_dark: bool, plant_id: str) -> go.Figure:
    """Create treemap showing hierarchical structure with health scores from CSV"""
    
    df_plant = df_raw[df_raw['plant_id'] == plant_id].copy()
    
    labels = [plant_id]
    parents = [""]
    values = [100]
    health_scores = [int(df_plant['health_score'].mean())]
    
    for sub_plant in df_plant['sub_plant'].unique():
        labels.append(sub_plant)
        parents.append(plant_id)
        sp_data = df_plant[df_plant['sub_plant'] == sub_plant]
        values.append(len(sp_data))
        health_scores.append(int(sp_data['health_score'].mean()))
        
        for equipment in sp_data['equipment'].unique():
            eq_label = f"{equipment[:15]}"
            labels.append(eq_label)
            parents.append(sub_plant)
            eq_data = sp_data[sp_data['equipment'] == equipment]
            values.append(len(eq_data))
            health_scores.append(int(eq_data['health_score'].mean()))
    
    colors = []
    for score in health_scores:
        if score >= 85:
            colors.append('#22c55e')
        elif score >= 70:
            colors.append('#f59e0b')
        else:
            colors.append('#ef4444')
    
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(width=2, color='white')
        ),
        text=[f"{label}<br>Health: {score}%" for label, score in zip(labels, health_scores)],
        hovertemplate='<b>%{label}</b><br>Health Score: %{customdata}%<extra></extra>',
        customdata=health_scores,
        textposition='middle center'
    ))
    
    bg_color = "#0f172a" if is_dark else "#ffffff"
    text_color = "#e5e7eb" if is_dark else "#0f172a"
    
    fig.update_layout(
        title={
            'text': f"Hierarchical Health Map - {plant_id} Overview",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': text_color}
        },
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=600,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    return fig

def create_network_diagram(is_dark: bool) -> go.Figure:
    """Create network diagram showing relationships - FIXED"""
    
    node_x = [0.5, 0.2, 0.5, 0.8, 0.1, 0.3, 0.5, 0.7, 0.9, 0.5]
    node_y = [1.0, 0.75, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25]
    
    node_labels = [
        "Mine Site",
        "Crushing", "Grinding", "Separation",
        "Crusher-1", "Mill-1", "Pump-1", "Crusher-2", "Mill-2",
        "Maintenance Hub"
    ]
    
    node_colors = ['#2563eb', '#3b82f6', '#3b82f6', '#3b82f6',
                   '#22c55e', '#f59e0b', '#ef4444', '#22c55e', '#22c55e',
                   '#8b5cf6']
    
    node_sizes = [60, 40, 40, 40, 30, 30, 30, 30, 30, 50]
    
    edge_x = []
    edge_y = []
    
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 7),
        (2, 5), (2, 8),
        (3, 6),
        (4, 9), (5, 9), (6, 9), (7, 9), (8, 9)
    ]
    
    for edge in edges:
        edge_x.extend([node_x[edge[0]], node_x[edge[1]], None])
        edge_y.extend([node_y[edge[0]], node_y[edge[1]], None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#94a3b8'),
        hoverinfo='none',
        mode='lines'
    )
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        text=node_labels,
        textposition="bottom center",
        textfont=dict(size=10, family='Arial'),  # FIXED: Changed from 'Arial Black' to 'Arial'
        hovertext=[f"<b>{label}</b><br>Click to explore" for label in node_labels]
    )
    
    bg_color = "#0f172a" if is_dark else "#ffffff"
    text_color = "#e5e7eb" if is_dark else "#0f172a"
    
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title={
            'text': "Mining Operations Network View",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': text_color}
        },
        showlegend=False,
        hovermode='closest',
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=500,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    return fig

# =====================================================
# INITIALIZE ISSUES FROM CSV
# =====================================================
def initialize_issues_from_csv() -> None:
    """Initialize issues from CSV data"""
    if not st.session_state.data_loaded and df_raw is not None:
        st.session_state.issues = []
        
        df_issues = df_raw[df_raw['completed'] == False].copy()
        
        for _, row in df_issues.iterrows():
            severity_map = {
                'Critical': '🔴 Critical',
                'Warning': '🟠 Attention',
                'Normal': '🟢 Normal'
            }
            
            st.session_state.issues.append({
                "Sub-Plant": row['sub_plant'],
                "Equipment": row['equipment'],
                "Component": row['component'],
                "Health": int(row['health_score']),
                "Severity": severity_map.get(row['severity'], '🟠 Attention'),
                "Action Type": row['maintenance_type'],
                "Due": row['action_required'],
                "Done": bool(row['completed']),
                "Owner": row['owner'],
            })
        
        st.session_state.data_loaded = True

# =====================================================
# MAIN APPLICATION
# =====================================================
def main():
    if df_raw is None:
        st.error("⚠️ Unable to load data. Please ensure 'mining_data.csv' is in the same directory as this script.")
        return
    
    # Apply theme
    theme_toggle = st.sidebar.toggle("🌗 Dark Mode", value=st.session_state.theme)
    st.session_state.theme = theme_toggle
    theme_colors = DARK_THEME if theme_toggle else LIGHT_THEME
    apply_theme(theme_toggle)
    
    # Initialize issues from CSV
    initialize_issues_from_csv()
    
    # Header
    st.markdown("## ⛏️ Mining Industry – Plant Health Dashboard")
    
    # Top controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        selected_plant = st.selectbox("🏭 Select Plant", PLANTS, key="plant_select")
    with c2:
        from_date = st.date_input("📅 From", date.today() - timedelta(days=7), key="from_date")
    with c3:
        to_date = st.date_input("📅 To", date.today(), key="to_date")
    
    st.caption(f"Plant: **{selected_plant}** | Period: **{from_date} → {to_date}**")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("📂 Navigation")
    tab = st.sidebar.radio("Select Section", ["📊 Overview", "🏗️ Hierarchy Visualization", "🚨 Alerts", "🛠️ Maintenance"], key="tab_select")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Detailed Insights")
    
    view_mode = st.sidebar.radio(
        "Select View",
        ["🏭 Plant Overview", "🚛 Sub-Plant / Asset Insights", "Truck Insights"],
        key="view_mode"
    )
    
    selected_subplant_insight = None
    selected_asset = None


    if view_mode == "Truck Insights":
     selected_truck = st.sidebar.selectbox(
        "Select Truck",
        ["Truck-1", "Truck-2", "Truck-3"],
        key="truck_select"
     )

     if selected_truck == "Truck-1":
        st.session_state.selected_truck = "Truck-1"
        st.switch_page("pages/truck.py")

     elif selected_truck == "Truck-2":
        st.session_state.selected_truck = "Truck-2"
        st.switch_page("pages/truck.py")

     elif selected_truck == "Truck-3":
        st.session_state.selected_truck = "Truck-3"
        st.switch_page("pages/truck.py")

    if view_mode == "🚛 Sub-Plant / Asset Insights":

     selected_subplant_insight = st.sidebar.selectbox(
        "Select Sub-Plant",
        list(PLANT_STRUCTURE.keys()),
        key="subplant_insight"
     )

     selected_asset = st.sidebar.selectbox(
        "Select Asset",
        list(PLANT_STRUCTURE[selected_subplant_insight].keys()),
        key="asset_select"
     )

     render_subplant_asset_insights(
        selected_plant,
        selected_subplant_insight,
        selected_asset,
        theme_colors
     )

    
    # Operations Control Panel
    render_operations_panel()
    
    # Tab content
    if tab == "📊 Overview":
        render_overview_tab(selected_plant, to_date, theme_colors)
    elif tab == "🏗️ Hierarchy Visualization":
        render_hierarchy_tab(theme_toggle, selected_plant)
    elif tab == "🚨 Alerts":
        render_alerts_tab(selected_plant, to_date)
    else:
        render_maintenance_tab(selected_plant, to_date)
    
    # Footer
    st.markdown("---")
    st.caption(
        "Industry-ready mining dashboard designed for Plant Heads, Operations Managers, "
        "and Maintenance Teams."
    )

# =====================================================
# OPERATIONS CONTROL PANEL
# =====================================================
def render_operations_panel() -> None:
    """Render the operations control panel in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🚦 Operations Control Panel")
    st.sidebar.caption(
        "Live view of plant issues, required actions, and completion status"
    )
    
    open_issues = [i for i in st.session_state.issues if not i["Done"]]
    critical_issues = [i for i in open_issues if i["Severity"] == "🔴 Critical"]
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🔴 Critical", len(critical_issues))
    with col2:
        st.metric("📋 Open", len(open_issues))
    
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
                    for i in range(len(st.session_state.issues)):
                        if st.session_state.issues[i] == issue:
                            st.session_state.issues[i]["Done"] = True
                            break
                    st.rerun()
    
    st.sidebar.markdown("### 🧭 Priority Guide")
    st.sidebar.markdown("""
🟢 **Proactive**  
Equipment healthy - Monitor

🟠 **Preventive**  
Early warning - Plan within **7 days**

🔴 **Predictive**  
High risk - Handle **immediately**
""")

# =====================================================
# HIERARCHY VISUALIZATION TAB
# =====================================================
def render_hierarchy_tab(is_dark: bool, plant_id: str) -> None:
    """Render the hierarchy visualization tab"""
    
    st.markdown("## 🏗️ Mining Operations Monitoring Hierarchy")
    st.markdown("### Understanding How Your Plant is Monitored from Top to Bottom")
    
    viz_type = st.radio(
        "Select Visualization Type:",
        ["📊 Interactive Flow Diagram", "🎴 Detailed Level Cards", "🗺️ Hierarchical Health Map", "🔗 Network View"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if viz_type == "📊 Interactive Flow Diagram":
        st.markdown("### Interactive Flow: From Mine Site to Maintenance Decision")
        st.info("👆 **Hover over each node** to see details. This diagram shows how data flows from the mine site down to individual maintenance decisions.")
        
        fig = create_hierarchy_flowchart(is_dark)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        st.markdown("#### 🎨 Color Guide")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🟢 **Green** = Proactive (Healthy)")
        with col2:
            st.markdown("🟠 **Amber** = Preventive (Warning)")
        with col3:
            st.markdown("🔴 **Red** = Predictive (Critical)")
    
    elif viz_type == "🎴 Detailed Level Cards":
        st.markdown("### 7-Level Monitoring System Explained")
        st.info("📚 Each card represents one level in our monitoring system. Follow the flow from top to bottom.")
        
        render_hierarchy_cards()
    
    elif viz_type == "🗺️ Hierarchical Health Map":
        st.markdown("### Real-Time Health Status Across All Levels")
        st.info("🔍 **Larger boxes** = higher level components. **Colors** show health status. Click to zoom in.")
        
        fig = create_treemap_visualization(is_dark, plant_id)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        df_plant = df_raw[df_raw['plant_id'] == plant_id]
        healthy_count = len(df_plant[df_plant['health_score'] >= 85])
        warning_count = len(df_plant[(df_plant['health_score'] >= 70) & (df_plant['health_score'] < 85)])
        critical_count = len(df_plant[df_plant['health_score'] < 70])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🟢 Healthy Assets", healthy_count, "85-100% Health")
        with col2:
            st.metric("🟠 Warning Assets", warning_count, "70-84% Health")
        with col3:
            st.metric("🔴 Critical Assets", critical_count, "Below 70% Health")
    
    else:
        st.markdown("### Network Topology - How Systems Connect")
        st.info("🔗 This shows the **relationships** between different parts of your mining operation.")
        
        fig = create_network_diagram(is_dark)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        st.markdown("#### 🎯 Node Colors in Network")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("🔵 **Blue** = Site/Sub-Plant")
        with col2:
            st.markdown("🟢 **Green** = Healthy Equipment")
        with col3:
            st.markdown("🟠 **Amber** = Warning Equipment")
        with col4:
            st.markdown("🔴 **Red** = Critical Equipment")
    
    st.markdown("---")
    st.markdown("### 📖 How to Use This Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### For Plant Managers
        - **Monitor** the overall health at Mine Site level
        - **Identify** which Sub-Plants need attention
        - **Plan** resources based on maintenance priorities
        - **Track** improvement over time
        """)
    
    with col2:
        st.markdown("""
        #### For Maintenance Teams
        - **Drill down** to specific equipment issues
        - **Review** sensor readings for components
        - **Prioritize** work based on health scores
        - **Execute** maintenance before failures occur
        """)
    
    st.markdown("---")
    st.markdown("### 🔄 Complete Monitoring Workflow")
    
    st.code("""
    STEP 1: Sensors collect real-time data (Vibration, Temperature, Pressure)
           ↓
    STEP 2: Data is analyzed to calculate Health Score (0-100%)
           ↓
    STEP 3: AI system categorizes equipment condition:
           • 85-100% = 🟢 Healthy (Proactive Monitoring)
           • 70-84%  = 🟠 Warning (Preventive Maintenance)
           • 0-69%   = 🔴 Critical (Predictive Maintenance)
           ↓
    STEP 4: Maintenance recommendations are generated
           ↓
    STEP 5: Alerts are sent to relevant teams
           ↓
    STEP 6: Actions are tracked in Operations Control Panel
    """, language="text")
    
    st.markdown("---")
    st.markdown("### 🎮 Try It Yourself")
    
    st.markdown("**Select a component to see its full hierarchy path:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_subplant = st.selectbox(
            "Sub-Plant",
            list(PLANT_STRUCTURE.keys()),
            key="hier_subplant"
        )
    
    with col2:
        selected_equipment = st.selectbox(
            "Equipment",
            list(PLANT_STRUCTURE[selected_subplant].keys()),
            key="hier_equipment"
        )
    
    with col3:
        selected_component = st.selectbox(
            "Component",
            PLANT_STRUCTURE[selected_subplant][selected_equipment],
            key="hier_component"
        )
    
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
    """Render overview tab content"""
    st.subheader("🏭 Overall Plant Health")
    
    df_plant = df_raw[df_raw['plant_id'] == selected_plant].copy()
    
    sub_scores = {}
    for sp in PLANT_STRUCTURE.keys():
        sp_data = df_plant[df_plant['sub_plant'] == sp]
        if not sp_data.empty:
            sub_scores[sp] = int(sp_data['health_score'].mean())
        else:
            sub_scores[sp] = 85
    
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
        st.plotly_chart(
            create_donut_chart(plant_health, "Overall Plant Health", theme_colors),
            use_container_width=True,
            config={'displayModeBar': False}
        )
    
    with d2:
        st.plotly_chart(
            create_donut_chart(
                max(30, 100 - len(critical_issues) * 10),
                "Risk Buffer",
                theme_colors
            ),
            use_container_width=True,
            config={'displayModeBar': False}
        )
    
    with d3:
        st.plotly_chart(
            create_donut_chart(
                max(40, 100 - len(open_issues) * 5),
                "Operational Stability",
                theme_colors
            ),
            use_container_width=True,
            config={'displayModeBar': False}
        )
    
    df_sub = pd.DataFrame({
        "Sub-Plant": sub_scores.keys(),
        "Health (%)": sub_scores.values()
    })
    
    st.plotly_chart(
        create_bar_chart(df_sub, "Sub-Plant", "Health (%)", "Sub-Plant Health"),
        use_container_width=True,
        config={'displayModeBar': False}
    )
    
    st.markdown("### 🏗️ Sub-Plant → Components")
    selected_subplant = st.selectbox(
        "Select Sub-Plant",
        list(PLANT_STRUCTURE.keys()),
        key="subplant_drilldown"
    )
    
    rows = []
    for eq, comps in PLANT_STRUCTURE[selected_subplant].items():
        for comp in comps:
            score = get_health_score(selected_plant, selected_subplant, eq, comp)
            rows.append({
                "Equipment": eq,
                "Component": comp,
                "Health (%)": score,
                "Status": status(score)
            })
    
    df_comp = pd.DataFrame(rows)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)
    
    st.markdown("### 🔩 Component → Sensors")
    selected_component = st.selectbox(
        "Select Component",
        df_comp["Component"].unique(),
        key="component_select"
    )
    
    sensor_rows = []
    comp_data = df_plant[
        (df_plant['sub_plant'] == selected_subplant) &
        (df_plant['component'] == selected_component)
    ]
    
    if not comp_data.empty:
        for _, row in comp_data.iterrows():
            sensor_rows.append({
                "Sensor": row['sensor_type'],
                "Health (%)": int(row['health_score']),
                "Status": status(int(row['health_score']))
            })
    
    if sensor_rows:
        st.dataframe(pd.DataFrame(sensor_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No sensor data available for this component")
    
    st.markdown("### ⚠️ Top Risk Areas (Quick View)")
    
    if open_issues:
        st.dataframe(
            pd.DataFrame(open_issues)[
                ["Sub-Plant", "Equipment", "Component", "Severity", "Action Type", "Due"]
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ No high-risk areas identified")
    
    st.markdown("### 🏭 Mining Operations Snapshot")
    
    try:
        st.image(
            "images/img1.jpg",
            caption="Mining plant operations monitored through real-time systems",
            use_container_width=True
        )
    except:
        st.info("📷 Operations image not available - Add 'img1.jpg' to your project directory")

def render_alerts_tab(selected_plant: str, to_date: date) -> None:
    """Render alerts tab content"""
    st.subheader("🚨 Plant → Sub-Plant → Component → Sensor Alerts")
    
    df_alerts = df_raw[
        (df_raw['plant_id'] == selected_plant) &
        (df_raw['health_score'] < 75)
    ].copy()
    
    if not df_alerts.empty:
        alert_display = df_alerts[[
            'plant_id', 'sub_plant', 'equipment', 'component', 
            'sensor_type', 'status', 'maintenance_type', 'action_required'
        ]].copy()
        
        alert_display.columns = [
            'Plant', 'Sub-Plant', 'Equipment', 'Component',
            'Sensor', 'Severity', 'Maintenance', 'Action'
        ]
        
        alert_display['Severity'] = alert_display['Severity'].apply(
            lambda x: f"🟢 {x}" if x == 'Healthy' else f"🟠 {x}" if x == 'Warning' else f"🔴 {x}"
        )
        
        st.dataframe(alert_display, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No active alerts")



def render_maintenance_tab(selected_plant: str, to_date: date) -> None:
    """Render maintenance tab content"""
    st.subheader("🛠️ Maintenance Planning (Industry View)")
    
    df_maint = df_raw[df_raw['plant_id'] == selected_plant].copy()
    
    if not df_maint.empty:
        maint_display = df_maint[[
            'sub_plant', 'equipment', 'component', 'health_score',
            'maintenance_type', 'priority', 'due_date'
        ]].copy()
        
        maint_display.columns = [
            'Sub-Plant', 'Equipment', 'Component', 'Health (%)',
            'Maintenance Type', 'Priority', 'Planned Date'
        ]
        
        maint_display['Planned Date'] = pd.to_datetime(maint_display['Planned Date']).dt.date
        
        st.dataframe(maint_display, use_container_width=True, hide_index=True)
        
        maint_counts = df_maint['maintenance_type'].value_counts()
        maint_df = pd.DataFrame({
            'Maintenance Type': maint_counts.index,
            'Count': maint_counts.values
        })
        
        st.plotly_chart(
            create_pie_chart(maint_df, "Maintenance Type", "Maintenance Strategy Distribution"),
            use_container_width=True,
            config={'displayModeBar': False}
        )
    else:
        st.info("No maintenance data available for this plant")
    
    st.success(
        "📌 Predictive maintenance should be prioritized for LOW health assets to "
        "avoid unplanned downtime."
    )

# =====================================================
# RUN APPLICATION
# =====================================================
if __name__ == "__main__":
    main()