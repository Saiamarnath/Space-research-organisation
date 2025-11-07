# Role-Based Access Control (RBAC) Implementation

## Summary of Changes

This document outlines the role-based access control (RBAC) implementation for the Space Research System.

## Changes Made

### 1. **Dashboard Access**
- **Admin Dashboard (`/dashboard`, `/`)** - ADMIN ONLY
  - Full access to all features including database management
  - Displays comprehensive mission control center with live statistics
  - Includes admin-specific controls and analytics

- **Common Dashboard (`/`, `/common-dashboard`)** - BOTH ADMIN & USER
  - Read-only overview of system statistics
  - Shows mission status, satellite fleet status
  - Quick links to missions, satellites, and research pages
  - Users see this as their home page

### 2. **Missions Page (`/missions`)** - VISIBLE TO BOTH, EDIT FOR ADMIN ONLY
- ✅ Both admin and user can view all missions
- ✅ Admin can see "Add New Mission" button
- ✅ Admin can see "Edit" buttons on mission cards
- ✅ Users see a read-only info banner: "You are viewing in read-only mode. Only administrators can edit mission data."
- ✅ Users cannot add, edit, or delete missions

### 3. **Satellites Page (`/satellites`)** - VISIBLE TO BOTH, EDIT FOR ADMIN ONLY
- ✅ Both admin and user can view all satellites
- ✅ Admin can see "Add New Satellite", "Edit Selected", and "Delete Selected" buttons
- ✅ Users see a read-only info banner: "You are viewing in read-only mode. Only administrators can edit satellite data."
- ✅ Users cannot add, edit, or delete satellites

### 4. **Research Facts Page (`/research`)** - VISIBLE TO BOTH, EDIT FOR ADMIN ONLY
- ✅ Both admin and user can view all research facts
- ✅ Admin can see the "Add New Research Fact" form
- ✅ Users see a read-only info banner: "You are viewing in read-only mode. Only administrators can add or edit research facts."
- ✅ Users cannot add, edit, or delete research facts
- ✅ Hidden form inputs added for non-admin users to prevent callback errors

### 5. **Navigation Bar Updates**
- **Admin Navigation:**
  - Home (Dashboard)
  - Admin Control
  - Missions
  - Satellites
  - Employees (admin-only, marked with icon)
  - Telemetry (admin-only, marked with icon)
  - Research Facts
  - Analytics (admin-only, marked with icon)
  - ADMIN badge (red)
  - Logout

- **User Navigation:**
  - Home (Common Dashboard)
  - Missions
  - Satellites
  - Research Facts
  - USER badge (blue)
  - Logout

### 6. **Routing Updates in app.py**
```python
# Admin-only routes
admin_routes = ['/employees', '/telemetry', '/analytics', '/admin-dashboard', '/dashboard']

# Route logic:
- '/' → Admin sees full dashboard, Users see common dashboard
- '/dashboard' → Admin only (users get unauthorized page)
- '/common-dashboard' → Both admin and user
- '/missions', '/satellites', '/research' → Both can view, only admin can edit
- '/employees', '/telemetry', '/analytics', '/admin-dashboard' → Admin only
```

## Code Implementation Details

### Modified Files:
1. **`app.py`**
   - Updated routing logic to show common dashboard to users
   - Added `/dashboard` and `/common-dashboard` routes
   - Updated admin_routes list to include `/dashboard`
   - Modified navigation bar for users to include "Home" link

2. **`pages/missions.py`**
   - Added `is_admin` check based on `user_role`
   - Conditional rendering of "Add New Mission" button (admin only)
   - Conditional rendering of "Edit" buttons on mission cards (admin only)
   - Added info banner for users

3. **`pages/satellites.py`**
   - Added `is_admin` check based on `user_role`
   - Conditional rendering of add/edit/delete buttons (admin only)
   - Added info banner for users

4. **`pages/research.py`**
   - Added `is_admin` check based on `user_role`
   - Conditional rendering of "Add New Research Fact" form (admin only)
   - Added info banner for users
   - Added hidden form inputs for non-admin to prevent callback errors

5. **`pages/common_dashboard.py`**
   - Already existed - no changes needed
   - Displays read-only overview for both roles

6. **`pages/dashboard.py`**
   - Already had admin-only check - no changes needed

## User Experience

### As Admin:
1. Login with admin credentials
2. See full dashboard with admin controls
3. Navigate to any page
4. Can add, edit, and delete data on all pages
5. See red "ADMIN" badge in navbar

### As Regular User:
1. Login with user credentials
2. See common dashboard with overview
3. Navigate to Missions, Satellites, or Research Facts
4. Can view all data but cannot modify anything
5. See blue "USER" badge in navbar
6. See informative banners explaining read-only access
7. Cannot access admin-only pages (Employees, Telemetry, Analytics, Admin Dashboard)

## Security Features
- ✅ Role-based routing with server-side validation
- ✅ Unauthorized page shown for restricted access attempts
- ✅ UI elements conditionally rendered based on role
- ✅ Session-based authentication
- ✅ Protected admin routes list

## Testing Checklist
- [ ] Test admin login - should see full dashboard
- [ ] Test user login - should see common dashboard
- [ ] Test missions page as admin - should see edit buttons
- [ ] Test missions page as user - should only see read-only view
- [ ] Test satellites page as admin - should see edit buttons
- [ ] Test satellites page as user - should only see read-only view
- [ ] Test research page as admin - should see add form
- [ ] Test research page as user - should only see read-only view
- [ ] Test admin-only pages as user - should see unauthorized page
- [ ] Test navigation bar - admin and user should see different links

## Future Enhancements
- Add edit/delete permissions at individual record level
- Add audit logging for all database changes
- Add user activity monitoring
- Add granular permissions (e.g., read-only admin, power user, etc.)
