import sqlite3
import json


def import_user_data(input_path, conn_str):
    with open (input_path, 'r') as f:
        data = json.load(f)
    conn = sqlite3.connect(conn_str)
    conn.execute("BEGIN TRANSACTION")
    try:
        for table, rows in data.items():
            conn.execute(f"DELETE FROM {table}")
            for row in rows:
                columns = list(row.keys())
                placeholders = ','.join(['?' for _ in columns])
                query = f"""
                    INSERT INTO {table} ({','.join(columns)})
                    VALUES ({placeholders})
                """
                conn.execute(query, list(row.values()))
        conn.execute("COMMIT")
    except Exception as e:
        conn.execute("ROLLBACK")
        raise e
    finally:
        conn.close()
