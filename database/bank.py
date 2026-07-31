import sqlite3


def connect():
    conn = sqlite3.connect("database/health.db")
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # ---------------- INVITATIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invitations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,

            birth_date DATE,

            profile_type TEXT NOT NULL,

            interest_reason TEXT,

            invitation_code TEXT UNIQUE,

            status TEXT DEFAULT 'pending',

            used INTEGER DEFAULT 0,

            approved_by INTEGER,

            requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            approved_at DATETIME,

            FOREIGN KEY(approved_by)
                REFERENCES administrators(id)
        )
    """)

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            invitation_id INTEGER,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,
            
            role TEXT NOT NULL DEFAULT 'patient',

            profile_type TEXT NOT NULL,

            profile_photo TEXT,

            active INTEGER DEFAULT 1,

            last_login DATETIME,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(invitation_id)
                REFERENCES invitations(id)
        )
    """)

    # ---------------- PATIENTS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            cpf TEXT,

            gender TEXT,

            blood_type TEXT,

            postal_code TEXT,

            address TEXT,

            house_number TEXT,

            address_line2 TEXT,

            neighborhood TEXT,

            city TEXT,

            state TEXT,

            notes TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- PROFESSIONALS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professionals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            specialty TEXT NOT NULL,

            license_number TEXT UNIQUE NOT NULL,

            institution TEXT,

            practice_area TEXT,

            phone TEXT,

            professional_email TEXT,

            active INTEGER DEFAULT 1,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- ADMINISTRATORS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administrators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            access_level TEXT DEFAULT 'admin',

            department TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- APPOINTMENTS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            professional_id INTEGER NOT NULL,

            appointment_date DATETIME NOT NULL,

            appointment_reason TEXT,

            status TEXT DEFAULT 'scheduled',

            meeting_link TEXT,

            notes TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(patient_id)
                REFERENCES patients(id),

            FOREIGN KEY(professional_id)
                REFERENCES professionals(id)
        )
    """)

    # ---------------- CLINICAL RECORDS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clinical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            appointment_id INTEGER NOT NULL,

            diagnosis TEXT,

            treatment TEXT,

            prescription TEXT,

            notes TEXT,

            recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(appointment_id)
                REFERENCES appointments(id)
        )
    """)

    # ---------------- MEDICAL DOCUMENTS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            uploaded_by INTEGER,

            file_name TEXT NOT NULL,

            document_type TEXT,

            file_path TEXT NOT NULL,

            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(patient_id)
                REFERENCES patients(id),

            FOREIGN KEY(uploaded_by)
                REFERENCES users(id)
        )
    """)



    # ---------------- NOTIFICATIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            type TEXT,

            title TEXT NOT NULL,

            message TEXT NOT NULL,

            is_read INTEGER DEFAULT 0,

            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- MESSAGES TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            sender_id INTEGER NOT NULL,

            receiver_id INTEGER NOT NULL,

            message TEXT NOT NULL,

            is_read INTEGER DEFAULT 0,

            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(sender_id)
                REFERENCES users(id),

            FOREIGN KEY(receiver_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- SECURITY LOGS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            action TEXT NOT NULL,

            ip_address TEXT,

            browser TEXT,

            device TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)



    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")