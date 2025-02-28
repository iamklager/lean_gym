import sqlite3
from datetime import datetime


def read_last_exercise_number(workout, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT ExerciseNumber
    	FROM workout_history
    	WHERE Date = ?
    		AND Workout = ?
    	ORDER By ExerciseNumber DESC
    	LIMIT 1;
        """,
        [today, workout]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return 0

    res = [entry[0] for entry in res]
    res = res[0]

    return res
