import sqlite3


def delete_workout(workout, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM workout_contents
        WHERE Workout = ?;
        """,
        [workout]
    )
    cursor.execute(
        """
        DELETE FROM workouts
        WHERE Workout = ?;
        """,
        [workout]
    )
    conn.commit()
    conn.close()

    return 0
