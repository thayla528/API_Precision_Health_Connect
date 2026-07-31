import sqlite3

conn = sqlite3.connect("database/health.db")

cursor = conn.cursor()

cursor.execute("""
SELECT message FROM messages
ORDER BY id DESC
LIMIT 1
""")

print(cursor.fetchone())

conn.close()