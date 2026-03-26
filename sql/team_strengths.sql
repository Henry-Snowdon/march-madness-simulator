USE MarchMadness2026;
GO

IF OBJECT_ID('mm.Team_Strengths', 'U') IS NOT NULL DROP TABLE mm.Team_Strengths;
GO

CREATE TABLE mm.Team_Strengths (
    team_id             INT PRIMARY KEY REFERENCES mm.Teams(team_id),
    kenpom_net_rating   FLOAT NOT NULL,
    kalshi_elite8       FLOAT NOT NULL,
    kalshi_final4       FLOAT NOT NULL,
    kalshi_final        FLOAT NOT NULL,
    kalshi_champion     FLOAT NOT NULL,
    entered_date        DATETIME DEFAULT GETDATE()
);
GO

INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Michigan'), 37.83, 0.8245, 0.5839, 0.3491, 0.1927);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Arizona'), 37.83, 0.7362, 0.5547, 0.3302, 0.1927);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Duke'), 37.82, 0.7067, 0.5061, 0.3208, 0.1651);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Houston'), 34.44, 0.5988, 0.4282, 0.2075, 0.1009);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Purdue'), 31.82, 0.7362, 0.3017, 0.1321, 0.0642);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Illinois'), 33.27, 0.4123, 0.2822, 0.1132, 0.055);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Iowa State'), 32.98, 0.6184, 0.2336, 0.1038, 0.0459);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'UConn'), 28.35, 0.5595, 0.1946, 0.0943, 0.0367);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Nebraska'), 27.15, 0.5595, 0.1655, 0.0566, 0.0183);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Michigan State'), 28.97, 0.4613, 0.1655, 0.0566, 0.0275);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'St. John''s'), 26.79, 0.2847, 0.146, 0.066, 0.0275);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Arkansas'), 25.85, 0.2454, 0.1168, 0.0472, 0.0275);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Iowa'), 23.4, 0.4515, 0.0973, 0.0377, 0.0092);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Tennessee'), 26.9, 0.373, 0.0973, 0.0283, 0.0183);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Alabama'), 27.34, 0.1767, 0.0681, 0.0377, 0.0092);
INSERT INTO mm.Team_Strengths (team_id, kenpom_net_rating, kalshi_elite8, kalshi_final4, kalshi_final, kalshi_champion)
VALUES ((SELECT team_id FROM mm.Teams WHERE team_name = 'Texas'), 20.24, 0.2552, 0.0584, 0.0189, 0.0092);

GO
PRINT 'Team strengths inserted!';
GO

SELECT
    ROUND(SUM(kalshi_elite8)   * 100, 2) AS elite8_sum,
    ROUND(SUM(kalshi_final4)   * 100, 2) AS final4_sum,
    ROUND(SUM(kalshi_final)    * 100, 2) AS final_sum,
    ROUND(SUM(kalshi_champion) * 100, 2) AS champion_sum
FROM mm.Team_Strengths;
GO