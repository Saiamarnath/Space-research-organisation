"""Pages package exports for app"""
from .login import login_page
from .signup import signup_page
from .login_selection import login_selection_page
from .admin_login import admin_login_page
from .user_login import user_login_page
from .admin_signup import admin_signup_page
from .user_signup import user_signup_page
from .research import research_facts_page
from .dashboard import dashboard_home
from .common_dashboard import common_dashboard_page
from .missions import missions_page
from .satellites import satellites_page
from .employees import employees_page
from .telemetry import telemetry_page
from .analytics import analytics_page
from .unauthorized import unauthorized_page
from .admin_dashboard import admin_dashboard_page

__all__ = [
    'login_page', 'signup_page', 'login_selection_page', 'admin_login_page', 'user_login_page',
    'admin_signup_page', 'user_signup_page', 'research_facts_page', 
    'dashboard_home', 'common_dashboard_page', 'missions_page', 'satellites_page', 
    'employees_page', 'telemetry_page', 'analytics_page', 'unauthorized_page', 
    'admin_dashboard_page',
]
