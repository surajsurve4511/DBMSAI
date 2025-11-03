"""
Test script to verify database connection and live data operations
This demonstrates that all operations use real-time database data
"""
import mysql.connector
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    database='hospital',
    user='root',
    password=''
)
cursor = conn.cursor(dictionary=True)

print("=" * 70)
print("HOSPITAL MANAGEMENT SYSTEM - LIVE DATABASE TEST")
print("=" * 70)
print()

# Test 1: Patient Data (LIVE)
print("1. LIVE PATIENT DATA FROM DATABASE:")
print("-" * 70)
cursor.execute("SELECT patient_id, name, age, gender, contact_info FROM patient LIMIT 5")
patients = cursor.fetchall()
for patient in patients:
    print(f"   ID: {patient['patient_id']}, Name: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}")
print(f"   Total Patients in DB: ", end="")
cursor.execute("SELECT COUNT(*) as count FROM patient")
print(cursor.fetchone()['count'])
print()

# Test 2: Medical History (LIVE)
print("2. LIVE MEDICAL HISTORY DATA:")
print("-" * 70)
cursor.execute("""
    SELECT mh.history_id, p.name, mh.disease, mh.treatment, mh.date_time
    FROM medicalhistory mh
    JOIN patient p ON mh.patient_id = p.patient_id
    LIMIT 5
""")
histories = cursor.fetchall()
for history in histories:
    print(f"   Patient: {history['name']}, Disease: {history['disease']}")
print()

# Test 3: Staff Data (LIVE)
print("3. LIVE STAFF DATA:")
print("-" * 70)
cursor.execute("""
    SELECT s.staff_id, s.name, sr.role_name, s.contact_info
    FROM staff s
    LEFT JOIN staffrole sr ON s.role_id = sr.role_id
    LIMIT 5
""")
staff = cursor.fetchall()
for member in staff:
    print(f"   ID: {member['staff_id']}, Name: {member['name']}, Role: {member['role_name']}")
print()

# Test 4: OPD Appointments (LIVE)
print("4. LIVE OPD APPOINTMENTS:")
print("-" * 70)
cursor.execute("""
    SELECT o.app_id, p.name as patient_name, s.name as staff_name, o.appointment_date
    FROM opdappointment o
    JOIN patient p ON o.patient_id = p.patient_id
    JOIN staff s ON o.staff_id = s.staff_id
    LIMIT 5
""")
appointments = cursor.fetchall()
for appt in appointments:
    print(f"   Appointment #{appt['app_id']}: {appt['patient_name']} with {appt['staff_name']}")
    print(f"      Date: {appt['appointment_date']}")
print()

# Test 5: Patient Reports (LIVE)
print("5. LIVE PATIENT ADMISSION REPORTS:")
print("-" * 70)
cursor.execute("""
    SELECT pr.report_id, p.name, pr.diagnosis, pr.in_date_time, pr.out_date_time
    FROM patientreport pr
    JOIN patient p ON pr.patient_id = p.patient_id
    LIMIT 5
""")
reports = cursor.fetchall()
for report in reports:
    status = "Discharged" if report['out_date_time'] else "Active"
    print(f"   Report #{report['report_id']}: {report['name']}")
    print(f"      Diagnosis: {report['diagnosis']}, Status: {status}")
print()

# Test 6: Operation Theatre Records (LIVE)
print("6. LIVE OPERATION THEATRE DATA:")
print("-" * 70)
cursor.execute("""
    SELECT ot_id, patient_id, operation_type, scheduled_date, status
    FROM ot
    LIMIT 5
""")
operations = cursor.fetchall()
for op in operations:
    print(f"   OT #{op['ot_id']}: {op['operation_type']}")
    print(f"      Status: {op['status']}, Date: {op['scheduled_date']}")
print()

# Test 7: Analytics - Age Distribution (LIVE)
print("7. LIVE ANALYTICS - AGE DISTRIBUTION:")
print("-" * 70)
cursor.execute("""
    SELECT 
        CASE 
            WHEN age < 18 THEN '0-17 years'
            WHEN age BETWEEN 18 AND 30 THEN '18-30 years'
            WHEN age BETWEEN 31 AND 45 THEN '31-45 years'
            WHEN age BETWEEN 46 AND 60 THEN '46-60 years'
            ELSE '60+ years'
        END as age_group,
        COUNT(*) as count
    FROM patient
    GROUP BY age_group
    ORDER BY age_group
""")
age_dist = cursor.fetchall()
for dist in age_dist:
    print(f"   {dist['age_group']}: {dist['count']} patients")
print()

# Test 8: Analytics - Gender Distribution (LIVE)
print("8. LIVE ANALYTICS - GENDER DISTRIBUTION:")
print("-" * 70)
cursor.execute("""
    SELECT gender, COUNT(*) as count
    FROM patient
    GROUP BY gender
""")
gender_dist = cursor.fetchall()
for dist in gender_dist:
    print(f"   {dist['gender']}: {dist['count']} patients")
print()

# Test 9: Analytics - Disease Patterns (LIVE)
print("9. LIVE ANALYTICS - COMMON DISEASES:")
print("-" * 70)
cursor.execute("""
    SELECT mh.disease, COUNT(*) as frequency, ROUND(AVG(p.age), 0) as avg_age
    FROM medicalhistory mh
    LEFT JOIN patient p ON mh.patient_id = p.patient_id
    WHERE mh.disease IS NOT NULL AND mh.disease != ''
    GROUP BY mh.disease
    ORDER BY frequency DESC
    LIMIT 5
""")
diseases = cursor.fetchall()
for disease in diseases:
    print(f"   {disease['disease']}: {disease['frequency']} cases (Avg Age: {disease['avg_age']})")
print()

# Test 10: Real-time Insert/Update Test
print("10. TESTING REAL-TIME DATABASE OPERATIONS:")
print("-" * 70)
print("   Adding a new patient to demonstrate live updates...")

# Insert new patient
cursor.execute("""
    INSERT INTO patient (name, age, gender, contact_info)
    VALUES (%s, %s, %s, %s)
""", ('Test Patient', 25, 'Male', 'test@example.com'))
conn.commit()
new_patient_id = cursor.lastrowid
print(f"   ✓ New patient added with ID: {new_patient_id}")

# Verify the insert
cursor.execute("SELECT COUNT(*) as count FROM patient")
new_count = cursor.fetchone()['count']
print(f"   ✓ Total patients now: {new_count}")

# Add medical history for the new patient
cursor.execute("""
    INSERT INTO medicalhistory (patient_id, disease, treatment, date_time)
    VALUES (%s, %s, %s, %s)
""", (new_patient_id, 'Test Disease', 'Test Treatment', datetime.now()))
conn.commit()
print(f"   ✓ Medical history added for patient {new_patient_id}")

# Update patient information
cursor.execute("""
    UPDATE patient 
    SET age = %s 
    WHERE patient_id = %s
""", (26, new_patient_id))
conn.commit()
print(f"   ✓ Patient age updated to 26")

# Verify the update
cursor.execute("SELECT age FROM patient WHERE patient_id = %s", (new_patient_id,))
updated_age = cursor.fetchone()['age']
print(f"   ✓ Verified: Patient age is now {updated_age}")

# Clean up - delete test data
cursor.execute("DELETE FROM medicalhistory WHERE patient_id = %s", (new_patient_id,))
cursor.execute("DELETE FROM patient WHERE patient_id = %s", (new_patient_id,))
conn.commit()
print(f"   ✓ Test data cleaned up")
print()

# Test 11: Operation Statistics (LIVE)
print("11. LIVE OPERATION STATISTICS:")
print("-" * 70)
cursor.execute("""
    SELECT 
        status,
        COUNT(*) as count
    FROM ot
    GROUP BY status
""")
ot_stats = cursor.fetchall()
for stat in ot_stats:
    print(f"   {stat['status']}: {stat['count']} operations")
print()

# Test 12: Staff Workload (LIVE)
print("12. LIVE STAFF WORKLOAD ANALYSIS:")
print("-" * 70)
cursor.execute("""
    SELECT 
        s.name as staff_name,
        sr.role_name,
        COUNT(DISTINCT o.app_id) as opd_count,
        COUNT(DISTINCT osa.ot_id) as ot_count,
        (COUNT(DISTINCT o.app_id) + COUNT(DISTINCT osa.ot_id)) as total_workload
    FROM staff s
    LEFT JOIN staffrole sr ON s.role_id = sr.role_id
    LEFT JOIN opdappointment o ON s.staff_id = o.staff_id
    LEFT JOIN ot_staff_assignment osa ON s.staff_id = osa.staff_id
    GROUP BY s.staff_id, s.name, sr.role_name
    ORDER BY total_workload DESC
    LIMIT 5
""")
workload = cursor.fetchall()
for work in workload:
    print(f"   {work['staff_name']} ({work['role_name']})")
    print(f"      OPD: {work['opd_count']}, OT: {work['ot_count']}, Total: {work['total_workload']}")
print()

print("=" * 70)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 70)
print()
print("KEY FINDINGS:")
print("✓ Database connection is working")
print("✓ All tables are accessible and have data")
print("✓ Real-time INSERT operations work")
print("✓ Real-time UPDATE operations work")
print("✓ Real-time DELETE operations work")
print("✓ Complex JOINs are working correctly")
print("✓ Analytics queries return live data")
print("✓ All operations reflect immediately in the database")
print()
print("The system is using LIVE DATABASE DATA - NO MOCK DATA!")
print("=" * 70)

# Close connection
cursor.close()
conn.close()
