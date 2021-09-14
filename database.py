import psycopg2

from typing import List, Dict
from psycopg2.extras import RealDictCursor

from config import username, password, host


conn = psycopg2.connect(
        dbname='dwh',
        user=username,
        password=password,
        host=host,
        port=5432)
# cursor = conn.cursor(cursor_factory=RealDictCursor)
cursor = conn.cursor()


def insert_on_conflict(table: str, array: List, sql: str) -> None:
    item = array[0]
    columns = ', '.join(item.keys())
    dd = ["%s" for _ in range(len(item.keys()))]
    placeholders = ", ".join(dd)
    row = sql.format(table, columns, placeholders)
    cursor.executemany(row, [tuple(item.values()) for item in array])
    conn.commit()
