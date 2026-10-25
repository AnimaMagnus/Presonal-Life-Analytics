import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)

with conn.cursor() as cur:
    cur.execute("SET search_path TO life;")
    cur.execute("SELECT count(*) FROM categories;")
    print(cur.fetchone())

conn.close()