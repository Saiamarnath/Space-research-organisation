"""
Authentication Module - Supabase Auth Integration with Role Management
"""
from config.database import supabase
import json


class Auth:
    """Authentication handler using Supabase Auth"""
    
    def __init__(self):
        self.client = supabase.auth
    
    def sign_up(self, email, password, username=None, role='user'):
        """
        Sign up a new user with role metadata
        
        Args:
            email: User email
            password: User password
            username: Optional username
            role: 'user' or 'admin'
            
        Returns:
            dict: User data or error
        """
        try:
            # Assign the role provided, default to 'user'
            user_role = (role or 'user').lower()
            
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "role": user_role
                    }
                }
            })
            
            if response.user:
                # Also insert into User table
                user_data = {
                    'user_id': response.user.id,
                    'username': username or email.split('@')[0],
                    'email': email,
                    'role': user_role,
                    'registration_date': 'now()'
                }
                
                try:
                    supabase.table('user').insert(user_data).execute()
                except Exception as db_error:
                    print(f"Warning: Could not insert into user table: {db_error}")
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "role": user_role
                    },
                    "session": {
                        "access_token": response.session.access_token if response.session else None
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Sign up failed"
                }
        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                return {
                    "success": False,
                    "error": "Email already registered"
                }
            return {
                "success": False,
                "error": str(e)
            }
    
    def sign_in(self, email, password):
        """
        Sign in existing user and retrieve role
        
        Args:
            email: User email
            password: User password
            
        Returns:
            dict: User data and session with role or error
        """
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Get user role from user metadata or database
                user_role = "user"  # Default
                
                # Try to get from user metadata
                if response.user.user_metadata:
                    user_role = response.user.user_metadata.get('role', 'user')
                
                # Try to get from database User table
                try:
                    user_record = supabase.table('user').select('role').eq('email', email).execute()
                    if user_record.data and len(user_record.data) > 0:
                        user_role = user_record.data[0].get('role', 'user')
                except Exception as db_error:
                    print(f"Could not fetch role from database: {db_error}")
                # Normalize role to lowercase for consistent RBAC checks
                user_role = (user_role or 'user').lower()
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "role": user_role
                    },
                    "session": {
                        "access_token": response.session.access_token if response.session else None
                    },
                    "access_token": response.session.access_token if response.session else None,
                    "role": user_role
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
        except Exception as e:
            error_msg = str(e)
            if "Invalid login credentials" in error_msg:
                return {
                    "success": False,
                    "error": "Invalid email or password"
                }
            return {
                "success": False,
                "error": error_msg
            }
    
    def sign_out(self):
        """
        Sign out current user
        
        Returns:
            dict: Success status
        """
        try:
            supabase.auth.sign_out()
            return {
                "success": True,
                "message": "Signed out successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user(self):
        """
        Get current authenticated user
        
        Returns:
            dict: User data or None
        """
        try:
            response = supabase.auth.get_user()
            if response and response.user:
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email
                    }
                }
            return {
                "success": False,
                "user": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "user": None
            }
    
    def get_session(self):
        """
        Get current session
        
        Returns:
            Session object or None
        """
        try:
            session = supabase.auth.get_session()
            return session
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def reset_password(self, email):
        """
        Send password reset email
        
        Args:
            email: User email
            
        Returns:
            dict: Success status
        """
        try:
            supabase.auth.reset_password_for_email(email)
            return {
                "success": True,
                "message": "Password reset email sent"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_user(self, attributes):
        """
        Update user attributes
        
        Args:
            attributes: Dict of attributes to update
            
        Returns:
            dict: Updated user or error
        """
        try:
            response = supabase.auth.update_user(attributes)
            if response and response.user:
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email
                    }
                }
            return {
                "success": False,
                "error": "Update failed"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def is_authenticated(self):
        """
        Check if user is authenticated
        
        Returns:
            bool: True if authenticated
        """
        try:
            user_response = self.get_user()
            return user_response.get("success", False) and user_response.get("user") is not None
        except:
            return False


# Create global auth instance
auth = Auth()


# Session management helpers for Dash
def store_session(session_data):
    """Prepare session payload for dcc.Store. Returns a plain dict."""
    try:
        user_data = session_data.get("user", {})
        access_token = session_data.get("access_token")
        role = (session_data.get("role", "user") or "user").lower()

        return {
            "access_token": access_token,
            "user_id": user_data.get("id") if isinstance(user_data, dict) else None,
            "email": user_data.get("email") if isinstance(user_data, dict) else None,
            "role": role,
        }
    except Exception as e:
        print(f"Error storing session: {e}")
        return None


def load_session(session_value):
    """Load session data from dcc.Store. Accepts dict or JSON string."""
    try:
        if not session_value:
            return None
        if isinstance(session_value, dict):
            # Normalize role if present
            if 'role' in session_value and isinstance(session_value['role'], str):
                session_value = {
                    **session_value,
                    'role': session_value['role'].lower()
                }
            return session_value
        if isinstance(session_value, str):
            data = json.loads(session_value)
            if 'role' in data and isinstance(data['role'], str):
                data['role'] = data['role'].lower()
            return data
        return None
    except Exception:
        return None


def check_authentication(session_data):
    """
    Check if user is authenticated based on session data
    
    Args:
        session_data: Session data from browser storage
        
    Returns:
        bool: True if authenticated
    """
    if not session_data:
        return False
    
    try:
        session = load_session(session_data)
        if not session:
            return False
        # Treat presence of either access_token or a user_id as authenticated
        if session.get("access_token") or session.get("user_id"):
            return True
        return False
    except:
        return False


def get_user_role(session_data):
    """
    Get user role from session data
    
    Args:
        session_data: Session data from browser storage
        
    Returns:
        str: User role ('admin' or 'user')
    """
    if not session_data:
        return None
    
    try:
        session = load_session(session_data)
        if session:
            role = session.get("role", "user")
            return role.lower() if isinstance(role, str) else "user"
        return None
    except:
        return None


def is_admin(session_data):
    """
    Check if user is admin
    
    Args:
        session_data: Session data from browser storage
        
    Returns:
        bool: True if user is admin
    """
    role = get_user_role(session_data)
    return role == "admin"