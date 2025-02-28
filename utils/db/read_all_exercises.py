import sqlite3


def read_all_exercises(conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT Exercise
            FROM exercises
            WHERE IncludeInApp = 1;
        """
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = [exercise[0] for exercise in res]

    return res
