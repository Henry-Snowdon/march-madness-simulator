"""
Who Should I Root For? - March Madness Pool Simulator (Demo)
Run with: streamlit run dashboard_demo.py
"""

import streamlit as st
import pandas as pd
import numpy as np
# Demo version: reads from CSV files instead of SQL Server
import os
import importlib.util
import warnings
from itertools import product
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Who Should I Root For? — Elite 8",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)
# Page name for Streamlit navigation
st._config.set_option("browser.gatherUsageStats", False)

st.markdown("""
<style>
    .stApp { background-color: #0d1b2a; color: #e8eaf0; }
    .block-container { padding: 1.2rem 2rem 1rem 2rem !important; max-width: 1400px; }

    .hero-title {
        font-size: 1.85rem; font-weight: 900; color: #ffffff;
        font-family: 'Arial Black', 'Arial', sans-serif;
        text-transform: uppercase; letter-spacing: 0.02em;
        text-shadow: 2px 2px 8px rgba(0,94,184,0.8);
        margin-bottom: 0.25rem;
    }
    .hero-sub1 {
        font-size: 0.75rem; color: #4da6ff; font-weight: 700;
        letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.4rem;
    }
    .hero-subtitle {
        font-size: 0.87rem; color: #a8bdd4; line-height: 1.6;
        margin-bottom: 1rem; max-width: 880px;
    }

    [data-testid="stSidebar"] {
        background-color: #0a1628 !important;
        border-right: 2px solid #005EB8;
    }
    [data-testid="stSidebar"] label { color: #c8dff0 !important; font-size: 0.8rem; }
    [data-testid="stSidebar"] .stSelectbox > div > div { font-size: 0.82rem; }
    [data-testid="stSidebar"] p { color: #c8dff0; }
    [data-testid="stSidebar"] h3 { color: #ffffff !important; }

    .section-label {
        font-size: 0.68rem; font-weight: 800; color: #4da6ff;
        text-transform: uppercase; letter-spacing: 0.12em;
        margin: 0.8rem 0 0.2rem 0; border-bottom: 1px solid #1e3a5f;
        padding-bottom: 0.2rem;
    }

    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #0d1b2a 0%, #112240 100%);
        border: 1px solid #005EB8; border-radius: 8px; padding: 0.5rem 0.8rem;
    }
    [data-testid="metric-container"] label { color: #c8dff0 !important; font-size: 0.72rem; }
    [data-testid="stMetricLabel"] { color: #c8dff0 !important; }
    [data-testid="stMetricDelta"] svg { display: none; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.2rem; font-weight: 800; }
    [data-testid="stMetricDelta"] { color: #79c0ff !important; font-size: 0.8rem; }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #0d1b2a; border-radius: 8px;
        padding: 3px; gap: 3px; border: 1px solid #1e3a5f;
    }
    .stTabs [data-baseweb="tab"] {
        color: #c8dff0; background-color: #112240;
        border-radius: 6px; padding: 5px 16px;
        font-size: 0.82rem; font-weight: 600;
        border: 1px solid #1e3a5f;
    }
    .stTabs [aria-selected="true"] {
        background-color: #005EB8 !important;
        color: #ffffff !important; font-weight: 800;
        border-color: #005EB8 !important;
    }

    .stButton > button {
        background-color: #005EB8; color: #ffffff;
        border: 2px solid #4da6ff; border-radius: 6px;
        font-weight: 800; font-size: 0.9rem;
        text-transform: uppercase; letter-spacing: 0.05em; width: 100%;
    }
    .stButton > button:hover { background-color: #0070d8; border-color: #ffffff; }

    .stDownloadButton > button {
        background-color: #155a2a; color: #56d364;
        border: 1px solid #2ea043; border-radius: 6px;
        font-weight: 700; width: 100%;
    }
    .stDownloadButton > button:hover { background-color: #2ea043; color: #ffffff; }

    [data-testid="stDataFrame"] { border: 1px solid #1e3a5f; border-radius: 6px; }
    .stProgress > div > div { background-color: #005EB8 !important; }
    hr { border-color: #1e3a5f; margin: 0.7rem 0; }
    .stCaption { color: #8ab0cc !important; font-size: 0.76rem; }
    .stAlert { border-radius: 6px; font-size: 0.82rem; }

    .logo-grid {
        display: flex; flex-wrap: wrap; gap: 10px;
        justify-content: center; align-items: center; padding: 8px 0;
    }
    .logo-item {
        display: flex; flex-direction: column; align-items: center;
        gap: 3px; width: 64px;
    }
    .logo-item img {
        width: 44px; height: 44px; object-fit: contain;
        border-radius: 50%; background: #ffffff;
        padding: 3px; border: 2px solid #005EB8;
    }
    .logo-item span {
        font-size: 0.58rem; color: #c8dff0; text-align: center;
        font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONFIG ──────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data_e8')

BRACKET_TREE = {
    57: (49, 50), 58: (51, 52), 59: (55, 56), 60: (53, 54),
    61: (57, 60), 62: (58, 59), 63: (61, 62),
}
SLOT_ROUND       = {**{s: 4 for s in range(57, 61)}, 61: 5, 62: 5, 63: 6}
POINTS_PER_ROUND = {1: 10, 2: 20, 3: 40, 4: 80, 5: 160, 6: 320}
S16_SLOTS        = list(range(57, 61))  # Elite 8 slots
LATE_SLOTS       = [61, 62, 63]
ALL_FUTURE_SLOTS = S16_SLOTS + LATE_SLOTS

TEAM_LOGOS = {
    "Duke":           "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
    "St. John's":     "https://a.espncdn.com/i/teamlogos/ncaa/500/2599.png",
    "Michigan State": "https://a.espncdn.com/i/teamlogos/ncaa/500/127.png",
    "UConn":          "https://a.espncdn.com/i/teamlogos/ncaa/500/41.png",
    "Arizona":        "https://a.espncdn.com/i/teamlogos/ncaa/500/12.png",
    "Arkansas":       "https://a.espncdn.com/i/teamlogos/ncaa/500/8.png",
    "Texas":          "https://a.espncdn.com/i/teamlogos/ncaa/500/251.png",
    "Purdue":         "https://a.espncdn.com/i/teamlogos/ncaa/500/2509.png",
    "Iowa":           "https://a.espncdn.com/i/teamlogos/ncaa/500/2294.png",
    "Nebraska":       "https://a.espncdn.com/i/teamlogos/ncaa/500/158.png",
    "Illinois":       "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png",
    "Houston":        "https://a.espncdn.com/i/teamlogos/ncaa/500/248.png",
    "Michigan":       "https://a.espncdn.com/i/teamlogos/ncaa/500/130.png",
    "Alabama":        "https://a.espncdn.com/i/teamlogos/ncaa/500/333.png",
    "Tennessee":      "https://a.espncdn.com/i/teamlogos/ncaa/500/2633.png",
    "Iowa State":     "https://a.espncdn.com/i/teamlogos/ncaa/500/66.png",
}

TEAM_ABBR = {
    "Duke": "DUKE", "St. John's": "SJU", "Michigan State": "MSU",
    "UConn": "UCONN", "Arizona": "ARIZ", "Arkansas": "ARK",
    "Texas": "TEX", "Purdue": "PUR", "Iowa": "IOWA",
    "Nebraska": "NEB", "Illinois": "ILL", "Houston": "HOU",
    "Michigan": "MICH", "Alabama": "ALA", "Tennessee": "TENN",
    "Iowa State": "ISU",
}

TEAM_COLORS = {
    "Duke":"#003087","St. John's":"#BA0C2F","Michigan State":"#18453B",
    "UConn":"#000E2F","Arizona":"#CC0033","Arkansas":"#9D2235",
    "Texas":"#BF5700","Purdue":"#000000","Iowa":"#000000",
    "Nebraska":"#E41C38","Illinois":"#E84A27","Houston":"#C8102E",
    "Michigan":"#FFCB05","Alabama":"#9E1B32","Tennessee":"#FF8200",
    "Iowa State":"#C8102E","Florida":"#0021A5","Clemson":"#F56600",
    "Vanderbilt":"#000000","North Carolina":"#7BAFD4","Kansas":"#0051BA",
    "Gonzaga":"#041E42","Kentucky":"#0033A0","Virginia":"#232D4B",
    "UCLA":"#2D68C4","Wisconsin":"#C5050C","Arkansas":"#9D2235",
    "BYU":"#002E5D","Texas Tech":"#CC0000","Georgia":"#BA0C2F",
    "VCU":"#FFB300","Texas A&M":"#500000","Ohio State":"#BB0000",
    "Villanova":"#00205B","Miami (Fla.)":"#005030","North Dakota State":"#0A5640",
    "High Point":"#592C82","Troy":"#8A2432","South Florida":"#006747",
    "Iowa":"#000000","TCU":"#4D1979","UCF":"#000000",
}
TEAM_COLORS_FG = {
    "Duke":"#FFFFFF","St. John's":"#FFFFFF","Michigan State":"#FFFFFF",
    "UConn":"#FFFFFF","Arizona":"#FFFFFF","Arkansas":"#FFFFFF",
    "Texas":"#FFFFFF","Purdue":"#CFB991","Iowa":"#FFCD00",
    "Nebraska":"#FFFFFF","Illinois":"#FFFFFF","Houston":"#FFFFFF",
    "Michigan":"#00274C","Alabama":"#FFFFFF","Tennessee":"#FFFFFF",
    "Iowa State":"#F1BE48","Florida":"#FA4616","Clemson":"#522D80",
    "Vanderbilt":"#866D4B","North Carolina":"#13294B","Kansas":"#E8000D",
    "Gonzaga":"#C8102E","Kentucky":"#FFFFFF","Virginia":"#F84C1E",
    "UCLA":"#F2A900","Wisconsin":"#FFFFFF","BYU":"#0062B8",
    "Texas Tech":"#000000","Georgia":"#000000","VCU":"#000000",
    "Texas A&M":"#FFFFFF","Ohio State":"#666666","Villanova":"#9EA2A2",
    "Troy":"#B3B3B3","South Florida":"#CFC493","TCU":"#A3A9AC",
}

def t_bg(team): return TEAM_COLORS.get(team, "#005EB8")
def t_fg(team): return TEAM_COLORS_FG.get(team, "#FFFFFF")

def team_pill(team):
    bg = t_bg(team); fg = t_fg(team)
    return (f'<span style="background:{bg};color:{fg};padding:2px 8px;'
            f'border-radius:4px;font-size:0.75rem;font-weight:700;'
            f'white-space:nowrap;">{team}</span>')

MATCHUPS = [
    ("East",    57, "Duke",     "UConn"),
    ("West",    58, "Arizona",  "Purdue"),
    ("South",   59, "Michigan", "Tennessee"),
    ("Midwest", 60, "Iowa",     "Illinois"),
]

# ─── HTML TABLE HELPER ───────────────────────────────────────────────────────
def html_table(rows_data, columns, highlight_fn=None, col_formats=None, height=None):
    """Render a dark-themed HTML table matching page aesthetic."""
    col_formats = col_formats or {}
    # thead rebuilt below with sticky support
    rows_html = ""
    for i, row in enumerate(rows_data):
        is_gold = highlight_fn(row) if highlight_fn else False
        if is_gold:
            row_bg   = "#c8a951"
            row_color = "#0a0f1e"
            fw       = "700"
        else:
            row_bg   = "#0d1b2a" if i % 2 == 0 else "#112240"
            row_color = "#c8dff0"
            fw       = "400"
        cells = ""
        for c in columns:
            val = row.get(c, "")
            if c in col_formats:
                try: val = col_formats[c].format(val)
                except: pass
            cells += (f'<td style="padding:6px 12px;font-size:0.82rem;'
                      f'color:{row_color};font-weight:{fw};'
                      f'border-bottom:1px solid #1e2d4a;white-space:nowrap;">'
                      f'{val}</td>')
        rows_html += f'<tr style="background:{row_bg};">{cells}</tr>'
    if height:
        scroll_style = (f'display:block;max-height:{height}px;overflow-y:auto;'
                        f'overflow-x:auto;border-radius:8px;border:1px solid #1e3a5f;')
        thead_sticky = ('position:sticky;top:0;z-index:1;')
        th_extra = thead_sticky
    else:
        scroll_style = 'border-radius:8px;overflow:hidden;border:1px solid #1e3a5f;'
        th_extra = ''
    # Rebuild thead with sticky if scrollable
    thead = "".join(
        f'<th style="padding:7px 12px;text-align:left;font-size:0.75rem;'
        f'font-weight:700;color:#4da6ff;text-transform:uppercase;'
        f'letter-spacing:0.06em;border-bottom:2px solid #1e3a5f;'
        f'background:#0a1628;white-space:nowrap;{th_extra}">{c}</th>'
        for c in columns)
    return (f'<div style="{scroll_style}">'
            f'<table style="width:100%;border-collapse:collapse;">'
            f'<thead><tr>{thead}</tr></thead>'
            f'<tbody>{rows_html}</tbody>'
            f'</table></div>')

# ─── LOAD SIM MODULE ─────────────────────────────────────────────────────────
@st.cache_resource
def load_sim_module():
    spec = importlib.util.spec_from_file_location(
        "sim32", os.path.join(os.path.dirname(__file__), "simulation_e8.py"))
    sim32 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sim32)
    return sim32

# ─── DATABASE ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_data():
    scores    = pd.read_csv(os.path.join(DATA_DIR, 'scores.csv'))
    picks_raw = pd.read_csv(os.path.join(DATA_DIR, 'picks.csv'))
    slots_raw = pd.read_csv(os.path.join(DATA_DIR, 'slots.csv'))
    strengths = pd.read_csv(os.path.join(DATA_DIR, 'strengths.csv'))
    teams     = pd.read_csv(os.path.join(DATA_DIR, 'teams.csv'))

    # picks: only unplayed slots, matching expected column name
    picks = picks_raw.rename(columns={'predicted_winner_id': 'predicted_winner_id'})

    # slots: only unplayed slots with both teams known
    slots = slots_raw[
        slots_raw['actual_winner_id'].isna() &
        slots_raw['team_1_id'].notna()
    ][['slot_id','round','region','team_1_id','team_2_id']].copy()

    return scores, picks, slots, strengths, teams

# ─── SIMULATION ──────────────────────────────────────────────────────────────
def run_simulation(n_sims, forced_outcomes, scores, picks, slots,
                   strength_map, bracket_ids, person_map, sim32, team_name_map):
    s16_info = [{'slot_id': int(r['slot_id']),
                 'team_1': int(r['team_1_id']),
                 'team_2': int(r['team_2_id'])}
                for _, r in slots[slots['slot_id'].isin(S16_SLOTS)].iterrows()]
    all_perms   = list(product([0, 1], repeat=4))
    all_results = np.zeros((16, len(bracket_ids)))
    scen_probs  = np.zeros(16)

    prog = st.progress(0, text="Running simulations...")
    for pi, perm in enumerate(all_perms):
        s16f = {}
        for gi, game in enumerate(s16_info):
            sid = game['slot_id']
            if sid not in forced_outcomes:
                s16f[sid] = game['team_1'] if perm[gi] == 0 else game['team_2']
        scen_probs[pi] = sim32.scenario_kenpom_prob(perm, s16_info, strength_map, forced_outcomes)
        aw = sim32.simulate_vectorized(n_sims, s16f, strength_map, slots[slots['slot_id'].isin(S16_SLOTS + LATE_SLOTS)], forced_outcomes)
        ts = sim32.score_all_brackets(n_sims, aw, picks, scores, bracket_ids)
        all_results[pi] = sim32.compute_win_probs(ts)
        if (pi+1) % 4 == 0:
            prog.progress((pi+1)/16, text=f"Scenario {pi+1}/16...")
    prog.empty()

    scen_probs  = scen_probs / scen_probs.sum()
    baseline    = all_results.T @ scen_probs
    best        = all_results.max(axis=0)
    worst       = all_results.min(axis=0)

    all_person_results, creators = sim32.compute_person_win_probs_from_bracket_results(
        all_results, bracket_ids, person_map)
    person_baseline = all_person_results.T @ scen_probs
    person_best     = all_person_results.max(axis=0)
    person_worst    = all_person_results.min(axis=0)

    game_impacts = []
    for gi, game in enumerate(s16_info):
        forced = game['slot_id'] in forced_outcomes
        t1m = np.array([p[gi] == 0 for p in all_perms]); t2m = ~t1m
        if forced:
            avg_t1 = baseline.copy(); avg_t2 = baseline.copy()
        else:
            t1p = scen_probs.copy(); t1p[t2m] = 0; t1p /= t1p.sum()
            t2p = scen_probs.copy(); t2p[t1m] = 0; t2p /= t2p.sum()
            avg_t1 = all_results.T @ t1p
            avg_t2 = all_results.T @ t2p
        game_impacts.append({
            'slot_id':        game['slot_id'],
            'team_1':         game['team_1'],
            'team_2':         game['team_2'],
            'team_1_name':    team_name_map.get(game['team_1'], str(game['team_1'])),
            'team_2_name':    team_name_map.get(game['team_2'], str(game['team_2'])),
            'avg_if_t1_wins': avg_t1,
            'avg_if_t2_wins': avg_t2,
            'swing':          avg_t1 - avg_t2,
            'abs_swing':      np.abs(avg_t1 - avg_t2),
        })

    return (baseline, best, worst, game_impacts, s16_info,
            all_results, all_perms, scen_probs,
            all_person_results, person_baseline, person_best, person_worst, creators)

# ─── EXCEL EXPORT ────────────────────────────────────────────────────────────
def build_excel_bytes(all_results, all_perms, scen_probs, s16_info,
                      game_impacts, scores, bracket_ids, bracket_names,
                      baseline, best, worst, team_name_map,
                      forced_outcomes, forced_names, person_map,
                      all_person_results, person_baseline, person_best,
                      person_worst, creators, sim32):
    orig_filename = sim32.build_filename(forced_outcomes or {}, forced_names or {})
    sim32.build_excel(
        all_results, all_perms, scen_probs, s16_info,
        game_impacts, scores, bracket_ids, bracket_names,
        baseline, best, worst, team_name_map,
        forced_outcomes or {}, forced_names or {}, person_map,
        all_person_results, person_baseline, person_best, person_worst, creators)
    with open(orig_filename, 'rb') as f:
        data = f.read()
    try: os.remove(orig_filename)
    except: pass
    return data

# ─── COLOR HELPERS ───────────────────────────────────────────────────────────
def color_pct(val):
    if not isinstance(val, (int, float)): return ''
    if val > 20:  return 'background-color: #0d3320; color: #56d364'
    if val > 10:  return 'background-color: #0d2040; color: #79c0ff'
    if val < 1:   return 'background-color: #2a0d0d; color: #f28b82'
    return 'color: #e8eaf0'

def color_swing_pos(val):
    """Swing is always positive — shade by magnitude."""
    if not isinstance(val, (int, float)): return 'color: #8ab0cc'
    if val > 5:   return 'background-color: #0d3320; color: #56d364; font-weight: 700'
    if val > 2:   return 'color: #56d364; font-weight: 600'
    if val > 0:   return 'color: #a8d5b5'
    return 'color: #8ab0cc'

def color_root(val):
    return 'color: #4da6ff; font-weight: 700'

# ─── LOGO GRID ───────────────────────────────────────────────────────────────
def render_logo_grid():
    items = ""
    for team, url in TEAM_LOGOS.items():
        abbr = TEAM_ABBR.get(team, team[:4].upper())
        items += f'<div class="logo-item"><img src="{url}" alt="{team}"/><span>{abbr}</span></div>'
    return f'<div class="logo-grid">{items}</div>'

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    sim32 = load_sim_module()

    try:
        scores, picks, slots, strengths, teams = load_data()
    except Exception as e:
        st.error(f"Could not load data files: {e}. Make sure the data/ folder exists.")
        st.stop()

    strength_map  = dict(zip(strengths['team_id'].astype(int), strengths['kenpom_net_rating']))
    team_name_map = dict(zip(teams['team_id'].astype(int), teams['team_name']))
    team_id_map   = dict(zip(teams['team_name'], teams['team_id'].astype(int)))
    bracket_ids   = scores['bracket_id'].tolist()
    bracket_names = dict(zip(scores['bracket_id'], scores['bracket_name']))
    person_map    = sim32.build_person_map(scores)
    creators      = sorted(person_map.keys())

    s16_info = [{'slot_id': int(r['slot_id']),
                 'team_1': int(r['team_1_id']),
                 'team_2': int(r['team_2_id'])}
                for _, r in slots[slots['slot_id'].isin(S16_SLOTS)].iterrows()]

    # ── NAV BAR ──────────────────────────────────────────────────────────────
    col_nav1, col_nav2, col_spacer = st.columns([1, 1, 6])
    with col_nav1:
        st.page_link("dashboard_e8_demo.py", label="Simulator", use_container_width=True)
    with col_nav2:
        st.page_link("pages/visualisations_e8_demo.py", label="Visualisations", use_container_width=True)
    st.divider()

    # ── HEADER ───────────────────────────────────────────────────────────────
    col_title, col_logos = st.columns([3, 2])
    with col_title:
        st.markdown('<div class="hero-title">Who Should I Root For?</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub1">A March Madness Pool Simulator — Elite 8</div>', unsafe_allow_html=True)
        st.markdown("""<div class="hero-subtitle">
            In many March Madness pools, the question of "who should I root for?" is often unclear.
            While some games are obvious, others are murkier. Should you root for a team you have
            going deep if they are overrepresented in rival brackets? How much does that difference
            in projection between you and your competitors actually matter? How much does each
            individual result affect your chances of winning the pool? These questions now have
            answers. Pick your bracket, run the simulator, and find out which Sweet 16 results
            improve your odds of winning. Force specific outcomes to stress-test your position,
            then download the full Excel breakdown — and root with the confidence that you are
            mathematically backing the right team. Happy simulating.
        </div>""", unsafe_allow_html=True)
    with col_logos:
        st.markdown(render_logo_grid(), unsafe_allow_html=True)

    st.divider()

    # ── CONTROLS EXPANDER ────────────────────────────────────────────────────
    with st.expander("⚙️ Elite 8 Simulator Settings", expanded=True):
        col_a, col_b, col_c = st.columns([1, 1, 1])

        with col_a:
            st.markdown('<div class="section-label">Perspective</div>', unsafe_allow_html=True)
            view_mode = st.radio("", ["Bracket", "Person"], horizontal=True,
                                 label_visibility="collapsed")
            if view_mode == "Bracket":
                selected_bracket = st.selectbox("Select bracket",
                    ["All Brackets"] + sorted(scores['bracket_name'].tolist()))
                selected_person  = None
            else:
                selected_person  = st.selectbox("Select person", ["All People"] + creators)
                selected_bracket = None

            st.markdown('<div class="section-label">Simulations</div>', unsafe_allow_html=True)
            n_sims = st.select_slider("Per scenario",
                                      options=[500, 1000, 2000, 5000, 10000], value=1000)
            st.caption(f"Total: {16 * n_sims:,} simulations")

        with col_b:
            st.markdown('<div class="section-label">Force Elite 8 Outcomes</div>',
                        unsafe_allow_html=True)
            st.caption("Lock results before simulating (optional)")
            forced_outcomes = {}
            forced_names    = {}
            for region, sid, t1, t2 in MATCHUPS[:2]:
                pick = st.selectbox(f"{t1} vs {t2}  |  {region}",
                                    ["No pick", t1, t2], key=f"slot_{sid}")
                if pick != "No pick":
                    tid = team_id_map.get(pick)
                    if tid:
                        forced_outcomes[sid] = tid
                        forced_names[tid]    = pick

        with col_c:
            st.markdown('<div class="section-label">&nbsp;</div>', unsafe_allow_html=True)
            st.caption("&nbsp;")
            for region, sid, t1, t2 in MATCHUPS[2:]:
                pick = st.selectbox(f"{t1} vs {t2}  |  {region}",
                                    ["No pick", t1, t2], key=f"slot_{sid}")
                if pick != "No pick":
                    tid = team_id_map.get(pick)
                    if tid:
                        forced_outcomes[sid] = tid
                        forced_names[tid]    = pick

        run_button = st.button("▶ RUN SIMULATION", type="primary", use_container_width=True)

    # ── SIMULATION RESULTS ───────────────────────────────────────────────────
    if run_button:
        if forced_outcomes:
            forced_disp = "  |  ".join([f"**{forced_names[tid]}** (Slot {sid})"
                                         for sid, tid in forced_outcomes.items()])
            st.info(f"Forced: {forced_disp}")

        with st.spinner(f"Running {16 * n_sims:,} simulations..."):
            (baseline, best, worst, game_impacts, s16_info_out,
             all_results, all_perms, scen_probs,
             all_person_results, person_baseline, person_best, person_worst,
             result_creators) = run_simulation(
                n_sims, forced_outcomes, scores, picks, slots,
                strength_map, bracket_ids, person_map, sim32, team_name_map)

        sort_order        = np.argsort(-baseline)
        person_sort_order = np.argsort(-person_baseline)
        bid_to_idx        = {bid: i for i, bid in enumerate(bracket_ids)}

        # ── Save results to session_state for visualisations page ─────────
        st.session_state['sim_results'] = {
            'game_impacts':    game_impacts,
            'baseline':        baseline,
            'bracket_ids':     bracket_ids,
            'bracket_names':   bracket_names,
            'team_name_map':   team_name_map,
            'forced_outcomes': forced_outcomes,
            'forced_names':    forced_names,
            'scores':          scores,
        }

        # Determine which person to highlight based on selected bracket or person
        if selected_bracket and selected_bracket != "All Brackets":
            _match = scores[scores['bracket_name'] == selected_bracket]['bracket_creator']
            highlighted_person = _match.iloc[0] if len(_match) > 0 else None
        elif selected_person and selected_person != "All People":
            highlighted_person = selected_person
        else:
            highlighted_person = None
        st.session_state['highlighted_person'] = highlighted_person

        tab1, tab2, tab3 = st.tabs(["  Bracket Results  ", "  Person Results  ", "  Game Impact (Who Should I Root For?)  "])

        # ── TAB 1: BRACKET RESULTS ────────────────────────────────────────
        with tab1:
            st.markdown('<div style="font-size:0.78rem; color:#8ab0cc;"><b style="color:#c8dff0;">Win %</b> represents how likely each bracket is to win the pool — given the inputs you selected before running the simulation.</div>', unsafe_allow_html=True)
            rows = []
            for rank, idx in enumerate(sort_order, 1):
                bid     = bracket_ids[idx]
                name    = bracket_names[bid]
                creator = scores[scores['bracket_id'] == bid]['bracket_creator'].iloc[0]
                pts     = int(scores[scores['bracket_id'] == bid]['current_score'].iloc[0])
                rows.append({
                    'Rank':    rank,
                    'Bracket': name,
                    'Creator': creator,
                    'Pts':     pts,
                    'Win %':   round(baseline[idx]*100, 2),
                })
            df = pd.DataFrame(rows)
            sel_name = selected_bracket if selected_bracket != "All Brackets" else None

            # Get all brackets belonging to highlighted person
            _person_brackets = []
            if highlighted_person and highlighted_person in person_map:
                _person_brackets = [bracket_names[b] for b in person_map[highlighted_person]
                                     if b in bracket_names]

            def highlight_bracket(row, sn=sel_name, pb=_person_brackets):
                if sn and row['Bracket'] == sn:
                    return ['background-color: #c8a951; color: #0a0f1e; font-weight: bold'] * len(row)
                if pb and row['Bracket'] in pb:
                    return ['background-color: #c8a951; color: #0a0f1e; font-weight: bold'] * len(row)
                return [''] * len(row)

            rows_data = df.to_dict('records')
            def hl_br(row):
                return (bool(sel_name and row['Bracket'] == sel_name) or
                        bool(_person_brackets and row['Bracket'] in _person_brackets))
            st.markdown(html_table(rows_data, ['Rank','Bracket','Creator','Pts','Win %'],
                hl_br, {'Win %': '{:.2f}%', 'Pts': '{:.0f}', 'Rank': '{:.0f}'}, height=460),
                unsafe_allow_html=True)

        # ── TAB 2: PERSON RESULTS ─────────────────────────────────────────
        with tab2:
            st.markdown('<div style="font-size:0.78rem; color:#8ab0cc;"><b style="color:#c8dff0;">Win %</b> represents how likely each person is to win the pool — i.e. how likely it is that any one of their brackets wins — given the inputs you selected before running the simulation.</div>', unsafe_allow_html=True)
            rows = []
            for rank, pi in enumerate(person_sort_order, 1):
                creator  = result_creators[pi]
                bids     = person_map[creator]
                bid_idxs = [bid_to_idx[bid] for bid in bids if bid in bid_to_idx]
                best_b   = round(max(baseline[i] for i in bid_idxs)*100, 2) if bid_idxs else 0
                best_pts = max(int(scores[scores['bracket_id']==bid]['current_score'].iloc[0])
                               for bid in bids if bid in bracket_ids)
                rows.append({
                    'Rank':         rank,
                    'Person':       creator,
                    'No. Brackets': len(bids),
                    'Brackets':     ", ".join([bracket_names[b] for b in bids if b in bracket_names]),
                    'Best Pts':     best_pts,
                    'Person Win %': round(person_baseline[pi]*100, 2),
                    'Best Bracket': best_b,
                })
            df_p = pd.DataFrame(rows)
            sel_person = selected_person if selected_person != "All People" else None

            rows_data_p = df_p.to_dict('records')
            def hl_pr(row):
                return bool(highlighted_person and row['Person'] == highlighted_person)
            st.markdown(html_table(rows_data_p,
                ['Rank','Person','No. Brackets','Brackets','Best Pts','Person Win %','Best Bracket'],
                hl_pr, {'Person Win %': '{:.2f}%', 'Best Bracket': '{:.2f}%',
                        'Best Pts': '{:.0f}', 'Rank': '{:.0f}', 'No. Brackets': '{:.0f}'},
                height=460), unsafe_allow_html=True)

        # ── TAB 3: GAME IMPACT ────────────────────────────────────────────
        with tab3:
            def get_impact_df(idx_or_idxs, is_person=False):
                rows = []
                for g in game_impacts:
                    forced = g['slot_id'] in forced_outcomes
                    t1, t2 = g['team_1_name'], g['team_2_name']

                    if forced:
                        # Forced — use whichever team was forced as T1
                        forced_team = forced_names.get(forced_outcomes.get(g['slot_id'], 0), t1)
                        other_team  = t2 if forced_team == t1 else t1
                        rows.append({
                            'Root For':   forced_team,
                            'Other Team': other_team,
                            'Win% if Root For Team Wins': 'N/A',
                            'Win% if Other':    'N/A',
                            'Swing':            'N/A',
                        })
                        continue

                    if is_person and isinstance(idx_or_idxs, list):
                        idxs = idx_or_idxs
                        p1c  = (1 - np.prod([1 - g['avg_if_t1_wins'][i] for i in idxs]))*100 if idxs else 0
                        p2c  = (1 - np.prod([1 - g['avg_if_t2_wins'][i] for i in idxs]))*100 if idxs else 0
                        sw   = p1c - p2c
                    elif isinstance(idx_or_idxs, int):
                        p1c  = g['avg_if_t1_wins'][idx_or_idxs]*100
                        p2c  = g['avg_if_t2_wins'][idx_or_idxs]*100
                        sw   = p1c - p2c
                    else:
                        # All — use average
                        p1c  = float(g['avg_if_t1_wins'].mean())*100
                        p2c  = float(g['avg_if_t2_wins'].mean())*100
                        sw   = p1c - p2c

                    # T1 always = the team that HELPS more (swing always positive)
                    if sw >= 0:
                        root, other   = t1, t2
                        p_root, p_oth = round(p1c, 2), round(p2c, 2)
                        swing         = round(sw, 2)
                    else:
                        root, other   = t2, t1
                        p_root, p_oth = round(p2c, 2), round(p1c, 2)
                        swing         = round(-sw, 2)

                    rows.append({
                        'Root For':            root,
                        'Other Team':          other,
                        'Win% if Root For Team Wins':    p_root,
                        'Win% if Other':       p_oth,
                        'Swing':               swing,
                    })

                df = pd.DataFrame(rows)
                if df.empty:
                    return df
                df = df.sort_values('Swing',
                    key=lambda x: pd.to_numeric(x, errors='coerce'),
                    ascending=False, na_position='last')
                return df

            def show_metrics(base, b, w, label="Win Probability"):
                c1, c2 = st.columns(2)
                c1.metric(label,  f"{base:.2f}%")
                c2.metric("Best Case", f"{b:.2f}%", f"+{b-base:.2f}%")

            def style_impact(df):
                cols = ['Root For', 'Other Team',
                        'Win% if Root For Team Wins', 'Win% if Other', 'Swing']
                thead_html = "".join(
                    f'<th style="padding:7px 12px;text-align:left;font-size:0.75rem;'
                    f'font-weight:700;color:#4da6ff;text-transform:uppercase;'
                    f'letter-spacing:0.06em;border-bottom:2px solid #1e3a5f;'
                    f'background:#0a1628;white-space:nowrap;'
                    f'position:sticky;top:0;z-index:1;">{c}</th>'
                    for c in cols)
                rows_html = ""
                for i, row in df.iterrows():
                    root  = row.get('Root For', '')
                    other = row.get('Other Team', '')
                    swing = row.get('Swing', '')
                    p_root = row.get('Win% if Root For Team Wins', '')
                    p_oth  = row.get('Win% if Other', '')
                    bg = "#0d1b2a" if i % 2 == 0 else "#112240"
                    # Team pills
                    root_cell  = team_pill(root) if root not in ('N/A', '') else root
                    other_cell = team_pill(other) if other not in ('N/A', '') else other
                    # Swing colored same as root team
                    root_color = t_bg(root) if root not in ('N/A', '') else '#c8dff0'
                    try:
                        swing_fmt = f'{float(swing):.2f}%'
                    except:
                        swing_fmt = str(swing)
                    try: p_root_fmt = f'{float(p_root):.2f}%'
                    except: p_root_fmt = str(p_root)
                    try: p_oth_fmt = f'{float(p_oth):.2f}%'
                    except: p_oth_fmt = str(p_oth)
                    td = f'padding:6px 12px;border-bottom:1px solid #1e2d4a;font-size:0.82rem;'
                    rows_html += (
                        f'<tr style="background:{bg};">'
                        f'<td style="{td}">{root_cell}</td>'
                        f'<td style="{td}">{other_cell}</td>'
                        f'<td style="{td}color:#c8dff0;">{p_root_fmt}</td>'
                        f'<td style="{td}color:#8ab0cc;">{p_oth_fmt}</td>'
                        f'<td style="{td}color:{root_color};font-weight:700;">{swing_fmt}</td>'
                        f'</tr>')
                st.markdown(
                    f'<div style="display:block;max-height:400px;overflow-y:auto;'
                    f'overflow-x:auto;border-radius:8px;border:1px solid #1e3a5f;">'
                    f'<table style="width:100%;border-collapse:collapse;">'
                    f'<thead><tr>{thead_html}</tr></thead>'
                    f'<tbody>{rows_html}</tbody>'
                    f'</table></div>',
                    unsafe_allow_html=True)

            # Build dynamic explanatory text
            forced_desc = ""
            if forced_outcomes:
                pairs = []
                for sid, tid in forced_outcomes.items():
                    winner = forced_names.get(tid, str(tid))
                    # Find the loser for this slot
                    for region, s, t1, t2 in MATCHUPS:
                        if s == sid:
                            loser = t2 if winner == t1 else t1
                            pairs.append(f"{winner} beat {loser}")
                            break
                forced_desc = " (and " + ", and ".join(pairs) + ")"

            st.markdown(
                f"""<div style="font-size:0.78rem; color:#8ab0cc; line-height:1.8;">
                <b style="color:#c8dff0;">Root For</b> — the team you should cheer for (mathematically increases your odds of winning the pool).<br>
                <b style="color:#c8dff0;">Win %</b> — how likely your selected bracket or person is to win the pool if that result happens{forced_desc}.<br>
                <b style="color:#c8dff0;">Swing</b> — how much difference that individual game outcome makes to your chances. The bigger the swing, the more consequential the result.
                </div>""",
                unsafe_allow_html=True
            )

            if view_mode == "Bracket":
                if selected_bracket == "All Brackets":
                    style_impact(get_impact_df(None))
                else:
                    sel_bid = scores[scores['bracket_name'] == selected_bracket]['bracket_id'].iloc[0]
                    sel_idx = bid_to_idx[sel_bid]
                    show_metrics(baseline[sel_idx]*100, best[sel_idx]*100, worst[sel_idx]*100)
                    st.caption(f"Bracket: {selected_bracket}")
                    style_impact(get_impact_df(sel_idx))
            else:
                if selected_person == "All People":
                    style_impact(get_impact_df(None, is_person=True))
                else:
                    pi_sel   = result_creators.index(selected_person)
                    bids     = person_map[selected_person]
                    bid_idxs = [bid_to_idx[b] for b in bid_to_idx if bid_to_idx[b] in [bid_to_idx.get(b) for b in bids]]
                    bid_idxs = [bid_to_idx[b] for b in bids if b in bid_to_idx]
                    show_metrics(person_baseline[pi_sel]*100,
                                 person_best[pi_sel]*100,
                                 person_worst[pi_sel]*100, "Person Win %")
                    st.caption("  |  ".join([bracket_names[b] for b in bids if b in bracket_names]))
                    style_impact(get_impact_df(bid_idxs, is_person=True))

        # ── DOWNLOAD ─────────────────────────────────────────────────────
        st.divider()
        with st.spinner("Building Excel..."):
            excel_bytes = build_excel_bytes(
                all_results, all_perms, scen_probs, s16_info_out,
                game_impacts, scores, bracket_ids, bracket_names,
                baseline, best, worst, team_name_map,
                forced_outcomes, forced_names, person_map,
                all_person_results, person_baseline, person_best, person_worst,
                result_creators, sim32)

        fname = sim32.build_filename(forced_outcomes or {}, forced_names or {})
        st.download_button("Download Full Excel (9 Sheets)", data=excel_bytes,
                           file_name=fname,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    else:
        st.markdown('<div style="background-color:#112240; border:1px solid #005EB8; border-radius:6px; padding:0.8rem 1rem; font-size:0.9rem; color:#c8dff0;">&#8593; Select your settings above and click <b style="color:#ffffff;">RUN SIMULATION</b> to get started.</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:0.5rem;font-size:0.82rem;color:#8ab0cc;">&#8593; Once you get tired of the numbers (impossible) — check out some fun visualisations of the data at the top of the screen!</div>', unsafe_allow_html=True)

    # ── CURRENT STANDINGS (bottom) ────────────────────────────────────────────
    st.divider()
    st.markdown("### Current Standings")
    col_l, col_r = st.columns(2)

    with col_l:
        st.caption("By Bracket")
        s = scores.sort_values('current_score', ascending=False).reset_index(drop=True)
        s.insert(0, 'Rank', range(1, len(s)+1))
        s_display = s[['Rank','bracket_name','bracket_creator','current_score']].rename(
            columns={'bracket_name':'Bracket','bracket_creator':'Creator','current_score':'Pts'}).copy()

        _hl_bracket = selected_bracket if (selected_bracket and selected_bracket != "All Brackets") else None
        _hl_person_s = st.session_state.get('highlighted_person', None)
        _person_brackets_s = [bracket_names[b] for b in person_map.get(_hl_person_s, [])
                               if b in bracket_names] if _hl_person_s else []
        def highlight_s_bracket(row, hb=_hl_bracket, pb=_person_brackets_s):
            if hb and row['Bracket'] == hb:
                return ['background-color: #c8a951; color: #0a0f1e; font-weight: bold'] * len(row)
            if pb and row['Bracket'] in pb:
                return ['background-color: #c8a951; color: #0a0f1e; font-weight: bold'] * len(row)
            return [''] * len(row)

        rows_s_br = s_display.to_dict('records')
        def hl_s_br(row, hb=_hl_bracket, pb=_person_brackets_s):
            return (bool(hb and row['Bracket'] == hb) or
                    bool(pb and row['Bracket'] in pb))
        st.markdown(html_table(rows_s_br, ['Rank','Bracket','Creator','Pts'],
            hl_s_br, {'Rank': '{:.0f}', 'Pts': '{:.0f}'}, height=280),
            unsafe_allow_html=True)

    with col_r:
        st.caption("By Person")
        ps = []
        for creator, bids in person_map.items():
            best_score = max(int(scores[scores['bracket_id']==bid]['current_score'].iloc[0])
                             for bid in bids if bid in bracket_ids)
            ps.append({'Person': creator, 'Best Score': best_score, 'Brackets': len(bids)})
        ps_df = pd.DataFrame(ps).sort_values('Best Score', ascending=False).reset_index(drop=True)
        ps_df.insert(0, 'Rank', range(1, len(ps_df)+1))
        _hl_person = st.session_state.get('highlighted_person', None)
        def highlight_s_person(row, hp=_hl_person):
            if hp and row['Person'] == hp:
                return ['background-color: #c8a951; color: #0a0f1e; font-weight: bold'] * len(row)
            return [''] * len(row)

        rows_s_pr = ps_df.to_dict('records')
        def hl_s_pr(row, hp=_hl_person):
            return bool(hp and row['Person'] == hp)
        st.markdown(html_table(rows_s_pr, ['Rank','Person','Best Score','Brackets'],
            hl_s_pr, {'Rank': '{:.0f}', 'Best Score': '{:.0f}', 'Brackets': '{:.0f}'},
            height=280), unsafe_allow_html=True)


    # ── FOOTER ───────────────────────────────────────────────────────────────
    st.divider()
    st.markdown('''<div style="display:flex;justify-content:space-between;
        align-items:flex-start;flex-wrap:wrap;gap:1rem;padding:0.5rem 0;
        border-top:1px solid #1e3a5f;">
        <div style="font-size:0.75rem;color:#8ab0cc;line-height:1.8;">
            <a href="https://www.linkedin.com/in/henry-snowdon-b14198377/" target="_blank" style="color:#c8dff0;font-weight:700;font-size:0.8rem;text-decoration:none;">Henry Snowdon</a><br>
            <span style="color:#4da6ff;">Predictive Modelling &nbsp;·&nbsp; Data Analysis &nbsp;·&nbsp; Practical Insights</span>
        </div>
        <div style="font-size:0.7rem;color:#5a7a9a;line-height:1.9;text-align:right;">
            <span style="color:#8ab0cc;font-weight:600;">Data Sources &amp; Credits</span><br>
            <a href="https://kenpom.com" target="_blank" style="color:#5a7a9a;text-decoration:none;">KenPom</a> — adjusted efficiency ratings used in Bradley-Terry win probability model<br>
            <a href="https://www.ncaa.com/march-madness" target="_blank" style="color:#5a7a9a;text-decoration:none;">NCAA March Madness</a> — official tournament results &amp; bracket structure<br>
            <a href="https://kalshi.com" target="_blank" style="color:#5a7a9a;text-decoration:none;">Kalshi</a> — prediction market probabilities (reference only)<br>
            Team logos via <a href="https://www.espn.com" target="_blank" style="color:#5a7a9a;text-decoration:none;">ESPN CDN</a> &nbsp;·&nbsp; Built with <a href="https://streamlit.io" target="_blank" style="color:#5a7a9a;text-decoration:none;">Streamlit</a> &amp; <a href="https://plotly.com" target="_blank" style="color:#5a7a9a;text-decoration:none;">Plotly</a>
        </div>
    </div>''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
