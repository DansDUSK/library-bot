import sqlite3

conn = sqlite3.connect("librarytask4.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    phone TEXT,
    id_profile TEXT)""")

conn.commit()
conn.close()