import sqlite3


def rename_workout(new_name, old_name, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE workouts
        SET Workout = ?
        WHERE Workout = ?;
        """,
        [new_name, old_name]
    )
    cursor.execute(
        """
        UPDATE workout_contents
        SET Workout = ?
        WHERE Workout = ?;
        """,
        [new_name, old_name]
    )
    conn.commit()
    conn.close()

    return 0
