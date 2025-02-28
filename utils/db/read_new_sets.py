import sqlite3
from datetime import datetime


def read_new_sets(workout, exercise, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT h.Intensity, e.UnitIntensity, h.Volume, e.UnitVolume
        FROM workout_history h
        INNER JOIN exercises e
            ON h.Exercise = e.Exercise
        WHERE h.Date = ?
            AND h.workout = ?
            AND h.Exercise = ?
        ORDER By h.ExerciseNumber ASC;
        """,
        [today, workout, exercise]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = [[entry[0], entry[1], entry[2], entry[3]] for entry in res]

    return res
