import sqlite3


def read_workouts(conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM workouts
        ORDER BY LastSession DESC;
    """)
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = [[entry[0], entry[1]] for entry in res]

    return res
