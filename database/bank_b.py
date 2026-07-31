import sqlite3

conn = sqlite3.connect("database/health.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE users
SET role = 'professional'
WHERE id = 2
""")

conn.commit()
conn.close()

print("Atualizado")