-- ============================================================
-- FIX team_1_id and team_2_id for slots 1-56
-- Uses subqueries to look up team_ids by name
-- ============================================================

USE MarchMadness2026;
GO

-- ── ROUND OF 64 (Slots 1-32) ─────────────────────────────────────────────────

UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Duke'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Siena') WHERE slot_id = 1;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Ohio State'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'TCU') WHERE slot_id = 2;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'St. John''s'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'UNI') WHERE slot_id = 3;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Kansas'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Cal Baptist') WHERE slot_id = 4;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Louisville'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'South Florida') WHERE slot_id = 5;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Michigan State'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'North Dakota State') WHERE slot_id = 6;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'UCLA'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'UCF') WHERE slot_id = 7;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'UConn'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Furman') WHERE slot_id = 8;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Arizona'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Long Island University') WHERE slot_id = 9;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Villanova'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Utah State') WHERE slot_id = 10;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Wisconsin'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'High Point') WHERE slot_id = 11;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Arkansas'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Hawai''i') WHERE slot_id = 12;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'BYU'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Texas') WHERE slot_id = 13;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Gonzaga'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Kennesaw State') WHERE slot_id = 14;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Miami (Fla.)'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Missouri') WHERE slot_id = 15;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Purdue'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Queens') WHERE slot_id = 16;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Florida'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Prairie View A&M') WHERE slot_id = 17;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Clemson'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Iowa') WHERE slot_id = 18;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Vanderbilt'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'McNeese') WHERE slot_id = 19;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Nebraska'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Troy') WHERE slot_id = 20;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'North Carolina'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'VCU') WHERE slot_id = 21;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Illinois'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Penn') WHERE slot_id = 22;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Saint Mary''s'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Texas A&M') WHERE slot_id = 23;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Houston'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Idaho') WHERE slot_id = 24;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Michigan'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Howard') WHERE slot_id = 25;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Georgia'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Saint Louis') WHERE slot_id = 26;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Texas Tech'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Akron') WHERE slot_id = 27;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Alabama'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Hofstra') WHERE slot_id = 28;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Tennessee'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Miami (Ohio)') WHERE slot_id = 29;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Virginia'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Wright State') WHERE slot_id = 30;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Kentucky'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Santa Clara') WHERE slot_id = 31;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Iowa State'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Tennessee State') WHERE slot_id = 32;

-- ── ROUND OF 32 (Slots 33-48) ────────────────────────────────────────────────

UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Duke'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'TCU') WHERE slot_id = 33;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'St. John''s'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Kansas') WHERE slot_id = 34;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Louisville'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Michigan State') WHERE slot_id = 35;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'UCLA'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'UConn') WHERE slot_id = 36;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Arizona'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Utah State') WHERE slot_id = 37;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'High Point'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Arkansas') WHERE slot_id = 38;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Texas'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Gonzaga') WHERE slot_id = 39;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Miami (Fla.)'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Purdue') WHERE slot_id = 40;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Florida'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Iowa') WHERE slot_id = 41;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Vanderbilt'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Nebraska') WHERE slot_id = 42;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'VCU'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Illinois') WHERE slot_id = 43;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Texas A&M'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Houston') WHERE slot_id = 44;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Michigan'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Saint Louis') WHERE slot_id = 45;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Texas Tech'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Alabama') WHERE slot_id = 46;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Tennessee'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Virginia') WHERE slot_id = 47;
UPDATE mm.Tournament_Slots SET team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Kentucky'), team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name = 'Iowa State') WHERE slot_id = 48;

GO

-- ── VERIFY ───────────────────────────────────────────────────────────────────
SELECT
    ts.slot_id, ts.round,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    tw.team_name AS actual_winner
FROM mm.Tournament_Slots ts
LEFT JOIN mm.Teams t1 ON ts.team_1_id = t1.team_id
LEFT JOIN mm.Teams t2 ON ts.team_2_id = t2.team_id
LEFT JOIN mm.Teams tw ON ts.actual_winner_id = tw.team_id
WHERE ts.slot_id BETWEEN 1 AND 56
ORDER BY ts.slot_id;
GO
