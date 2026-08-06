import sqlite3


DATABASE = "database/health.db"


def migrate():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        PRAGMA foreign_keys = ON
    """)


    # ---------------- EXAMS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            exam_name TEXT NOT NULL,

            status TEXT DEFAULT 'pending',

            result_file TEXT,

            requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            completed_at DATETIME,


            FOREIGN KEY(patient_id)
                REFERENCES patients(id)

        )
    """)



    # ---------------- MEDICATIONS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            medication_name TEXT NOT NULL,

            dosage TEXT,

            start_date DATE,

            end_date DATE,

            active INTEGER DEFAULT 1,


            FOREIGN KEY(patient_id)
                REFERENCES patients(id)

        )
    """)



    # ---------------- VACCINES TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vaccines (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            vaccine_name TEXT NOT NULL,

            application_date DATE,

            dose TEXT,


            FOREIGN KEY(patient_id)
                REFERENCES patients(id)

        )
    """)



    conn.commit()

    conn.close()


    print("Migration completed successfully!")



if __name__ == "__main__":

    migrate()