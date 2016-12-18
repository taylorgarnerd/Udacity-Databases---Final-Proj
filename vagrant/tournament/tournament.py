#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "update players set wins = 0, matches = 0"
    )

    conn.commit()

    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "delete from players *"
    )

    conn.commit()

    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "select name from players"
    )

    players = cursor.fetchall()

    conn.close()

    return len(players)

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect();
    cursor = conn.cursor();

    cursor.execute(
        "insert into players (name, wins, matches) values (%s, %s, %s)",(name, 0, 0)
    )
    conn.commit()

    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "select * from players order by wins desc"
    )

    data = cursor.fetchall()

    conn.close()

    return data

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "update players set wins = wins + 1, matches = matches + 1 where id = %s",(winner,)
    )
    cursor.execute(
        "update players set matches = matches + 1 where id = %s",(loser,)
    )

    conn.commit()

    conn.close()

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
    standings = playerStandings()
    swiss = []
    count = 1
    player1 = ()
    player2 = ()

    for row in standings:
        if count % 2 == 0:
            player2 = row
            swiss.append((player1[0], player1[1], player2[0], player2[1]))
        else:
            player1 = row
        count += 1

    return swiss
