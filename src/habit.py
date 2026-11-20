import os
from src.db import get_connection
from datetime import date

def get_user_id(conn):
    email = os.getenv("USER_EMAIL")
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("User not found in the users table")
        else:
            return row[0]

def ask_habit(prompt):
    while True:
        answer = input(prompt)
        if answer.strip() == "":
            print("Please enter a valid habit.")
            continue
        return answer.strip()
    
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

def save_habit(conn, user_id, habit_name, target_count=1, target_period='day'):
    sql = """
        INSERT INTO habits (user_id, name, target_count, target_period)
        VALUES (%s, %s, %s, %s)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (user_id, habit_name, target_count, target_period))
        conn.commit()

def ask_habit_details():
    habit_name = ask_habit("Enter the name of the habit you want to track: ")
    target_count = ask_number("Enter the target count for this habit (default 1): ", 1, 100, whole=True)
    target_period = input("Enter the target period (day/week/month, default 'day'): ").strip().lower() or 'day'
    if target_period not in ['day', 'week', 'month']:
        print("Invalid period. Defaulting to 'day'.")
        target_period = 'day'
    return habit_name, target_count, target_period

if __name__ == "__main__":
    conn = get_connection()
    user_id = get_user_id(conn)
    habit_name, target_count, target_period = ask_habit_details()
    save_habit(conn, user_id, habit_name, target_count, target_period)
    print(f"Habit '{habit_name}' saved successfully for user ID {user_id}.")