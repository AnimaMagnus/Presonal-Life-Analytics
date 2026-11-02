import os
from src.db import get_connection
from datetime import date

def get_user_id(conn):
    email = os.getenv("USER_EMAIL")
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id from users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("User not found in the users table")
        else:
            return row[0]

def ask_number(prompt, low, high, whole=False):
    while True:
        answer = input(prompt)
        try:
            value = float(answer)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if low <= value <= high:
            if whole and not value.is_integer():
                print("Please enter a whole number.")
                continue
            return int(value) if whole else round(value, 1)
        else:
            print(f"Please enter a number between {low} and {high}.")

def ask_checkin():
    sleep = ask_number("Sleep hours (0-24): ", 0, 24)
    mood = ask_number("Mood (1-5): ", 1, 5, whole=True)
    energy = ask_number("Energy (1-5): ", 1, 5, whole=True)
    productivity = ask_number("Productivity (1-5): ", 1, 5, whole=True)
    gratitude = input("What are you grateful for today? ") or None
    went_well = input("What went well today? ") or None
    went_hard = input("What went hard today? ") or None
    return {
        "sleep_hours": sleep,
        "mood": mood,
        "energy": energy,
        "productivity": productivity,
        "gratitude": gratitude,
        "went_well": went_well,
        "was_hard": went_hard
    }

def save_checkin(conn, user_id, data):
    sql = """
        INSERT INTO daily_checkins
            (user_id, checkin_date, sleep_hours, mood, energy, productivity,
             gratitude, went_well, was_hard)
        VALUES
            (%(user_id)s, %(checkin_date)s, %(sleep_hours)s, %(mood)s, %(energy)s,
             %(productivity)s, %(gratitude)s, %(went_well)s, %(was_hard)s)
    """
    params = {**data, "user_id": user_id, "checkin_date": date.today()}
    with conn.cursor() as cur:
        cur.execute(sql, params)

if __name__ == "__main__":
    with get_connection() as conn:
        user_id = get_user_id(conn)
        data = ask_checkin()
        save_checkin(conn, user_id, data)
        print("Check-in saved.")