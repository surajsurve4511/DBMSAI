# 🏥 MediCare Hospital Management System

A comprehensive, AI-powered Hospital Management System built with Flask, MySQL, and modern web technologies.

## ✨ Features

### 🎯 Core Functionality
- **Patient Management**: Complete patient registration, profile management, and medical history tracking
- **OPD Appointments**: Schedule and manage out-patient department appointments
- **Admission & Discharge**: Patient admission reports and discharge management
- **Operation Theatre**: Schedule and track surgical operations with status updates
- **Ward Management**: Monitor bed occupancy across general wards, ICU, and special rooms
- **Staff Management**: Manage hospital staff with roles and shift assignments

### 🤖 AI-Powered Features
- **Patient Risk Assessment**: AI-driven risk prediction based on age, medical history, and admissions
- **Bed Occupancy Forecasting**: 7-day predictive analytics for bed utilization
- **Treatment Recommendations**: AI-powered treatment suggestions based on diagnosis
- **Disease Pattern Analysis**: Analyze and visualize common disease trends
- **Resource Optimization**: Intelligent suggestions for optimal resource allocation
- **Operation Duration Prediction**: Estimate OT time based on procedure type

### 🎨 User Interface
- Modern, responsive design with gradient color schemes
- Interactive dashboard with real-time statistics
- Animated cards and smooth transitions
- Mobile-friendly responsive layouts
- Beautiful data visualizations with Chart.js

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **MySQL**: Database management
- **Pandas & NumPy**: Data processing
- **Scikit-learn**: Machine learning capabilities

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Data visualization
- **Bootstrap Icons**: Icon library
- **Custom CSS**: Modern gradient designs
- **Vanilla JavaScript**: Interactive features

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server (XAMPP, WAMP, or standalone)
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```powershell
   cd C:\Suraj\SPPU\Project\DBMSAI
   ```

2. **Install required packages**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure Database**
   - Open `config.py`
   - Update database credentials if needed:
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'database': 'hospital',
         'user': 'root',
         'password': '',  # Update if you have a password
         'port': 3306
     }
     ```

4. **Ensure MySQL is running**
   - Start XAMPP/WAMP or MySQL service
   - Make sure the `hospital` database exists with all tables

5. **Run the application**
   ```powershell
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
DBMSAI/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database models and operations
├── ai_features.py         # AI/ML features and analytics
├── db_connect.py          # Original schema viewer
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── script.js     # JavaScript functionality
└── templates/
    ├── base.html          # Base template
    ├── dashboard.html     # Main dashboard
    ├── patients.html      # Patient list
    ├── patient_detail.html # Patient profile
    ├── add_patient.html   # Add new patient
    ├── edit_patient.html  # Edit patient
    ├── opd.html          # OPD appointments
    ├── reports.html      # Patient reports
    ├── ot.html           # Operation theatre
    ├── wards.html        # Ward management
    ├── staff.html        # Staff management
    └── analytics.html    # AI analytics dashboard
```

## 🎯 Usage Guide

### Dashboard
- View real-time statistics of patients, admissions, appointments, and operations
- Monitor AI-powered insights and recommendations
- Quick access to recent patients and today's appointments

### Patient Management
1. Add new patients with complete information
2. View patient profiles with AI risk assessment
3. Track medical history and health insights
4. Edit patient information as needed

### OPD Appointments
1. Schedule appointments with available doctors
2. Track today's appointments
3. Set follow-up visit dates

### Patient Reports
1. Admit patients with diagnosis and treatment plans
2. AI automatically provides treatment recommendations
3. Discharge patients when ready

### Operation Theatre
1. Schedule surgical operations
2. Update operation status (Scheduled → In Progress → Completed)
3. AI estimates operation duration

### Ward Management
- Visual bed occupancy for general ward
- Monitor ICU beds and equipment
- Track special room availability

### Analytics Dashboard
- View 7-day bed occupancy predictions
- Analyze common disease patterns
- Get resource optimization suggestions
- Interactive charts and visualizations

## 🔒 Security Notes

⚠️ **Important**: This is a development version. For production use:
- Change the `SECRET_KEY` in `config.py`
- Use environment variables for sensitive data
- Implement user authentication
- Add input validation and sanitization
- Use HTTPS
- Implement proper access controls

## 🤝 Contributing

This project was created as part of a DBMS/AI project. Feel free to:
- Report bugs
- Suggest new features
- Improve AI algorithms
- Enhance UI/UX

## 📝 Database Schema

The system uses the following tables:
- `patient` - Patient information
- `medicalhistory` - Medical history records
- `patientreport` - Admission/discharge reports
- `opdappointment` - OPD appointments
- `ot` - Operation theatre records
- `generalward` - General ward bed allocation
- `icu` - ICU bed management
- `specialroom` - Special room allocation
- `roomtype` - Room type definitions
- `staff` - Staff information
- `staffrole` - Staff role definitions
- `instrument` - Medical instruments
- `ot_instrument` - OT instrument assignments
- `ot_staff_assignment` - OT staff assignments

## 🎓 AI Features Explained

### Risk Assessment Algorithm
- Analyzes patient age, medical history frequency, and admission count
- Generates risk score (0-100) and categorizes as Low/Medium/High
- Provides personalized recommendations based on risk level

### Bed Occupancy Prediction
- Uses historical admission data from past 30 days
- Applies trend analysis and moving averages
- Predicts occupancy for next 7 days

### Treatment Recommendations
- Knowledge-based system with common medical conditions
- Provides evidence-based treatment suggestions
- Customizable knowledge base for different diagnoses

## 📞 Support

For issues or questions:
- Check the console for error messages
- Verify database connection
- Ensure all dependencies are installed
- Review the error logs in the terminal

## 📄 License

This project is created for educational purposes as part of SPPU DBMS/AI coursework.

## 🌟 Acknowledgments

- Bootstrap for the responsive framework
- Chart.js for data visualizations
- Flask community for excellent documentation
- AI/ML algorithms inspired by healthcare analytics research

---

**Made with ❤️ for better healthcare management**
