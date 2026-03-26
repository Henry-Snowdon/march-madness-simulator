"""
March Madness Pool — Visualisations
"""
import streamlit as st
import pandas as pd
import numpy as np
# Demo: reads from CSV files
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Visualisations — March Madness Pool",
                   page_icon=None, layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1b2a; color: #e8eaf0; }
    [data-testid="collapsedControl"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    section[data-testid="stSidebarCollapsedControl"] { display: none !important; }
    .st-emotion-cache-1rtdyuf { display: none !important; }
    .st-emotion-cache-h5rgaw { display: none !important; }
    button[aria-label="Close sidebar"] { display: none !important; }
    button[aria-label="Collapse sidebar"] { display: none !important; }
    .block-container { padding: 1.2rem 2rem 1rem 2rem !important; max-width: 1400px; }
    [data-testid="stSidebar"] { background-color: #0a1628 !important; border-right: 2px solid #005EB8; }
    [data-testid="stSidebar"] label { color: #c8dff0 !important; font-size: 0.8rem; }
    .section-label { font-size: 0.68rem; font-weight: 800; color: #4da6ff;
        text-transform: uppercase; letter-spacing: 0.12em;
        margin: 0.8rem 0 0.2rem 0; border-bottom: 1px solid #1e3a5f; padding-bottom: 0.2rem; }
    hr { border-color: #1e3a5f; margin: 0.7rem 0; }
    .stCaption { color: #8ab0cc !important; font-size: 0.76rem; }
    #MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

ROUND_NAMES = {1:'Round of 64', 2:'Round of 32', 3:'Sweet 16',
               4:'Elite 8', 5:'Final Four', 6:'Championship'}

TEAM_COLORS = {
    "Duke":                  ("#003087","#FFFFFF"), "Ohio State":         ("#BB0000","#666666"),
    "St. John's":            ("#BA0C2F","#FFFFFF"), "Kansas":             ("#0051BA","#E8000D"),
    "Louisville":            ("#AD0000","#000000"), "Michigan State":     ("#18453B","#FFFFFF"),
    "UCLA":                  ("#2D68C4","#F2A900"), "UConn":              ("#000E2F","#E4002B"),
    "Arizona":               ("#CC0033","#003366"), "Villanova":          ("#00205B","#9EA2A2"),
    "Wisconsin":             ("#C5050C","#FFFFFF"), "Arkansas":           ("#9D2235","#FFFFFF"),
    "BYU":                   ("#002E5D","#0062B8"), "Gonzaga":            ("#041E42","#C8102E"),
    "Miami (Fla.)":          ("#005030","#F47321"), "Purdue":             ("#000000","#CFB991"),
    "Florida":               ("#0021A5","#FA4616"), "Clemson":            ("#F56600","#522D80"),
    "Vanderbilt":            ("#000000","#866D4B"), "Nebraska":           ("#E41C38","#FFFFFF"),
    "North Carolina":        ("#7BAFD4","#13294B"), "Illinois":           ("#E84A27","#13294B"),
    "Saint Mary's":          ("#8C1515","#00205B"), "Houston":            ("#C8102E","#FFFFFF"),
    "Michigan":              ("#FFCB05","#00274C"), "Georgia":            ("#BA0C2F","#000000"),
    "Texas Tech":            ("#CC0000","#000000"), "Alabama":            ("#9E1B32","#FFFFFF"),
    "Tennessee":             ("#FF8200","#FFFFFF"), "Virginia":           ("#232D4B","#F84C1E"),
    "Kentucky":              ("#0033A0","#FFFFFF"), "Iowa State":         ("#C8102E","#F1BE48"),
    "Siena":                 ("#006747","#C4B581"), "TCU":                ("#4D1979","#A3A9AC"),
    "UNI":                   ("#4B116F","#FFCC33"), "Cal Baptist":        ("#002F6C","#C99700"),
    "South Florida":         ("#006747","#CFC493"), "North Dakota State": ("#0A5640","#FFC72C"),
    "UCF":                   ("#000000","#BA9B37"), "Furman":             ("#4B2E83","#FFFFFF"),
    "Long Island University":("#00A1E0","#FFFFFF"), "Utah State":         ("#00263A","#FFFFFF"),
    "High Point":            ("#592C82","#FFFFFF"), "Hawai'i":            ("#024731","#FFFFFF"),
    "Texas":                 ("#BF5700","#FFFFFF"), "Kennesaw State":     ("#FDBB30","#000000"),
    "Missouri":              ("#000000","#F1B82D"), "Queens":             ("#002D72","#B9975B"),
    "Prairie View A&M":      ("#522398","#FFB81C"), "Iowa":               ("#000000","#FFCD00"),
    "McNeese":               ("#00529B","#FDBB30"), "Troy":               ("#8A2432","#B3B3B3"),
    "VCU":                   ("#FFB300","#000000"), "Penn":               ("#990000","#011F5B"),
    "Texas A&M":             ("#500000","#FFFFFF"), "Idaho":              ("#B18E2F","#000000"),
    "Howard":                ("#003A8F","#C8102E"), "Saint Louis":        ("#003DA5","#FFFFFF"),
    "Akron":                 ("#00285E","#FEC524"), "Hofstra":            ("#FDBB30","#003DA5"),
    "Miami (Ohio)":          ("#B61E2E","#FFFFFF"), "Wright State":       ("#006B3F","#CDB87C"),
    "Santa Clara":           ("#862633","#FFFFFF"), "Tennessee State":    ("#003DA5","#FFFFFF"),
}

TEAM_LOGOS = {
    "Duke":"https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
    "St. John's":"https://a.espncdn.com/i/teamlogos/ncaa/500/2599.png",
    "Michigan State":"https://a.espncdn.com/i/teamlogos/ncaa/500/127.png",
    "UConn":"https://a.espncdn.com/i/teamlogos/ncaa/500/41.png",
    "Arizona":"https://a.espncdn.com/i/teamlogos/ncaa/500/12.png",
    "Arkansas":"https://a.espncdn.com/i/teamlogos/ncaa/500/8.png",
    "Texas":"https://a.espncdn.com/i/teamlogos/ncaa/500/251.png",
    "Purdue":"https://a.espncdn.com/i/teamlogos/ncaa/500/2509.png",
    "Iowa":"https://a.espncdn.com/i/teamlogos/ncaa/500/2294.png",
    "Nebraska":"https://a.espncdn.com/i/teamlogos/ncaa/500/158.png",
    "Illinois":"https://a.espncdn.com/i/teamlogos/ncaa/500/356.png",
    "Houston":"https://a.espncdn.com/i/teamlogos/ncaa/500/248.png",
    "Michigan":"https://a.espncdn.com/i/teamlogos/ncaa/500/130.png",
    "Alabama":"https://a.espncdn.com/i/teamlogos/ncaa/500/333.png",
    "Tennessee":"https://a.espncdn.com/i/teamlogos/ncaa/500/2633.png",
    "Iowa State":"https://a.espncdn.com/i/teamlogos/ncaa/500/66.png",
    "Florida":"https://a.espncdn.com/i/teamlogos/ncaa/500/57.png",
    "Ohio State":"https://a.espncdn.com/i/teamlogos/ncaa/500/194.png",
    "Kansas":"https://a.espncdn.com/i/teamlogos/ncaa/500/2305.png",
    "Kentucky":"https://a.espncdn.com/i/teamlogos/ncaa/500/96.png",
    "North Carolina":"https://a.espncdn.com/i/teamlogos/ncaa/500/153.png",
    "UCLA":"https://a.espncdn.com/i/teamlogos/ncaa/500/26.png",
    "Gonzaga":"https://a.espncdn.com/i/teamlogos/ncaa/500/2250.png",
    "Villanova":"https://a.espncdn.com/i/teamlogos/ncaa/500/222.png",
    "Clemson":"https://a.espncdn.com/i/teamlogos/ncaa/500/228.png",
    "VCU":"https://a.espncdn.com/i/teamlogos/ncaa/500/2670.png",
    "Texas A&M":"https://a.espncdn.com/i/teamlogos/ncaa/500/245.png",
    "South Florida":"https://a.espncdn.com/i/teamlogos/ncaa/500/58.png",
}


ALL_TEAM_LOGOS = {
    "Duke":"https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
    "Ohio State":"https://a.espncdn.com/i/teamlogos/ncaa/500/194.png",
    "St. John's":"https://a.espncdn.com/i/teamlogos/ncaa/500/2599.png",
    "Kansas":"https://a.espncdn.com/i/teamlogos/ncaa/500/2305.png",
    "Louisville":"https://a.espncdn.com/i/teamlogos/ncaa/500/97.png",
    "Michigan State":"https://a.espncdn.com/i/teamlogos/ncaa/500/127.png",
    "UCLA":"https://a.espncdn.com/i/teamlogos/ncaa/500/26.png",
    "UConn":"https://a.espncdn.com/i/teamlogos/ncaa/500/41.png",
    "Arizona":"https://a.espncdn.com/i/teamlogos/ncaa/500/12.png",
    "Villanova":"https://a.espncdn.com/i/teamlogos/ncaa/500/222.png",
    "Wisconsin":"https://a.espncdn.com/i/teamlogos/ncaa/500/275.png",
    "Arkansas":"https://a.espncdn.com/i/teamlogos/ncaa/500/8.png",
    "BYU":"https://a.espncdn.com/i/teamlogos/ncaa/500/252.png",
    "Gonzaga":"https://a.espncdn.com/i/teamlogos/ncaa/500/2250.png",
    "Miami (Fla.)":"https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png",
    "Purdue":"https://a.espncdn.com/i/teamlogos/ncaa/500/2509.png",
    "Florida":"https://a.espncdn.com/i/teamlogos/ncaa/500/57.png",
    "Clemson":"https://a.espncdn.com/i/teamlogos/ncaa/500/228.png",
    "Vanderbilt":"https://a.espncdn.com/i/teamlogos/ncaa/500/238.png",
    "Nebraska":"https://a.espncdn.com/i/teamlogos/ncaa/500/158.png",
    "North Carolina":"https://a.espncdn.com/i/teamlogos/ncaa/500/153.png",
    "Illinois":"https://a.espncdn.com/i/teamlogos/ncaa/500/356.png",
    "Saint Mary's":"https://a.espncdn.com/i/teamlogos/ncaa/500/2608.png",
    "Houston":"https://a.espncdn.com/i/teamlogos/ncaa/500/248.png",
    "Michigan":"https://a.espncdn.com/i/teamlogos/ncaa/500/130.png",
    "Georgia":"https://a.espncdn.com/i/teamlogos/ncaa/500/61.png",
    "Texas Tech":"https://a.espncdn.com/i/teamlogos/ncaa/500/2641.png",
    "Alabama":"https://a.espncdn.com/i/teamlogos/ncaa/500/333.png",
    "Tennessee":"https://a.espncdn.com/i/teamlogos/ncaa/500/2633.png",
    "Virginia":"https://a.espncdn.com/i/teamlogos/ncaa/500/258.png",
    "Kentucky":"https://a.espncdn.com/i/teamlogos/ncaa/500/96.png",
    "Iowa State":"https://a.espncdn.com/i/teamlogos/ncaa/500/66.png",
    "Siena":"https://a.espncdn.com/i/teamlogos/ncaa/500/2561.png",
    "TCU":"https://a.espncdn.com/i/teamlogos/ncaa/500/2628.png",
    "UNI":"https://a.espncdn.com/i/teamlogos/ncaa/500/2269.png",
    "Cal Baptist":"https://a.espncdn.com/i/teamlogos/ncaa/500/2856.png",
    "South Florida":"https://a.espncdn.com/i/teamlogos/ncaa/500/58.png",
    "North Dakota State":"https://a.espncdn.com/i/teamlogos/ncaa/500/2449.png",
    "UCF":"https://a.espncdn.com/i/teamlogos/ncaa/500/2116.png",
    "Furman":"https://a.espncdn.com/i/teamlogos/ncaa/500/231.png",
    "Long Island University":"https://a.espncdn.com/i/teamlogos/ncaa/500/2085.png",
    "Utah State":"https://a.espncdn.com/i/teamlogos/ncaa/500/328.png",
    "High Point":"https://a.espncdn.com/i/teamlogos/ncaa/500/2272.png",
    "Hawai'i":"https://a.espncdn.com/i/teamlogos/ncaa/500/62.png",
    "Texas":"https://a.espncdn.com/i/teamlogos/ncaa/500/251.png",
    "Kennesaw State":"https://a.espncdn.com/i/teamlogos/ncaa/500/2509.png",
    "Missouri":"https://a.espncdn.com/i/teamlogos/ncaa/500/142.png",
    "Queens":"https://a.espncdn.com/i/teamlogos/ncaa/500/2931.png",
    "Prairie View A&M":"https://a.espncdn.com/i/teamlogos/ncaa/500/2504.png",
    "Iowa":"https://a.espncdn.com/i/teamlogos/ncaa/500/2294.png",
    "McNeese":"https://a.espncdn.com/i/teamlogos/ncaa/500/2383.png",
    "Troy":"https://a.espncdn.com/i/teamlogos/ncaa/500/2653.png",
    "VCU":"https://a.espncdn.com/i/teamlogos/ncaa/500/2670.png",
    "Penn":"https://a.espncdn.com/i/teamlogos/ncaa/500/219.png",
    "Texas A&M":"https://a.espncdn.com/i/teamlogos/ncaa/500/245.png",
    "Idaho":"https://a.espncdn.com/i/teamlogos/ncaa/500/70.png",
    "Howard":"https://a.espncdn.com/i/teamlogos/ncaa/500/47.png",
    "Saint Louis":"https://a.espncdn.com/i/teamlogos/ncaa/500/139.png",
    "Akron":"https://a.espncdn.com/i/teamlogos/ncaa/500/2006.png",
    "Hofstra":"https://a.espncdn.com/i/teamlogos/ncaa/500/2259.png",
    "Miami (Ohio)":"https://a.espncdn.com/i/teamlogos/ncaa/500/193.png",
    "Wright State":"https://a.espncdn.com/i/teamlogos/ncaa/500/2714.png",
    "Santa Clara":"https://a.espncdn.com/i/teamlogos/ncaa/500/2608.png",
    "Tennessee State":"https://a.espncdn.com/i/teamlogos/ncaa/500/2634.png",
}

def team_bg(team): return TEAM_COLORS.get(team, ("#005EB8","#FFFFFF"))[0]
def team_fg(team): return TEAM_COLORS.get(team, ("#005EB8","#FFFFFF"))[1]

PLOT_LAYOUT = dict(
    paper_bgcolor='#0d1b2a', plot_bgcolor='#112240',
    font=dict(color='#c8dff0', family='Arial'),
    title_font=dict(color='#ffffff', size=16, family='Arial Black'),
    legend=dict(bgcolor='#112240', bordercolor='#1e3a5f', borderwidth=1,
                font=dict(color='#c8dff0')),
    margin=dict(t=60, b=40, l=40, r=40),
)

def apply_theme(fig):
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(gridcolor='#1e3a5f', tickfont=dict(color='#c8dff0'),
                     title_font=dict(color='#8ab0cc'))
    fig.update_yaxes(gridcolor='#1e3a5f', tickfont=dict(color='#c8dff0'),
                     title_font=dict(color='#8ab0cc'))
    return fig

# ── Separate cached queries for performance ───────────────────────────────────
@st.cache_data(ttl=3600)
def load_predictions():
    df = pd.read_csv(os.path.join(DATA_DIR, 'predictions.csv'))
    df['match_time'] = pd.to_datetime(df['match_time'])
    return df

@st.cache_data(ttl=3600)
def load_slots():
    return pd.read_csv(os.path.join(DATA_DIR, 'slots.csv'))

@st.cache_data(ttl=3600)
def load_champs():
    df = pd.read_csv(os.path.join(DATA_DIR, 'brackets.csv'))
    return df[['bracket_name','bracket_creator','champion']]


def main():
    # ── HEADER WITH ALL 64 TEAM LOGOS ───────────────────────────────────────
    col_title, col_logos = st.columns([2, 3])
    with col_title:
        st.markdown("# Pool Visualisations")
        st.markdown('<div style="font-size:0.75rem;color:#4da6ff;font-weight:700;'
                    'letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.3rem;">'
                    'March Madness 2026 — Data & Analysis</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.82rem;color:#8ab0cc;font-style:italic;'
            'margin-bottom:0.8rem;max-width:520px;line-height:1.5;">'
            "Not a numbers person? Perfect — you\'re exactly who this page was built for. "
            "We took the cold, lifeless spreadsheet data and turned it into "
            '<b style="color:#c8dff0;">gorgeous, colour-coded charts</b> ' 
            "that even your bracket-busting uncle can understand. "
            "Scroll down, look at the pretty colours, and pretend you knew "
            "what was going to happen all along. You\'re welcome."
            '</div>', unsafe_allow_html=True)
    with col_logos:
        items = ""
        for team, url in ALL_TEAM_LOGOS.items():
            tc = team_bg(team)
            items += (f'<div style="display:inline-flex;flex-direction:column;'
                      f'align-items:center;gap:2px;margin:3px;">'
                      f'<img src="{url}" style="width:36px;height:36px;object-fit:contain;'
                      f'border-radius:50%;background:#ffffff;padding:2px;'
                      f'border:2px solid {tc};" />'
                      f'</div>')
        st.markdown(f'<div style="display:flex;flex-wrap:wrap;justify-content:center;'
                    f'align-items:center;padding:6px 0;">{items}</div>',
                    unsafe_allow_html=True)

    try:
        with st.spinner("Loading data..."):
            predictions = load_predictions()
            all_slots   = load_slots()
            champs      = load_champs()
    except Exception as e:
        st.error(f"Could not load data files: {e}")
        st.stop()

    # ── CHART 1: SLOT PICKER ─────────────────────────────────────────────────
    st.divider()
    st.markdown("## Who Did the Pool Predict?")
    st.caption("Select any matchup to see how the pool split their predictions.")

    # Include ALL slots with both teams known (extends to slot 63)
    slot_options = {}
    for _, row in all_slots.iterrows():
        sid = int(row['slot_id'])
        rnd = ROUND_NAMES.get(int(row['round']), f"Round {row['round']}")
        # For known matchups use team names; for undecided use round/region label
        if pd.notna(row.get('team_1')) and pd.notna(row.get('team_2')):
            label = f"Slot {sid} — {rnd} ({row['region']}): {row['team_1']} vs {row['team_2']}"
        else:
            # Check if predictions exist for this slot
            if sid in predictions['slot_id'].values:
                region = row['region'] if pd.notna(row.get('region')) else ''
                label = f"Slot {sid} — {rnd} ({region}): TBD vs TBD"
            else:
                continue
        slot_options[label] = sid

    if slot_options:
        selected_label = st.selectbox("Select matchup", list(slot_options.keys()))
        selected_sid   = slot_options[selected_label]
        slot_preds     = predictions[predictions['slot_id'] == selected_sid]

        if len(slot_preds) > 0:
            pred_counts   = slot_preds['predicted_winner'].value_counts().reset_index()
            pred_counts.columns = ['Team','Count']
            actual_winner = (slot_preds['actual_winner'].iloc[0]
                             if pd.notna(slot_preds['actual_winner'].iloc[0]) else None)
            pie_colors = [team_bg(t) for t in pred_counts['Team']]

            col1, col2 = st.columns([1.2, 1])
            with col1:
                fig_pie = go.Figure(go.Pie(
                    labels=pred_counts['Team'], values=pred_counts['Count'], hole=0.45,
                    marker=dict(colors=pie_colors, line=dict(color='#0d1b2a', width=3)),
                    textinfo='label+percent', textfont=dict(size=13, color='#ffffff'),
                    hovertemplate='<b>%{label}</b><br>%{value} brackets (%{percent})<extra></extra>'
                ))
                fig_pie.update_layout(**PLOT_LAYOUT,
                    title=f"Slot {selected_sid} — {ROUND_NAMES.get(int(all_slots[all_slots['slot_id']==selected_sid]['round'].iloc[0]), '')} Predictions", showlegend=True, height=400,
                    annotations=[dict(text=f"{pred_counts['Count'].sum()}<br>brackets",
                                      x=0.5, y=0.5, font_size=14,
                                      font_color='#c8dff0', showarrow=False)])
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                st.markdown("**Prediction breakdown:**")
                total_p = pred_counts['Count'].sum()
                for _, row in pred_counts.iterrows():
                    icon  = ("Correct" if actual_winner and row['Team'] == actual_winner
                             else ("Incorrect" if actual_winner else ""))
                    color = ("#56d364" if icon=="Correct" else
                             ("#f28b82" if icon=="Incorrect" else "#c8dff0"))
                    tc  = team_bg(row['Team'])
                    pct = round(row['Count'] / total_p * 100, 1)
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:8px;margin:0.4rem 0;">'
                        f'<div style="width:14px;height:14px;border-radius:3px;'
                        f'background:{tc};flex-shrink:0;"></div>'
                        f'<div style="color:{color};font-size:0.95rem;"><b>{row["Team"]}</b> — '
                        f'{row["Count"]} brackets ({pct}%)'
                        f'{"  Correct" if icon=="Correct" else ("  Incorrect" if icon=="Incorrect" else "")}'
                        f'</div></div>', unsafe_allow_html=True)
                if actual_winner:
                    st.markdown(
                        f'<div style="margin-top:1rem;padding:0.5rem;background:#112240;'
                        f'border:1px solid #005EB8;border-radius:6px;color:#c8dff0;">'
                        f'Actual result: <b style="color:#56d364;">{actual_winner}</b> won</div>',
                        unsafe_allow_html=True)

    # ── CHART 2: BUST ANALYSIS ────────────────────────────────────────────────
    st.divider()
    st.markdown("## Bust Analysis — First Wrong Prediction Per Bracket")
    st.caption("The first game each bracket got wrong, sorted by who survived the longest.")

    incorrect = predictions[predictions['result'] == 'Incorrect'].copy()
    if len(incorrect) > 0:
        match_rank = (predictions[predictions['match_time'].notna()]
                      [['slot_id','match_time']].drop_duplicates()
                      .sort_values('match_time').reset_index(drop=True))
        match_rank['match_number'] = match_rank.index + 1
        slot_to_num = dict(zip(match_rank['slot_id'], match_rank['match_number']))

        bust_data = []
        for bracket_name, grp in incorrect.groupby('bracket_name'):
            creator    = grp['bracket_creator'].iloc[0]
            first_bust = grp.sort_values('match_time').iloc[0]
            bust_data.append({
                'Match No.':     slot_to_num.get(first_bust['slot_id'], 0),
                'Bracket':       bracket_name,
                'Busted By':     first_bust['predicted_winner'],
                'Actual Winner': first_bust['actual_winner'],
                'Round':         ROUND_NAMES.get(int(first_bust['round']), ''),
                'match_time':    first_bust['match_time'],
            })

        bust_df = (pd.DataFrame(bust_data)
                   .sort_values('Match No.', ascending=False)
                   .reset_index(drop=True))

        bust_counts = bust_df['Busted By'].value_counts().reset_index()
        bust_counts.columns = ['Team','Count']
        total_busted = bust_counts['Count'].sum()
        bust_counts['Pct'] = (bust_counts['Count'] / total_busted * 100).round(1)
        pie_colors_b = [team_bg(t) for t in bust_counts['Team']]

        col1, col2 = st.columns([1, 1.2])
        with col1:
            fig_bust = go.Figure(go.Pie(
                labels=bust_counts['Team'], values=bust_counts['Count'], hole=0.35,
                marker=dict(colors=pie_colors_b, line=dict(color='#0d1b2a', width=2)),
                textinfo='label+percent',
                textfont=dict(size=11, color='#ffffff'),
                hovertemplate='<b>%{label}</b><br>Busted %{value} brackets (%{percent})<extra></extra>',
                showlegend=False,
            ))
            fig_bust.update_layout(**PLOT_LAYOUT,
                title="Which Team First Busted Each Bracket", height=420,
                annotations=[dict(text=f"{total_busted}<br>busted",
                                  x=0.5, y=0.5, font_size=13,
                                  font_color='#c8dff0', showarrow=False)])
            st.plotly_chart(fig_bust, use_container_width=True)

        with col2:
            st.markdown("**First bust per bracket (survived longest first):**")
            table_html = (
                '<table style="width:100%;border-collapse:collapse;font-size:0.8rem;">'
                '<thead><tr style="background:#1e3a5f;color:#c8dff0;">'
                '<th style="padding:6px 8px;text-align:left;">Match No.</th>'
                '<th style="padding:6px 8px;text-align:left;">Bracket</th>'
                '<th style="padding:6px 8px;text-align:left;">Busted By</th>'
                '<th style="padding:6px 8px;text-align:left;">Round</th>'
                '</tr></thead><tbody>')
            for i, row in bust_df.iterrows():
                is_top = (i == 0)
                tc = team_bg(row['Busted By']); fc = team_fg(row['Busted By'])
                row_style = ('background:#0d3320;color:#56d364;font-weight:700;' if is_top
                             else ('background:#0d1b2a;color:#c8dff0;' if i % 2 == 0
                                   else 'background:#112240;color:#c8dff0;'))
                bracket_label = (f'&#127881; {row["Bracket"]}' if is_top
                                 else row['Bracket'])
                table_html += (
                    f'<tr style="{row_style}">'
                    f'<td style="padding:5px 8px;">{row["Match No."]}</td>'
                    f'<td style="padding:5px 8px;">{bracket_label}</td>'
                    f'<td style="padding:5px 8px;">'
                    f'<span style="background:{tc};color:{fc};padding:1px 6px;'
                    f'border-radius:3px;font-size:0.74rem;font-weight:700;">'
                    f'{row["Busted By"]}</span></td>'
                    f'<td style="padding:5px 8px;">{row["Round"]}</td>'
                    f'</tr>')
            table_html += '</tbody></table>'
            st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("No incorrect predictions yet.")

    # ── CHART 3: BIGGEST UPSETS ───────────────────────────────────────────────
    st.divider()
    st.markdown("## Biggest Upsets")
    st.caption("Results that the fewest brackets predicted.")

    completed = predictions[predictions['actual_winner'].notna()].copy()
    if len(completed) > 0:
        upset_data = []
        for slot_id, grp in completed.groupby('slot_id'):
            actual   = grp['actual_winner'].iloc[0]
            total    = len(grp); correct = grp['correct'].sum()
            pct      = round(correct / total * 100, 1) if total > 0 else 0
            rnd      = ROUND_NAMES.get(int(grp['round'].iloc[0]), '')
            region   = grp['region'].iloc[0]
            loser_r  = grp[grp['predicted_winner'] != actual]
            loser    = (loser_r['predicted_winner'].mode().iloc[0]
                        if len(loser_r) > 0 else '?')
            upset_data.append({
                'slot_id': int(slot_id), 'Round': rnd, 'Region': region,
                'Winner': actual, 'Expected Winner': loser,
                '% Predicted': pct,
                'correct_brackets': grp[grp['correct']==1]['bracket_name'].tolist(),
            })

        upset_df = pd.DataFrame(upset_data).sort_values('% Predicted')
        top10 = upset_df.head(5)
        bar_colors = [team_bg(row['Winner']) for _, row in top10.iterrows()]

        fig_upset = go.Figure(go.Bar(
            x=top10['% Predicted'],
            y=[f"{row['Winner']} over {row['Expected Winner']}  ({row['Round']} · {row['Region']})"
               for _, row in top10.iterrows()],
            orientation='h',
            marker=dict(color=bar_colors, line=dict(color='#0d1b2a', width=1)),
            text=[f"{pct}%" for pct in top10['% Predicted']],
            textposition='outside', textfont=dict(color='#c8dff0', size=11),
            hovertemplate='<b>%{y}</b><br>%{x}% predicted<extra></extra>'
        ))
        fig_upset.update_layout(**PLOT_LAYOUT,
            title="Top 5 Least Predicted Results",
            xaxis_title="% of Brackets That Predicted This Result",
            yaxis=dict(autorange='reversed'), height=300, xaxis=dict(range=[0,115]))
        st.plotly_chart(apply_theme(fig_upset), use_container_width=True)

        st.markdown("**Top 3 biggest upsets:**")
        cols = st.columns(3)
        for i, (_, row) in enumerate(upset_df.head(3).iterrows()):
            with cols[i]:
                tc = team_bg(row['Winner']); fc = team_fg(row['Winner'])
                cb = row['correct_brackets']
                congrats = (f'<div style="font-size:0.65rem;color:#56d364;margin-top:0.5rem;'
                            f'font-style:italic;">Congrats: {", ".join(cb)}</div>'
                            if cb else
                            f'<div style="font-size:0.65rem;color:#8ab0cc;margin-top:0.5rem;'
                            f'font-style:italic;">No brackets predicted this</div>')
                st.markdown(
                    f'<div style="background:#112240;border:1px solid {tc};border-radius:8px;'
                    f'padding:0.8rem;text-align:center;">'
                    f'<div style="font-size:0.7rem;color:#8ab0cc;font-weight:700;'
                    f'text-transform:uppercase;">{row["Round"]} · {row["Region"]}</div>'
                    f'<div style="background:{tc};color:{fc};font-size:1.1rem;font-weight:800;'
                    f'margin:0.4rem 0;padding:4px 8px;border-radius:4px;">{row["Winner"]}</div>'
                    f'<div style="font-size:0.8rem;color:#8ab0cc;">over {row["Expected Winner"]}</div>'
                    f'<div style="font-size:1.4rem;font-weight:800;color:#c8a951;margin-top:0.4rem;">'
                    f'{row["% Predicted"]}%</div>'
                    f'<div style="font-size:0.7rem;color:#8ab0cc;">of brackets predicted this</div>'
                    f'{congrats}</div>', unsafe_allow_html=True)
    else:
        st.info("No completed results yet.")

    # ── CHART 4: AVG PREDICTED ROUND ELIMINATED ───────────────────────────────
    st.divider()
    st.markdown("## Average Predicted Round Eliminated")
    st.caption("How far did the pool collectively predict each team would go?")

    elim_data = predictions[predictions['predicted_loser'].notna()].copy()
    if len(elim_data) > 0:
        avg_elim = (elim_data.groupby('predicted_loser')['round']
                    .mean().round(1).reset_index())
        avg_elim.columns = ['Team','Avg Round Eliminated']
        avg_elim = avg_elim.sort_values('Avg Round Eliminated', ascending=False)

        # Default highlight = none, moved inline below chart
        selected_team = st.selectbox(
            "Highlight a team",
            ["None"] + sorted(avg_elim['Team'].tolist()),
            key="elim_team_select")

        bar_colors = []
        for _, r in avg_elim.iterrows():
            is_sel = (selected_team != "None" and r['Team'] == selected_team)
            bar_colors.append('#c8a951' if is_sel else team_bg(r['Team']))

        fig_elim = go.Figure(go.Bar(
            x=avg_elim['Team'], y=avg_elim['Avg Round Eliminated'],
            marker=dict(color=bar_colors, line=dict(color='#0d1b2a', width=1)),
            text=avg_elim['Avg Round Eliminated'].apply(lambda x: f"{x:.1f}"),
            textposition='outside', textfont=dict(color='#c8dff0', size=10),
            hovertemplate='<b>%{x}</b><br>Avg round eliminated: %{y:.1f}<extra></extra>'
        ))
        for rnd, name in ROUND_NAMES.items():
            fig_elim.add_hline(y=rnd, line_dash='dot', line_color='#1e3a5f',
                               annotation_text=name,
                               annotation_font=dict(color='#4da6ff', size=9),
                               annotation_position='right')
        fig_elim.update_layout(**PLOT_LAYOUT,
            title="Average Round Each Team Was Predicted to be Eliminated",
            xaxis_title="Team", yaxis_title="Average Round Eliminated",
            yaxis=dict(range=[0,7], tickvals=list(range(1,7)),
                       ticktext=[ROUND_NAMES[i] for i in range(1,7)]),
            height=500, xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig_elim), use_container_width=True)

        # Color swatches
        swatch_html = '<div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:0.3rem;">'
        for _, r in avg_elim.iterrows():
            tc = team_bg(r['Team']); fc = team_fg(r['Team'])
            swatch_html += (f'<div style="background:{tc};color:{fc};padding:2px 7px;'
                            f'border-radius:4px;font-size:0.63rem;font-weight:700;">{r["Team"]}</div>')
        swatch_html += '</div>'
        st.markdown(swatch_html, unsafe_allow_html=True)

        if selected_team != "None":
            team_row = avg_elim[avg_elim['Team'] == selected_team]
            if len(team_row) > 0:
                avg_rnd = team_row.iloc[0]['Avg Round Eliminated']
                tc = team_bg(selected_team)
                st.markdown(
                    f'<div style="margin-top:0.6rem;background:#112240;border:1px solid {tc};'
                    f'border-radius:8px;padding:0.8rem 1.2rem;display:inline-block;">'
                    f'<b style="color:{tc};">{selected_team}</b> — '
                    f'average predicted elimination: <b style="color:#ffffff;">{avg_rnd:.1f}</b> '
                    f'<span style="color:#8ab0cc;">({ROUND_NAMES.get(round(avg_rnd), "")})</span>'
                    f'</div>', unsafe_allow_html=True)
    else:
        st.info("No elimination data available yet.")

    # ── CHART 5: GAME IMPACT HEATMAP ─────────────────────────────────────────
    st.divider()
    st.markdown("## Game Impact Heatmap")
    st.caption("How much each Sweet 16 matchup matters to each bracket — populated from the simulator.")

    sim = st.session_state.get('sim_results', None)
    if sim is None:
        st.info("Run the simulator on the main page first, then come back here to see the heatmap.")
    else:
        game_impacts  = sim['game_impacts']
        baseline      = sim['baseline']
        bracket_ids   = sim['bracket_ids']
        bracket_names = sim['bracket_names']
        team_name_map = sim['team_name_map']
        forced        = sim['forced_outcomes']
        scores_sim    = sim['scores']

        sort_order = np.argsort(-baseline)
        sorted_brackets = [bracket_names[bracket_ids[i]] for i in sort_order]

        # Build matrix: rows = brackets, cols = games
        game_labels = []
        matrix_data = []
        for g in game_impacts:
            is_forced = g['slot_id'] in forced
            t1 = g['team_1_name']; t2 = g['team_2_name']
            game_labels.append(f"{t1} vs {t2}")
            col_vals = []
            for idx in sort_order:
                if is_forced:
                    col_vals.append(0.0)
                else:
                    col_vals.append(float(np.abs(g['swing'][idx]) * 100))
            matrix_data.append(col_vals)

        z = np.array(matrix_data).T  # rows=brackets, cols=games

        fig_heat = go.Figure(go.Heatmap(
            z=z,
            x=game_labels,
            y=sorted_brackets,
            colorscale=[[0,'#0a1f3d'],[0.3,'#1a4a8a'],[0.6,'#8b1a1a'],[1,'#cc2200']],
            hovertemplate='<b>%{y}</b><br>%{x}<br>Swing: %{z:.2f}%<extra></extra>',
            colorbar=dict(
                title=dict(text='Swing %', font=dict(color='#c8dff0')),
                tickfont=dict(color='#c8dff0'))
        ))
        heat_layout = {**PLOT_LAYOUT}
        heat_layout['margin'] = dict(t=120, b=40, l=40, r=40)
        fig_heat.update_layout(**heat_layout,
            title=dict(text="Game Impact Heatmap — Swing % per Bracket",
                       y=0.98, yanchor='top'),
            xaxis_tickangle=-40,
            height=max(450, len(sorted_brackets) * 20),
            xaxis=dict(side='top', tickfont=dict(size=10)))
        st.plotly_chart(apply_theme(fig_heat), use_container_width=True)
        st.caption("Color intensity = how much that game's outcome swings each bracket's win probability. "
                   "Forced games show as 0.")

    # ── CHART 6: CHAMPION PICK BREAKDOWN ─────────────────────────────────────
    st.divider()
    st.markdown("## Champion Pick Breakdown")
    st.caption("Which teams did the pool pick to win it all?")

    champ_counts = champs['champion'].value_counts().reset_index()
    champ_counts.columns = ['Team','Count']
    champ_colors = [team_bg(t) for t in champ_counts['Team']]

    col1, col2 = st.columns([1.3, 1])
    with col1:
        fig_champ = go.Figure(go.Pie(
            labels=champ_counts['Team'], values=champ_counts['Count'], hole=0.4,
            marker=dict(colors=champ_colors, line=dict(color='#0d1b2a', width=2)),
            textinfo='label+percent', textfont=dict(size=12, color='#ffffff'),
            hovertemplate='<b>%{label}</b><br>%{value} brackets (%{percent})<extra></extra>'
        ))
        fig_champ.update_layout(**PLOT_LAYOUT,
            title="Championship Picks Across All Brackets", height=440,
            annotations=[dict(text=f"{champ_counts['Count'].sum()}<br>brackets",
                              x=0.5, y=0.5, font_size=14,
                              font_color='#c8dff0', showarrow=False)])
        st.plotly_chart(fig_champ, use_container_width=True)

    with col2:
        st.markdown("**Picks breakdown:**")
        # HTML legend with logos
        for _, row in champ_counts.iterrows():
            tc  = team_bg(row['Team']); fc = team_fg(row['Team'])
            pct = round(row['Count'] / champ_counts['Count'].sum() * 100, 1)
            logo_url = TEAM_LOGOS.get(row['Team'], '')
            logo_html = (f'<img src="{logo_url}" style="width:28px;height:28px;'
                         f'object-fit:contain;border-radius:50%;background:#ffffff;'
                         f'padding:2px;border:1px solid {tc};" />'
                         if logo_url else
                         f'<div style="width:28px;height:28px;border-radius:50%;'
                         f'background:{tc};"></div>')
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;margin:0.45rem 0;">'
                f'{logo_html}'
                f'<div style="flex:1;">'
                f'<span style="background:{tc};color:{fc};padding:2px 8px;border-radius:4px;'
                f'font-size:0.8rem;font-weight:700;">{row["Team"]}</span>'
                f'<span style="color:#8ab0cc;font-size:0.8rem;margin-left:6px;">'
                f'{row["Count"]} brackets ({pct}%)</span>'
                f'</div></div>', unsafe_allow_html=True)


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
