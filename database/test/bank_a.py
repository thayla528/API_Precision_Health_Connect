import sqlite3

conn = sqlite3.connect("database/health.db")
cursor = conn.cursor()

cursor.execute("""
SELECT 
id,
full_name,
email,
role,
profile_type
FROM users
""")

for row in cursor.fetchall():
    print(row)