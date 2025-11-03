# ✅ Pre-Launch Checklist

## Before Running the Application

### 1. System Requirements ✓
- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] MySQL server installed (XAMPP/WAMP/Standalone)
- [ ] Web browser (Chrome/Firefox/Edge)
- [ ] 2GB RAM minimum
- [ ] 500MB free disk space

### 2. Database Setup ✓
- [ ] MySQL server is running
- [ ] `hospital` database exists
- [ ] All 14 tables are created
- [ ] Database has sample data (optional but recommended)
- [ ] Can connect via db_connect.py script

### 3. Python Dependencies ✓
- [ ] Flask 3.0.0
- [ ] mysql-connector-python 8.2.0
- [ ] pandas 2.1.3
- [ ] numpy 1.26.2
- [ ] scikit-learn 1.3.2
- [ ] plotly 5.18.0
- [ ] python-dateutil 2.8.2
- [ ] Werkzeug 3.0.1

Run: `pip install -r requirements.txt`

### 4. File Structure ✓
- [ ] app.py exists
- [ ] database.py exists
- [ ] ai_features.py exists
- [ ] config.py exists
- [ ] templates/ folder with all HTML files
- [ ] static/css/style.css exists
- [ ] static/js/script.js exists

### 5. Configuration ✓
- [ ] Database credentials in config.py are correct
- [ ] Host: localhost
- [ ] Database: hospital
- [ ] User: root (or your MySQL user)
- [ ] Password: (empty or your password)
- [ ] Port: 3306

### 6. Quick Tests ✓
- [ ] Run: `python check_setup.py` - All checks pass
- [ ] Run: `python db_connect.py` - Shows schema
- [ ] Port 5000 is available (or change in config)

---

## First-Time Setup (One-Time Only)

### Step 1: Verify Python
```powershell
python --version
```
Should show Python 3.8+

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```
Wait for installation to complete

### Step 3: Check Setup
```powershell
python check_setup.py
```
All items should show ✓

### Step 4: Verify Database
```powershell
python db_connect.py
```
Should display database schema

---

## Running the Application

### Method 1: Using Batch File (Easiest)
```powershell
start.bat
```

### Method 2: Direct Python
```powershell
python app.py
```

### Method 3: With Flask
```powershell
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

---

## After Starting

### Expected Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### Access the Application:
1. Open browser
2. Go to: `http://localhost:5000`
3. You should see the dashboard

---

## Testing Checklist

### Dashboard
- [ ] Statistics cards display correctly
- [ ] Numbers animate on load
- [ ] AI suggestions appear
- [ ] Recent patients list shows
- [ ] Today's appointments display

### Patient Management
- [ ] Can view patient list
- [ ] Search functionality works
- [ ] Can add new patient
- [ ] Can view patient details
- [ ] AI risk assessment shows
- [ ] Can edit patient info

### OPD Module
- [ ] Can schedule appointment
- [ ] Today's appointments display
- [ ] All appointments list shows
- [ ] Doctor dropdown populates

### Reports Module
- [ ] Can admit patient
- [ ] Active admissions display
- [ ] Can discharge patient
- [ ] Treatment recommendations appear

### OT Module
- [ ] Can schedule operation
- [ ] Scheduled operations show
- [ ] Can update status
- [ ] Duration estimate appears

### Ward Management
- [ ] Bed grid displays correctly
- [ ] Occupancy status visible
- [ ] ICU table shows
- [ ] Special rooms list displays

### Staff Module
- [ ] Staff list displays
- [ ] Can add new staff
- [ ] Roles dropdown works

### Analytics
- [ ] Bed forecast chart displays
- [ ] Disease patterns show
- [ ] Predictions table visible
- [ ] Optimization suggestions appear

---

## Troubleshooting Quick Fixes

### Issue: Can't start application
**Fix**: 
```powershell
pip install --upgrade flask
python app.py
```

### Issue: Database connection failed
**Fix**:
1. Start MySQL in XAMPP/WAMP
2. Verify database name is 'hospital'
3. Check config.py credentials

### Issue: Templates not found
**Fix**:
```powershell
cd C:\Suraj\SPPU\Project\DBMSAI
python app.py
```

### Issue: Port already in use
**Fix**: 
Edit config.py:
```python
PORT = 5001  # Change to different port
```

### Issue: CSS not loading
**Fix**:
1. Clear browser cache (Ctrl+F5)
2. Check static/css/style.css exists
3. Restart application

### Issue: JavaScript errors
**Fix**:
1. Check browser console (F12)
2. Verify static/js/script.js exists
3. Check for Bootstrap CDN loading

---

## Performance Tips

- [ ] Keep MySQL running in background
- [ ] Use Chrome or Firefox for best experience
- [ ] Close unnecessary applications
- [ ] Ensure good internet for CDN resources
- [ ] Clear browser cache periodically

---

## Demo Preparation

### Before Demo:
1. [ ] Add 5-10 sample patients
2. [ ] Create 2-3 appointments for today
3. [ ] Admit 1-2 patients
4. [ ] Schedule 1-2 operations
5. [ ] Add medical history for patients

### During Demo:
1. Start with Dashboard - show statistics
2. Navigate to Patients - show search
3. Open Patient Detail - show AI risk
4. Go to Analytics - show predictions
5. Show Ward Management - bed grid
6. Highlight AI features throughout

---

## Common Success Indicators

✅ Server starts without errors
✅ Browser opens and shows dashboard
✅ All navigation links work
✅ Statistics display correct numbers
✅ Forms can be submitted
✅ Data appears in tables
✅ Charts and graphs render
✅ AI features calculate and display
✅ Modals open and close
✅ Search and filter work
✅ Responsive design on resize
✅ No console errors (F12)

---

## Final Verification

Before presenting:
- [ ] All pages load correctly
- [ ] No Python errors in terminal
- [ ] No JavaScript errors in console
- [ ] Database has sample data
- [ ] All features are working
- [ ] UI looks professional
- [ ] Animations are smooth
- [ ] Forms validate correctly
- [ ] AI predictions display
- [ ] Charts render properly

---

## Emergency Backup Plan

If something goes wrong:
1. Restart MySQL server
2. Restart the Flask application
3. Clear browser cache
4. Check error messages
5. Use check_setup.py to diagnose
6. Review error logs in terminal

---

## Contact & Support

If you encounter issues:
1. Check terminal for error messages
2. Review browser console (F12)
3. Verify database connection
4. Check all files are present
5. Review this checklist again

---

## Success! 🎉

If all checkboxes are ticked:
- Your system is ready to run!
- All features should work perfectly
- You're ready to demonstrate!

**Now run**: `start.bat` or `python app.py`

**Then visit**: http://localhost:5000

**Enjoy your AI-Powered Hospital Management System!** 🏥✨

---

**Last Updated**: November 3, 2025
**Version**: 1.0.0
**Status**: Production Ready
