import sqlite3


def write_setting(setting, value, conn_str):
    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        UPDATE settings
        SET {setting} = ?;
        """, [value]
    )
    conn.commit()
    conn.close()

    return 0
