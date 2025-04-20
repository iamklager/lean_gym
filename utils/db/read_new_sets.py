import sqlite3
from datetime import datetime


def read_new_sets(workout, exercise, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            CASE
                WHEN round(h.Intensity, 2) = CAST(h.Intensity AS INTEGER) THEN CAST(h.Intensity AS INTEGER)
                ELSE round(h.Intensity, 2)
            END AS Intensity,
            e.UnitIntensity,
            CASE
                WHEN round(h.Volume, 2) = CAST(h.Volume AS INTEGER) THEN CAST(h.Volume AS INTEGER)
                ELSE round(h.Volume, 2)
            END AS Volume,
            e.UnitVolume
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
