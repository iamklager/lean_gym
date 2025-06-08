import sqlite3


def add_exercise_to_workout(exercise, workout, conn_str):

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO workout_contents (Workout, ExerciseID, Exercise)
        SELECT
            ? AS Workout,
            COALESCE(MAX(ExerciseID), -1) + 1 AS ExerciseID,
            ? AS Exercise
        FROM workout_contents
        WHERE Workout = ?
        """,
        [workout, exercise, workout]
    )
    conn.commit()
    conn.close()

    return 0
