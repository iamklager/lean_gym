import sqlite3


def read_workout(workout, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT Exercise
            FROM workout_contents
            WHERE Workout = ?;
        """,
        [workout]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = [entry[0] for entry in res]

    return res
