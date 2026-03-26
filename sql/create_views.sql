USE MarchMadness2026;
GO

-- ============================================================
-- CREATE ALL VIEWS FOR MarchMadness2026
-- ============================================================

-- ── VIEW 1: vw_Slots ─────────────────────────────────────────
-- Tournament slots with all team names instead of IDs
CREATE OR ALTER VIEW mm.vw_Slots AS
SELECT
    ts.slot_id,
    ts.round,
    ts.region,
    ts.team_1_id,
    t1.team_name       AS team_1_name,
    t1.seed            AS team_1_seed,
    ts.team_2_id,
    t2.team_name       AS team_2_name,
    t2.seed            AS team_2_seed,
    ts.actual_winner_id,
    tw.team_name       AS actual_winner_name,
    tw.seed            AS actual_winner_seed,
    ts.actual_loser_id,
    tl.team_name       AS actual_loser_name,
    ts.potential_points,
    ts.match_time,
    CASE
        WHEN ts.actual_winner_id IS NOT NULL THEN 'Completed'
        WHEN ts.team_1_id IS NOT NULL        THEN 'Upcoming'
        ELSE                                      'TBD'
    END                AS match_status
FROM mm.Tournament_Slots ts
LEFT JOIN mm.Teams t1 ON ts.team_1_id       = t1.team_id
LEFT JOIN mm.Teams t2 ON ts.team_2_id       = t2.team_id
LEFT JOIN mm.Teams tw ON ts.actual_winner_id = tw.team_id
LEFT JOIN mm.Teams tl ON ts.actual_loser_id  = tl.team_id;
GO

-- ── VIEW 2: vw_Champion_Picks ────────────────────────────────
-- Bracket contestants with predicted champion name
CREATE OR ALTER VIEW mm.vw_Champion_Picks AS
SELECT
    bc.bracket_id,
    bc.bracket_name,
    bc.bracket_creator,
    bc.predicted_tournament_winner  AS predicted_champion_id,
    t.team_name                     AS predicted_champion_name,
    t.seed                          AS predicted_champion_seed,
    t.region                        AS predicted_champion_region,
    -- Flag if their pick is still alive
    CASE
        WHEN EXISTS (
            SELECT 1 FROM mm.Tournament_Slots ts
            WHERE ts.actual_loser_id = bc.predicted_tournament_winner
        ) THEN 'Eliminated'
        ELSE 'Still Alive'
    END AS champion_pick_status
FROM mm.Bracket_Contestants bc
LEFT JOIN mm.Teams t ON bc.predicted_tournament_winner = t.team_id;
GO

-- ── VIEW 3: vw_Predictions ───────────────────────────────────
-- Bracket predictions with all team names instead of IDs
CREATE OR ALTER VIEW mm.vw_Predictions AS
SELECT
    bp.prediction_id,
    bp.bracket_id,
    bc.bracket_name,
    bc.bracket_creator,
    bp.slot_id,
    ts.round,
    ts.region,
    ts.match_time,
    t1.team_name       AS team_1_name,
    t1.seed            AS team_1_seed,
    t2.team_name       AS team_2_name,
    t2.seed            AS team_2_seed,
    bp.predicted_winner_id,
    pw.team_name       AS predicted_winner_name,
    pw.seed            AS predicted_winner_seed,
    bp.predicted_loser_id,
    pl.team_name       AS predicted_loser_name,
    ts.actual_winner_id,
    aw.team_name       AS actual_winner_name,
    -- Was the prediction correct?
    CASE
        WHEN ts.actual_winner_id IS NULL          THEN 'Not Yet Played'
        WHEN ts.actual_winner_id = bp.predicted_winner_id THEN 'Correct'
        ELSE                                           'Incorrect'
    END                AS prediction_result,
    -- Points earned
    CASE
        WHEN ts.actual_winner_id = bp.predicted_winner_id THEN ts.potential_points
        ELSE 0
    END                AS points_earned
FROM mm.Bracket_Predictions bp
JOIN mm.Bracket_Contestants bc  ON bp.bracket_id        = bc.bracket_id
JOIN mm.Tournament_Slots    ts  ON bp.slot_id           = ts.slot_id
LEFT JOIN mm.Teams t1           ON ts.team_1_id         = t1.team_id
LEFT JOIN mm.Teams t2           ON ts.team_2_id         = t2.team_id
LEFT JOIN mm.Teams pw           ON bp.predicted_winner_id = pw.team_id
LEFT JOIN mm.Teams pl           ON bp.predicted_loser_id  = pl.team_id
LEFT JOIN mm.Teams aw           ON ts.actual_winner_id    = aw.team_id;
GO

-- ── VIEW 4: vw_Predicted_Elimination ────────────────────────
-- For each bracket, which round each team was predicted to be eliminated
-- (i.e. the round where they picked that team to lose)
CREATE OR ALTER VIEW mm.vw_Predicted_Elimination AS
SELECT
    bp.bracket_id,
    bc.bracket_name,
    bc.bracket_creator,
    bp.slot_id,
    ts.round           AS elimination_round,
    CASE ts.round
        WHEN 1 THEN 'Round of 64'
        WHEN 2 THEN 'Round of 32'
        WHEN 3 THEN 'Sweet 16'
        WHEN 4 THEN 'Elite 8'
        WHEN 5 THEN 'Final Four'
        WHEN 6 THEN 'Championship'
    END                AS elimination_round_name,
    ts.region,
    pl.team_id         AS eliminated_team_id,
    pl.team_name       AS eliminated_team_name,
    pl.seed            AS eliminated_team_seed,
    pw.team_name       AS predicted_winner_name,
    -- Did the elimination actually happen as predicted?
    CASE
        WHEN ts.actual_loser_id IS NULL                    THEN 'Not Yet Played'
        WHEN ts.actual_loser_id = bp.predicted_loser_id   THEN 'Correct'
        ELSE                                                    'Incorrect'
    END                AS elimination_result
FROM mm.Bracket_Predictions bp
JOIN mm.Bracket_Contestants bc  ON bp.bracket_id          = bc.bracket_id
JOIN mm.Tournament_Slots    ts  ON bp.slot_id             = ts.slot_id
LEFT JOIN mm.Teams pl           ON bp.predicted_loser_id  = pl.team_id
LEFT JOIN mm.Teams pw           ON bp.predicted_winner_id = pw.team_id
WHERE bp.predicted_loser_id IS NOT NULL;
GO

-- ── VIEW 5: vw_Bracket_Scores ────────────────────────────────
-- Scores broken down by round for each bracket
CREATE OR ALTER VIEW mm.vw_Bracket_Scores AS
SELECT
    bc.bracket_id,
    bc.bracket_name,
    bc.bracket_creator,
    -- Total score
    COALESCE(SUM(
        CASE WHEN ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS total_score,
    -- Round of 64
    COALESCE(SUM(
        CASE WHEN ts.round = 1 AND ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS r64_score,
    COALESCE(SUM(
        CASE WHEN ts.round = 1 AND ts.actual_winner_id IS NOT NULL
             THEN 1 ELSE 0 END), 0)                         AS r64_correct,
    -- Round of 32
    COALESCE(SUM(
        CASE WHEN ts.round = 2 AND ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS r32_score,
    COALESCE(SUM(
        CASE WHEN ts.round = 2 AND ts.actual_winner_id IS NOT NULL
             THEN 1 ELSE 0 END), 0)                         AS r32_correct,
    -- Sweet 16
    COALESCE(SUM(
        CASE WHEN ts.round = 3 AND ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS s16_score,
    COALESCE(SUM(
        CASE WHEN ts.round = 3 AND ts.actual_winner_id IS NOT NULL
             THEN 1 ELSE 0 END), 0)                         AS s16_correct,
    -- Elite 8
    COALESCE(SUM(
        CASE WHEN ts.round = 4 AND ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS e8_score,
    COALESCE(SUM(
        CASE WHEN ts.round = 4 AND ts.actual_winner_id IS NOT NULL
             THEN 1 ELSE 0 END), 0)                         AS e8_correct,
    -- Final Four
    COALESCE(SUM(
        CASE WHEN ts.round = 5 AND ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS ff_score,
    COALESCE(SUM(
        CASE WHEN ts.round = 5 AND ts.actual_winner_id IS NOT NULL
             THEN 1 ELSE 0 END), 0)                         AS ff_correct,
    -- Championship
    COALESCE(SUM(
        CASE WHEN ts.round = 6 AND ts.actual_winner_id = bp.predicted_winner_id
             THEN ts.potential_points ELSE 0 END), 0)       AS champ_score,
    COALESCE(SUM(
        CASE WHEN ts.round = 6 AND ts.actual_winner_id IS NOT NULL
             THEN 1 ELSE 0 END), 0)                         AS champ_correct,
    -- Max possible remaining score
    COALESCE(SUM(
        CASE WHEN ts.actual_winner_id IS NULL
             THEN ts.potential_points ELSE 0 END), 0)       AS max_remaining_score
FROM mm.Bracket_Contestants bc
JOIN mm.Bracket_Predictions bp ON bc.bracket_id = bp.bracket_id
JOIN mm.Tournament_Slots    ts ON bp.slot_id     = ts.slot_id
GROUP BY bc.bracket_id, bc.bracket_name, bc.bracket_creator;
GO


-- ── VIEW 8: vw_Team_Pick_Popularity ─────────────────────────
-- How many brackets picked each team to win each round
-- Includes all rounds (played and unplayed)
CREATE OR ALTER VIEW mm.vw_Team_Pick_Popularity AS
SELECT
    pw.team_id,
    pw.team_name,
    pw.seed,
    pw.region,
    ts.round,
    CASE ts.round
        WHEN 1 THEN 'Round of 64'
        WHEN 2 THEN 'Round of 32'
        WHEN 3 THEN 'Sweet 16'
        WHEN 4 THEN 'Elite 8'
        WHEN 5 THEN 'Final Four'
        WHEN 6 THEN 'Championship'
    END                             AS round_name,
    ts.potential_points,
    COUNT(bp.prediction_id)         AS num_brackets_picked,
    -- What % of brackets picked this team to win this round
    ROUND(COUNT(bp.prediction_id) * 100.0 /
        (SELECT COUNT(DISTINCT bracket_id) FROM mm.Bracket_Contestants), 1)
                                    AS pct_brackets_picked,
    -- Did they actually win this round?
    CASE
        WHEN ts.actual_winner_id IS NULL          THEN 'Not Yet Played'
        WHEN ts.actual_winner_id = pw.team_id     THEN 'Won'
        ELSE                                           'Lost'
    END                             AS actual_result,
    -- How many brackets got this pick correct
    SUM(CASE WHEN ts.actual_winner_id = pw.team_id THEN 1 ELSE 0 END)
                                    AS num_correct
FROM mm.Bracket_Predictions bp
JOIN mm.Tournament_Slots ts ON bp.slot_id             = ts.slot_id
JOIN mm.Teams pw            ON bp.predicted_winner_id = pw.team_id
GROUP BY
    pw.team_id, pw.team_name, pw.seed, pw.region,
    ts.round, ts.potential_points, ts.actual_winner_id;
GO

PRINT 'All views created successfully!';
GO

-- ── QUICK VERIFICATION QUERIES ───────────────────────────────
-- Uncomment to test each view:

-- SELECT * FROM mm.vw_Slots ORDER BY slot_id;
-- SELECT * FROM mm.vw_Champion_Picks ORDER BY bracket_creator;
-- SELECT * FROM mm.vw_Predictions WHERE round = 3 ORDER BY slot_id, bracket_name;
-- SELECT * FROM mm.vw_Predicted_Elimination ORDER BY bracket_name, elimination_round;
-- SELECT * FROM mm.vw_Bracket_Scores ORDER BY total_score DESC;
GO
