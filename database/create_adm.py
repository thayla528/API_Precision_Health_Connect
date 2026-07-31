import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database/health.db")
cursor = conn.cursor()

# Cria o usuário administrador
cursor.execute("""
INSERT INTO users (
    full_name,
    email,
    password,
    role,
    profile_type
)
VALUES (?, ?, ?, ?, ?)
""", (
    "Administrador",
    "thaylamoralles@gmail.com",
    generate_password_hash("@Parabens2008"),
    "administrator",
    "administrator"
))

# Recupera o id do usuário criado
user_id = cursor.lastrowid

# Cadastra esse usuário como administrador
cursor.execute("""
INSERT INTO administrators (
    user_id,
    access_level,
    department
)
VALUES (?, ?, ?)
""", (
    user_id,
    "super_admin",
    "Sistema"
))

conn.commit()
conn.close()

print("Administrador criado com sucesso!")