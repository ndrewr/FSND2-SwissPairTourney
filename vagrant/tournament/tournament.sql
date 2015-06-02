-- Table definitions for the tournament project.
-- ***************************************************************************

CREATE DATABASE tournament;
\c tournament;

-- useful reset for testing purposes
DROP TABLE players CASCADE;
DROP TABLE matches CASCADE;
DROP VIEW Num_Matches CASCADE;
DROP VIEW Num_Wins;

-- schema definitions, literally taken from project spec sheet
CREATE TABLE Players (
	name	text,
	id		serial,
	PRIMARY KEY (id)
);

-- NOTE: with current match report structure 'winner' column is redundant
-- 	but needed IF ties are allowed. Would require rewritten tests however
CREATE TABLE Matches (
	p1		integer REFERENCES Players(id),
	p2		integer REFERENCES Players(id),
	winner	integer REFERENCES Players(id)
);

/* 
	Create views covering:
	- Finding the number of matches each player has played.
	- The number of wins for each player.
	- The player standings.
*/
-- number of matches
CREATE VIEW Num_Matches AS SELECT Players.id, COUNT(Matches.*) AS matches 
FROM Players LEFT JOIN Matches 
ON Players.id = Matches.p1 OR Players.id = Matches.p2 
GROUP BY Players.id;

-- view for number of wins
CREATE VIEW Num_Wins AS SELECT Players.id, COUNT(Matches.winner) AS wins 
FROM Players LEFT JOIN Matches 
ON Players.id = Matches.winner GROUP BY Players.id;

-- view for player standings (desc)
CREATE VIEW Standings AS SELECT Players.id, Players.name, wins, matches 
FROM Players, Num_Matches, Num_Wins 
WHERE Players.id = Num_Matches.id AND Players.id = Num_Wins.id
ORDER BY wins DESC;