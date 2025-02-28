import sqlite3


def delete_exercise_from_workout(exercise, workout, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM workout_contents
        WHERE Workout = ?
            AND Exercise = ?;
        """,
        [workout, exercise]
    )
    conn.commit()
    conn.close()

    return 0
