import sqlite3
from datetime import datetime


def write_bodyweight(weight, conn_str):
    today = datetime.today().strftime('%Y-%m-%d')

    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO weight_history (Date, Weight)
        VALUES (?, ?)
        ON CONFLICT(Date) DO UPDATE SET Weight = excluded.Weight;
        """,
        [today, weight]
    )
    conn.commit()
    conn.close()

    return 0
