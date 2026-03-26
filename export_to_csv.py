"""
Export SQL Server data to CSV files for static demo deployment.
Run this once: python export_to_csv.py
"""

import pyodbc
import pandas as pd
import os

SERVER   = r'localhost\SQLEXPRESS'
DATABASE = 'MarchMadness2026'
SCHEMA   = 'mm'

os.makedirs('data', exist_ok=True)

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;",
    autocommit=True)

print("Exporting data to CSV files...")

# Teams
df = pd.read_sql(f"SELECT team_id, team_name, seed, region FROM {SCHEMA}.Teams", conn)
df.to_csv('data/teams.csv', index=False)
print(f"  teams.csv — {len(df)} rows")

# Tournament slots
df = pd.read_sql(f"""
    SELECT ts.slot_id, ts.round, ts.region, ts.match_time, ts.potential_points,
           ts.team_1_id, ts.team_2_id, ts.actual_winner_id, ts.actual_loser_id,
           t1.team_name AS team_1, t2.team_name AS team_2,
           aw.team_name AS actual_winner, al.team_name AS actual_loser
    FROM {SCHEMA}.Tournament_Slots ts
    LEFT JOIN {SCHEMA}.Teams t1 ON ts.team_1_id = t1.team_id
    LEFT JOIN {SCHEMA}.Teams t2 ON ts.team_2_id = t2.team_id
    LEFT JOIN {SCHEMA}.Teams aw ON ts.actual_winner_id = aw.team_id
    LEFT JOIN {SCHEMA}.Teams al ON ts.actual_loser_id = al.team_id
    ORDER BY ts.slot_id
""", conn)
df.to_csv('data/slots.csv', index=False)
print(f"  slots.csv — {len(df)} rows")

# Bracket contestants
df = pd.read_sql(f"""
    SELECT bc.bracket_id, bc.bracket_name, bc.bracket_creator,
           bc.predicted_tournament_winner, t.team_name AS champion
    FROM {SCHEMA}.Bracket_Contestants bc
    JOIN {SCHEMA}.Teams t ON bc.predicted_tournament_winner = t.team_id
""", conn)
df['bracket_name'] = df['bracket_name'].replace(
    'The ghost of Ali Khamenei', 'oh! what a lovely bracket')
df.to_csv('data/brackets.csv', index=False)
print(f"  brackets.csv — {len(df)} rows")

# Predictions (full join — main data source)
df = pd.read_sql(f"""
    SELECT bc.bracket_id, bc.bracket_name, bc.bracket_creator,
           bp.slot_id, ts.round, ts.region, ts.match_time, ts.potential_points,
           t1.team_name AS team_1, t2.team_name AS team_2,
           pw.team_name AS predicted_winner, pl.team_name AS predicted_loser,
           aw.team_name AS actual_winner, al.team_name AS actual_loser,
           CASE WHEN ts.actual_winner_id = bp.predicted_winner_id THEN 1 ELSE 0 END AS correct,
           CASE WHEN ts.actual_winner_id IS NULL THEN 'Not Played'
                WHEN ts.actual_winner_id = bp.predicted_winner_id THEN 'Correct'
                ELSE 'Incorrect' END AS result
    FROM {SCHEMA}.Bracket_Predictions bp
    JOIN {SCHEMA}.Bracket_Contestants bc ON bp.bracket_id = bc.bracket_id
    JOIN {SCHEMA}.Tournament_Slots ts    ON bp.slot_id = ts.slot_id
    LEFT JOIN {SCHEMA}.Teams t1 ON ts.team_1_id = t1.team_id
    LEFT JOIN {SCHEMA}.Teams t2 ON ts.team_2_id = t2.team_id
    LEFT JOIN {SCHEMA}.Teams pw ON bp.predicted_winner_id = pw.team_id
    LEFT JOIN {SCHEMA}.Teams pl ON bp.predicted_loser_id  = pl.team_id
    LEFT JOIN {SCHEMA}.Teams aw ON ts.actual_winner_id    = aw.team_id
    LEFT JOIN {SCHEMA}.Teams al ON ts.actual_loser_id     = al.team_id
""", conn)
df['bracket_name'] = df['bracket_name'].replace(
    'The ghost of Ali Khamenei', 'oh! what a lovely bracket')
df.to_csv('data/predictions.csv', index=False)
print(f"  predictions.csv — {len(df)} rows")

# Picks (unplayed only — for simulation)
picks = df[df['actual_winner'].isna()][['bracket_id','slot_id','predicted_winner']].copy()
# Map predicted_winner name back to team_id
teams = pd.read_sql(f"SELECT team_id, team_name FROM {SCHEMA}.Teams", conn)
name_to_id = dict(zip(teams['team_name'], teams['team_id']))
picks['predicted_winner_id'] = picks['predicted_winner'].map(name_to_id)
picks[['bracket_id','slot_id','predicted_winner_id']].to_csv('data/picks.csv', index=False)
print(f"  picks.csv — {len(picks)} rows")

# Team strengths
df = pd.read_sql(f"""
    SELECT t.team_id, t.team_name, ts.kenpom_net_rating
    FROM {SCHEMA}.Team_Strengths ts
    JOIN {SCHEMA}.Teams t ON ts.team_id = t.team_id
""", conn)
df.to_csv('data/strengths.csv', index=False)
print(f"  strengths.csv — {len(df)} rows")

# Current scores
df = pd.read_sql(f"""
    SELECT bc.bracket_id, bc.bracket_name, bc.bracket_creator,
           COALESCE(SUM(CASE WHEN ts.actual_winner_id = bp.predicted_winner_id
                        THEN ts.potential_points ELSE 0 END), 0) AS current_score
    FROM {SCHEMA}.Bracket_Contestants bc
    JOIN {SCHEMA}.Bracket_Predictions bp ON bc.bracket_id = bp.bracket_id
    JOIN {SCHEMA}.Tournament_Slots    ts ON bp.slot_id    = ts.slot_id
    GROUP BY bc.bracket_id, bc.bracket_name, bc.bracket_creator
""", conn)
df['bracket_name'] = df['bracket_name'].replace(
    'The ghost of Ali Khamenei', 'oh! what a lovely bracket')
df.to_csv('data/scores.csv', index=False)
print(f"  scores.csv — {len(df)} rows")

conn.close()
print("\nAll done! Run: streamlit run dashboard_demo.py")
