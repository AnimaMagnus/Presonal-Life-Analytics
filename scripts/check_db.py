from src.db import get_connection

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM categories;")
        print(cur.fetchone())