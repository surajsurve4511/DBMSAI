# database.py
import mysql.connector
from mysql.connector import Error
from config import Config
from contextlib import contextmanager

class Database:
    """Database connection and operations handler"""
    
    @staticmethod
    @contextmanager
    def get_connection():
        """Context manager for database connections"""
        conn = None
        try:
            conn = mysql.connector.connect(**Config.DB_CONFIG)
            yield conn
        except Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()
    
    @staticmethod
    def execute_query(query, params=None, fetch=True):
        """Execute a query and return results"""
        with Database.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                conn.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
    
    @staticmethod
    def execute_many(query, data):
        """Execute query with multiple data sets"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, data)
            conn.commit()
            cursor.close()
            return True


class PatientModel:
    """Patient management operations"""
    
    @staticmethod
    def get_all_patients(limit=None, offset=0):
        """Get all patients with pagination"""
        query = "SELECT * FROM patient ORDER BY patient_id DESC"
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        return Database.execute_query(query)
    
    @staticmethod
    def get_patient_by_id(patient_id):
        """Get patient details by ID"""
        query = "SELECT * FROM patient WHERE patient_id = %s"
        result = Database.execute_query(query, (patient_id,))
        return result[0] if result else None
    
    @staticmethod
    def add_patient(name, age, gender, contact_info):
        """Add new patient"""
        query = """
            INSERT INTO patient (name, age, gender, contact_info) 
            VALUES (%s, %s, %s, %s)
        """
        return Database.execute_query(query, (name, age, gender, contact_info), fetch=False)
    
    @staticmethod
    def update_patient(patient_id, name, age, gender, contact_info):
        """Update patient information"""
        query = """
            UPDATE patient 
            SET name = %s, age = %s, gender = %s, contact_info = %s 
            WHERE patient_id = %s
        """
        Database.execute_query(query, (name, age, gender, contact_info, patient_id), fetch=False)
        return True
    
    @staticmethod
    def delete_patient(patient_id):
        """Delete patient"""
        query = "DELETE FROM patient WHERE patient_id = %s"
        Database.execute_query(query, (patient_id,), fetch=False)
        return True
    
    @staticmethod
    def search_patients(search_term):
        """Search patients by name or contact"""
        query = """
            SELECT * FROM patient 
            WHERE name LIKE %s OR contact_info LIKE %s
            ORDER BY patient_id DESC
        """
        search = f"%{search_term}%"
        return Database.execute_query(query, (search, search))
    
    @staticmethod
    def get_patient_count():
        """Get total patient count"""
        query = "SELECT COUNT(*) as count FROM patient"
        result = Database.execute_query(query)
        return result[0]['count'] if result else 0


class MedicalHistoryModel:
    """Medical history operations"""
    
    @staticmethod
    def get_patient_history(patient_id):
        """Get medical history for a patient"""
        query = """
            SELECT * FROM medicalhistory 
            WHERE patient_id = %s 
            ORDER BY date_time DESC
        """
        return Database.execute_query(query, (patient_id,))
    
    @staticmethod
    def add_history(patient_id, disease, treatment, date_time):
        """Add medical history entry"""
        query = """
            INSERT INTO medicalhistory (patient_id, disease, treatment, date_time) 
            VALUES (%s, %s, %s, %s)
        """
        return Database.execute_query(query, (patient_id, disease, treatment, date_time), fetch=False)


class PatientReportModel:
    """Patient report operations"""
    
    @staticmethod
    def get_all_reports(limit=None):
        """Get all patient reports"""
        query = """
            SELECT pr.*, p.name as patient_name, p.age, p.gender 
            FROM patientreport pr
            LEFT JOIN patient p ON pr.patient_id = p.patient_id
            ORDER BY pr.in_date_time DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return Database.execute_query(query)
    
    @staticmethod
    def get_report_by_id(report_id):
        """Get specific report"""
        query = """
            SELECT pr.*, p.name as patient_name, p.age, p.gender, p.contact_info
            FROM patientreport pr
            LEFT JOIN patient p ON pr.patient_id = p.patient_id
            WHERE pr.report_id = %s
        """
        result = Database.execute_query(query, (report_id,))
        return result[0] if result else None
    
    @staticmethod
    def add_report(patient_id, diagnosis, treatment, in_date_time):
        """Add new patient report"""
        query = """
            INSERT INTO patientreport (patient_id, diagnosis, treatment, in_date_time) 
            VALUES (%s, %s, %s, %s)
        """
        return Database.execute_query(query, (patient_id, diagnosis, treatment, in_date_time), fetch=False)
    
    @staticmethod
    def update_report_discharge(report_id, out_date_time):
        """Update report with discharge time"""
        query = """
            UPDATE patientreport 
            SET out_date_time = %s 
            WHERE report_id = %s
        """
        Database.execute_query(query, (out_date_time, report_id), fetch=False)
        return True
    
    @staticmethod
    def get_active_reports():
        """Get reports without discharge date"""
        query = """
            SELECT pr.*, p.name as patient_name, p.age 
            FROM patientreport pr
            LEFT JOIN patient p ON pr.patient_id = p.patient_id
            WHERE pr.out_date_time IS NULL
            ORDER BY pr.in_date_time DESC
        """
        return Database.execute_query(query)


class OPDModel:
    """OPD appointment operations"""
    
    @staticmethod
    def get_all_appointments(limit=None):
        """Get all OPD appointments"""
        query = """
            SELECT o.*, p.name as patient_name, p.age, s.name as staff_name
            FROM opdappointment o
            LEFT JOIN patient p ON o.patient_id = p.patient_id
            LEFT JOIN staff s ON o.staff_id = s.staff_id
            ORDER BY o.appointment_date DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return Database.execute_query(query)
    
    @staticmethod
    def add_appointment(patient_id, staff_id, issue_description, appointment_date, next_visit_date=None):
        """Add new OPD appointment"""
        query = """
            INSERT INTO opdappointment 
            (patient_id, staff_id, issue_description, appointment_date, next_visit_date) 
            VALUES (%s, %s, %s, %s, %s)
        """
        return Database.execute_query(
            query, 
            (patient_id, staff_id, issue_description, appointment_date, next_visit_date), 
            fetch=False
        )
    
    @staticmethod
    def get_today_appointments():
        """Get today's appointments"""
        query = """
            SELECT o.*, p.name as patient_name, s.name as staff_name
            FROM opdappointment o
            LEFT JOIN patient p ON o.patient_id = p.patient_id
            LEFT JOIN staff s ON o.staff_id = s.staff_id
            WHERE DATE(o.appointment_date) = CURDATE()
            ORDER BY o.appointment_date
        """
        return Database.execute_query(query)


class StaffModel:
    """Staff management operations"""
    
    @staticmethod
    def get_all_staff():
        """Get all staff members"""
        query = """
            SELECT s.*, sr.role_name 
            FROM staff s
            LEFT JOIN staffrole sr ON s.role_id = sr.role_id
            ORDER BY s.staff_id
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_staff_by_role(role_name):
        """Get staff by role"""
        query = """
            SELECT s.*, sr.role_name 
            FROM staff s
            LEFT JOIN staffrole sr ON s.role_id = sr.role_id
            WHERE sr.role_name = %s
        """
        return Database.execute_query(query, (role_name,))
    
    @staticmethod
    def add_staff(name, role_id, shift_time):
        """Add new staff member"""
        query = """
            INSERT INTO staff (name, role_id, shift_time) 
            VALUES (%s, %s, %s)
        """
        return Database.execute_query(query, (name, role_id, shift_time), fetch=False)
    
    @staticmethod
    def get_all_roles():
        """Get all staff roles"""
        query = "SELECT * FROM staffrole"
        return Database.execute_query(query)


class OTModel:
    """Operation Theatre operations"""
    
    @staticmethod
    def get_all_operations(limit=None):
        """Get all operations"""
        query = """
            SELECT o.*, p.name as patient_name, p.age 
            FROM ot o
            LEFT JOIN patient p ON o.patient_id = p.patient_id
            ORDER BY o.date DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return Database.execute_query(query)
    
    @staticmethod
    def add_operation(patient_id, date, procedure_name, status):
        """Add new operation"""
        query = """
            INSERT INTO ot (patient_id, date, procedure_name, status) 
            VALUES (%s, %s, %s, %s)
        """
        return Database.execute_query(query, (patient_id, date, procedure_name, status), fetch=False)
    
    @staticmethod
    def update_operation_status(ot_id, status):
        """Update operation status"""
        query = "UPDATE ot SET status = %s WHERE ot_id = %s"
        Database.execute_query(query, (status, ot_id), fetch=False)
        return True
    
    @staticmethod
    def get_scheduled_operations():
        """Get scheduled operations"""
        query = """
            SELECT o.*, p.name as patient_name 
            FROM ot o
            LEFT JOIN patient p ON o.patient_id = p.patient_id
            WHERE o.status = 'Scheduled'
            ORDER BY o.date
        """
        return Database.execute_query(query)


class WardModel:
    """Ward management operations"""
    
    @staticmethod
    def get_general_ward_occupancy():
        """Get general ward bed occupancy"""
        query = """
            SELECT gw.*, p.name as patient_name, pr.diagnosis 
            FROM generalward gw
            LEFT JOIN patient p ON gw.patient_id = p.patient_id
            LEFT JOIN patientreport pr ON gw.report_id = pr.report_id
            ORDER BY gw.bed_no
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_icu_occupancy():
        """Get ICU bed occupancy"""
        query = """
            SELECT i.*, pr.patient_id, p.name as patient_name, pr.diagnosis 
            FROM icu i
            LEFT JOIN patientreport pr ON i.report_id = pr.report_id
            LEFT JOIN patient p ON pr.patient_id = p.patient_id
            ORDER BY i.icu_id
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_special_rooms():
        """Get special room occupancy"""
        query = """
            SELECT sr.*, rt.room_type_name, p.name as patient_name, pr.diagnosis 
            FROM specialroom sr
            LEFT JOIN roomtype rt ON sr.room_type_id = rt.room_type_id
            LEFT JOIN patient p ON sr.patient_id = p.patient_id
            LEFT JOIN patientreport pr ON sr.report_id = pr.report_id
            ORDER BY sr.room_id
        """
        return Database.execute_query(query)
    
    @staticmethod
    def assign_general_ward(bed_no, patient_id, report_id):
        """Assign patient to general ward"""
        query = """
            INSERT INTO generalward (bed_no, patient_id, report_id) 
            VALUES (%s, %s, %s)
        """
        return Database.execute_query(query, (bed_no, patient_id, report_id), fetch=False)
    
    @staticmethod
    def get_available_beds():
        """Get count of available beds in general ward"""
        query = """
            SELECT COUNT(*) as occupied FROM generalward WHERE patient_id IS NOT NULL
        """
        result = Database.execute_query(query)
        occupied = result[0]['occupied'] if result else 0
        return {'occupied': occupied, 'total': 50, 'available': 50 - occupied}


class DashboardModel:
    """Dashboard statistics"""
    
    @staticmethod
    def get_statistics():
        """Get dashboard statistics"""
        stats = {}
        
        # Total patients
        query = "SELECT COUNT(*) as count FROM patient"
        result = Database.execute_query(query)
        stats['total_patients'] = result[0]['count'] if result else 0
        
        # Active admissions
        query = "SELECT COUNT(*) as count FROM patientreport WHERE out_date_time IS NULL"
        result = Database.execute_query(query)
        stats['active_admissions'] = result[0]['count'] if result else 0
        
        # Today's appointments
        query = "SELECT COUNT(*) as count FROM opdappointment WHERE DATE(appointment_date) = CURDATE()"
        result = Database.execute_query(query)
        stats['today_appointments'] = result[0]['count'] if result else 0
        
        # Scheduled operations
        query = "SELECT COUNT(*) as count FROM ot WHERE status = 'Scheduled'"
        result = Database.execute_query(query)
        stats['scheduled_operations'] = result[0]['count'] if result else 0
        
        # Staff count
        query = "SELECT COUNT(*) as count FROM staff"
        result = Database.execute_query(query)
        stats['total_staff'] = result[0]['count'] if result else 0
        
        # ICU occupancy
        query = "SELECT COUNT(*) as count FROM icu WHERE report_id IS NOT NULL"
        result = Database.execute_query(query)
        stats['icu_occupied'] = result[0]['count'] if result else 0
        
        return stats
