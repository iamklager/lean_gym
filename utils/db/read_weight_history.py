import sqlite3
from datetime import datetime, timedelta


def read_weight_history(conn_str):
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
           	Weight,
           	AVG(WEIGHT) OVER (
          		ORDER BY Date ASC
          		ROWS BETWEEN 4 PRECEDING
         			AND 0 FOLLOWING
           	) AS Mean
        FROM weight_history
        WHERE Date >= ?
        ORDER BY Date ASC;
        """,
        [start]
    )
    res = cursor.fetchall()
    conn.close()

    if len(res) == 0:
        return []

    res = [[entry[0] , entry[1], entry[2]] for entry in res]

    return res
