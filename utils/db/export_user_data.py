import sqlite3
import json


def export_user_data(output_path, conn_str):
    tables = ["workouts", "workout_contents", "workout_history", "weight_history"]
    data = {}
    conn = sqlite3.connect(conn_str)
    for table in tables:
        cursor = conn.execute(f"SELECT * FROM {table};")
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        data[table] = rows
    conn.close()
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
