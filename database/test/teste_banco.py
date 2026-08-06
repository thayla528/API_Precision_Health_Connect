from database.bank import connect


conn = connect()
cursor = conn.cursor()


print("PATIENTS:")
cursor.execute("SELECT * FROM patients")
patients = cursor.fetchall()

for patient in patients:
    print(dict(patient))


print("\nPROFESSIONALS:")
cursor.execute("SELECT * FROM professionals")
professionals = cursor.fetchall()

for professional in professionals:
    print(dict(professional))

print("\nAPPOINTMENTS:")
cursor.execute("SELECT * FROM appointments")
appointments = cursor.fetchall()



conn.close()