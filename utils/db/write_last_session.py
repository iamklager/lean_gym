import sqlite3
from datetime import datetime


def write_last_session(workout, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE workouts
        SET LastSession = ?
        WHERE Workout = ?;
        """,
        [today, workout]
    )
    conn.commit()
    conn.close()

    return 0
