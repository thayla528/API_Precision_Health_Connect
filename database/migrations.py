from database.bank import connect


def migrate():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
        PRAGMA table_info(professionals)
    """)

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]


    if "specialty" not in columns:

        cursor.execute("""
            ALTER TABLE professionals
            ADD COLUMN specialty TEXT
        """)


    conn.commit()
    conn.close()


if __name__ == "__main__":
    migrate()
    print("Migration completed!")