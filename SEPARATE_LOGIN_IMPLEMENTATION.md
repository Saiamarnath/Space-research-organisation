# Separate Admin and User Login/Signup Implementation

## Overview
This update separates the login and signup flows for Admin and User roles, eliminating confusion and providing a clear, role-specific authentication experience.

## New Pages Created

### 1. **Login Selection Page** (`/login-select`)
- Central landing page for authentication
- Two large cards: "Admin Login" and "User Login"
- Clear visual distinction:
  - **Admin**: Red theme with shield icon
  - **User**: Blue theme with user icon
- Shows privileges for each role
- Links to both signup options

### 2. **Admin Login Page** (`/admin-login`)
- **Red theme** with shield icon
- Title: "ADMIN ACCESS PORTAL"
- Warning badge: "RESTRICTED ACCESS - ADMINISTRATORS ONLY"
- Test credentials displayed in red
- Links to:
  - User Login
  - Admin Signup

### 3. **User Login Page** (`/login`)
- **Blue theme** with user icon
- Title: "USER ACCESS PORTAL"
- Info badge: "USER ACCESS - VIEW MISSIONS & DATA"
- Test credentials displayed in blue
- Links to:
  - Admin Login
  - User Signup

### 4. **Admin Signup Page** (`/admin-signup`)
- **Red theme** with shield icon
- Title: "ADMIN REGISTRATION"
- Warning badge: "ADMIN ACCOUNTS HAVE FULL SYSTEM CONTROL"
- Stricter password requirement (8+ characters)
- Lists admin privileges
- Links to:
  - Admin Login
  - User Signup

### 5. **User Signup Page** (`/user-signup`)
- **Blue theme** with astronaut icon
- Title: "USER REGISTRATION"
- Info badge: "USER ACCOUNTS CAN VIEW MISSIONS & DATA"
- Standard password requirement (6+ characters)
- Lists user access rights
- Links to:
  - User Login
  - Admin Signup

## Routes

| Route | Page | Access | Description |
|-------|------|--------|-------------|
| `/login-select` | Login Selection | Public | Choose between Admin/User login |
| `/admin-login` | Admin Login | Public | Admin authentication |
| `/login` | User Login | Public | User authentication |
| `/admin-signup` | Admin Signup | Public | Register as admin |
| `/user-signup` or `/signup` | User Signup | Public | Register as user |

## Visual Design Differences

### Admin Pages (Red Theme)
- 🔴 Red color scheme (#ef4444)
- 🛡️ Shield icons
- ⚠️ Warning badges
- Gradient: Red to darker red
- Border: Red with glow effect
- Button: Red gradient background

### User Pages (Blue Theme)
- 🔵 Blue/Cyan color scheme (#06b6d4)
- 👤 User icons
- ℹ️ Info badges
- Gradient: Cyan to blue
- Border: Cyan with glow effect
- Button: Blue/info color

## Authentication Flow

### For New Users:
```
1. Visit site → Redirected to /login-select
2. Choose role:
   - Admin → /admin-signup → /admin-login → Admin Dashboard
   - User → /user-signup → /login → Common Dashboard
```

### For Existing Users:
```
1. Visit /login-select
2. Choose appropriate login:
   - Admin → /admin-login → Admin Dashboard (if credentials match admin role)
   - User → /login → Common Dashboard (if credentials match user role)
```

### Logout Flow:
```
1. Click Logout
2. Redirected to /login-select (landing page)
```

## Callbacks Added

### 1. `handle_admin_login`
- Inputs: `admin-login-button`, `admin-login-email`, `admin-login-password`
- Outputs: Session store, error message, redirect trigger
- Validates admin credentials

### 2. `handle_user_login`
- Inputs: `user-login-button`, `user-login-email`, `user-login-password`
- Outputs: Session store, error message, redirect trigger
- Validates user credentials

### 3. `handle_admin_signup`
- Inputs: `admin-signup-button`, username, email, password, confirm
- Output: Success/error message
- Requires 8+ character password
- Creates admin account

### 4. `handle_user_signup`
- Inputs: `user-signup-button`, username, email, password, confirm
- Output: Success/error message
- Requires 6+ character password
- Creates user account

## Benefits

### ✅ Clarity
- No confusion about which login to use
- Clear role distinction from the start
- Visual cues (colors, icons) reinforce roles

### ✅ Security
- Separate authentication flows
- Clear warnings for admin access
- Different password requirements

### ✅ User Experience
- Intuitive navigation
- Role-appropriate messaging
- Clean, modern design

### ✅ Flexibility
- Easy to switch between roles
- Cross-links between pages
- Central selection point

## Test Credentials

### Admin:
- **Email**: `admin@test.com`
- **Password**: `admin123456`
- **Display**: Red code blocks

### User:
- **Email**: `user@space.com`
- **Password**: `user123`
- **Display**: Blue code blocks

## Files Modified

1. **`pages/admin_login.py`** - NEW
2. **`pages/user_login.py`** - NEW
3. **`pages/admin_signup.py`** - NEW
4. **`pages/user_signup.py`** - NEW
5. **`pages/login_selection.py`** - NEW
6. **`pages/__init__.py`** - Updated exports
7. **`app.py`** - Added routes and callbacks

## Old vs New Flow

### OLD:
```
/login → Single login page → Determines role after login
/signup → Single signup page → All users created equal
```

### NEW:
```
/login-select → Choose role
  ├─ Admin → /admin-login or /admin-signup
  └─ User  → /login or /user-signup

Clear separation before authentication
```

## Migration Notes

- Old `/login` route now serves User Login
- Old `/signup` route now serves User Signup
- New `/login-select` is the main landing page
- All unauthorized access redirects to `/login-select`
- Logout redirects to `/login-select`

## Future Enhancements

- [ ] Email verification for new signups
- [ ] Password reset functionality per role
- [ ] Social login options (Google, GitHub)
- [ ] Two-factor authentication for admins
- [ ] Account approval workflow for admin signups
- [ ] Role switching mechanism
