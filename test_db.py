import mysql.connector

conn = mysql.connector.connect(
    host='localhost', 
    database='hospital', 
    user='root', 
    password=''
)
cursor = conn.cursor()

print("Patient table structure:")
cursor.execute('DESCRIBE Patient')
for row in cursor.fetchall():
    print(row)

print("\nMedicalHistory table structure:")
cursor.execute('DESCRIBE MedicalHistory')
for row in cursor.fetchall():
    print(row)

print("\nSample Patient data:")
cursor.execute('SELECT * FROM Patient LIMIT 2')
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
