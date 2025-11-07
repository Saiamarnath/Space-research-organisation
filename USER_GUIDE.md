# User Guide - Role-Based Access Control

## 🎯 Overview

The Space Research System now has two types of users with different access levels:

---

## 👤 USER ACCESS (Regular Users)

### What Users Can Do:
✅ **View** missions, satellites, and research facts  
✅ Access the Common Dashboard with system overview  
✅ Browse all data in read-only mode  
✅ Navigate between allowed pages  

### What Users Cannot Do:
❌ Cannot add new missions, satellites, or research facts  
❌ Cannot edit existing data  
❌ Cannot delete records  
❌ Cannot access admin-only pages (Employees, Telemetry, Analytics, Admin Dashboard)  

### User Navigation Menu:
```
┌─────────────────────────────────────────────┐
│ 🏠 Home                                     │
│ 🚀 Missions                                 │
│ 🛰️  Satellites                              │
│ 🧪 Research Facts                           │
│ 👤 USER (badge)                             │
│ 🚪 Logout                                   │
└─────────────────────────────────────────────┘
```

### User Dashboard (Home Page):
- Mission statistics and overview
- Satellite fleet status
- Recent missions list
- Quick links to other pages
- **Read-only mode** - no edit buttons visible

---

## 🛡️ ADMIN ACCESS (Administrators)

### What Admins Can Do:
✅ **Everything users can do**, PLUS:  
✅ **Add** new missions, satellites, and research facts  
✅ **Edit** existing missions, satellites, and research facts  
✅ **Delete** records  
✅ Access full Admin Dashboard with detailed analytics  
✅ Access admin-only pages:
   - Employee Management
   - Telemetry Data
   - Advanced Analytics
   - Admin Control Panel

### Admin Navigation Menu:
```
┌─────────────────────────────────────────────┐
│ 📊 Dashboard (Admin Dashboard)              │
│ 🛡️  Admin Control (marked with red border) │
│ 🚀 Missions                                 │
│ 🛰️  Satellites                              │
│ 👥 Employees (admin-only, red border)       │
│ 📡 Telemetry (admin-only, red border)       │
│ 🧪 Research Facts                           │
│ 📈 Analytics (admin-only, red border)       │
│ 🛡️  ADMIN (red badge)                       │
│ 🚪 Logout                                   │
└─────────────────────────────────────────────┘
```

### Admin Dashboard (Home Page):
- Full mission control center
- Live telemetry feed
- Satellite tracking
- Department activity
- Complete system analytics
- **Full edit access** - all control buttons visible

---

## 📄 Page-by-Page Access Guide

### 1️⃣ Missions Page (`/missions`)

#### 👤 USER VIEW:
```
┌────────────────────────────────────────────┐
│  ℹ️  You are viewing in read-only mode.    │
│     Only administrators can edit mission   │
│     data.                                  │
├────────────────────────────────────────────┤
│  Mission Cards (view only)                │
│  - No edit buttons                         │
│  - No delete options                       │
│  Data Table (browsable)                    │
└────────────────────────────────────────────┘
```

#### 🛡️ ADMIN VIEW:
```
┌────────────────────────────────────────────┐
│  ➕ Add New Mission                        │
├────────────────────────────────────────────┤
│  Mission Cards                             │
│  - ✏️  Edit button on each card           │
│  - 🗑️  Delete options available           │
│  Data Table (editable)                     │
└────────────────────────────────────────────┘
```

---

### 2️⃣ Satellites Page (`/satellites`)

#### 👤 USER VIEW:
```
┌────────────────────────────────────────────┐
│  ℹ️  You are viewing in read-only mode.    │
│     Only administrators can edit satellite │
│     data.                                  │
├────────────────────────────────────────────┤
│  Satellites Table (view only)             │
│  - No selection enabled                    │
│  - No action buttons                       │
└────────────────────────────────────────────┘
```

#### 🛡️ ADMIN VIEW:
```
┌────────────────────────────────────────────┐
│  ➕ Add New Satellite                      │
│  ✏️  Edit Selected                         │
│  🗑️  Delete Selected                       │
├────────────────────────────────────────────┤
│  Satellites Table (editable)              │
│  - Row selection enabled                   │
│  - Full CRUD operations                    │
└────────────────────────────────────────────┘
```

---

### 3️⃣ Research Facts Page (`/research`)

#### 👤 USER VIEW:
```
┌────────────────────────────────────────────┐
│  ℹ️  You are viewing in read-only mode.    │
│     Only administrators can add or edit    │
│     research facts.                        │
├────────────────────────────────────────────┤
│  Research Facts Table (view only)         │
│  - Can browse and filter                   │
│  - No add/edit/delete                      │
└────────────────────────────────────────────┘
```

#### 🛡️ ADMIN VIEW:
```
┌────────────────────────────────────────────┐
│  ➕ Add New Research Fact (Admin Only)     │
│  ┌──────────────────────────────────────┐ │
│  │ Fact Title:  [____________]          │ │
│  │ Category:    [▼ Dropdown]            │ │
│  │ Description: [____________]          │ │
│  │ Source:      [____________]          │ │
│  │              [➕ Add Fact]            │ │
│  └──────────────────────────────────────┘ │
├────────────────────────────────────────────┤
│  Research Facts Table (editable)          │
│  - Full management capabilities            │
└────────────────────────────────────────────┘
```

---

## 🚫 Restricted Pages (Admin Only)

These pages show an "Unauthorized Access" message for regular users:

1. **Employees** (`/employees`) - Employee management
2. **Telemetry** (`/telemetry`) - Real-time satellite data
3. **Analytics** (`/analytics`) - Advanced analytics dashboard
4. **Admin Dashboard** (`/admin-dashboard`) - Full admin control panel
5. **Full Dashboard** (`/dashboard`) - Complete mission control

If a user tries to access these pages, they see:
```
┌────────────────────────────────────────────┐
│  ⚠️  UNAUTHORIZED ACCESS                    │
│                                            │
│  This page is for administrators only.     │
│  You don't have permission to view this    │
│  content.                                  │
│                                            │
│  [🔙 Go Back]                              │
└────────────────────────────────────────────┘
```

---

## 🔐 Login Flow

### User Login:
1. Navigate to `/login`
2. Enter user credentials
3. Redirected to **Common Dashboard** (`/`)
4. See USER badge (blue) in navigation

### Admin Login:
1. Navigate to `/login`
2. Enter admin credentials
3. Redirected to **Admin Dashboard** (`/`)
4. See ADMIN badge (red) in navigation

---

## 🎨 Visual Indicators

### Admin Indicators:
- 🔴 Red "ADMIN" badge in navbar
- 🔴 Red borders on admin-only nav items
- 🛡️ Shield icon next to admin features
- ➕ Add buttons visible
- ✏️ Edit buttons visible
- 🗑️ Delete buttons visible

### User Indicators:
- 🔵 Blue "USER" badge in navbar
- ℹ️ Blue info banners on pages
- 👁️ Eye icon indicating read-only access
- 🔒 No edit controls visible
- Clean, simplified interface

---

## 📝 Quick Reference Table

| Feature | User Access | Admin Access |
|---------|-------------|--------------|
| View Missions | ✅ Yes | ✅ Yes |
| Add/Edit/Delete Missions | ❌ No | ✅ Yes |
| View Satellites | ✅ Yes | ✅ Yes |
| Add/Edit/Delete Satellites | ❌ No | ✅ Yes |
| View Research Facts | ✅ Yes | ✅ Yes |
| Add/Edit/Delete Research Facts | ❌ No | ✅ Yes |
| Common Dashboard | ✅ Yes | ✅ Yes |
| Full Admin Dashboard | ❌ No | ✅ Yes |
| Employee Management | ❌ No | ✅ Yes |
| Telemetry Data | ❌ No | ✅ Yes |
| Analytics | ❌ No | ✅ Yes |

---

## 🆘 Need Help?

- **Forgot Password?** Contact your system administrator
- **Need Admin Access?** Request upgrade from current administrator
- **Found a Bug?** Report to the development team
- **Feature Request?** Submit through the proper channels

---

**Last Updated:** November 6, 2025  
**Version:** 2.0 - RBAC Implementation
