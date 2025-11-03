# ai_features.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from database import Database
import json

class HealthAI:
    """AI-powered health analytics and predictions"""
    
    @staticmethod
    def predict_patient_risk(patient_id):
        """
        Predict patient risk level based on medical history and current condition
        Returns: risk_score (0-100), risk_level (Low/Medium/High), recommendations
        """
        try:
            # Get patient data
            query = """
                SELECT p.age, p.gender, 
                       COUNT(DISTINCT mh.history_id) as history_count,
                       COUNT(DISTINCT pr.report_id) as admission_count
                FROM patient p
                LEFT JOIN medicalhistory mh ON p.patient_id = mh.patient_id
                LEFT JOIN patientreport pr ON p.patient_id = pr.patient_id
                WHERE p.patient_id = %s
                GROUP BY p.patient_id
            """
            result = Database.execute_query(query, (patient_id,))
            
            if not result:
                return {'risk_score': 0, 'risk_level': 'Unknown', 'recommendations': []}
            
            data = result[0]
            age = data['age'] or 30
            history_count = data['history_count'] or 0
            admission_count = data['admission_count'] or 0
            
            # Simple risk scoring algorithm
            risk_score = 0
            
            # Age factor (0-30 points)
            if age > 70:
                risk_score += 30
            elif age > 60:
                risk_score += 20
            elif age > 50:
                risk_score += 10
            elif age < 5:
                risk_score += 15
            
            # Medical history factor (0-35 points)
            risk_score += min(history_count * 5, 35)
            
            # Admission history factor (0-35 points)
            risk_score += min(admission_count * 7, 35)
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = 'High'
                color = 'danger'
            elif risk_score >= 40:
                risk_level = 'Medium'
                color = 'warning'
            else:
                risk_level = 'Low'
                color = 'success'
            
            # Generate recommendations
            recommendations = []
            if risk_score >= 70:
                recommendations.append('Immediate medical attention recommended')
                recommendations.append('Consider ICU monitoring')
                recommendations.append('Frequent vital signs monitoring required')
            elif risk_score >= 40:
                recommendations.append('Regular medical check-ups advised')
                recommendations.append('Monitor for any symptom changes')
                recommendations.append('Maintain prescribed medication schedule')
            else:
                recommendations.append('Maintain healthy lifestyle')
                recommendations.append('Annual check-up recommended')
                recommendations.append('Continue preventive care')
            
            if age > 65:
                recommendations.append('Age-specific health screening advised')
            
            return {
                'risk_score': min(risk_score, 100),
                'risk_level': risk_level,
                'color': color,
                'recommendations': recommendations,
                'factors': {
                    'age': age,
                    'history_count': history_count,
                    'admission_count': admission_count
                }
            }
        except Exception as e:
            print(f"Error in predict_patient_risk: {e}")
            return {
                'risk_score': 0,
                'risk_level': 'Unknown',
                'color': 'secondary',
                'recommendations': ['Unable to calculate risk'],
                'factors': {}
            }
    
    @staticmethod
    def predict_bed_occupancy(days_ahead=7):
        """
        Predict bed occupancy for next N days
        Returns: list of predicted occupancy rates
        """
        try:
            # Get historical admission data
            query = """
                SELECT DATE(in_date_time) as date, COUNT(*) as admissions
                FROM patientreport
                WHERE in_date_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY DATE(in_date_time)
                ORDER BY date
            """
            historical_data = Database.execute_query(query)
            
            if not historical_data or len(historical_data) < 7:
                # Not enough data, return default predictions
                return [{'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'), 
                        'predicted_occupancy': 65 + (i * 2)} for i in range(days_ahead)]
            
            # Calculate average and trend
            admissions = [d['admissions'] for d in historical_data]
            avg_admissions = np.mean(admissions)
            
            # Simple linear trend
            if len(admissions) > 1:
                trend = (admissions[-1] - admissions[0]) / len(admissions)
            else:
                trend = 0
            
            # Generate predictions
            predictions = []
            total_beds = 50  # Assuming 50 general ward beds
            
            for i in range(days_ahead):
                predicted_admissions = avg_admissions + (trend * i)
                predicted_occupancy = (predicted_admissions / total_beds) * 100
                predicted_occupancy = min(max(predicted_occupancy, 40), 95)  # Clamp between 40-95%
                
                predictions.append({
                    'date': (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d'),
                    'predicted_occupancy': round(predicted_occupancy, 1),
                    'predicted_count': round(predicted_admissions)
                })
            
            return predictions
        except Exception as e:
            print(f"Error in predict_bed_occupancy: {e}")
            return [{'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'), 
                    'predicted_occupancy': 65} for i in range(days_ahead)]
    
    @staticmethod
    def analyze_disease_patterns():
        """
        Analyze common disease patterns from medical history
        Returns: top diseases and their frequencies
        """
        try:
            query = """
                SELECT mh.disease, COUNT(*) as frequency,
                       ROUND(AVG(p.age), 0) as avg_patient_age
                FROM medicalhistory mh
                LEFT JOIN patient p ON mh.patient_id = p.patient_id
                WHERE mh.disease IS NOT NULL AND mh.disease != ''
                GROUP BY mh.disease
                ORDER BY frequency DESC
                LIMIT 10
            """
            results = Database.execute_query(query)
            
            if not results:
                return []
            
            total = sum([r['frequency'] for r in results])
            
            patterns = []
            for result in results:
                patterns.append({
                    'disease': result['disease'],
                    'frequency': result['frequency'],
                    'percentage': round((result['frequency'] / total) * 100, 1) if total > 0 else 0,
                    'avg_age': int(result['avg_patient_age']) if result['avg_patient_age'] else 0
                })
            
            return patterns
        except Exception as e:
            print(f"Error in analyze_disease_patterns: {e}")
            return []
    
    @staticmethod
    def get_age_wise_distribution():
        """Get age-wise patient distribution"""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN age < 18 THEN '0-17'
                        WHEN age BETWEEN 18 AND 30 THEN '18-30'
                        WHEN age BETWEEN 31 AND 45 THEN '31-45'
                        WHEN age BETWEEN 46 AND 60 THEN '46-60'
                        ELSE '60+'
                    END as age_group,
                    COUNT(*) as count
                FROM patient
                GROUP BY age_group
                ORDER BY 
                    CASE age_group
                        WHEN '0-17' THEN 1
                        WHEN '18-30' THEN 2
                        WHEN '31-45' THEN 3
                        WHEN '46-60' THEN 4
                        ELSE 5
                    END
            """
            results = Database.execute_query(query)
            return results if results else []
        except Exception as e:
            print(f"Error in age distribution: {e}")
            return []
    
    @staticmethod
    def get_gender_distribution():
        """Get gender-wise patient distribution"""
        try:
            query = """
                SELECT gender, COUNT(*) as count
                FROM patient
                GROUP BY gender
            """
            results = Database.execute_query(query)
            return results if results else []
        except Exception as e:
            return []
    
    @staticmethod
    def get_monthly_admissions():
        """Get monthly admission trends"""
        try:
            query = """
                SELECT 
                    DATE_FORMAT(in_date_time, '%Y-%m') as month,
                    COUNT(*) as admissions
                FROM patientreport
                WHERE in_date_time >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY month
                ORDER BY month
            """
            results = Database.execute_query(query)
            return results if results else []
        except Exception as e:
            return []
    
    @staticmethod
    def get_operation_statistics():
        """Get operation theatre statistics"""
        try:
            query = """
                SELECT 
                    status,
                    COUNT(*) as count
                FROM ot
                GROUP BY status
            """
            results = Database.execute_query(query)
            return results if results else []
        except Exception as e:
            return []
    
    @staticmethod
    def get_staff_workload():
        """Analyze staff workload"""
        try:
            query = """
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
                LIMIT 10
            """
            results = Database.execute_query(query)
            return results if results else []
        except Exception as e:
            print(f"Error in get_staff_workload: {e}")
            return []
    
    @staticmethod
    def get_average_stay_duration():
        """Calculate average hospital stay duration"""
        try:
            query = """
                SELECT 
                    AVG(DATEDIFF(out_date_time, in_date_time)) as avg_days
                FROM patientreport
                WHERE out_date_time IS NOT NULL
            """
            result = Database.execute_query(query)
            if result and result[0]['avg_days']:
                return round(result[0]['avg_days'], 1)
            return 0
        except Exception as e:
            return 0
    
    @staticmethod
    def get_readmission_rate():
        """Calculate patient readmission rate"""
        try:
            query = """
                SELECT 
                    COUNT(DISTINCT patient_id) as total_patients,
                    COUNT(*) as total_admissions
                FROM patientreport
            """
            result = Database.execute_query(query)
            if result and result[0]['total_patients'] > 0:
                readmission_rate = ((result[0]['total_admissions'] - result[0]['total_patients']) / 
                                  result[0]['total_patients']) * 100
                return round(max(0, readmission_rate), 1)
            return 0
        except Exception as e:
            return 0
    
    @staticmethod
    def get_treatment_recommendations(diagnosis):
        """
        Get AI-powered treatment recommendations based on diagnosis
        Returns: list of recommended treatments
        """
        # Common treatment mappings (simplified)
        treatment_knowledge_base = {
            'fever': [
                'Antipyretic medications (Paracetamol)',
                'Adequate hydration',
                'Rest and monitoring',
                'Check for underlying infection'
            ],
            'diabetes': [
                'Blood sugar monitoring',
                'Insulin therapy if required',
                'Dietary modifications',
                'Regular exercise regimen',
                'Foot care and regular check-ups'
            ],
            'hypertension': [
                'Antihypertensive medications',
                'Low sodium diet',
                'Regular blood pressure monitoring',
                'Stress management',
                'Regular cardiovascular check-ups'
            ],
            'infection': [
                'Appropriate antibiotic therapy',
                'Complete blood count monitoring',
                'Adequate rest and nutrition',
                'Follow-up cultures if needed'
            ],
            'fracture': [
                'Immobilization and casting',
                'Pain management',
                'X-ray follow-up',
                'Physical therapy post-healing',
                'Calcium and Vitamin D supplementation'
            ],
            'asthma': [
                'Bronchodilators',
                'Inhaled corticosteroids',
                'Avoid triggers and allergens',
                'Peak flow monitoring',
                'Action plan for exacerbations'
            ],
            'cardiac': [
                'ECG monitoring',
                'Cardiac enzyme tests',
                'Medication as per condition',
                'Lifestyle modifications',
                'Regular cardiologist follow-up'
            ]
        }
        
        if not diagnosis:
            return ['Comprehensive diagnostic evaluation needed', 
                   'Detailed patient history required',
                   'Appropriate investigations recommended']
        
        diagnosis_lower = diagnosis.lower()
        recommendations = []
        
        # Search for matching conditions
        for condition, treatments in treatment_knowledge_base.items():
            if condition in diagnosis_lower:
                recommendations.extend(treatments)
        
        # Generic recommendations if no match
        if not recommendations:
            recommendations = [
                'Detailed clinical evaluation recommended',
                'Appropriate diagnostic tests',
                'Specialist consultation if needed',
                'Symptomatic treatment',
                'Regular monitoring and follow-up'
            ]
        
        return recommendations
    
    @staticmethod
    def predict_ot_duration(procedure_name):
        """
        Predict operation theatre duration based on procedure
        Returns: estimated duration in hours
        """
        # Simplified duration estimates
        duration_map = {
            'appendectomy': {'min': 1, 'max': 2, 'avg': 1.5},
            'cesarean': {'min': 1, 'max': 1.5, 'avg': 1.25},
            'hernia': {'min': 1, 'max': 2, 'avg': 1.5},
            'orthopedic': {'min': 2, 'max': 4, 'avg': 3},
            'cardiac': {'min': 3, 'max': 6, 'avg': 4.5},
            'neuro': {'min': 3, 'max': 8, 'avg': 5},
            'laparoscopy': {'min': 1, 'max': 3, 'avg': 2},
            'default': {'min': 1, 'max': 3, 'avg': 2}
        }
        
        procedure_lower = procedure_name.lower() if procedure_name else ''
        
        for key, duration in duration_map.items():
            if key in procedure_lower:
                return duration
        
        return duration_map['default']
    
    @staticmethod
    def generate_health_insights(patient_id):
        """
        Generate comprehensive health insights for a patient
        """
        try:
            # Get patient basic info
            patient_query = "SELECT * FROM patient WHERE patient_id = %s"
            patient = Database.execute_query(patient_query, (patient_id,))
            
            if not patient:
                return None
            
            patient = patient[0]
            
            # Get medical history
            history_query = """
                SELECT COUNT(*) as total_visits,
                       MAX(date_time) as last_visit
                FROM medicalhistory
                WHERE patient_id = %s
            """
            history = Database.execute_query(history_query, (patient_id,))[0]
            
            # Get admission history
            admission_query = """
                SELECT COUNT(*) as total_admissions,
                       MAX(in_date_time) as last_admission
                FROM patientreport
                WHERE patient_id = %s
            """
            admissions = Database.execute_query(admission_query, (patient_id,))[0]
            
            # Calculate health score (0-100)
            health_score = 100
            age = patient['age'] or 30
            
            if age > 70:
                health_score -= 15
            elif age > 60:
                health_score -= 10
            
            health_score -= min(history['total_visits'] * 3, 30)
            health_score -= min(admissions['total_admissions'] * 5, 25)
            health_score = max(health_score, 40)
            
            return {
                'patient': patient,
                'health_score': health_score,
                'total_visits': history['total_visits'],
                'total_admissions': admissions['total_admissions'],
                'last_visit': history['last_visit'],
                'last_admission': admissions['last_admission']
            }
        except Exception as e:
            print(f"Error generating health insights: {e}")
            return None
    
    @staticmethod
    def get_resource_optimization_suggestions():
        """
        AI-powered suggestions for resource optimization
        """
        suggestions = []
        
        try:
            # Check bed utilization
            ward_query = "SELECT COUNT(*) as occupied FROM generalward WHERE patient_id IS NOT NULL"
            ward_result = Database.execute_query(ward_query)
            occupied = ward_result[0]['occupied'] if ward_result else 0
            total_beds = 50
            utilization = (occupied / total_beds) * 100
            
            if utilization > 90:
                suggestions.append({
                    'type': 'Critical',
                    'category': 'Bed Management',
                    'message': 'General ward occupancy is very high (>90%). Consider expediting discharges or arranging additional beds.',
                    'priority': 'high'
                })
            elif utilization < 30:
                suggestions.append({
                    'type': 'Info',
                    'category': 'Bed Management',
                    'message': 'General ward occupancy is low (<30%). Resources can be optimized.',
                    'priority': 'low'
                })
            
            # Check pending operations
            ot_query = "SELECT COUNT(*) as pending FROM ot WHERE status = 'Scheduled'"
            ot_result = Database.execute_query(ot_query)
            pending = ot_result[0]['pending'] if ot_result else 0
            
            if pending > 10:
                suggestions.append({
                    'type': 'Warning',
                    'category': 'Operation Theatre',
                    'message': f'{pending} operations pending. Consider scheduling additional OT time.',
                    'priority': 'medium'
                })
            
            # Check today's appointments
            appt_query = "SELECT COUNT(*) as today FROM opdappointment WHERE DATE(appointment_date) = CURDATE()"
            appt_result = Database.execute_query(appt_query)
            today_appts = appt_result[0]['today'] if appt_result else 0
            
            if today_appts > 50:
                suggestions.append({
                    'type': 'Info',
                    'category': 'OPD Management',
                    'message': f'{today_appts} appointments today. Ensure adequate staff allocation.',
                    'priority': 'medium'
                })
            
            # If no issues found
            if not suggestions:
                suggestions.append({
                    'type': 'Success',
                    'category': 'System Status',
                    'message': 'All resources are optimally utilized. No immediate actions required.',
                    'priority': 'low'
                })
            
            return suggestions
        except Exception as e:
            print(f"Error in resource optimization: {e}")
            return [{
                'type': 'Error',
                'category': 'System',
                'message': 'Unable to generate optimization suggestions.',
                'priority': 'low'
            }]
