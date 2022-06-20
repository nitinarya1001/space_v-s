import sqlite3

conn = sqlite3.connect('spacevs.sqlite')
cur = conn.cursor()


def data_saving(PLAYER, PLAYER_PASS):

    # cur.execute('''DROP TABLE IF EXISTS players''')
    # cur.execute('''DROP TABLE IF EXISTS battle''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT, player_pass TEXT)''')
    cur.execute(
        '''INSERT INTO players (player_name,player_pass)
        VALUES (?,?)''', (PLAYER, PLAYER_PASS))
    conn.commit()


def data_check(PLAYER, PLAYER_PASS, logorreg):
    try:
        cur.execute(
            '''SELECT * FROM players''')
    except:
        # Table doesnt exist...create one
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT, player_pass TEXT)''')
        conn.commit

    if logorreg == "login":

        cur.execute(
            '''SELECT player_id FROM players
        WHERE player_name = (?) AND player_pass = (?) ''', (PLAYER, PLAYER_PASS))
        data = cur.fetchone()
        if data:
            return True  # yes data
        else:
            return False  # no data]

    elif logorreg == "reg":
        cur.execute(
            '''SELECT player_id FROM players
        WHERE player_name = (?)''', (PLAYER,))
        data = cur.fetchone()
        if data:
            return True  # yes data
        else:
            return False  # no data


def game_scores_saving(PLAYER1, PLAYER2, winner):
    # cur.execute(
    #     '''CREATE TABLE IF NOT EXISTS battle (p_id INTEGER ,
    #     wins INTEGER NOT NULL , loses INTEGER NOT NULL)''')
    if winner == PLAYER1:
        cur.execute(
            '''SELECT player_id FROM players where player_name = (?)''', (PLAYER1,))
        win_id = cur.fetchone()[0]
    elif winner == PLAYER2:
        cur.execute(
            '''SELECT player_id FROM players where player_name = (?)''', (PLAYER2,))
        win_id = cur.fetchone()[0]

    cur.execute(
        '''UPDATE battle SET wins = wins + 1 WHERE p_id = (?)''', (win_id,))
    conn.commit()


def game_scores_retriev(PLAYER1, PLAYER2):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS battle (p_id INTEGER NOT NULL , wins INTEGER NOT NULL)''')
    cur.execute(
        '''SELECT player_id FROM players where player_name = (?)''', (PLAYER1,))
    pl_id = cur.fetchone()[0]
    cur.execute(
        '''INSERT OR IGNORE INTO battle (p_id, wins) VALUES (?,?)''', (pl_id, 0))
    cur.execute(
        '''SELECT wins FROM battle where p_id = (?)''', (pl_id,))
    win1 = cur.fetchone()[0]
    cur.execute(
        '''SELECT player_id FROM players where player_name = (?)''', (PLAYER2,))
    pl_id = cur.fetchone()[0]
    cur.execute(
        '''INSERT OR IGNORE INTO battle (p_id, wins) VALUES (?,?)''', (pl_id, 0))
    cur.execute(
        '''SELECT wins FROM battle where p_id = (?)''', (pl_id,))
    win2 = cur.fetchone()[0]
    conn.commit()
    return win1, win2


def battle_drop():
    cur.execute('''DROP TABLE IF EXISTS battle''')
    conn.commit()
    return
