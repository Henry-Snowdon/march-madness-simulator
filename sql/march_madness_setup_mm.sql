-- ============================================================
-- MARCH MADNESS POOL DATABASE - SQL SERVER
-- Full setup: Tables, seed data, slots, and view
-- Generated: March 2026
-- ============================================================

USE master;
GO

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'MarchMadness2026')
BEGIN
    CREATE DATABASE MarchMadness2026;
END
GO

USE MarchMadness2026;
GO

-- Create schema if it doesn't exist
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'mm')
BEGIN
    EXEC('CREATE SCHEMA mm');
END
GO

-- ============================================================
-- DROP OBJECTS IF THEY EXIST (for clean re-runs)
-- ============================================================
IF OBJECT_ID('mm.vw_Prediction_Results', 'V') IS NOT NULL DROP VIEW mm.vw_Prediction_Results;
IF OBJECT_ID('mm.Bracket_Predictions', 'U') IS NOT NULL DROP TABLE mm.Bracket_Predictions;
IF OBJECT_ID('mm.Bracket_Contestants', 'U') IS NOT NULL DROP TABLE mm.Bracket_Contestants;
IF OBJECT_ID('mm.Tournament_Slots', 'U') IS NOT NULL DROP TABLE mm.Tournament_Slots;
IF OBJECT_ID('mm.Teams', 'U') IS NOT NULL DROP TABLE mm.Teams;
GO

-- ============================================================
-- TABLE 1: TEAMS
-- ============================================================
CREATE TABLE mm.Teams (
    team_id     INT IDENTITY(1,1) PRIMARY KEY,
    team_name   NVARCHAR(100) NOT NULL UNIQUE,
    seed        INT NOT NULL,
    region      NVARCHAR(50) NOT NULL  -- East, West, Midwest, South, FirstFour
);
GO

-- ============================================================
-- TABLE 2: TOURNAMENT_SLOTS
-- ============================================================
CREATE TABLE mm.Tournament_Slots (
    slot_id             INT IDENTITY(1,1) PRIMARY KEY,
    round               INT NOT NULL,           -- 1=R64, 2=R32, 3=S16, 4=E8, 5=F4, 6=Championship
    region              NVARCHAR(50) NULL,       -- NULL for F4 and Championship
    parent_slot_id      INT NULL REFERENCES mm.Tournament_Slots(slot_id),
    team_1_id           INT NULL REFERENCES mm.Teams(team_id),
    team_2_id           INT NULL REFERENCES mm.Teams(team_id),
    actual_winner_id    INT NULL REFERENCES mm.Teams(team_id),
    actual_loser_id     INT NULL REFERENCES mm.Teams(team_id),
    match_time          DATETIME NULL,
    potential_points    INT NOT NULL            -- R1=1, R2=2, S16=4, E8=8, F4=16, Champ=32
);
GO

-- ============================================================
-- TABLE 3: BRACKET_CONTESTANTS
-- ============================================================
CREATE TABLE mm.Bracket_Contestants (
    bracket_id                      INT IDENTITY(1,1) PRIMARY KEY,
    bracket_name                    NVARCHAR(100) NOT NULL UNIQUE,
    bracket_creator                 NVARCHAR(100) NOT NULL,
    predicted_tournament_winner     INT NOT NULL REFERENCES mm.Teams(team_id)
);
GO

-- ============================================================
-- TABLE 4: BRACKET_PREDICTIONS
-- ============================================================
CREATE TABLE mm.Bracket_Predictions (
    prediction_id       INT IDENTITY(1,1) PRIMARY KEY,
    slot_id             INT NOT NULL REFERENCES mm.Tournament_Slots(slot_id),
    bracket_id          INT NOT NULL REFERENCES mm.Bracket_Contestants(bracket_id),
    predicted_winner_id INT NOT NULL REFERENCES mm.Teams(team_id),
    predicted_loser_id  INT NOT NULL REFERENCES mm.Teams(team_id),
    CONSTRAINT UQ_Bracket_Slot UNIQUE (slot_id, bracket_id)
);
GO

-- ============================================================
-- SEED DATA: TEAMS (all 68 — including First Four)
-- ============================================================

-- EAST REGION
INSERT INTO mm.Teams (team_name, seed, region) VALUES
('Duke',                1, 'East'),
('UConn',               2, 'East'),
('Michigan State',      3, 'East'),
('Nebraska',            4, 'East'),
('Vanderbilt',          5, 'East'),
('Louisville',          6, 'East'),
('UCLA',                7, 'East'),
('Clemson',             8, 'East'),
('TCU',                 9, 'East'),
('UCF',                10, 'East'),
('VCU',                11, 'East'),
('McNeese',            12, 'East'),
('Troy',               13, 'East'),
('North Dakota State', 14, 'East'),
('Furman',             15, 'East'),
('Siena',              16, 'East');

-- WEST REGION
INSERT INTO mm.Teams (team_name, seed, region) VALUES
('Arizona',             1, 'West'),
('Iowa State',          2, 'West'),
('Virginia',            3, 'West'),
('Alabama',             4, 'West'),
('Texas Tech',          5, 'West'),
('Tennessee',           6, 'West'),
('Kentucky',            7, 'West'),
('Villanova',           8, 'West'),
('Utah State',          9, 'West'),
('Santa Clara',        10, 'West'),
('Miami (Ohio)',        11, 'West'),
('Akron',              12, 'West'),
('Hofstra',            13, 'West'),
('Wright State',       14, 'West'),
('Tennessee State',    15, 'West'),
('Long Island University', 16, 'West');

-- MIDWEST REGION
INSERT INTO mm.Teams (team_name, seed, region) VALUES
('Michigan',            1, 'Midwest'),
('Houston',             2, 'Midwest'),
('Illinois',            3, 'Midwest'),
('Arkansas',            4, 'Midwest'),
('St. John''s',         5, 'Midwest'),
('North Carolina',      6, 'Midwest'),
('Saint Mary''s',       7, 'Midwest'),
('Georgia',             8, 'Midwest'),
('Saint Louis',         9, 'Midwest'),
('Texas A&M',          10, 'Midwest'),
('Texas',              11, 'Midwest'),
('High Point',         12, 'Midwest'),
('Hawai''i',           13, 'Midwest'),
('Penn',               14, 'Midwest'),
('Idaho',              15, 'Midwest'),
('Howard',             16, 'Midwest');

-- SOUTH REGION
INSERT INTO mm.Teams (team_name, seed, region) VALUES
('Florida',             1, 'South'),
('Purdue',              2, 'South'),
('Gonzaga',             3, 'South'),
('Kansas',              4, 'South'),
('Wisconsin',           5, 'South'),
('BYU',                 6, 'South'),
('Miami (Fla.)',         7, 'South'),
('Ohio State',          8, 'South'),
('Iowa',                9, 'South'),
('Missouri',           10, 'South'),
('South Florida',      11, 'South'),
('UNI',                12, 'South'),
('Cal Baptist',        13, 'South'),
('Kennesaw State',     14, 'South'),
('Queens',             15, 'South'),
('Prairie View A&M',   16, 'South');

-- FIRST FOUR TEAMS (already played — winners entered in their regions above)
-- NC State, UMBC, Lehigh, SMU were eliminated in First Four
INSERT INTO mm.Teams (team_name, seed, region) VALUES
('NC State',            11, 'FirstFour'),
('UMBC',                16, 'FirstFour'),
('Lehigh',              16, 'FirstFour'),
('SMU',                 11, 'FirstFour');
GO

-- ============================================================
-- SEED DATA: TOURNAMENT SLOTS
-- 63 slots total. parent_slot_id = slot the winner advances to.
-- Slots 1-32:   Round 1 (R64)
-- Slots 33-48:  Round 2 (R32)
-- Slots 49-56:  Sweet 16
-- Slots 57-60:  Elite 8
-- Slots 61-62:  Final Four
-- Slot  63:     Championship
--
-- BRACKET STRUCTURE (by region):
-- EAST:    slots 1-8   (R64), 33-36 (R32), 49-50 (S16), 57 (E8)
-- WEST:    slots 9-16  (R64), 37-40 (R32), 51-52 (S16), 58 (E8)
-- MIDWEST: slots 17-24 (R64), 41-44 (R32), 53-54 (S16), 59 (E8)
-- SOUTH:   slots 25-32 (R64), 45-48 (R32), 55-56 (S16), 60 (E8)
-- FINAL FOUR: 61 (East vs West winner), 62 (Midwest vs South winner)
-- CHAMPIONSHIP: 63
-- ============================================================

-- ============================================================
-- STEP 1: Insert all 63 slots with parent_slot_id = NULL first
-- to avoid FK self-reference chicken-and-egg problem.
-- STEP 2: UPDATE parent_slot_id relationships after all rows exist.
-- STEP 3: UPDATE team and result data.
-- ============================================================

SET IDENTITY_INSERT mm.Tournament_Slots ON;

-- ── INSERT ALL 63 SLOTS (parent_slot_id = NULL for now) ─────
INSERT INTO mm.Tournament_Slots (slot_id, round, region, parent_slot_id, team_1_id, team_2_id, actual_winner_id, actual_loser_id, match_time, potential_points) VALUES
-- ROUND 1 — EAST
( 1, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
( 2, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
( 3, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
( 4, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
( 5, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
( 6, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
( 7, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
( 8, 1, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
-- ROUND 1 — WEST
( 9, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(10, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(11, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(12, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(13, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(14, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(15, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(16, 1, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
-- ROUND 1 — MIDWEST
(17, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(18, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(19, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(20, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(21, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(22, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(23, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(24, 1, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
-- ROUND 1 — SOUTH
(25, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(26, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(27, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(28, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(29, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(30, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
(31, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-20', 1),
(32, 1, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-19', 1),
-- ROUND 2 — EAST
(33, 2, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(34, 2, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(35, 2, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(36, 2, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
-- ROUND 2 — WEST
(37, 2, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(38, 2, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(39, 2, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(40, 2, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
-- ROUND 2 — MIDWEST
(41, 2, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(42, 2, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(43, 2, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(44, 2, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
-- ROUND 2 — SOUTH
(45, 2, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(46, 2, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(47, 2, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
(48, 2, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-22', 2),
-- SWEET 16
(49, 3, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-27', 4),
(50, 3, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-28', 4),
(51, 3, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-27', 4),
(52, 3, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-28', 4),
(53, 3, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-27', 4),
(54, 3, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-28', 4),
(55, 3, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-27', 4),
(56, 3, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-28', 4),
-- ELITE 8
(57, 4, 'East',    NULL, NULL, NULL, NULL, NULL, '2026-03-29', 8),
(58, 4, 'West',    NULL, NULL, NULL, NULL, NULL, '2026-03-29', 8),
(59, 4, 'Midwest', NULL, NULL, NULL, NULL, NULL, '2026-03-30', 8),
(60, 4, 'South',   NULL, NULL, NULL, NULL, NULL, '2026-03-30', 8),
-- FINAL FOUR
(61, 5, NULL,      NULL, NULL, NULL, NULL, NULL, '2026-04-04', 16),
(62, 5, NULL,      NULL, NULL, NULL, NULL, NULL, '2026-04-04', 16),
-- CHAMPIONSHIP
(63, 6, NULL,      NULL, NULL, NULL, NULL, NULL, '2026-04-06', 32);

SET IDENTITY_INSERT mm.Tournament_Slots OFF;
GO

-- ============================================================
-- STEP 2: UPDATE parent_slot_id (bracket tree structure)
-- All slots now exist so FK constraint is satisfied
-- ============================================================

-- Round 1 → Round 2 parents (EAST)
UPDATE mm.Tournament_Slots SET parent_slot_id = 33 WHERE slot_id IN (1, 2);
UPDATE mm.Tournament_Slots SET parent_slot_id = 34 WHERE slot_id IN (3, 4);
UPDATE mm.Tournament_Slots SET parent_slot_id = 35 WHERE slot_id IN (5, 6);
UPDATE mm.Tournament_Slots SET parent_slot_id = 36 WHERE slot_id IN (7, 8);
-- Round 1 → Round 2 parents (WEST)
UPDATE mm.Tournament_Slots SET parent_slot_id = 37 WHERE slot_id IN (9, 10);
UPDATE mm.Tournament_Slots SET parent_slot_id = 38 WHERE slot_id IN (11, 12);
UPDATE mm.Tournament_Slots SET parent_slot_id = 39 WHERE slot_id IN (13, 14);
UPDATE mm.Tournament_Slots SET parent_slot_id = 40 WHERE slot_id IN (15, 16);
-- Round 1 → Round 2 parents (MIDWEST)
UPDATE mm.Tournament_Slots SET parent_slot_id = 41 WHERE slot_id IN (17, 18);
UPDATE mm.Tournament_Slots SET parent_slot_id = 42 WHERE slot_id IN (19, 20);
UPDATE mm.Tournament_Slots SET parent_slot_id = 43 WHERE slot_id IN (21, 22);
UPDATE mm.Tournament_Slots SET parent_slot_id = 44 WHERE slot_id IN (23, 24);
-- Round 1 → Round 2 parents (SOUTH)
UPDATE mm.Tournament_Slots SET parent_slot_id = 45 WHERE slot_id IN (25, 26);
UPDATE mm.Tournament_Slots SET parent_slot_id = 46 WHERE slot_id IN (27, 28);
UPDATE mm.Tournament_Slots SET parent_slot_id = 47 WHERE slot_id IN (29, 30);
UPDATE mm.Tournament_Slots SET parent_slot_id = 48 WHERE slot_id IN (31, 32);
-- Round 2 → Sweet 16 parents
UPDATE mm.Tournament_Slots SET parent_slot_id = 49 WHERE slot_id IN (33, 34);
UPDATE mm.Tournament_Slots SET parent_slot_id = 50 WHERE slot_id IN (35, 36);
UPDATE mm.Tournament_Slots SET parent_slot_id = 51 WHERE slot_id IN (37, 38);
UPDATE mm.Tournament_Slots SET parent_slot_id = 52 WHERE slot_id IN (39, 40);
UPDATE mm.Tournament_Slots SET parent_slot_id = 53 WHERE slot_id IN (41, 42);
UPDATE mm.Tournament_Slots SET parent_slot_id = 54 WHERE slot_id IN (43, 44);
UPDATE mm.Tournament_Slots SET parent_slot_id = 55 WHERE slot_id IN (45, 46);
UPDATE mm.Tournament_Slots SET parent_slot_id = 56 WHERE slot_id IN (47, 48);
-- Sweet 16 → Elite 8 parents
UPDATE mm.Tournament_Slots SET parent_slot_id = 57 WHERE slot_id IN (49, 50);
UPDATE mm.Tournament_Slots SET parent_slot_id = 58 WHERE slot_id IN (51, 52);
UPDATE mm.Tournament_Slots SET parent_slot_id = 59 WHERE slot_id IN (53, 54);
UPDATE mm.Tournament_Slots SET parent_slot_id = 60 WHERE slot_id IN (55, 56);
-- Elite 8 → Final Four parents
UPDATE mm.Tournament_Slots SET parent_slot_id = 61 WHERE slot_id IN (57, 58);
UPDATE mm.Tournament_Slots SET parent_slot_id = 62 WHERE slot_id IN (59, 60);
-- Final Four → Championship
UPDATE mm.Tournament_Slots SET parent_slot_id = 63 WHERE slot_id IN (61, 62);
GO

-- ============================================================
-- STEP 3: UPDATE team matchups and known results
-- ============================================================

-- EAST Round 1
UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Duke'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Siena'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Duke'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Siena')
WHERE slot_id = 1;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Clemson'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='TCU'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='TCU'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Clemson')
WHERE slot_id = 2;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Vanderbilt'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='McNeese'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Vanderbilt'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='McNeese')
WHERE slot_id = 3;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Nebraska'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Troy'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Nebraska'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Troy')
WHERE slot_id = 4;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Louisville'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='VCU'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Louisville'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='VCU')
WHERE slot_id = 5;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Michigan State'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='North Dakota State'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Michigan State'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='North Dakota State')
WHERE slot_id = 6;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='UCLA'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='UCF')
WHERE slot_id = 7; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='UConn'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Furman'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='UConn'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Furman')
WHERE slot_id = 8;

-- WEST Round 1
UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Arizona'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Long Island University'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Arizona'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Long Island University')
WHERE slot_id = 9;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Utah State'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Villanova'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Utah State'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Villanova')
WHERE slot_id = 10;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Texas Tech'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Akron'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Texas Tech'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Akron')
WHERE slot_id = 11;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Alabama'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Hofstra'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Alabama'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Hofstra')
WHERE slot_id = 12;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Tennessee'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Miami (Ohio)'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Tennessee'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Miami (Ohio)')
WHERE slot_id = 13;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Virginia'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Wright State'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Virginia'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Wright State')
WHERE slot_id = 14;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Kentucky'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Santa Clara'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Kentucky'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Santa Clara')
WHERE slot_id = 15;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Iowa State'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Tennessee State'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Iowa State'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Tennessee State')
WHERE slot_id = 16;

-- MIDWEST Round 1
UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Michigan'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Howard'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Michigan'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Howard')
WHERE slot_id = 17;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Saint Louis'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Georgia'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Saint Louis'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Georgia')
WHERE slot_id = 18;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='St. John''s'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='UNI')
WHERE slot_id = 19; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Texas A&M'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Saint Mary''s'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Texas A&M'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Saint Mary''s')
WHERE slot_id = 20;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Texas'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='BYU'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Texas'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='BYU')
WHERE slot_id = 21;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Illinois'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Penn'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Illinois'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Penn')
WHERE slot_id = 22;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Arkansas'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Hawai''i'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Arkansas'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Hawai''i')
WHERE slot_id = 23;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Houston'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Idaho'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Houston'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Idaho')
WHERE slot_id = 24;

-- SOUTH Round 1
UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Florida'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Prairie View A&M')
WHERE slot_id = 25; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Iowa'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Clemson')
WHERE slot_id = 26; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Kansas'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Cal Baptist')
WHERE slot_id = 27; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Miami (Fla.)'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Missouri')
WHERE slot_id = 28; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Gonzaga'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Kennesaw State'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Gonzaga'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Kennesaw State')
WHERE slot_id = 29;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='North Carolina'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='VCU'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='VCU'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='North Carolina')
WHERE slot_id = 30;

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Purdue'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='Queens')
WHERE slot_id = 31; -- result TBD

UPDATE mm.Tournament_Slots SET
    team_1_id = (SELECT team_id FROM mm.Teams WHERE team_name='Wisconsin'),
    team_2_id = (SELECT team_id FROM mm.Teams WHERE team_name='High Point'),
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='High Point'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Wisconsin')
WHERE slot_id = 32;

-- ROUND 2 known results
UPDATE mm.Tournament_Slots SET
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Duke'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='TCU')
WHERE slot_id = 33;

UPDATE mm.Tournament_Slots SET
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Nebraska'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Vanderbilt')
WHERE slot_id = 34;

UPDATE mm.Tournament_Slots SET
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Michigan State'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Louisville')
WHERE slot_id = 35;

UPDATE mm.Tournament_Slots SET
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Michigan'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='Saint Louis')
WHERE slot_id = 41;

UPDATE mm.Tournament_Slots SET
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Arkansas'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='High Point')
WHERE slot_id = 44;

UPDATE mm.Tournament_Slots SET
    actual_winner_id = (SELECT team_id FROM mm.Teams WHERE team_name='Purdue'),
    actual_loser_id  = (SELECT team_id FROM mm.Teams WHERE team_name='High Point')
WHERE slot_id = 48;
GO

-- ============================================================
-- VIEW: vw_Prediction_Results
-- ============================================================
CREATE VIEW mm.vw_Prediction_Results AS
SELECT
    bc.bracket_id,
    bc.bracket_creator,
    bc.bracket_name,
    bp.slot_id,
    ts.round,
    ts.region,
    t_actual.team_name       AS actual_winner_name,
    t_actual.seed            AS actual_winner_seed,
    t_pred.team_name         AS predicted_winner_name,
    CASE
        WHEN ts.actual_winner_id IS NULL THEN NULL  -- game not yet played
        WHEN bp.predicted_winner_id = ts.actual_winner_id THEN 1
        ELSE 0
    END AS correct,
    CASE
        WHEN ts.actual_winner_id IS NULL THEN 0
        WHEN bp.predicted_winner_id = ts.actual_winner_id THEN ts.potential_points
        ELSE 0
    END AS points_won
FROM mm.Bracket_Predictions bp
JOIN mm.Bracket_Contestants bc  ON bp.bracket_id   = bc.bracket_id
JOIN mm.Tournament_Slots ts     ON bp.slot_id       = ts.slot_id
LEFT JOIN mm.Teams t_actual     ON ts.actual_winner_id = t_actual.team_id
LEFT JOIN mm.Teams t_pred       ON bp.predicted_winner_id = t_pred.team_id;
GO

-- ============================================================
-- HELPFUL QUERIES TO GET YOU STARTED
-- ============================================================

-- Leaderboard
-- SELECT bracket_creator, bracket_name, SUM(points_won) AS total_points
-- FROM mm.vw_Prediction_Results
-- GROUP BY bracket_creator, bracket_name
-- ORDER BY total_points DESC;

-- Upsets that busted brackets
-- SELECT t.team_name, t.seed, ts.round, COUNT(*) AS brackets_busted
-- FROM mm.Tournament_Slots ts
-- JOIN Teams t ON ts.actual_winner_id = t.team_id
-- JOIN Bracket_Predictions bp ON ts.slot_id = bp.slot_id
-- WHERE bp.predicted_winner_id != ts.actual_winner_id
--   AND t.seed >= 10
-- GROUP BY t.team_name, t.seed, ts.round
-- ORDER BY brackets_busted DESC;

-- Championship pick breakdown
-- SELECT t.team_name, COUNT(*) AS num_brackets_picked
-- FROM mm.Bracket_Contestants bc
-- JOIN Teams t ON bc.predicted_tournament_winner = t.team_id
-- GROUP BY t.team_name
-- ORDER BY num_brackets_picked DESC;

PRINT 'March Madness 2026 database setup complete!';
GO
