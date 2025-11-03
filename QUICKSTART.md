# Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Start MySQL
- Open XAMPP Control Panel
- Start Apache and MySQL services

### Step 3: Run the Application
```powershell
python app.py
```

### Step 4: Access the System
Open your browser and navigate to:
```
http://localhost:5000
```

## 🎮 Quick Tour

### 1. Dashboard (`/`)
- View hospital statistics at a glance
- See AI-powered insights
- Monitor today's activities

### 2. Add a Patient (`/patients` → Add New Patient)
- Name: John Doe
- Age: 45
- Gender: Male
- Contact: +1-234-567-8900, john@example.com

### 3. Schedule an OPD Appointment (`/opd`)
- Select patient ID
- Choose doctor
- Set appointment date/time

### 4. View AI Analytics (`/analytics`)
- See bed occupancy predictions
- Analyze disease patterns
- Get optimization suggestions

## 🎯 Key Features to Try

1. **Patient Risk Assessment**
   - Go to any patient detail page
   - View AI-generated risk score
   - See personalized recommendations

2. **Treatment Recommendations**
   - Admit a patient with diagnosis
   - AI will suggest treatments automatically

3. **Bed Occupancy Forecast**
   - Visit Analytics page
   - See 7-day prediction chart

4. **Ward Management**
   - Visual bed occupancy display
   - ICU monitoring
   - Special room tracking

## 🐛 Troubleshooting

### Issue: Can't connect to database
**Solution**: 
- Check if MySQL is running
- Verify database credentials in `config.py`
- Make sure `hospital` database exists

### Issue: Module not found error
**Solution**:
```powershell
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution**: Change port in `config.py`:
```python
PORT = 5001  # or any other available port
```

### Issue: Templates not found
**Solution**: Make sure you're running from the project root directory:
```powershell
cd C:\Suraj\SPPU\Project\DBMSAI
python app.py
```

## 📊 Sample Data

To test the system, you can add sample data:

### Sample Patients
1. John Doe, 45, Male, +1234567890
2. Jane Smith, 32, Female, +1234567891
3. Robert Brown, 68, Male, +1234567892
4. Emily Davis, 25, Female, +1234567893
5. Michael Wilson, 55, Male, +1234567894

### Sample Diagnoses
- Fever and Common Cold
- Diabetes Mellitus Type 2
- Hypertension
- Respiratory Infection
- Fracture - Left Arm
- Asthma
- Cardiac Arrhythmia

## 🎨 UI Highlights

- **Modern Gradient Design**: Beautiful color schemes throughout
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Engaging user experience
- **Interactive Charts**: Real-time data visualization
- **Icon Integration**: Clear visual indicators

## 🔧 Configuration

Edit `config.py` to customize:
- Database connection
- Application settings
- AI model parameters
- Pagination limits

## 📱 Mobile Access

The system is fully responsive! Access from any device:
- Desktop computers
- Tablets
- Smartphones

## 🎓 Learning Resources

To understand the codebase:
1. Start with `app.py` - Main application routes
2. Check `database.py` - Database operations
3. Review `ai_features.py` - AI algorithms
4. Explore templates - UI structure
5. Study `static/css/style.css` - Styling

## ⚡ Performance Tips

- Keep MySQL running for faster queries
- Use Chrome/Firefox for best experience
- Clear browser cache if styles don't load
- Use pagination for large datasets

## 🌟 Pro Tips

1. Use the search feature in Patient Management
2. Check AI suggestions on the dashboard daily
3. Monitor bed occupancy predictions weekly
4. Review disease patterns for trends
5. Keep staff information updated

## 📈 Next Steps

1. Add more patients to test AI features
2. Create appointments for different dates
3. Admit patients to test ward management
4. Schedule operations to test OT module
5. Explore all analytics features

## 💡 Need Help?

- Check the README.md for detailed documentation
- Review error messages in the console
- Verify all files are in place
- Ensure database schema matches

Enjoy using MediCare HMS! 🏥✨
