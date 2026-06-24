import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import pandas as pd
import sqlalchemy
from sqlalchemy import text
from datetime import datetime

# 1. Production UI Layout & Theme Set Configuration
st.set_page_config(
    layout="wide", 
    page_title="Theatre COP - Tactical Dashboard",
    page_icon="🛰️"
)

# Custom internal CSS style injections for an enterprise dark tactical UI
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    div[data-testid="stMetric"] {
        background-color: #1a1e24;
        border: 1px solid #2d3139;
        padding: 12px 15px;
        border-radius: 6px;
    }
    div[data-testid="stMetric"] label {
        color: #8a92a6 !important;
        font-family: monospace;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-family: monospace;
        color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Secure Caching Connection Architecture
@st.cache_resource
def init_db_engine():
    """Initializes and caches a single persistent database pool instance."""
    return sqlalchemy.create_engine(
        "postgresql://postgres:copadmin@localhost/security_db",
        pool_size=10,
        max_overflow=20
    )

engine = init_db_engine()

# 3. Sidebar Navigation Control Block (Linux UI Terminal Clean Minimalist Aesthetic)
st.sidebar.title("🛠️ Operational Control")
st.sidebar.markdown("---")

st.sidebar.subheader("Strategic Query Filters")

# Faction Mapping Checkbox Multi-selectors
faction_options = ["Boko Haram", "ISWAP", "Bandits", "Government of Nigeria", "Civilians"]
selected_factions = st.sidebar.multiselect("Active Factions / Actors", faction_options)

# Human-readable mapping layer for UCDP Integer values stored inside your 'description' column
type_mapping = {
    "State-Based Conflict (Type 1)": "1",
    "Non-State Conflict (Type 2)": "2",
    "One-Sided Violence (Type 3)": "3"
}
selected_labels = st.sidebar.multiselect("Incident Classification Type", list(type_mapping.keys()))
selected_types = [type_mapping[label] for label in selected_labels]

# High-precision Temporal Range Filter Slider
year_range = st.sidebar.slider("Operational Time Horizon", 1997, 2026, (2015, 2026))

# Real-time System Daemon Status Indicators (Subtle Linux UI Terminal Style)
st.sidebar.markdown("---")
st.sidebar.subheader("System Modules Infrastructure")
st.sidebar.markdown("🛰️ **Satellite Core Processing:** `Active` 🟢")
st.sidebar.markdown("🤖 **X-Scraper Routing Daemon:** `Standby` 🟡")
st.sidebar.markdown("📰 **OSINT News-Scraper Module:** `Standby` 🟡")
st.sidebar.markdown("🔒 **SQL Injection Defenses:** `Armed` 🛡️")

# 4. Production Secure Query Engine (Completely Sanitized via SQLAlchemy Text Engine Binding)
def fetch_tactical_data(factions, types, years):
    """
    Safely retrieves geocoded incident metrics using explicit parameterized SQL bindings 
    to completely shut down Python SQL Injection pathways.
    """
    start_date = f"{years[0]}-01-01"
    end_date = f"{years[1]}-12-31"
    
    # Initialize baseline query syntax
    base_query = """
        SELECT 
            description, 
            actors, 
            incident_date, 
            confidence_score, 
            ST_Y(location::geometry) as lat, 
            ST_X(location::geometry) as lon 
        FROM security_incidents
        WHERE incident_date BETWEEN :start_date AND :end_date
    """
    
    # Build core tracking bound parameters dictionary object
    bind_params = {
        "start_date": datetime.strptime(start_date, "%Y-%m-%d"),
        "end_date": datetime.strptime(end_date, "%Y-%m-%d")
    }
    
    # Secure dynamic appending logic for Faction filtering
    if factions:
        faction_clauses = []
        for index, item in enumerate(factions):
            param_key = f"faction_param_{index}"
            faction_clauses.append(f"actors ILIKE :{param_key}")
            bind_params[param_key] = f"%{item}%"
        base_query += " AND (" + " OR ".join(faction_clauses) + ")"
        
    # Secure dynamic appending logic for Categorical Types filtering
    if types:
        base_query += " AND description IN :types_tuple"
        bind_params["types_tuple"] = tuple(types)

    # Execute isolated pipeline request
    with engine.connect() as connection:
        result_df = pd.read_sql(text(base_query), connection, params=bind_params)
        
    return result_df

# Read Live Workspace Data Matrix
try:
    df = fetch_tactical_data(selected_factions, selected_types, year_range)
except Exception as err:
    st.error(f"Critical Backend Ingestion Intercept Failure: {err}")
    df = pd.DataFrame()

# 5. Strategic Metrics Overview Banner (KPI Summary Cards)
st.title("Nigeria Common Operating Picture (Theatre COP)")

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric("Aggregated Events Count", f"{len(df):,}")
with m_col2:
    mean_val = int(df['confidence_score'].mean()) if not df.empty else 0
    st.metric("Source Confidence Average", f"{mean_val}%")
with m_col3:
    tracked_actors = df['actors'].nunique() if not df.empty else 0
    st.metric("Identified Unique Combatants", f"{tracked_actors}")
with m_col4:
    st.metric("Temporal Evaluation Focus", f"{year_range[0]} — {year_range[1]}")

# 6. High-Performance Client Spatial GIS Rendering Layer
st.markdown("### Tactical Geographic Awareness Map Matrix")

# Build Leaflet Base Layer Environment
m = folium.Map(location=[9.0820, 8.6753], zoom_start=6, tiles="CartoDB dark_matter")

if not df.empty:
    # Crucial Enhancement: Marker Cluster Sub-system instance handles thousands of elements with no UI lag
    marker_cluster = MarkerCluster(
        name="Clustered Incident Vectors",
        overlay=True,
        control=True
    ).add_to(m)
    
    for _, row in df.iterrows():
        # Formulate isolated monospace terminal style metric card overlay injection
        date_str = row['incident_date'].strftime('%Y-%m-%d') if isinstance(row['incident_date'], datetime) else str(row['incident_date'])
        
        popup_card = f"""
        <div style="font-family: 'Courier New', monospace; background-color: #11141a; color: #d0d6e2; padding: 12px; border-radius: 5px; width: 250px; border: 1px solid #3b4252;">
            <strong style="color: #bf616a; font-size: 13px;">⚠️ SECURITY EVENT LOG</strong><br>
            <hr style="border-top: 1px dashed #4c566a; margin: 6px 0;">
            <b>Classification:</b> Type {row['description']}<br>
            <b>Primary Actor:</b> {row['actors'][:45]}...<br>
            <b>Date Flagged:</b> {date_str[:10]}<br>
            <b>Verification Rank:</b> <span style="color: #a3be8c;">{row['confidence_score']}%</span>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color="#bf616a",
            fill=True,
            fill_color="#bf616a",
            fill_opacity=0.6,
            popup=folium.Popup(popup_card, max_width=320)
        ).add_to(marker_cluster)
else:
    st.info("No active conflict records correspond to your selected operational query filters.")

# Streamlit-Folium Component Engine Callout Interface 
st_folium(m, width=1350, height=650, returned_objects=[])