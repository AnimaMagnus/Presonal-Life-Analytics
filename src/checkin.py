import os
from src.db import get_connection

def get_user_id(conn):
    email = os.getenv("USER_EMAIL")
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id from users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row is None:
            print("User not found.")
            raise ValueError("User not found in the users table")
        else:
            return row[0]

if __name__ == "__main__":
    with get_connection() as conn:
        print(get_user_id(conn))