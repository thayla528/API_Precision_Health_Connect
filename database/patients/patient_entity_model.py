from database.bank import connect


class PatientEntityModel:

    @staticmethod
    def create(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patients (
                user_id
            )
            VALUES (?)
        """, (
            user_id,
        ))

        conn.commit()

        patient_id = cursor.lastrowid

        conn.close()

        return patient_id


    @staticmethod
    def get_by_id(patient_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        conn.close()

        return patient


    @staticmethod
    def get_by_user_id(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE user_id = ?
        """, (user_id,))

        patient = cursor.fetchone()

        conn.close()

        return patient



    @staticmethod
    def search_patients(search=""):

        conn = connect()
        cursor = conn.cursor()

        search = search.strip()

        if search:

            cursor.execute("""
                           SELECT p.id AS patient_id,

                                  p.user_id,

                                  p.cpf,

                                  p.gender,

                                  p.blood_type,

                                  p.city,

                                  p.state,

                                  u.full_name,

                                  u.email,

                                  u.profile_photo

                           FROM patients p

                                    JOIN users u
                                         ON p.user_id = u.id

                           WHERE u.full_name LIKE ?
                              OR p.cpf LIKE ?

                           ORDER BY u.full_name ASC LIMIT 50

                           """, (
                               f"%{search}%",
                               f"%{search}%"
                           ))

        else:

            cursor.execute("""
                           SELECT p.id AS patient_id,

                                  p.user_id,

                                  p.cpf,

                                  p.gender,

                                  p.blood_type,

                                  p.city,

                                  p.state,

                                  u.full_name,

                                  u.email,

                                  u.profile_photo

                           FROM patients p

                                    JOIN users u
                                         ON p.user_id = u.id

                           ORDER BY u.full_name ASC LIMIT 50

                           """)

        patients = cursor.fetchall()

        conn.close()

        return patients



