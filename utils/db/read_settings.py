import sqlite3


def read_settings(conn_str):
    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT PauseTime, PauseVibration, PauseSound
        FROM settings;
        """
    )
    res = cursor.fetchall()
    conn.close()

    res = list(res[0])

    return res
