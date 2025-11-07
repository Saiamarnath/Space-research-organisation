# 🎯 DEPLOYMENT & SETUP GUIDE

## Table of Contents
1. [Quick Start](#quick-start)
2. [Detailed Setup](#detailed-setup)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### For Immediate Testing (Development)

```powershell
# 1. Navigate to project
cd "c:\Users\Shreelakshmi\Downloads\rn"

# 2. Activate virtual environment
.\venv311\Scripts\Activate.ps1

# 3. Install/update dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from .env.example)
# Add your Supabase credentials

# 5. Run the application
python app.py

# 6. Open browser
# Navigate to: http://localhost:8050

# 7. Login with test credentials
# Admin: admin@test.com / admin123456
# User: user@space.com / user123
```

---

## Detailed Setup

### Step 1: System Requirements

**Operating System**: Windows 10/11, macOS, or Linux

**Python**: Version 3.11 or higher
```powershell
python --version
# Should output: Python 3.11.x or higher
```

**pip**: Latest version
```powershell
python -m pip install --upgrade pip
```

### Step 2: Virtual Environment

**Why**: Isolates project dependencies from system Python

```powershell
# Create virtual environment (if not exists)
python -m venv venv311

# Activate on Windows PowerShell
.\venv311\Scripts\Activate.ps1

# Activate on Windows CMD
.\venv311\Scripts\activate.bat

# Activate on macOS/Linux
source venv311/bin/activate

# Verify activation (you should see (venv311) in prompt)
```

### Step 3: Install Dependencies

```powershell
# Ensure virtual environment is activated
pip install -r requirements.txt

# Verify installation
pip list
# Should show: dash, dash-bootstrap-components, plotly, supabase, etc.
```

### Step 4: Project Structure Verification

Ensure all files are in place:

```
rn/
├── app.py                      ✅ Main application
├── requirements.txt            ✅ Dependencies
├── .env                        ⚠️ Create this file
├── assets/
│   ├── styles.css              ✅ Space theme CSS
│   └── custom.js               ✅ JavaScript
├── config/
│   └── database.py             ✅ Database operations
├── utils/
│   └── auth.py                 ✅ Authentication
└── pages/
    ├── login.py                ✅ Login page
    ├── signup.py               ✅ Signup page
    ├── dashboard.py            ✅ Dashboard
    └── ...                     ✅ Other pages
```

---

## Environment Configuration

### Create .env File

Create a file named `.env` in the root directory:

```env
# ============================================
# SUPABASE CONFIGURATION
# ============================================

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# ============================================
# FLASK CONFIGURATION (Optional)
# ============================================

FLASK_ENV=development
SECRET_KEY=your-secret-key-generate-random-string
DEBUG=True

# ============================================
# APPLICATION CONFIGURATION (Optional)
# ============================================

PORT=8050
HOST=0.0.0.0
```

### Get Supabase Credentials

1. **Go to Supabase Dashboard**:
   - Visit: https://supabase.com
   - Sign in or create account

2. **Create/Select Project**:
   - Click "New Project"
   - Choose organization
   - Enter project name (e.g., "space-research")
   - Choose database password (save this!)
   - Select region (closest to your users)
   - Wait for setup (~2 minutes)

3. **Get API Keys**:
   - Go to Settings → API
   - Copy **Project URL** → This is your `SUPABASE_URL`
   - Copy **anon/public** key → This is your `SUPABASE_KEY`
   - Copy **service_role** key → This is your `SUPABASE_SERVICE_KEY`

4. **Paste into .env file**

### Generate Secret Key

```powershell
# In Python console
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY in .env
```

---

## Database Setup

### Step 1: Create Tables

In Supabase SQL Editor, run this schema:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (for auth metadata)
CREATE TABLE IF NOT EXISTS "user" (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    registration_date TIMESTAMP DEFAULT NOW()
);

-- Departments
CREATE TABLE IF NOT EXISTS department (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    budget DECIMAL(15, 2),
    head_emp_id INTEGER
);

-- Employees
CREATE TABLE IF NOT EXISTS employee (
    emp_id SERIAL PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    dept_id INTEGER REFERENCES department(dept_id),
    hire_date DATE,
    salary DECIMAL(12, 2)
);

-- Missions
CREATE TABLE IF NOT EXISTS mission (
    mission_id SERIAL,
    pad_id INTEGER,
    loc_id INTEGER,
    mission_name VARCHAR(200) NOT NULL,
    launch_date DATE,
    status VARCHAR(50),
    budget DECIMAL(15, 2),
    objective TEXT,
    PRIMARY KEY (mission_id, pad_id, loc_id)
);

-- Satellites
CREATE TABLE IF NOT EXISTS satellite (
    sat_id SERIAL PRIMARY KEY,
    sat_name VARCHAR(100) NOT NULL,
    orbit_type VARCHAR(50),
    launch_date DATE,
    status VARCHAR(50) DEFAULT 'Operational',
    mass DECIMAL(10, 2),
    mission_id INTEGER
);

-- Telemetry
CREATE TABLE IF NOT EXISTS telemetry (
    telemetry_id SERIAL PRIMARY KEY,
    sat_id INTEGER REFERENCES satellite(sat_id),
    timestamp TIMESTAMP DEFAULT NOW(),
    altitude DECIMAL(10, 2),
    velocity DECIMAL(10, 2),
    temperature DECIMAL(5, 2),
    battery_level DECIMAL(5, 2),
    status VARCHAR(50)
);

-- Research Facts
CREATE TABLE IF NOT EXISTS research_fact (
    fact_id INTEGER,
    user_id UUID REFERENCES "user"(user_id),
    fact_title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    source VARCHAR(255),
    date_added DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (fact_id, user_id)
);

-- Locations
CREATE TABLE IF NOT EXISTS location (
    loc_id SERIAL PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6)
);

-- Equipment
CREATE TABLE IF NOT EXISTS equipment (
    equip_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    status VARCHAR(50),
    last_maintenance DATE
);

-- Create indexes for better performance
CREATE INDEX idx_mission_status ON mission(status);
CREATE INDEX idx_satellite_status ON satellite(status);
CREATE INDEX idx_employee_dept ON employee(dept_id);
CREATE INDEX idx_telemetry_sat ON telemetry(sat_id);
CREATE INDEX idx_research_user ON research_fact(user_id);
```

### Step 2: Insert Sample Data

```sql
-- Insert admin user (must match Supabase Auth user)
INSERT INTO "user" (user_id, username, email, role) 
VALUES ('your-admin-uuid-from-supabase-auth', 'Admin', 'admin@test.com', 'admin');

-- Insert regular user
INSERT INTO "user" (user_id, username, email, role) 
VALUES ('your-user-uuid-from-supabase-auth', 'User', 'user@space.com', 'user');

-- Insert sample departments
INSERT INTO department (dept_name, budget) VALUES
('Mission Control', 5000000),
('Engineering', 8000000),
('Research', 6000000),
('Operations', 4000000);

-- Insert sample missions
INSERT INTO mission (mission_id, pad_id, loc_id, mission_name, launch_date, status, budget, objective) VALUES
(1, 1, 1, 'Mars Explorer', '2024-06-15', 'In Progress', 15000000, 'Mars surface exploration'),
(2, 1, 1, 'Lunar Gateway', '2024-03-10', 'Completed', 12000000, 'Moon orbital station'),
(3, 2, 1, 'Jupiter Probe', '2024-09-20', 'Planned', 20000000, 'Jupiter atmosphere study');

-- Insert sample satellites
INSERT INTO satellite (sat_name, orbit_type, launch_date, status, mass, mission_id) VALUES
('StarLink-A1', 'LEO', '2023-01-15', 'Operational', 260.5, 1),
('GPS-III-5', 'MEO', '2023-06-22', 'Operational', 4400.0, 2),
('Hubble-Next', 'LEO', '2024-02-10', 'Operational', 11000.0, 1);

-- Add more sample data as needed...
```

### Step 3: Set Up Row Level Security (RLS)

```sql
-- Enable RLS on sensitive tables
ALTER TABLE "user" ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_fact ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read all user records
CREATE POLICY "Users can view all users" ON "user"
    FOR SELECT USING (true);

-- Policy: Users can update their own record
CREATE POLICY "Users can update own record" ON "user"
    FOR UPDATE USING (auth.uid() = user_id);

-- Policy: Users can read all research facts
CREATE POLICY "Anyone can view research facts" ON research_fact
    FOR SELECT USING (true);

-- Policy: Users can insert their own research facts
CREATE POLICY "Users can insert own facts" ON research_fact
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own research facts
CREATE POLICY "Users can update own facts" ON research_fact
    FOR UPDATE USING (auth.uid() = user_id);

-- Policy: Users can delete their own research facts
CREATE POLICY "Users can delete own facts" ON research_fact
    FOR DELETE USING (auth.uid() = user_id);
```

### Step 4: Enable Supabase Auth

1. In Supabase Dashboard → Authentication → Settings
2. Enable Email provider
3. Configure email templates (optional)
4. Set site URL: `http://localhost:8050` (dev) or your domain (prod)
5. Add redirect URLs if needed

### Step 5: Create Test Users in Supabase Auth

**Option A: Using Supabase Dashboard**
1. Go to Authentication → Users
2. Click "Add user" → "Create new user"
3. Email: `admin@test.com`, Password: `admin123456`
4. Repeat for user: `user@space.com`, Password: `user123`

**Option B: Using Signup Page**
1. Run the application
2. Go to `/signup`
3. Create accounts normally
4. Then update role in database:
   ```sql
   UPDATE "user" SET role = 'admin' WHERE email = 'admin@test.com';
   ```

---

## Testing

### Manual Testing Checklist

**Authentication**:
- [ ] Login with admin account works
- [ ] Login with user account works
- [ ] Invalid credentials show error
- [ ] Logout works
- [ ] Signup creates new account
- [ ] Password strength meter works
- [ ] Enter key submits forms

**Navigation**:
- [ ] All navbar links work
- [ ] Protected routes redirect to login
- [ ] Unauthorized access shows 403 page
- [ ] Role-based menu items show correctly

**Dashboard**:
- [ ] Live UTC clock updates
- [ ] Stat counters animate on load
- [ ] Mission ticker scrolls
- [ ] Charts display correctly
- [ ] Responsive on mobile

**Data Pages**:
- [ ] Missions page loads data
- [ ] Satellites page loads data
- [ ] Tables are sortable/filterable
- [ ] Admin can access all pages
- [ ] User restricted appropriately

**UI/UX**:
- [ ] Animations are smooth
- [ ] Hover effects work
- [ ] Loading states show
- [ ] Error messages display
- [ ] Responsive on all screen sizes

**Easter Eggs**:
- [ ] Type "houston" shows message
- [ ] Rapid-click logo launches rocket
- [ ] Keyboard shortcuts work

### Automated Testing (Future)

```powershell
# Install testing dependencies
pip install pytest pytest-dash selenium

# Run tests
pytest tests/

# Coverage report
pytest --cov=app tests/
```

---

## Deployment

### Option 1: Heroku

```powershell
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SUPABASE_URL=your_url
heroku config:set SUPABASE_KEY=your_key
heroku config:set SUPABASE_SERVICE_KEY=your_service_key

# Create Procfile
echo "web: gunicorn app:server" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

### Option 2: Render

1. Go to https://render.com
2. Connect GitHub repository
3. Create new Web Service
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:server`
6. Add environment variables in dashboard
7. Deploy

### Option 3: Railway

1. Go to https://railway.app
2. Create new project from GitHub
3. Add environment variables
4. Railway auto-detects Python
5. Deploy automatically

### Option 4: DigitalOcean App Platform

1. Go to DigitalOcean
2. Create App → From GitHub
3. Configure build settings
4. Add environment variables
5. Deploy

### Option 5: Docker (Advanced)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["gunicorn", "app:server", "-b", "0.0.0.0:8050"]
```

Build and run:

```powershell
docker build -t space-research .
docker run -p 8050:8050 --env-file .env space-research
```

---

## Troubleshooting

### Common Issues

#### 1. Module Not Found Error
```
ModuleNotFoundError: No module named 'dash'
```

**Solutions**:
```powershell
# Verify virtual environment is activated
# You should see (venv311) in prompt

# If not, activate it
.\venv311\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Database Connection Error
```
Error: Could not connect to Supabase
```

**Solutions**:
- Check `.env` file exists in root directory
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Test connection:
  ```python
  from supabase import create_client
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  url = os.getenv("SUPABASE_URL")
  key = os.getenv("SUPABASE_KEY")
  
  client = create_client(url, key)
  result = client.table('user').select('*').execute()
  print(result.data)
  ```

#### 3. CSS Not Loading
```
Styles not appearing, page looks unstyled
```

**Solutions**:
- Verify `assets/styles.css` exists
- Clear browser cache: `Ctrl + Shift + R`
- Check browser console (F12) for errors
- Verify file is not empty
- Check file permissions

#### 4. Login Not Working
```
Login button does nothing or shows error
```

**Solutions**:
- Open browser console (F12) → Check for JavaScript errors
- Verify Supabase Auth is enabled
- Check user exists in both Supabase Auth AND user table
- Verify credentials are correct
- Check network tab for failed API calls

#### 5. Port Already in Use
```
Error: [Errno 48] Address already in use
```

**Solutions**:
```powershell
# Find process using port 8050
netstat -ano | findstr :8050

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change port in app.py
# app.run_server(port=8051)
```

#### 6. Permission Denied on Activation
```
Execution of scripts is disabled on this system
```

**Solutions**:
```powershell
# Run PowerShell as Administrator
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv311\Scripts\Activate.ps1
```

#### 7. Charts Not Displaying
```
Plotly charts show as blank
```

**Solutions**:
- Check data exists in database
- Verify Plotly version: `pip show plotly`
- Clear browser cache
- Check console for errors
- Verify dark theme config in chart functions

---

## Performance Optimization

### For Large Datasets

1. **Enable pagination**:
```python
dash_table.DataTable(
    page_size=20,  # Reduce from default
    virtualization=True  # For 1000+ rows
)
```

2. **Use caching**:
```python
from flask_caching import Cache

cache = Cache(server, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@cache.memoize(timeout=60)
def get_missions():
    return db.get_all_missions()
```

3. **Lazy load images/charts**:
```python
dcc.Loading(
    children=[dcc.Graph(figure=fig)],
    type="circle"
)
```

---

## Security Best Practices

1. **Never commit .env file**:
```bash
# Add to .gitignore
.env
*.env
```

2. **Use environment variables**:
```python
import os
SECRET_KEY = os.getenv('SECRET_KEY')
```

3. **Enable HTTPS in production**

4. **Implement rate limiting**

5. **Sanitize user inputs**

6. **Keep dependencies updated**:
```powershell
pip list --outdated
pip install --upgrade package_name
```

---

## Monitoring & Logs

### Enable Logging

Add to `app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Production Monitoring

- Use **Sentry** for error tracking
- Use **LogRocket** for session replay
- Use **Google Analytics** for usage tracking
- Monitor with **Datadog** or **New Relic**

---

## Backup & Recovery

### Database Backup

```bash
# In Supabase Dashboard
# Settings → Database → Backups
# Enable automatic backups
# Download manual backup
```

### Application Backup

```powershell
# Backup code
git push origin main

# Backup .env securely
# Store in password manager or secure vault
```

---

## Support & Resources

**Documentation**:
- Dash: https://dash.plotly.com
- Supabase: https://supabase.com/docs
- Plotly: https://plotly.com/python

**Community**:
- Dash Community: https://community.plotly.com
- Supabase Discord: https://discord.supabase.com

**This Project**:
- Check README.md for features
- Review code comments
- Check browser console for errors

---

**🚀 You're all set! Launch the mission control center and explore the cosmos!**

