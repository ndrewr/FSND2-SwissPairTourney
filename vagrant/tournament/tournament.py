#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    DB = psycopg2.connect("dbname=tournament")
    cursor = DB.cursor()
    return DB, cursor


def disconnect(DB):
    """Cleanup helper that commits then disconnects."""
    DB.commit()
    DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM Matches")
    disconnect(DB)


def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM Players")
    disconnect(DB)


def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    cursor.execute("SELECT COUNT(*) AS num FROM Players")
    num = cursor.fetchone()[0]
    DB.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, cursor = connect()
    # safely pass in the given name string
    clean_name = bleach.clean(name)
    cursor.execute("INSERT INTO Players (name) VALUES (%s)", (clean_name,))
    disconnect(DB)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    First entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, cursor = connect()
    cursor.execute("SELECT * FROM Standings")
    list = cursor.fetchall()
    DB.close()
    return list


# to implement 'ties' needs a third param and rewritten tests
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      p1:  the id number of the first player
      p2:  the id number of the second player
      winner:  the id number of the player who won
    """
    DB, cursor = connect()
    cursor.execute("INSERT INTO Matches (p1, p2, winner) VALUES (%s, %s, %s)",
                    (winner, loser, winner))
    disconnect(DB)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB, cursor = connect()
    # use the player standings to construct swiss pairs list
    standings = playerStandings()
    # take each pair of adjacent players and return them as a match tuple
    # [(id1, name1, id2, name2)]
    SP = [
        (standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1])
        for i in range(0, len(standings), 2)]
    DB.close()
    return SP
