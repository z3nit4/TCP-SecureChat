import sqlite3 

conn = sqlite3.connect("database/chat.db")

cursor = conn.cursor()

cusrsor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL, 
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEAFULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database initialized.")