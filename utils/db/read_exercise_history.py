import sqlite3
from datetime import datetime, timedelta


#def read_exercise_history(exercise, conn_str):
#    today = datetime.today().strftime('%Y-%m-%d')
#
#    conn = sqlite3.connect(conn_str)
#    cursor = conn.cursor()
#    cursor.execute(
#            """
#            WITH d AS (
#               	SELECT DISTINCT Date
#               	FROM workout_history
#               	WHERE Exercise = ?
#              		AND Date != ?
#               	ORDER BY Date DESC
#               	LIMIT 4
#            )
#            SELECT
#               	h.Date,
#               	h.Intensity,
#               	COUNT(*) AS n
#            FROM workout_history h
#            JOIN d ON h.Date = d.Date
#            WHERE Exercise = ?
#        	AND h.Date != ?
#                GROUP BY h.Date, h.Intensity;
#
#            """,
#            [exercise, today, exercise, today]
#    )
#    res = cursor.fetchall()
#    conn.close()
#
#    if len(res) == 0:
#            return []
#
#    res = [[entry[0] , entry[1], entry[2]] for entry in res]
#
#    return res
#
def read_exercise_history(exercise, conn_str):
    today = datetime.today()
    start = today - timedelta(weeks=4)
    today = today.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
            """
            SELECT
               	Date,
               	Intensity,
               	COUNT(*) AS n
            FROM workout_history
            WHERE Exercise = ?
           	    AND Date != ?
                AND Date >= ?
            GROUP BY Date, Intensity;
            """,
            [exercise, today, start]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
            return []

    res = [[entry[0] , entry[1], entry[2]] for entry in res]

    return res
