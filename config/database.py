"""
Database Configuration - Supabase PostgreSQL Connection
Enhanced with Research Facts and better error handling
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from postgrest import APIResponse
# --- IMPORT IS CORRECT ---
import pandas as pd

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Service client (for admin operations)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_SERVICE_KEY else supabase


class Database:
    """Database operations wrapper"""

    def __init__(self):
        # Read-only operations can use the public client
        self.client = supabase
        # Write/Update/Delete operations MUST use the admin client
        self.admin = supabase_admin
        
        # --- CLIENT FOR STORED PROCEDURES ---
        if SUPABASE_SERVICE_KEY:
            self.admin_raw_client = create_client(
                SUPABASE_URL, 
                SUPABASE_SERVICE_KEY
            )
        else:
            self.admin_raw_client = self.client


    # ============================================
    # DEPARTMENT OPERATIONS
    # ============================================
    # ... (omitted, no changes) ...
    def get_all_departments(self):
        """Get all departments"""
        try:
            response = self.client.table('department').select('*').order('dept_id').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching departments: {e}")
            return []

    def get_department_by_id(self, dept_id):
        """Get department by ID"""
        try:
            response = self.client.table('department').select('*').eq('dept_id', dept_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching department: {e}")
            return None
            
    def add_department(self, dept_data):
        """Add new department"""
        try:
            response = self.admin.table('department').insert(dept_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding department: {e}")
            return None

    def update_department(self, dept_id, dept_data):
        """Update department"""
        try:
            response = self.admin.table('department').update(dept_data).eq('dept_id', dept_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating department: {e}")
            return None

    def delete_department(self, dept_id):
        """Delete department"""
        try:
            response = self.admin.table('department').delete().eq('dept_id', dept_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting department: {e}")
            return False

    # ============================================
    # EMPLOYEE OPERATIONS
    # ============================================
    # ... (omitted, no changes) ...
    def get_all_employees(self):
        """Get all employees with department info"""
        try:
            response = self.client.table('employee_hierarchy').select('*').order('emp_id').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching employees: {e}")
            try:
                response = self.client.table('employee').select('*').order('emp_id').execute()
                return response.data
            except:
                return []

    def get_employee_by_id(self, emp_id):
        """Get employee by ID"""
        try:
            response = self.client.table('employee').select('*').eq('emp_id', emp_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching employee: {e}")
            return None

    def add_employee(self, employee_data):
        """Add new employee"""
        try:
            response = self.admin.table('employee').insert(employee_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding employee: {e}")
            return None

    def update_employee(self, emp_id, employee_data):
        """Update employee"""
        try:
            response = self.admin.table('employee').update(employee_data).eq('emp_id', emp_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating employee: {e}")
            return None

    def delete_employee(self, emp_id):
        """Delete employee"""
        try:
            response = self.admin.table('employee').delete().eq('emp_id', emp_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False

    # ============================================
    # SATELLITE OPERATIONS
    # ============================================
    # ... (omitted, no changes) ...
    def get_all_satellites(self):
        """Get all satellites with status"""
        try:
            response = self.client.table('satellite_status_report').select('*').order('sat_id').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching satellites from view: {e}")
            try:
                response = self.client.table('satellite').select('*').order('sat_id').execute()
                return response.data
            except:
                return []

    def get_satellite_by_id(self, sat_id):
        """Get satellite by ID"""
        try:
            response = self.client.table('satellite').select('*').eq('sat_id', sat_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching satellite: {e}")
            return None

    def add_satellite(self, sat_data):
        """Add new satellite"""
        try:
            response = self.admin.table('satellite').insert(sat_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding satellite: {e}")
            return None

    def update_satellite(self, sat_id, sat_data):
        """Update satellite"""
        try:
            response = self.admin.table('satellite').update(sat_data).eq('sat_id', sat_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating satellite: {e}")
            return None

    def delete_satellite(self, sat_id):
        """Delete satellite"""
        try:
            response = self.admin.table('satellite').delete().eq('sat_id', sat_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting satellite: {e}")
            return False

    def get_operational_satellites(self):
        """Get only operational satellites"""
        try:
            response = self.client.table('satellite').select('*').eq('status', 'Operational').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching operational satellites: {e}")
            return []

    # ============================================
    # MISSION OPERATIONS
    # ============================================
    # ... (omitted, no changes) ...
    def get_all_missions(self):
        """Get all missions"""
        try:
            response = self.client.table('mission').select('*').order('mission_id').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching missions: {e}")
            return []

    def add_mission(self, mission_data):
        """Add new mission"""
        try:
            response = self.admin.table('mission').insert(mission_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding mission: {e}")
            return None

    def update_mission(self, mission_id, pad_id, loc_id, mission_data):
        """Update mission by composite ID"""
        try:
            response = (self.admin.table('mission')
                        .update(mission_data)
                        .eq('mission_id', mission_id)
                        .eq('pad_id', pad_id)
                        .eq('loc_id', loc_id)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating mission: {e}")
            return None

    def delete_mission(self, mission_id, pad_id, loc_id):
        """Delete mission by composite ID"""
        try:
            response = (self.admin.table('mission')
                        .delete()
                        .eq('mission_id', mission_id)
                        .eq('pad_id', pad_id)
                        .eq('loc_id', loc_id)
                        .execute())
            return True
        except Exception as e:
            print(f"Error deleting mission: {e}")
            return False

    def get_active_missions(self):
        """Get active missions"""
        try:
            response = self.client.table('active_missions').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching active missions from view: {e}")
            try:
                response = self.client.table('mission').select('*').in_('status', ['In Progress', 'Planned']).execute()
                return response.data
            except:
                return []

    def get_mission_by_id(self, mission_id, pad_id, loc_id):
        """Get mission by composite ID"""
        try:
            response = (self.client.table('mission')
                        .select('*')
                        .eq('mission_id', mission_id)
                        .eq('pad_id', pad_id)
                        .eq('loc_id', loc_id)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching mission: {e}")
            return None

    # ============================================
    # TELEMETRY, EQUIPMENT, RESEARCH OPERATIONS
    # ============================================
    # ... (omitted, no changes) ...
    def get_latest_telemetry(self, sat_id, limit=10):
        """Get latest telemetry for a satellite"""
        try:
            response = (self.client.table('telemetry')
                        .select('*')
                        .eq('sat_id', sat_id)
                        .order('timestamp', desc=True)
                        .limit(limit)
                        .execute())
            return response.data
        except Exception as e:
            print(f"Error fetching telemetry: {e}")
            return []

    def get_all_telemetry(self):
        """Get all telemetry data"""
        try:
            response = self.client.table('telemetry').select('*').order('timestamp', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching telemetry: {e}")
            return []

    def get_all_equipment(self):
        """Get all equipment"""
        try:
            response = self.client.table('equipment').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching equipment: {e}")
            return []

    def get_all_research_facts(self):
        """Get all research facts, with usernames (flat, no errors)"""
        try:
            facts_response = self.client.table('research_fact').select('*').order('date_added', desc=True).execute()
            users_response = self.client.table('user').select('user_id', 'username').execute()

            facts = facts_response.data or []
            users = users_response.data or []
            user_map = {u['user_id']: u.get('username', 'Unknown') for u in users}

            result = []
            for fact in facts:
                fact_copy = fact.copy()
                fact_copy['username'] = user_map.get(fact_copy['user_id'], 'Unknown')
                result.append(fact_copy)
            return result
        except Exception as e:
            print(f"Error fetching research facts: {e}")
            try:
                response = self.client.table('research_fact').select('*').execute()
                return response.data or []
            except:
                return []


    def add_research_fact(self, fact_data):
        """Add new research fact"""
        try:
            existing = self.admin.table('research_fact').select('fact_id').eq('user_id', fact_data['user_id']).execute()
            
            if existing.data:
                max_fact_id = max([f.get('fact_id', 0) for f in existing.data])
                fact_data['fact_id'] = max_fact_id + 1
            else:
                fact_data['fact_id'] = 1
            
            response = self.admin.table('research_fact').insert(fact_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding research fact: {e}")
            return None

    def update_research_fact(self, fact_id, user_id, fact_data):
        """Update research fact"""
        try:
            response = (self.admin.table('research_fact')
                       .update(fact_data)
                       .eq('fact_id', fact_id)
                       .eq('user_id', user_id)
                       .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating research fact: {e}")
            return None

    def delete_research_fact(self, fact_id, user_id):
        """Delete research fact"""
        try:
            response = (self.admin.table('research_fact')
                       .delete()
                       .eq('fact_id', fact_id)
                       .eq('user_id', user_id)
                       .execute())
            return True
        except Exception as e:
            print(f"Error deleting research fact: {e}")
            return False

    # ============================================
    # ANALYTICS & STATISTICS
    # ============================================
    # ... (omitted, no changes) ...
    def get_department_summary(self):
        """Get department summary statistics"""
        try:
            response = self.client.table('department_summary').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching department summary: {e}")
            return []

    def get_mission_statistics(self):
        """Get mission statistics"""
        try:
            all_missions = self.get_all_missions()
            stats = {
                'total': len(all_missions),
                'completed': len([m for m in all_missions if m.get('status') == 'Completed']),
                'in_progress': len([m for m in all_missions if m.get('status') == 'In Progress']),
                'planned': len([m for m in all_missions if m.get('status') == 'Planned']),
                'total_budget': sum([float(m.get('budget', 0) or 0) for m in all_missions])
            }
            return stats
        except Exception as e:
            print(f"Error calculating mission statistics: {e}")
            return {'total': 0, 'completed': 0, 'in_progress': 0, 'planned': 0, 'total_budget': 0}

    def get_satellite_statistics(self):
        """Get satellite statistics"""
        try:
            all_satellites = self.get_all_satellites()
            stats = {
                'total': len(all_satellites),
                'operational': len([s for s in all_satellites if s.get('sat_status', s.get('status')) == 'Operational']),
                'maintenance': len([s for s in all_satellites if s.get('sat_status', s.get('status')) == 'Maintenance']),
                'total_mass': sum([float(s.get('mass', 0) or 0) for s in all_satellites])
            }
            return stats
        except Exception as e:
            print(f"Error calculating satellite statistics: {e}")
            return {'total': 0, 'operational': 0, 'maintenance': 0, 'total_mass': 0}

    # ============================================
    # SEARCH OPERATIONS
    # ============================================
    # ... (omitted, no changes) ...

    # ============================================
    # --- ANALYTICS FUNCTIONS (FIXED) ---
    # ============================================

    # ============================================
    # --- ANALYTICS FUNCTIONS (FIXED) ---
    # ============================================

    def call_get_employee_details(self, emp_id: int):
        """Calls the GetEmployeeDetails stored procedure"""
        try:
            response: APIResponse = self.admin_raw_client.rpc(
                'get_employee_details',
                {'emp_id_param': emp_id}  # <-- FIXED: Changed 'emp_id' to 'emp_id_param'
            ).execute()
            return response.data
        except Exception as e:
            print(f"Error calling GetEmployeeDetails procedure: {e}")
            return []

    def call_generate_salary_report(self):
        """Calls the GenerateSalaryReport stored procedure"""
        try:
            response: APIResponse = self.admin_raw_client.rpc(
                'generate_salary_report', {}
            ).execute()
            return response.data
        except Exception as e:
            print(f"Error calling GenerateSalaryReport procedure: {e}")
            return []

    def get_employees_above_avg_salary(self):
        """Runs the correlated subquery for employees above dept avg"""
        try:
            employees = self.get_all_employees()
            if not employees:
                return []
                
            df = pd.DataFrame(employees)
            df['salary'] = pd.to_numeric(df['salary'])
            # Use 'dept_id' which is present in the employee_hierarchy view
            df['dept_id'] = pd.to_numeric(df['dept_id'], errors='coerce')
            df.dropna(subset=['dept_id'], inplace=True)
            
            dept_avg = df.groupby('dept_id')['salary'].mean().to_dict()
            df['dept_avg'] = df['dept_id'].map(dept_avg)
            
            result_df = df[df['salary'] > df['dept_avg']].copy()
            
            # Round for cleaner display
            result_df['dept_avg'] = result_df['dept_avg'].round(2)
            
            return result_df.to_dict('records')
            
        except Exception as e:
            print(f"Error running correlated subquery: {e}")
            return []
            
    def call_get_years_of_service(self, emp_id: int):
        """Calls the GetYearsOfService function"""
        try:
            response: APIResponse = self.admin_raw_client.rpc(
                'get_years_of_service',
                {'emp_id_param': emp_id}  # <-- FIXED: Changed 'p_emp_id' to 'emp_id_param'
            ).execute()
            return response.data
        except Exception as e:
            print(f"Error calling GetYearsOfService function: {e}")
            return None

    def call_count_subordinates(self, emp_id: int):
        """Calls the CountSubordinates function"""
        try:
            response: APIResponse = self.admin_raw_client.rpc(
                'count_subordinates',
                {'supervisor_id_param': emp_id}  # <-- FIXED: Changed 'p_supervisor_id' to 'supervisor_id_param'
            ).execute()
            return response.data
        except Exception as e:
            print(f"Error calling CountSubordinates function: {e}")
            return None
# Create global database instance
db = Database()