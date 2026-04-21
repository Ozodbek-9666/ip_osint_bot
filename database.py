import sqlite3

def init_db():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, full_name):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, username, full_name) VALUES (?, ?, ?)", 
                   (user_id, username, full_name))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.execute("SELECT username, full_name FROM users LIMIT 10") # Oxirgi 10 ta foydalanuvchi
    users = cursor.fetchall()
    conn.close()
    return count, users