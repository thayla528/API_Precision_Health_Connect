import sqlite3
import os
import traceback

print("\n========================================")
print("       TESTE DO TELEFONE NO BANCO")
print("========================================")

try:
    DB_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "health.db"
    )

    print("Banco utilizado:")
    print(DB_PATH)
    print("----------------------------------------")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Conexão com o banco: OK")
    print("----------------------------------------")

    # Verifica se a coluna phone existe
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()

    print("COLUNAS DA TABELA USERS:")
    for column in columns:
        print(dict(column))

    print("----------------------------------------")

    # Busca todos os usuários
    cursor.execute("""
        SELECT id, full_name, email, phone
        FROM users
        ORDER BY id
    """)

    users = cursor.fetchall()

    print("USUÁRIOS ENCONTRADOS:")

    if not users:
        print("NENHUM USUÁRIO ENCONTRADO.")
    else:
        for user in users:
            print(dict(user))

    print("----------------------------------------")

    # Busca especificamente o administrador 2
    cursor.execute("""
        SELECT id, full_name, email, phone
        FROM users
        WHERE id = ?
    """, (2,))

    user = cursor.fetchone()

    print("USUÁRIO ID 2:")

    if user:
        print(dict(user))
    else:
        print("USUÁRIO ID 2 NÃO EXISTE.")

    print("----------------------------------------")

    conn.close()

    print("Banco fechado.")
    print("TESTE FINALIZADO.")
    print("========================================\n")

except Exception as e:
    print("\n!!!!!!!!!!!! ERRO !!!!!!!!!!!!")
    print(e)
    print("----------------------------------------")
    traceback.print_exc()
    print("========================================\n")