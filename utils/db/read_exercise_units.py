import sqlite3


def read_exercise_units(exercise, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT UnitIntensity, UnitVolume
    	FROM exercises
        WHERE exercise = ?;
        """,
        [exercise]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = list(res[0])

    return res
