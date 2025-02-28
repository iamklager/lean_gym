import sqlite3


def add_workout(workout, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO workouts (Workout, LastSession)
        VALUES (?, NULL);
        """,
        [workout]
    )
    conn.commit()
    conn.close()

    return 0
