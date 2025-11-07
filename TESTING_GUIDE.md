# 🧪 Testing Guide - RBAC & UX Fixes

## Overview
This guide will help you test the three critical fixes implemented:
1. **RBAC (Role-Based Access Control)** - Admin vs User permissions
2. **Password Toggle** - Show/hide password functionality
3. **Enter Key Submission** - Keyboard shortcuts for login

---

## 🚀 Quick Start

### 1. Start the Application
The application is already running at: **http://localhost:8050**

### 2. Test Accounts
Use these accounts from your Supabase database:

| Email | Password | Role | Use Case |
|-------|----------|------|----------|
| `admin@space.com` | (your password) | **ADMIN** | Full access to all features |
| `analyst_mike@space.com` | (your password) | **USER** | Read-only, limited access |
| `testuser@space.com` | (your password) | **USER** | Read-only, limited access |

---

## 🔐 Test 1: Password Toggle Functionality

### Steps:
1. Navigate to **http://localhost:8050/login**
2. Click in the **password** field
3. Type any text (e.g., "test123")
4. Click the **eye icon** 👁️ on the right side of the password field

### Expected Behavior:
✅ **First click**: Password becomes visible (plain text), icon changes to 👁️‍🗨️ (slashed eye)
✅ **Second click**: Password becomes hidden (dots), icon changes back to 👁️
✅ **Instant response**: No page reload, smooth transition
✅ **Proper cursor**: Eye icon shows pointer cursor on hover

### Pass Criteria:
- [ ] Password toggles between hidden/visible
- [ ] Icon changes between `fa-eye` and `fa-eye-slash`
- [ ] No console errors
- [ ] Works smoothly without lag

---

## ⌨️ Test 2: Enter Key Submission

### Steps:
1. Navigate to **http://localhost:8050/login**
2. Type a **valid email** in the email field
3. Press **Enter** (do NOT click Login button)
4. Cursor should move to password field
5. Type a **valid password** in the password field
6. Press **Enter** again

### Expected Behavior:
✅ **From email field**: Pressing Enter submits the form (attempts login)
✅ **From password field**: Pressing Enter submits the form (attempts login)
✅ **Success message**: If credentials are correct, shows green success alert with checkmark icon
✅ **Error message**: If credentials are wrong, shows red error alert with shake animation
✅ **Redirect**: On success, redirects to dashboard

### Pass Criteria:
- [ ] Enter key works from email field
- [ ] Enter key works from password field
- [ ] Login button click still works
- [ ] Error messages display correctly with animations
- [ ] Successful login redirects to dashboard

---

## 🛡️ Test 3: RBAC (Role-Based Access Control)

### Part A: Login as ADMIN

1. **Login**: Use `admin@space.com`
2. **Check Navbar**: Should see these items with **red underlines**:
   - 🏢 Employees
   - 📡 Telemetry
   - 📊 Analytics
3. **Check Role Badge**: Top-right should show red badge:
   ```
   🛡️ ADMIN
   ```

### Part B: Test Admin Access

1. Navigate to **Dashboard** - Should see welcome message: "Welcome, admin@space.com"
2. Navigate to **Missions** - Should have full CRUD access
3. Navigate to **Satellites** - Should have full CRUD access
4. Navigate to **Research Facts**:
   - Header should show: **"🛡️ ADMIN ACCESS"** (red badge)
   - Description: "You can edit and delete any fact"
   - All edit/delete buttons visible for ALL facts
5. Navigate to **Employees** - Should work (admin-only page)
6. Navigate to **Telemetry** - Should work (admin-only page)
7. Navigate to **Analytics** - Should work (admin-only page)

### Part C: Login as USER

1. **Logout**: Click logout in navbar
2. **Login**: Use `analyst_mike@space.com` or `testuser@space.com`
3. **Check Navbar**: Should see:
   - **Blue badge**: 👤 USER
   - **NO red underlines** on any items
   - **Missing items**: Employees, Telemetry, Analytics (hidden)

### Part D: Test User Restrictions

1. Navigate to **Dashboard** - Should see welcome message
2. Navigate to **Missions** - Should be **read-only** (no edit/delete buttons for users)
3. Navigate to **Satellites** - Should be **read-only**
4. Navigate to **Research Facts**:
   - Header should show: **"👤 USER ACCESS"** (blue badge)
   - Description: "You can only edit or delete your own contributions"
   - Edit/delete buttons ONLY visible for facts created by this user
5. Try to navigate to **http://localhost:8050/employees** manually:
   - Should show **"ACCESS RESTRICTED"** page
   - Red shield icon with shake animation
   - Warning message: "This section is restricted to ADMIN personnel only"
6. Try **http://localhost:8050/telemetry** - Same restriction
7. Try **http://localhost:8050/analytics** - Same restriction

### RBAC Pass Criteria:
- [ ] Admin sees all menu items with red badges
- [ ] User sees limited menu items with blue badge
- [ ] Admin can access Employees/Telemetry/Analytics
- [ ] User gets "ACCESS RESTRICTED" page for admin pages
- [ ] Research facts show correct role badges
- [ ] Edit/delete buttons respect ownership rules
- [ ] Navbar styling reflects roles (red for admin, blue for user)

---

## 🎨 Visual Indicators

### Admin Visual Cues:
- **Navbar Badge**: 🛡️ ADMIN (red background, shield icon)
- **Admin Pages**: Red underline border (2px solid #ef4444)
- **Research Header**: Red shield badge "ADMIN ACCESS"
- **Full Permissions**: Can edit/delete any content

### User Visual Cues:
- **Navbar Badge**: 👤 USER (blue background, user icon)
- **Limited Pages**: Only Dashboard, Missions, Satellites, Research visible
- **Research Header**: Blue user badge "USER ACCESS"
- **Limited Permissions**: Can only edit/delete own research facts

---

## 🐛 Common Issues & Solutions

### Issue 1: "Password toggle doesn't work"
**Solution**: 
- Check browser console for JavaScript errors
- Verify `assets/custom.js` is loaded
- Clear browser cache and reload

### Issue 2: "Enter key does nothing"
**Solution**:
- Check that `n_submit=0` is set on email and password inputs
- Verify `handle_login` callback has `Input('login-email', 'n_submit')`
- Check browser console for callback errors

### Issue 3: "Both admin and user see same pages"
**Solution**:
- Check Supabase user table has correct `role` column values
- Verify session storage contains role: `dcc.Store(id='session-store')`
- Check `create_navbar()` function reads role from session
- Confirm `is_admin` variable is set correctly in callbacks

### Issue 4: "Unauthorized page doesn't show"
**Solution**:
- Verify route `/unauthorized` exists in `app.py`
- Check that callbacks redirect to `/unauthorized` for non-admin users
- Ensure `pages/unauthorized.py` is imported

---

## ✅ Complete Test Checklist

### Password Toggle:
- [ ] Icon changes between eye and slashed-eye
- [ ] Password text toggles between hidden/visible
- [ ] Cursor shows pointer on hover
- [ ] No page reload or flashing

### Enter Key:
- [ ] Enter works from email field
- [ ] Enter works from password field
- [ ] Success message appears on valid login
- [ ] Error message appears on invalid login
- [ ] Shake animation plays on error
- [ ] Redirect happens on success

### RBAC - Admin:
- [ ] Red admin badge in navbar
- [ ] Red underlines on admin-only items
- [ ] Can access Employees page
- [ ] Can access Telemetry page
- [ ] Can access Analytics page
- [ ] Research shows "ADMIN ACCESS" badge
- [ ] Can edit/delete any research fact

### RBAC - User:
- [ ] Blue user badge in navbar
- [ ] No admin items in navbar
- [ ] Employees link hidden
- [ ] Telemetry link hidden
- [ ] Analytics link hidden
- [ ] Manual URL access shows "ACCESS RESTRICTED"
- [ ] Research shows "USER ACCESS" badge
- [ ] Can only edit/delete own research facts

---

## 📸 Screenshots to Take

For documentation purposes, capture:
1. **Login page** - showing password toggle eye icon
2. **Admin navbar** - with red badges and admin items
3. **User navbar** - with blue badge, missing admin items
4. **Research page (admin)** - showing red "ADMIN ACCESS" badge
5. **Research page (user)** - showing blue "USER ACCESS" badge
6. **Unauthorized page** - when user tries to access admin page
7. **Success alert** - green message after login
8. **Error alert** - red message with shake animation

---

## 🎯 Success Metrics

All fixes are working correctly if:
- ✅ Password toggle works instantly with visual feedback
- ✅ Enter key submits login form from both fields
- ✅ Admin can access all pages and see red badges
- ✅ User cannot access admin pages and sees blue badges
- ✅ Research facts respect ownership rules
- ✅ Unauthorized page displays for restricted access
- ✅ No console errors in browser developer tools

---

## 📝 Notes

### Browser Compatibility:
- **Tested on**: Chrome, Edge, Firefox
- **Requires**: Modern browser with JavaScript enabled
- **Best experience**: Chrome/Edge with hardware acceleration

### Performance:
- Password toggle uses **client-side callback** (instant, no server delay)
- Enter key uses **standard Dash callback** (requires server response)
- RBAC checks happen on **server-side** (secure, cannot be bypassed)

### Security:
- Role information stored in **Supabase user table**
- Session data verified on **every callback**
- Admin pages protected by **server-side checks**
- Client-side restrictions are **visual only** (server validates all actions)

---

## 🆘 Need Help?

If tests fail, check:
1. **Terminal output**: Look for Python errors
2. **Browser console**: Press F12, check Console tab for JavaScript errors
3. **Network tab**: Verify API calls to Supabase succeed
4. **Supabase dashboard**: Confirm user table has role column with correct values

Happy testing! 🚀✨
