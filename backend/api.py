"""
FastAPI Backend - Advanced API for Space Research System
Optional: Use this for complex operations, stored procedures, etc.
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uvicorn

from config.database import db, supabase
from utils.auth import auth

# ============================================
# INITIALIZE FASTAPI
# ============================================

app = FastAPI(
    title="Space Research API",
    description="Backend API for Space Research System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Dash app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ============================================
# PYDANTIC MODELS
# ============================================

class Employee(BaseModel):
    emp_id: Optional[int] = None
    emp_name: str
    position: str
    salary: float
    hire_date: str
    phone: Optional[str] = None
    supervisor_id: Optional[int] = None
    dept_id: Optional[int] = None

class Satellite(BaseModel):
    sat_id: Optional[int] = None
    sat_name: str
    launch_date: str
    status: str
    orbit_type: str
    mass: float
    manager_id: Optional[int] = None

class Mission(BaseModel):
    mission_id: int
    pad_id: int
    loc_id: int
    mission_name: str
    launch_date: str
    end_date: Optional[str] = None
    status: str
    objective: Optional[str] = None
    budget: float

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None

# ============================================
# AUTHENTICATION DEPENDENCY
# ============================================

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token from Supabase"""
    token = credentials.credentials
    try:
        # Verify with Supabase
        user = supabase.auth.get_user(token)
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@app.post("/api/auth/signup")
async def signup(user: UserSignup):
    """Sign up new user"""
    result = auth.sign_up(user.email, user.password, user.username)
    if result.get("success"):
        return {
            "message": "User created successfully",
            "user": result.get("user")
        }
    raise HTTPException(status_code=400, detail=result.get("error"))

@app.post("/api/auth/login")
async def login(user: UserLogin):
    """Login user"""
    result = auth.sign_in(user.email, user.password)
    if result.get("success"):
        return {
            "access_token": result.get("access_token"),
            "token_type": "bearer",
            "user": result.get("user")
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(current_user: dict = Depends(verify_token)):
    """Logout user"""
    result = auth.sign_out()
    return {"message": "Logged out successfully"}

@app.get("/api/auth/me")
async def get_current_user(current_user: dict = Depends(verify_token)):
    """Get current authenticated user"""
    return current_user

# ============================================
# EMPLOYEE ENDPOINTS
# ============================================

@app.get("/api/employees")
async def get_employees(current_user: dict = Depends(verify_token)):
    """Get all employees"""
    employees = db.get_all_employees()
    return employees

@app.get("/api/employees/{emp_id}")
async def get_employee(emp_id: int, current_user: dict = Depends(verify_token)):
    """Get employee by ID"""
    employee = db.get_employee_by_id(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/api/employees")
async def create_employee(employee: Employee, current_user: dict = Depends(verify_token)):
    """Create new employee"""
    employee_data = employee.dict(exclude_none=True)
    result = db.add_employee(employee_data)
    if result:
        return {"message": "Employee created successfully", "employee": result}
    raise HTTPException(status_code=400, detail="Failed to create employee")

@app.put("/api/employees/{emp_id}")
async def update_employee(
    emp_id: int,
    employee: Employee,
    current_user: dict = Depends(verify_token)
):
    """Update employee"""
    employee_data = employee.dict(exclude_none=True)
    result = db.update_employee(emp_id, employee_data)
    if result:
        return {"message": "Employee updated successfully", "employee": result}
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/api/employees/{emp_id}")
async def delete_employee(emp_id: int, current_user: dict = Depends(verify_token)):
    """Delete employee"""
    result = db.delete_employee(emp_id)
    if result:
        return {"message": "Employee deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")

# ============================================
# SATELLITE ENDPOINTS
# ============================================

@app.get("/api/satellites")
async def get_satellites(current_user: dict = Depends(verify_token)):
    """Get all satellites"""
    satellites = db.get_all_satellites()
    return satellites

@app.get("/api/satellites/{sat_id}")
async def get_satellite(sat_id: int, current_user: dict = Depends(verify_token)):
    """Get satellite by ID"""
    satellite = db.get_satellite_by_id(sat_id)
    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return satellite

@app.get("/api/satellites/operational")
async def get_operational_satellites(current_user: dict = Depends(verify_token)):
    """Get operational satellites only"""
    satellites = db.get_operational_satellites()
    return satellites

# ============================================
# MISSION ENDPOINTS
# ============================================

@app.get("/api/missions")
async def get_missions(current_user: dict = Depends(verify_token)):
    """Get all missions"""
    missions = db.get_all_missions()
    return missions

@app.get("/api/missions/active")
async def get_active_missions(current_user: dict = Depends(verify_token)):
    """Get active missions"""
    missions = db.get_active_missions()
    return missions

@app.get("/api/missions/{mission_id}/{pad_id}/{loc_id}")
async def get_mission(
    mission_id: int,
    pad_id: int,
    loc_id: int,
    current_user: dict = Depends(verify_token)
):
    """Get mission by composite ID"""
    mission = db.get_mission_by_id(mission_id, pad_id, loc_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

# ============================================
# TELEMETRY ENDPOINTS
# ============================================

@app.get("/api/telemetry")
async def get_all_telemetry(current_user: dict = Depends(verify_token)):
    """Get all telemetry data"""
    telemetry = db.get_all_telemetry()
    return telemetry

@app.get("/api/telemetry/{sat_id}")
async def get_satellite_telemetry(
    sat_id: int,
    limit: int = 10,
    current_user: dict = Depends(verify_token)
):
    """Get telemetry for specific satellite"""
    telemetry = db.get_latest_telemetry(sat_id, limit)
    return telemetry

# ============================================
# ANALYTICS ENDPOINTS
# ============================================

@app.get("/api/analytics/mission-stats")
async def get_mission_statistics(current_user: dict = Depends(verify_token)):
    """Get mission statistics"""
    stats = db.get_mission_statistics()
    return stats

@app.get("/api/analytics/satellite-stats")
async def get_satellite_statistics(current_user: dict = Depends(verify_token)):
    """Get satellite statistics"""
    stats = db.get_satellite_statistics()
    return stats

@app.get("/api/analytics/department-summary")
async def get_department_summary(current_user: dict = Depends(verify_token)):
    """Get department summary"""
    summary = db.get_department_summary()
    return summary

# ============================================
# SEARCH ENDPOINTS
# ============================================

@app.get("/api/search/missions")
async def search_missions(
    q: str,
    current_user: dict = Depends(verify_token)
):
    """Search missions"""
    missions = db.search_missions(q)
    return missions

@app.get("/api/search/employees")
async def search_employees(
    q: str,
    current_user: dict = Depends(verify_token)
):
    """Search employees"""
    employees = db.search_employees(q)
    return employees

# ============================================
# DEPARTMENT ENDPOINTS
# ============================================

@app.get("/api/departments")
async def get_departments(current_user: dict = Depends(verify_token)):
    """Get all departments"""
    departments = db.get_all_departments()
    return departments

@app.get("/api/departments/{dept_id}")
async def get_department(dept_id: int, current_user: dict = Depends(verify_token)):
    """Get department by ID"""
    department = db.get_department_by_id(dept_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# ============================================
# EQUIPMENT ENDPOINTS
# ============================================

@app.get("/api/equipment")
async def get_equipment(current_user: dict = Depends(verify_token)):
    """Get all equipment"""
    equipment = db.get_all_equipment()
    return equipment

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "message": "Space Research API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test database connection
        db.get_all_departments()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ============================================
# RUN API
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )