import sqlite3
from datetime import datetime


def write_new_set(workout, exercise, exercise_number, intensity, volume, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO workout_history (
            Date,
            Workout,
            ExerciseNumber,
            Exercise,
            Intensity,
            Volume
        )
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        [today, workout, exercise_number, exercise, intensity, volume]
    )
    conn.commit()
    conn.close()

    return 0
