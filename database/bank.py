import sqlite3


def connect():
    conn = sqlite3.connect("database/health.db")
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():
    conn = connect()
    cursor = conn.cursor()

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

    # ---------------- ADMINISTRATORS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administrators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            phone TEXT,

            access_level TEXT DEFAULT 'admin',

            department TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- VERIFICATIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT NOT NULL,
            phone TEXT,

            email_code TEXT NOT NULL,
            phone_code TEXT,

            email_verified INTEGER DEFAULT 0,
            phone_verified INTEGER DEFAULT 0,

            email_expires_at DATETIME NOT NULL,
            phone_expires_at DATETIME,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

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

    # ---------------- PATIENT PROFESSIONAL TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_professional (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            professional_id INTEGER NOT NULL,

            status TEXT DEFAULT 'active',

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(patient_id, professional_id),

            FOREIGN KEY(patient_id)
                REFERENCES patients(id),

            FOREIGN KEY(professional_id)
                REFERENCES professionals(id)
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

    # ---------------- PRESCRIPTIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,

            professional_id INTEGER NOT NULL,

            appointment_id INTEGER,

            medication TEXT NOT NULL,

            dosage TEXT,

            frequency TEXT,

            duration TEXT,

            prescription_type TEXT,

            instructions TEXT,

            status TEXT DEFAULT 'pending',

            issued_at DATETIME,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(patient_id)
                REFERENCES patients(id),

            FOREIGN KEY(professional_id)
                REFERENCES professionals(id),

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


    # ---------------- INSTITUTIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,
            institution_type TEXT,

            phone TEXT,
            email TEXT,

            postal_code TEXT,
            address TEXT,
            house_number TEXT,
            address_line2 TEXT,
            neighborhood TEXT,
            city TEXT,
            state TEXT,

            latitude REAL CHECK (
                latitude IS NULL OR latitude BETWEEN -90 AND 90
            ),

            longitude REAL CHECK (
                longitude IS NULL OR longitude BETWEEN -180 AND 180
            ),

            active INTEGER NOT NULL DEFAULT 1
                CHECK (active IN (0, 1)),

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------- PROFESSIONAL INSTITUTIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            professional_id INTEGER NOT NULL,
            institution_id INTEGER NOT NULL,

            is_primary INTEGER NOT NULL DEFAULT 0
                CHECK (is_primary IN (0, 1)),

            active INTEGER NOT NULL DEFAULT 1
                CHECK (active IN (0, 1)),

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            UNIQUE (professional_id, institution_id),

            FOREIGN KEY (professional_id)
                REFERENCES professionals(id),

            FOREIGN KEY (institution_id)
                REFERENCES institutions(id)
        )
    """)

    # ---------------- EXAMS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,
            professional_id INTEGER NOT NULL,

            appointment_id INTEGER,
            institution_id INTEGER,
            result_document_id INTEGER,

            exam_name TEXT NOT NULL,
            exam_type TEXT,
            description TEXT,
            preparation_instructions TEXT,

            requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scheduled_at DATETIME,
            completed_at DATETIME,

            status TEXT NOT NULL DEFAULT 'requested'
                CHECK (
                    status IN (
                        'requested',
                        'scheduled',
                        'in_progress',
                        'completed',
                        'cancelled'
                    )
                ),

            notes TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (patient_id)
                REFERENCES patients(id),

            FOREIGN KEY (professional_id)
                REFERENCES professionals(id),

            FOREIGN KEY (appointment_id)
                REFERENCES appointments(id),

            FOREIGN KEY (institution_id)
                REFERENCES institutions(id),

            FOREIGN KEY (result_document_id)
                REFERENCES medical_documents(id)
        )
    """)

    # ---------------- INDEXES ----------------
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_institutions_location
        ON institutions(latitude, longitude)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_professional_institutions_professional
        ON professional_institutions(professional_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_professional_institutions_institution
        ON professional_institutions(institution_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_exams_patient
        ON exams(patient_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_exams_professional
        ON exams(professional_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_exams_institution
        ON exams(institution_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_exams_appointment
        ON exams(appointment_id)
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

    # ---------------- REVOKED TOKENS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS revoked_tokens (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            jti TEXT UNIQUE NOT NULL,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ---------------- AUDIT LOGS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            action TEXT NOT NULL,

            table_name TEXT NOT NULL,

            record_id INTEGER NOT NULL,

            old_data TEXT,

            new_data TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,


            FOREIGN KEY(user_id)
                REFERENCES users(id)

        )
    """)

    # ---------------- PASSWORD RESETS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            email TEXT NOT NULL,

            reset_code TEXT NOT NULL,

            expires_at DATETIME NOT NULL,

            used INTEGER DEFAULT 0,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")