import sqlite3
from datetime import datetime


def read_last_sets(exercise, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
            WITH temp AS (
                SELECT Date, Workout, Exercise
                FROM workout_history
                WHERE Exercise = ?
                    AND Date < ?
                ORDER BY Date DESC
                LIMIT 1
            )
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
            INNER JOIN temp t
               	ON h.Date = t.Date
              		AND h.Workout = t.Workout
              		AND h.Exercise = t.Exercise
                        JOIN exercises e
               	ON h.Exercise = e.Exercise
            ORDER By ExerciseNumber ASC;
        """,
        [exercise, today]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = [[entry[0], entry[1], entry[2], entry[3]] for entry in res]

    return res
