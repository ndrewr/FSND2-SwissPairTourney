Udacity Fullstack Nanodegree - Project 2
=====================================================
### Swiss-Pair tournament ###
### Author: Andrew Roy Chen, May 2015 ###


SUMMARY:
-----------------------------------------------------
Defines data tables needed to implement a roster of unique players and a list 
of matches with win/loss results. Views are also utilized to simplify more complex queries.
Demonstrates basic database administration proficiency.


FILE STRUCTURE:
-----------------------------------------------------
This project is expanded from the 'Common code for the Relational Databases and Full Stack Fundamentals' 
courses found here: http://github.com/udacity/fullstack-nanodegree-vm

The project uses a pre-configured vagrant setup. 
(quick start detailed here: http://docs.vagrantup.com/v2/getting-started/)

Actual project code is located in the directory:
	./vagrant/tournament

and consists of three files:
tournament.sql -> defines the database schema 'tournament'
tournament.py -> defines modules used to interact with the tournament database
tournament_test.py -> defines a sequence of tests used to verify the modules in tournament.py


INSTRUCTIONS TO RUN:
-----------------------------------------------------
Vagrant is not required to run the project.

If running separately, first ensure the following python modules are already installed:
- postgresql
- psycopg2
- bleach

Next to build and access the database we run:
	psql 

followed by the command below to execute the sql definition file:
	\i tournament.sql

Then run the test file with the command:
	python ./vagrant/tournament/tournament_test.py

Expected output should be:
	1. Old matches can be deleted.
	2. Player records can be deleted.
	3. After deleting, countPlayers() returns zero.
	4. After registering a player, countPlayers() returns 1.
	5. Players can be registered and deleted.
	6. Newly registered players appear in the standings with no matches.
	7. After a match, players have updated standings.
	8. After one match, players with one win are paired.
	Success!  All tests pass!
