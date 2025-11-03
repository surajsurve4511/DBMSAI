# Hospital Management System - Quick Setup Script
# Run this script after getting your Gemini API key

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Hospital Management System Setup  " -ForegroundColor Cyan
Write-Host "  Gemini AI Enhanced Version 2.0    " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher" -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host ""
Write-Host "[2/5] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 3: Setup .env file
Write-Host ""
Write-Host "[3/5] Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
    Write-Host "  Please ensure GEMINI_API_KEY is configured" -ForegroundColor Cyan
} else {
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "✓ Created .env file from template" -ForegroundColor Green
        Write-Host ""
        Write-Host "  ⚠️  IMPORTANT: Edit .env file and add your Gemini API key" -ForegroundColor Yellow
        Write-Host "     Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    } else {
        Write-Host "✗ .env.example not found" -ForegroundColor Red
    }
}

# Step 4: Check MySQL
Write-Host ""
Write-Host "[4/5] Checking MySQL connection..." -ForegroundColor Yellow
try {
    $mysqlTest = mysql --version 2>&1
    Write-Host "✓ MySQL client found" -ForegroundColor Green
    Write-Host "  Make sure MySQL server is running" -ForegroundColor Cyan
} catch {
    Write-Host "⚠ MySQL client not found in PATH" -ForegroundColor Yellow
    Write-Host "  Please ensure MySQL server is running on localhost:3306" -ForegroundColor Cyan
}

# Step 5: Database setup reminder
Write-Host ""
Write-Host "[5/5] Database setup..." -ForegroundColor Yellow
Write-Host "  Please ensure:" -ForegroundColor Cyan
Write-Host "  • MySQL server is running" -ForegroundColor White
Write-Host "  • Database 'hospital' exists" -ForegroundColor White
Write-Host "  • Sample data is loaded (INSERT statements)" -ForegroundColor White
Write-Host "  • Database credentials in config.py are correct" -ForegroundColor White

# Final instructions
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!                    " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "1. Edit .env file and add your GEMINI_API_KEY" -ForegroundColor White
Write-Host "2. Verify database connection in config.py" -ForegroundColor White
Write-Host "3. Run the application: python app.py" -ForegroundColor White
Write-Host "4. Open browser: http://127.0.0.1:5000" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Green
Write-Host "• Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "• Gemini Setup: GEMINI_SETUP_GUIDE.md" -ForegroundColor White
Write-Host "• Full Docs: README.md" -ForegroundColor White
Write-Host ""
Write-Host "New Features:" -ForegroundColor Green
Write-Host "✨ Google Gemini AI Integration" -ForegroundColor White
Write-Host "📊 8 New Analytics Methods" -ForegroundColor White
Write-Host "🤖 AI Symptom Analyzer" -ForegroundColor White
Write-Host "📈 Enhanced Charts & Visualizations" -ForegroundColor White
Write-Host "💡 Personalized Health Tips" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
