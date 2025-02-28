import sqlite3


def add_exercise_to_workout(exercise, workout, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO workout_contents (Workout, Exercise)
        VALUES (?, ?);
        """,
        [workout, exercise]
    )
    conn.commit()
    conn.close()

    return 0
