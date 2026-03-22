import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="IPL 2025 Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CSS ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Barlow+Condensed:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:        #08090d;
    --surface:   #0e1018;
    --card:      #13161f;
    --card2:     #191d28;
    --border:    #1f2535;
    --border2:   #2a3348;
    --gold:      #f5c842;
    --gold2:     #e8a020;
    --green:     #00d97e;
    --blue:      #1e9fff;
    --red:       #ff4560;
    --orange:    #ff7d1a;
    --text:      #e8eaf2;
    --muted:     #4a5470;
    --muted2:    #6b7899;
    --radius:    12px;
    --radius-sm: 7px;
}

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container { padding: 0 2rem 5rem !important; max-width: 1400px; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.1rem 2rem !important; }

.sb-logo {
    display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.15rem;
}
.sb-logo-badge {
    width: 38px; height: 38px; border-radius: 9px; flex-shrink: 0;
    background: linear-gradient(135deg, var(--gold), var(--gold2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 0 18px rgba(245,200,66,0.35);
    animation: badge-pulse 3s ease-in-out infinite;
}
@keyframes badge-pulse {
    0%,100% { box-shadow: 0 0 14px rgba(245,200,66,0.3); }
    50%      { box-shadow: 0 0 28px rgba(245,200,66,0.55); }
}
.sb-logo-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.6rem; font-weight: 800; letter-spacing: 2px;
    background: linear-gradient(90deg, var(--gold), var(--orange));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1;
}
.sb-logo-sub {
    font-size: 0.68rem; color: var(--muted2); letter-spacing: 1px;
    margin-bottom: 1.6rem; padding-left: 46px; text-transform: uppercase;
}
.sb-section {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--muted); margin: 1.1rem 0 0.55rem;
    display: flex; align-items: center; gap: 7px;
}
.sb-section::after { content:''; flex:1; height:1px; background:var(--border); }

/* Multiselect / text input */
div[data-testid="stMultiSelect"] > div,
div[data-testid="stTextInput"] input {
    background: #0b0d14 !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(245,200,66,0.4) !important;
    box-shadow: 0 0 0 3px rgba(245,200,66,0.07) !important;
}

/* Download button */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, var(--gold), var(--gold2)) !important;
    color: #08090d !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important; font-weight: 700 !important; letter-spacing: 1.5px !important;
    border: none !important; border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.5rem !important; width: 100% !important;
    box-shadow: 0 4px 20px rgba(245,200,66,0.2) !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(245,200,66,0.35) !important;
}

/* Sidebar pills */
.sb-pill-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.sb-pill {
    font-size: 0.66rem; font-weight: 600; padding: 2px 9px;
    border-radius: 99px; letter-spacing: 0.3px;
}
.sp-gold   { background: rgba(245,200,66,0.1); color: var(--gold);  border: 1px solid rgba(245,200,66,0.2); }
.sp-green  { background: rgba(0,217,126,0.1);  color: var(--green); border: 1px solid rgba(0,217,126,0.2); }
.sp-blue   { background: rgba(30,159,255,0.1); color: var(--blue);  border: 1px solid rgba(30,159,255,0.2); }
.sp-red    { background: rgba(255,69,96,0.1);  color: var(--red);   border: 1px solid rgba(255,69,96,0.2); }

/* ── HERO ── */
.hero {
    position: relative; overflow: hidden;
    background: linear-gradient(160deg, #0d1220 0%, #0a0f18 40%, #0c1008 100%);
    border-bottom: 1px solid var(--border);
    padding: 3rem 3rem 2.6rem;
    margin: 0 -2rem 2.5rem;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background-image:
        radial-gradient(ellipse 600px 300px at 80% 50%, rgba(245,200,66,0.06) 0%, transparent 70%),
        radial-gradient(ellipse 400px 400px at 10% 80%, rgba(0,217,126,0.05) 0%, transparent 65%);
    animation: hero-breathe 8s ease-in-out infinite;
}
@keyframes hero-breathe {
    0%,100% { opacity: 0.8; }
    50%      { opacity: 1.2; }
}
/* Pitch lines */
.hero::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: repeating-linear-gradient(
        90deg,
        rgba(245,200,66,0.025) 0px,
        rgba(245,200,66,0.025) 1px,
        transparent 1px,
        transparent 80px
    );
}
.hero-inner { position: relative; z-index: 2; }
.hero-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(245,200,66,0.09); border: 1px solid rgba(245,200,66,0.2);
    border-radius: 99px; padding: 4px 14px 4px 8px;
    font-size: 0.7rem; font-weight: 700; color: var(--gold); letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 1rem;
    animation: fade-up 0.5s ease both;
}
.hero-chip-dot {
    width: 6px; height: 6px; border-radius: 50%; background: var(--gold);
    animation: blink 1.5s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }
.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 5rem; font-weight: 800; letter-spacing: 3px;
    line-height: 0.88; margin: 0 0 0.9rem;
    animation: fade-up 0.6s 0.05s ease both;
}
.ht-white {
    display: block;
    background: linear-gradient(90deg, #fff 0%, #cdd8f0 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.ht-gold {
    display: block;
    background: linear-gradient(90deg, var(--gold) 0%, var(--orange) 80%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub {
    font-size: 1rem; color: var(--muted2); line-height: 1.6;
    max-width: 480px; margin: 0 0 1.8rem;
    animation: fade-up 0.6s 0.1s ease both;
}
.hero-sub strong { color: var(--text); }
.hero-tags { display: flex; gap: 0.6rem; flex-wrap: wrap; animation: fade-up 0.6s 0.15s ease both; }
.hero-tag {
    padding: 4px 13px; border-radius: 6px; font-size: 0.78rem;
    font-weight: 600; border: 1px solid; letter-spacing: 0.3px;
    transition: transform 0.2s;
}
.hero-tag:hover { transform: translateY(-2px); }
.ht-gold-tag   { color: var(--gold);  background: rgba(245,200,66,0.08); border-color: rgba(245,200,66,0.22); }
.ht-green-tag  { color: var(--green); background: rgba(0,217,126,0.08);  border-color: rgba(0,217,126,0.22); }
.ht-blue-tag   { color: var(--blue);  background: rgba(30,159,255,0.08); border-color: rgba(30,159,255,0.22); }
.ht-red-tag    { color: var(--red);   background: rgba(255,69,96,0.08);  border-color: rgba(255,69,96,0.22); }

@keyframes fade-up {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1rem; margin-bottom: 2.2rem;
}
.kpi-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 1.25rem 1.4rem;
    position: relative; overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
    animation: fade-up 0.5s ease both;
}
.kpi-card:hover { transform: translateY(-3px); border-color: var(--border2); }
.kpi-card::before {
    content: ''; position: absolute; inset: 0; opacity: 0.035;
    background: var(--kpi-color, var(--gold));
}
.kpi-card::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--kpi-color, var(--gold)), transparent);
}
.kpi-icon { font-size: 1.4rem; margin-bottom: 0.55rem; display: block; }
.kpi-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.4rem; font-weight: 700; letter-spacing: 1px; line-height: 1;
    color: var(--kpi-color, var(--gold)); margin-bottom: 0.2rem;
}
.kpi-lbl {
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1.5px; color: var(--muted2);
}

/* ── SECTION HEADER ── */
.sec-hdr {
    display: flex; align-items: center; gap: 0.7rem;
    margin-bottom: 1rem;
}
.sec-hdr-line { flex: 1; height: 1px; background: var(--border); }
.sec-hdr-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: var(--text);
}
.sec-hdr-dot {
    width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.dot-gold   { background: var(--gold);  box-shadow: 0 0 8px var(--gold); }
.dot-green  { background: var(--green); box-shadow: 0 0 8px var(--green); }
.dot-blue   { background: var(--blue);  box-shadow: 0 0 8px var(--blue); }
.dot-red    { background: var(--red);   box-shadow: 0 0 8px var(--red); }
.dot-orange { background: var(--orange);box-shadow: 0 0 8px var(--orange); }

/* ── PLAYER STAT CARD ── */
.player-stat-grid {
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem; margin: 1rem 0 1.2rem;
}
.pstat {
    background: var(--card2); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 0.9rem 1rem;
    text-align: center; transition: border-color 0.2s;
}
.pstat:hover { border-color: var(--border2); }
.pstat-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.8rem; font-weight: 700; letter-spacing: 1px; line-height: 1;
    margin-bottom: 0.2rem;
}
.pstat-lbl { font-size: 0.68rem; color: var(--muted2); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }

/* ── CHART WRAPPER ── */
.chart-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 1.4rem 1.4rem 0.8rem;
    margin-bottom: 1.5rem;
}

/* ── DATA TABLE ── */
div[data-testid="stDataFrame"] {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}

/* ── TABS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--card) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
    gap: 0 !important; padding: 4px !important;
    margin-bottom: 1.2rem !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 6px !important;
    color: var(--muted2) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important; font-weight: 600 !important; letter-spacing: 1px !important;
    padding: 0.4rem 1.2rem !important; border: none !important;
    transition: all 0.2s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, var(--gold), var(--gold2)) !important;
    color: #08090d !important;
}

/* ── EXPANDER ── */
details { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important; }
summary { color: var(--muted2) !important; font-size: 0.85rem !important; font-weight: 600 !important; }

/* ── MISC ── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stRadio"] label { font-size: 0.9rem !important; color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
@st.cache_data
def load_data():
    return pd.read_csv("ipl_2025_deliveries.csv")

try:
    df = load_data()
    data_loaded = True
except FileNotFoundError:
    st.error("⚠️  `ipl_2025_deliveries.csv` not found. Please place it in the same folder as this script.")
    st.stop()

# ================== CHART HELPERS ==================
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Rajdhani', color='#e8eaf2'),
    margin=dict(l=10, r=10, t=40, b=10),
    height=340,
)

def hex_to_rgba(hex_color, alpha):
    """Convert #rrggbb to rgba(r,g,b,alpha) string — works with all Plotly versions."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

def bar_chart(x, y, title, color, orientation='v'):
    color_dim  = hex_to_rgba(color, 0.2)   # dim shade for low values
    color_full = hex_to_rgba(color, 1.0)   # full shade for high values

    if orientation == 'h':
        fig = go.Figure(go.Bar(
            x=y, y=x, orientation='h',
            marker=dict(
                color=y,
                colorscale=[[0, color_dim], [1, color_full]],
                line=dict(width=0),
            ),
            text=[f"{int(v)}" for v in y],
            textposition='outside',
            textfont=dict(size=11, color='#e8eaf2', family='JetBrains Mono'),
        ))
        fig.update_layout(
            **CHART_LAYOUT,
            title=dict(text=title, font=dict(size=13, color='#4a5470'), x=0),
            xaxis=dict(showgrid=True, gridcolor='#1f2535', color='#4a5470', tickfont=dict(size=10)),
            yaxis=dict(showgrid=False, color='#e8eaf2', tickfont=dict(size=11, family='Rajdhani')),
        )
    else:
        fig = go.Figure(go.Bar(
            x=x, y=y, orientation='v',
            marker=dict(
                color=y,
                colorscale=[[0, color_dim], [1, color_full]],
                line=dict(width=0),
            ),
            text=[f"{int(v)}" for v in y],
            textposition='outside',
            textfont=dict(size=10, color='#e8eaf2', family='JetBrains Mono'),
        ))
        fig.update_layout(
            **CHART_LAYOUT,
            title=dict(text=title, font=dict(size=13, color='#4a5470'), x=0),
            xaxis=dict(showgrid=False, color='#e8eaf2', tickangle=-35, tickfont=dict(size=10, family='Rajdhani')),
            yaxis=dict(showgrid=True, gridcolor='#1f2535', color='#4a5470'),
        )
    return fig

def donut_chart(labels, values, title, colors):
    donut_layout = {**CHART_LAYOUT, 'height': 320}
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color='#08090d', width=2)),
        textinfo='label+percent',
        textfont=dict(size=11, family='Rajdhani'),
        hovertemplate='<b>%{label}</b><br>%{value:,}<extra></extra>',
    ))
    fig.update_layout(
        **donut_layout,
        title=dict(text=title, font=dict(size=13, color='#4a5470'), x=0),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
    )
    return fig

def line_chart(x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines+markers',
        line=dict(color=color, width=2.5),
        marker=dict(size=5, color=color, line=dict(width=1.5, color='#08090d')),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)',
        hovertemplate='Over %{x}<br>Runs: %{y}<extra></extra>',
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=13, color='#4a5470'), x=0),
        xaxis=dict(showgrid=True, gridcolor='#1f2535', color='#4a5470'),
        yaxis=dict(showgrid=True, gridcolor='#1f2535', color='#4a5470'),
    )
    return fig

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-badge">🏏</div>
        <div class="sb-logo-title">IPL 2025</div>
    </div>
    <div class="sb-logo-sub">Deliveries Analytics Dashboard</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Filters</div>', unsafe_allow_html=True)
    selected_teams = st.multiselect(
        "Batting Team", df["batting_team"].unique(),
        default=list(df["batting_team"].unique()), label_visibility="collapsed",
        placeholder="All Batting Teams"
    )
    selected_bowling = st.multiselect(
        "Bowling Team", df["bowling_team"].unique(),
        default=list(df["bowling_team"].unique()), label_visibility="collapsed",
        placeholder="All Bowling Teams"
    )
    selected_innings = st.multiselect(
        "Innings", df["innings"].unique(),
        default=list(df["innings"].unique()), label_visibility="collapsed",
        placeholder="All Innings"
    )

    st.markdown('<div class="sb-section">Player Lookup</div>', unsafe_allow_html=True)
    search_batter = st.text_input("🏏 Batter name", placeholder="e.g. Virat Kohli")
    search_bowler = st.text_input("🎯 Bowler name", placeholder="e.g. Bumrah")

    st.markdown('<div class="sb-section">Export</div>', unsafe_allow_html=True)
    filtered_df_for_export = df[
        (df["batting_team"].isin(selected_teams)) &
        (df["bowling_team"].isin(selected_bowling)) &
        (df["innings"].isin(selected_innings))
    ]
    st.download_button(
        "📥 DOWNLOAD FILTERED CSV",
        data=filtered_df_for_export.to_csv(index=False),
        file_name="ipl_2025_filtered.csv",
        mime="text/csv",
    )

    st.markdown('<div class="sb-section">Stats</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-pill-row">
        <span class="sb-pill sp-gold">🏟️ IPL 2025</span>
        <span class="sb-pill sp-green">⚡ Live Data</span>
        <span class="sb-pill sp-blue">📊 Plotly</span>
        <span class="sb-pill sp-red">🔥 Interactive</span>
    </div>
    """, unsafe_allow_html=True)

# ================== FILTERED DATA ==================
fdf = df[
    (df["batting_team"].isin(selected_teams)) &
    (df["bowling_team"].isin(selected_bowling)) &
    (df["innings"].isin(selected_innings))
]

# ================== HERO ==================
total_matches = df["match_id"].nunique()
total_runs    = fdf["runs_of_bat"].sum() + fdf["extras"].sum()
total_wickets = fdf["player_dismissed"].notna().sum()
total_sixes   = len(fdf[fdf["runs_of_bat"] == 6])

st.markdown(f"""
<div class="hero">
    <div class="hero-inner">
        <div class="hero-chip">
            <span class="hero-chip-dot"></span>
            Season 2025 · Ball-by-Ball Analytics
        </div>
        <div class="hero-title">
            <span class="ht-white">IPL 2025</span>
            <span class="ht-gold">DASHBOARD</span>
        </div>
        <p class="hero-sub">
            Complete ball-by-ball breakdown of <strong>IPL 2025</strong>.
            Explore batting, bowling, venues and player performances.
        </p>
        <div class="hero-tags">
            <span class="hero-tag ht-gold-tag">🏏 Batting Stats</span>
            <span class="hero-tag ht-green-tag">🎯 Bowling Analysis</span>
            <span class="hero-tag ht-blue-tag">📍 Venue Insights</span>
            <span class="hero-tag ht-red-tag">👤 Player Lookup</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================== KPI CARDS ==================
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card" style="--kpi-color: var(--gold);">
        <span class="kpi-icon">🏟️</span>
        <div class="kpi-val">{total_matches}</div>
        <div class="kpi-lbl">Matches Played</div>
    </div>
    <div class="kpi-card" style="--kpi-color: var(--green);">
        <span class="kpi-icon">🏏</span>
        <div class="kpi-val">{total_runs:,}</div>
        <div class="kpi-lbl">Total Runs</div>
    </div>
    <div class="kpi-card" style="--kpi-color: var(--red);">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-val">{total_wickets}</div>
        <div class="kpi-lbl">Wickets Taken</div>
    </div>
    <div class="kpi-card" style="--kpi-color: var(--orange);">
        <span class="kpi-icon">💥</span>
        <div class="kpi-val">{total_sixes}</div>
        <div class="kpi-lbl">Sixes Hit</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================== PLAYER LOOKUP ==================
if search_batter:
    pdata = df[df["striker"].str.contains(search_batter, case=False, na=False)]
    if not pdata.empty:
        t_runs  = pdata["runs_of_bat"].sum()
        t_balls = len(pdata)
        t_fours = len(pdata[pdata["runs_of_bat"] == 4])
        t_sixes = len(pdata[pdata["runs_of_bat"] == 6])
        sr      = round((t_runs / t_balls) * 100, 2) if t_balls else 0
        dism    = df[df["player_dismissed"].str.lower() == search_batter.lower()].shape[0] if "player_dismissed" in df.columns else 0
        avg     = round(t_runs / dism, 2) if dism else "—"

        st.markdown(f"""
        <div class="sec-hdr" style="margin-top:0.5rem;">
            <span class="sec-hdr-dot dot-gold"></span>
            <span class="sec-hdr-title">🏏 Batter — {search_batter.title()}</span>
            <div class="sec-hdr-line"></div>
        </div>
        <div class="player-stat-grid">
            <div class="pstat"><div class="pstat-val" style="color:var(--gold);">{t_runs}</div><div class="pstat-lbl">Runs</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--blue);">{t_balls}</div><div class="pstat-lbl">Balls</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--green);">{t_fours}</div><div class="pstat-lbl">Fours</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--orange);">{t_sixes}</div><div class="pstat-lbl">Sixes</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--red);">{sr}</div><div class="pstat-lbl">Strike Rate</div></div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 View ball-by-ball data"):
            st.dataframe(pdata, use_container_width=True, hide_index=True)
    else:
        st.warning(f"No batter found matching '{search_batter}'.")

if search_bowler:
    bdata = df[df["bowler"].str.contains(search_bowler, case=False, na=False)]
    if not bdata.empty:
        t_balls   = len(bdata)
        t_runs_c  = (bdata["runs_of_bat"] + bdata["extras"] - bdata["byes"] - bdata["legbyes"]).sum()
        t_wkts    = bdata["player_dismissed"].notna().sum()
        overs     = t_balls // 6 + (t_balls % 6) / 6
        econ      = round(t_runs_c / overs, 2) if overs else 0
        sr_bowl   = round(t_balls / t_wkts, 2) if t_wkts else "—"

        st.markdown(f"""
        <div class="sec-hdr" style="margin-top:0.5rem;">
            <span class="sec-hdr-dot dot-red"></span>
            <span class="sec-hdr-title">🎯 Bowler — {search_bowler.title()}</span>
            <div class="sec-hdr-line"></div>
        </div>
        <div class="player-stat-grid">
            <div class="pstat"><div class="pstat-val" style="color:var(--red);">{t_wkts}</div><div class="pstat-lbl">Wickets</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--blue);">{t_balls}</div><div class="pstat-lbl">Balls</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--orange);">{t_runs_c}</div><div class="pstat-lbl">Runs Given</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--green);">{econ}</div><div class="pstat-lbl">Economy</div></div>
            <div class="pstat"><div class="pstat-val" style="color:var(--gold);">{sr_bowl}</div><div class="pstat-lbl">Strike Rate</div></div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 View ball-by-ball data"):
            st.dataframe(bdata, use_container_width=True, hide_index=True)
    else:
        st.warning(f"No bowler found matching '{search_bowler}'.")

# ================== MAIN TABS ==================
tab1, tab2, tab3, tab4 = st.tabs(["🏏  BATTING", "🎯  BOWLING", "📊  RUNS BREAKDOWN", "📍  VENUES"])

# ── TAB 1: BATTING ──
with tab1:
    st.markdown("""
    <div class="sec-hdr">
        <span class="sec-hdr-dot dot-gold"></span>
        <span class="sec-hdr-title">Top Run Scorers</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    top_batters = fdf.groupby("striker")["runs_of_bat"].sum().sort_values(ascending=False).head(10)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = bar_chart(top_batters.index.tolist(), top_batters.values.tolist(),
                        "Top 10 Batters by Runs", "#f5c842")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig2 = donut_chart(
            top_batters.index.tolist()[:5],
            top_batters.values.tolist()[:5],
            "Top 5 Share of Runs",
            ["#f5c842", "#ff7d1a", "#00d97e", "#1e9fff", "#ff4560"]
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Boundary breakdown
    st.markdown("""
    <div class="sec-hdr" style="margin-top:0.5rem;">
        <span class="sec-hdr-dot dot-green"></span>
        <span class="sec-hdr-title">Boundary Hitters</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    top_fours = fdf[fdf["runs_of_bat"] == 4].groupby("striker").size().sort_values(ascending=False).head(8)
    top_sixes = fdf[fdf["runs_of_bat"] == 6].groupby("striker").size().sort_values(ascending=False).head(8)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig3 = bar_chart(top_fours.index.tolist(), top_fours.values.tolist(),
                         "Most Fours", "#1e9fff", orientation='h')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig4 = bar_chart(top_sixes.index.tolist(), top_sixes.values.tolist(),
                         "Most Sixes 💥", "#ff7d1a", orientation='h')
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 2: BOWLING ──
with tab2:
    st.markdown("""
    <div class="sec-hdr">
        <span class="sec-hdr-dot dot-red"></span>
        <span class="sec-hdr-title">Top Wicket Takers</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    wicket_df = fdf[fdf["player_dismissed"].notna()]
    top_bowlers = wicket_df.groupby("bowler")["player_dismissed"].count().sort_values(ascending=False).head(10)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = bar_chart(top_bowlers.index.tolist(), top_bowlers.values.tolist(),
                        "Top 10 Bowlers by Wickets", "#ff4560")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig2 = donut_chart(
            top_bowlers.index.tolist()[:5],
            top_bowlers.values.tolist()[:5],
            "Top 5 Wicket Share",
            ["#ff4560", "#ff7d1a", "#f5c842", "#00d97e", "#1e9fff"]
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Economy leaders
    st.markdown("""
    <div class="sec-hdr" style="margin-top:0.5rem;">
        <span class="sec-hdr-dot dot-blue"></span>
        <span class="sec-hdr-title">Economy Rate Leaders (min 30 balls)</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    bowler_balls  = fdf.groupby("bowler").size()
    bowler_runs   = (fdf["runs_of_bat"] + fdf["extras"] - fdf["byes"] - fdf["legbyes"]).groupby(fdf["bowler"]).sum()
    econ_df       = pd.DataFrame({"balls": bowler_balls, "runs": bowler_runs})
    econ_df       = econ_df[econ_df["balls"] >= 30].copy()
    econ_df["economy"] = (econ_df["runs"] / (econ_df["balls"] / 6)).round(2)
    best_econ     = econ_df["economy"].sort_values().head(8)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig3 = bar_chart(best_econ.index.tolist(), best_econ.values.tolist(),
                     "Best Economy Rates (lower = better)", "#00d97e", orientation='h')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 3: RUNS BREAKDOWN ──
with tab3:
    st.markdown("""
    <div class="sec-hdr">
        <span class="sec-hdr-dot dot-orange"></span>
        <span class="sec-hdr-title">Run Type Distribution</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    run_types = {
        "Bat Runs":  int(fdf["runs_of_bat"].sum()),
        "Extras":    int(fdf["extras"].sum()),
        "Wides":     int(fdf["wide"].sum()),
        "Leg Byes":  int(fdf["legbyes"].sum()),
        "Byes":      int(fdf["byes"].sum()),
        "No Balls":  int(fdf["noballs"].sum()),
    }

    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_d = donut_chart(
            list(run_types.keys()), list(run_types.values()),
            "Run Composition",
            ["#f5c842","#ff7d1a","#ff4560","#00d97e","#1e9fff","#9f5cf7"]
        )
        st.plotly_chart(fig_d, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        colors_rt = ["#f5c842","#ff7d1a","#ff4560","#00d97e","#1e9fff","#9f5cf7"]
        fig_b = go.Figure(go.Bar(
            x=list(run_types.keys()), y=list(run_types.values()),
            marker=dict(color=colors_rt, line=dict(width=0)),
            text=[f"{v:,}" for v in run_types.values()],
            textposition='outside',
            textfont=dict(size=11, color='#e8eaf2', family='JetBrains Mono'),
        ))
        fig_b.update_layout(
            **CHART_LAYOUT,
            title=dict(text="Run Types Breakdown", font=dict(size=13, color='#4a5470'), x=0),
            xaxis=dict(showgrid=False, color='#e8eaf2', tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor='#1f2535', color='#4a5470'),
        )
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Over-by-over run rate
    if "over" in fdf.columns:
        st.markdown("""
        <div class="sec-hdr" style="margin-top:0.5rem;">
            <span class="sec-hdr-dot dot-green"></span>
            <span class="sec-hdr-title">Over-by-Over Run Rate</span>
            <div class="sec-hdr-line"></div>
        </div>
        """, unsafe_allow_html=True)

        over_runs = fdf.groupby("over")["runs_of_bat"].sum()
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_l = line_chart(over_runs.index.tolist(), over_runs.values.tolist(),
                           "Total Runs per Over", "#00d97e")
        st.plotly_chart(fig_l, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Team run totals
    st.markdown("""
    <div class="sec-hdr" style="margin-top:0.5rem;">
        <span class="sec-hdr-dot dot-gold"></span>
        <span class="sec-hdr-title">Team Batting Totals</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    team_runs = fdf.groupby("batting_team")["runs_of_bat"].sum().sort_values(ascending=False)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_t = bar_chart(team_runs.index.tolist(), team_runs.values.tolist(),
                      "Total Bat Runs by Team", "#f5c842")
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 4: VENUES ──
with tab4:
    st.markdown("""
    <div class="sec-hdr">
        <span class="sec-hdr-dot dot-blue"></span>
        <span class="sec-hdr-title">Matches per Venue</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    venue_counts = df.groupby("venue")["match_id"].nunique().sort_values(ascending=False)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_v = bar_chart(venue_counts.index.tolist(), venue_counts.values.tolist(),
                      "Matches Hosted per Venue", "#1e9fff")
    st.plotly_chart(fig_v, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Runs scored per venue
    st.markdown("""
    <div class="sec-hdr" style="margin-top:0.5rem;">
        <span class="sec-hdr-dot dot-orange"></span>
        <span class="sec-hdr-title">Total Runs Scored per Venue</span>
        <div class="sec-hdr-line"></div>
    </div>
    """, unsafe_allow_html=True)

    venue_runs = df.groupby("venue")["runs_of_bat"].sum().sort_values(ascending=False)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_vr = bar_chart(venue_runs.index.tolist(), venue_runs.values.tolist(),
                           "Bat Runs per Venue", "#ff7d1a", orientation='h')
        st.plotly_chart(fig_vr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        # Average runs per match per venue
        venue_avg = (venue_runs / venue_counts).dropna().sort_values(ascending=False).head(6)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_va = donut_chart(
            venue_avg.index.tolist(),
            venue_avg.round(0).astype(int).values.tolist(),
            "Avg Runs/Match (Top 6)",
            ["#ff7d1a","#f5c842","#00d97e","#1e9fff","#ff4560","#9f5cf7"]
        )
        st.plotly_chart(fig_va, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem; border-top: 1px solid #1f2535; margin-top: 2rem;">
    <div style="font-family:'Barlow Condensed',sans-serif; font-size:1rem; letter-spacing:2px; color:#4a5470; text-transform:uppercase;">
        IPL 2025 · Ball-by-Ball Analytics Dashboard
    </div>
</div>
""", unsafe_allow_html=True)
