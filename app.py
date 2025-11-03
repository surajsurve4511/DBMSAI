# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
from database import (
    PatientModel, MedicalHistoryModel, PatientReportModel, 
    OPDModel, StaffModel, OTModel, WardModel, DashboardModel
)
from ai_features import HealthAI
from gemini_ai import gemini_ai
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f"Error: {str(error)}")
    return jsonify({'error': str(error)}), 500

# ==================== HOME & DASHBOARD ====================
@app.route('/')
def index():
    """Main dashboard"""
    try:
        stats = DashboardModel.get_statistics()
        recent_patients = PatientModel.get_all_patients(limit=5)
        today_appointments = OPDModel.get_today_appointments()
        active_reports = PatientReportModel.get_active_reports()
        ai_suggestions = HealthAI.get_resource_optimization_suggestions()
        
        return render_template('dashboard.html', 
                             stats=stats,
                             recent_patients=recent_patients,
                             today_appointments=today_appointments,
                             active_reports=active_reports,
                             ai_suggestions=ai_suggestions,
                             now=datetime.now())
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

# ==================== PATIENTS ====================
@app.route('/patients')
def patients():
    """Patient management page"""
    try:
        all_patients = PatientModel.get_all_patients()
        return render_template('patients.html', patients=all_patients)
    except Exception as e:
        return f"Error loading patients: {str(e)}", 500

@app.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    """Patient detail page with AI insights"""
    try:
        patient = PatientModel.get_patient_by_id(patient_id)
        if not patient:
            flash('Patient not found', 'error')
            return redirect(url_for('patients'))
        
        medical_history = MedicalHistoryModel.get_patient_history(patient_id)
        risk_analysis = HealthAI.predict_patient_risk(patient_id)
        health_insights = HealthAI.generate_health_insights(patient_id)
        
        # Gemini AI insights
        gemini_insights = None
        health_tips = []
        if gemini_ai.enabled:
            gemini_insights = gemini_ai.generate_patient_insights(patient, medical_history)
            conditions = [h['disease'] for h in medical_history[:3]]
            health_tips = gemini_ai.generate_health_tips(patient['age'], patient['gender'], conditions)
        
        return render_template('patient_detail.html',
                             patient=patient,
                             medical_history=medical_history,
                             risk_analysis=risk_analysis,
                             health_insights=health_insights,
                             gemini_insights=gemini_insights,
                             health_tips=health_tips)
    except Exception as e:
        return f"Error loading patient details: {str(e)}", 500

@app.route('/patient/add', methods=['GET', 'POST'])
def add_patient():
    """Add new patient"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            age = request.form.get('age')
            gender = request.form.get('gender')
            contact_info = request.form.get('contact_info')
            
            patient_id = PatientModel.add_patient(name, age, gender, contact_info)
            flash(f'Patient added successfully! ID: {patient_id}', 'success')
            return redirect(url_for('patients'))
        except Exception as e:
            flash(f'Error adding patient: {str(e)}', 'error')
            return redirect(url_for('add_patient'))
    
    return render_template('add_patient.html')

@app.route('/patient/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """Edit patient information"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            age = request.form.get('age')
            gender = request.form.get('gender')
            contact_info = request.form.get('contact_info')
            
            PatientModel.update_patient(patient_id, name, age, gender, contact_info)
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('patient_detail', patient_id=patient_id))
        except Exception as e:
            flash(f'Error updating patient: {str(e)}', 'error')
    
    patient = PatientModel.get_patient_by_id(patient_id)
    return render_template('edit_patient.html', patient=patient)

@app.route('/api/patients/search')
def search_patients():
    """Search patients API"""
    try:
        search_term = request.args.get('q', '')
        if search_term:
            results = PatientModel.search_patients(search_term)
        else:
            results = PatientModel.get_all_patients(limit=10)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== OPD APPOINTMENTS ====================
@app.route('/opd')
def opd_appointments():
    """OPD appointments page"""
    try:
        appointments = OPDModel.get_all_appointments(limit=50)
        today_appointments = OPDModel.get_today_appointments()
        staff_list = StaffModel.get_staff_by_role('Doctor')
        
        return render_template('opd.html',
                             appointments=appointments,
                             today_appointments=today_appointments,
                             staff_list=staff_list)
    except Exception as e:
        return f"Error loading OPD appointments: {str(e)}", 500

@app.route('/opd/add', methods=['POST'])
def add_opd_appointment():
    """Add new OPD appointment"""
    try:
        patient_id = request.form.get('patient_id')
        staff_id = request.form.get('staff_id')
        issue_description = request.form.get('issue_description')
        appointment_date = request.form.get('appointment_date')
        next_visit_date = request.form.get('next_visit_date') or None
        
        app_id = OPDModel.add_appointment(
            patient_id, staff_id, issue_description, 
            appointment_date, next_visit_date
        )
        
        flash(f'Appointment scheduled successfully! ID: {app_id}', 'success')
        return redirect(url_for('opd_appointments'))
    except Exception as e:
        flash(f'Error scheduling appointment: {str(e)}', 'error')
        return redirect(url_for('opd_appointments'))

# ==================== PATIENT REPORTS ====================
@app.route('/reports')
def patient_reports():
    """Patient reports and admissions"""
    try:
        all_reports = PatientReportModel.get_all_reports(limit=50)
        active_reports = PatientReportModel.get_active_reports()
        
        return render_template('reports.html',
                             all_reports=all_reports,
                             active_reports=active_reports)
    except Exception as e:
        return f"Error loading reports: {str(e)}", 500

@app.route('/report/add', methods=['POST'])
def add_report():
    """Add new patient report (admission)"""
    try:
        patient_id = request.form.get('patient_id')
        diagnosis = request.form.get('diagnosis')
        treatment = request.form.get('treatment')
        in_date_time = request.form.get('in_date_time')
        
        # Get patient data for Gemini AI
        patient = PatientModel.get_patient_by_id(patient_id)
        medical_history = MedicalHistoryModel.get_patient_history(patient_id)
        
        # Get AI treatment recommendations
        if gemini_ai.enabled and patient:
            # Use Gemini AI for advanced treatment plan
            gemini_treatment = gemini_ai.generate_treatment_plan(
                diagnosis, patient['age'], medical_history
            )
            treatment_with_ai = f"{treatment}\n\n🤖 AI-Generated Treatment Plan:\n{gemini_treatment}"
        else:
            # Use basic AI
            recommendations = HealthAI.get_treatment_recommendations(diagnosis)
            treatment_with_ai = f"{treatment}\n\nAI Recommendations:\n- " + "\n- ".join(recommendations)
        
        report_id = PatientReportModel.add_report(
            patient_id, diagnosis, treatment_with_ai, in_date_time
        )
        
        flash(f'Patient admitted successfully! Report ID: {report_id}', 'success')
        return redirect(url_for('patient_reports'))
    except Exception as e:
        flash(f'Error admitting patient: {str(e)}', 'error')
        return redirect(url_for('patient_reports'))

@app.route('/report/<int:report_id>/discharge', methods=['POST'])
def discharge_patient(report_id):
    """Discharge patient"""
    try:
        out_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        PatientReportModel.update_report_discharge(report_id, out_date_time)
        
        flash('Patient discharged successfully!', 'success')
        return redirect(url_for('patient_reports'))
    except Exception as e:
        flash(f'Error discharging patient: {str(e)}', 'error')
        return redirect(url_for('patient_reports'))

# ==================== OPERATION THEATRE ====================
@app.route('/ot')
def operation_theatre():
    """Operation theatre management"""
    try:
        all_operations = OTModel.get_all_operations(limit=50)
        scheduled_ops = OTModel.get_scheduled_operations()
        
        return render_template('ot.html',
                             all_operations=all_operations,
                             scheduled_ops=scheduled_ops)
    except Exception as e:
        return f"Error loading OT data: {str(e)}", 500

@app.route('/ot/add', methods=['POST'])
def add_operation():
    """Schedule new operation"""
    try:
        patient_id = request.form.get('patient_id')
        date = request.form.get('date')
        procedure_name = request.form.get('procedure_name')
        status = request.form.get('status', 'Scheduled')
        
        # Get AI duration estimate
        duration_estimate = HealthAI.predict_ot_duration(procedure_name)
        
        ot_id = OTModel.add_operation(patient_id, date, procedure_name, status)
        
        flash(f'Operation scheduled! ID: {ot_id}. Est. Duration: {duration_estimate["avg"]} hours', 'success')
        return redirect(url_for('operation_theatre'))
    except Exception as e:
        flash(f'Error scheduling operation: {str(e)}', 'error')
        return redirect(url_for('operation_theatre'))

@app.route('/ot/<int:ot_id>/update_status', methods=['POST'])
def update_ot_status(ot_id):
    """Update operation status"""
    try:
        status = request.form.get('status')
        OTModel.update_operation_status(ot_id, status)
        
        flash('Operation status updated!', 'success')
        return redirect(url_for('operation_theatre'))
    except Exception as e:
        flash(f'Error updating status: {str(e)}', 'error')
        return redirect(url_for('operation_theatre'))

# ==================== WARD MANAGEMENT ====================
@app.route('/wards')
def ward_management():
    """Ward and bed management"""
    try:
        general_ward = WardModel.get_general_ward_occupancy()
        icu_beds = WardModel.get_icu_occupancy()
        special_rooms = WardModel.get_special_rooms()
        bed_stats = WardModel.get_available_beds()
        
        return render_template('wards.html',
                             general_ward=general_ward,
                             icu_beds=icu_beds,
                             special_rooms=special_rooms,
                             bed_stats=bed_stats)
    except Exception as e:
        return f"Error loading ward data: {str(e)}", 500

# ==================== STAFF MANAGEMENT ====================
@app.route('/staff')
def staff_management():
    """Staff management page"""
    try:
        all_staff = StaffModel.get_all_staff()
        all_roles = StaffModel.get_all_roles()
        
        return render_template('staff.html',
                             all_staff=all_staff,
                             all_roles=all_roles)
    except Exception as e:
        return f"Error loading staff data: {str(e)}", 500

@app.route('/staff/add', methods=['POST'])
def add_staff():
    """Add new staff member"""
    try:
        name = request.form.get('name')
        role_id = request.form.get('role_id')
        shift_time = request.form.get('shift_time')
        
        staff_id = StaffModel.add_staff(name, role_id, shift_time)
        
        flash(f'Staff member added successfully! ID: {staff_id}', 'success')
        return redirect(url_for('staff_management'))
    except Exception as e:
        flash(f'Error adding staff: {str(e)}', 'error')
        return redirect(url_for('staff_management'))

# ==================== AI FEATURES & ANALYTICS ====================
@app.route('/analytics')
def analytics():
    """AI-powered analytics dashboard"""
    try:
        bed_predictions = HealthAI.predict_bed_occupancy(7)
        disease_patterns = HealthAI.analyze_disease_patterns()
        optimization_suggestions = HealthAI.get_resource_optimization_suggestions()
        
        # Additional analytics
        age_distribution = HealthAI.get_age_wise_distribution()
        gender_distribution = HealthAI.get_gender_distribution()
        monthly_admissions = HealthAI.get_monthly_admissions()
        operation_stats = HealthAI.get_operation_statistics()
        staff_workload = HealthAI.get_staff_workload()
        avg_stay = HealthAI.get_average_stay_duration()
        readmission_rate = HealthAI.get_readmission_rate()
        
        # Gemini AI trend analysis
        gemini_trends = None
        if gemini_ai.enabled and disease_patterns:
            gemini_trends = gemini_ai.analyze_hospital_trends(disease_patterns)
        
        return render_template('analytics.html',
                             bed_predictions=bed_predictions,
                             disease_patterns=disease_patterns,
                             optimization_suggestions=optimization_suggestions,
                             age_distribution=age_distribution,
                             gender_distribution=gender_distribution,
                             monthly_admissions=monthly_admissions,
                             operation_stats=operation_stats,
                             staff_workload=staff_workload,
                             avg_stay=avg_stay,
                             readmission_rate=readmission_rate,
                             gemini_trends=gemini_trends)
    except Exception as e:
        return f"Error loading analytics: {str(e)}", 500

@app.route('/symptom-analyzer')
def symptom_analyzer():
    """AI-powered symptom analyzer page"""
    return render_template('symptom_analyzer.html')

@app.route('/api/ai/patient-risk/<int:patient_id>')
def api_patient_risk(patient_id):
    """API endpoint for patient risk prediction"""
    try:
        risk_data = HealthAI.predict_patient_risk(patient_id)
        return jsonify(risk_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/treatment-recommendations', methods=['POST'])
def api_treatment_recommendations():
    """API endpoint for treatment recommendations"""
    try:
        data = request.get_json()
        diagnosis = data.get('diagnosis', '')
        recommendations = HealthAI.get_treatment_recommendations(diagnosis)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bed-occupancy-forecast')
def api_bed_occupancy_forecast():
    """API endpoint for bed occupancy prediction"""
    try:
        days = request.args.get('days', 7, type=int)
        predictions = HealthAI.predict_bed_occupancy(days)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== UTILITY ROUTES ====================
@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    try:
        stats = DashboardModel.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-symptoms', methods=['POST'])
def analyze_symptoms_api():
    """API endpoint for Gemini AI symptom analysis"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        age = data.get('age')
        gender = data.get('gender')
        
        if not gemini_ai.enabled:
            return jsonify({
                'error': 'Gemini AI not configured',
                'message': 'Please configure GEMINI_API_KEY in .env file'
            }), 503
        
        analysis = gemini_ai.analyze_symptoms(symptoms, age, gender)
        return jsonify({'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict-complications', methods=['POST'])
def predict_complications_api():
    """API endpoint for complication prediction"""
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        
        if not gemini_ai.enabled:
            return jsonify({
                'error': 'Gemini AI not configured',
                'message': 'Please configure GEMINI_API_KEY in .env file'
            }), 503
        
        patient = PatientModel.get_patient_by_id(patient_id)
        medical_history = MedicalHistoryModel.get_patient_history(patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        complications = gemini_ai.predict_complications(patient, medical_history)
        return jsonify({'complications': complications})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/discharge-summary/<int:report_id>')
def generate_discharge_summary_api(report_id):
    """API endpoint for generating discharge summary"""
    try:
        if not gemini_ai.enabled:
            return jsonify({
                'error': 'Gemini AI not configured',
                'message': 'Please configure GEMINI_API_KEY in .env file'
            }), 503
        
        # Get report and patient details
        report = PatientReportModel.get_report_by_id(report_id)
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        patient = PatientModel.get_patient_by_id(report['PatientID'])
        medical_history = MedicalHistoryModel.get_patient_history(report['PatientID'])
        
        summary = gemini_ai.generate_discharge_summary(report, patient, medical_history)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-analytics')
def advanced_analytics_api():
    """API endpoint for advanced analytics data"""
    try:
        data = {
            'age_distribution': HealthAI.get_age_wise_distribution(),
            'gender_distribution': HealthAI.get_gender_distribution(),
            'monthly_admissions': HealthAI.get_monthly_admissions(),
            'operation_statistics': HealthAI.get_operation_statistics(),
            'staff_workload': HealthAI.get_staff_workload(),
            'avg_stay_duration': HealthAI.get_average_stay_duration(),
            'readmission_rate': HealthAI.get_readmission_rate(),
            'disease_patterns': HealthAI.analyze_disease_patterns()
        }
        
        # Add Gemini AI trends if enabled
        if gemini_ai.enabled and data['disease_patterns']:
            data['ai_trends'] = gemini_ai.analyze_hospital_trends(data['disease_patterns'])
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.template_filter('datetime')
def format_datetime(value, format='%Y-%m-%d %H:%M'):
    """Format datetime for templates"""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            return value
    return value.strftime(format)

@app.template_filter('date')
def format_date(value, format='%Y-%m-%d'):
    """Format date for templates"""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except:
            return value
    return value.strftime(format)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
