import sqlite3


conn = sqlite3.connect("database/health.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM messages")

conn.commit()

conn.close()

print("Mensagens removidas com sucesso.")