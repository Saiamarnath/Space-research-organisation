# ⚡ QUICK REFERENCE GUIDE

## Common Commands

### Starting the Application
```powershell
# 1. Navigate to project
cd "c:\Users\Shreelakshmi\Downloads\rn"

# 2. Activate virtual environment
.\venv311\Scripts\Activate.ps1

# 3. Run application
python app.py

# 4. Open browser to:
http://localhost:8050
```

### Stopping the Application
```powershell
# Press Ctrl+C in terminal
# Or close the terminal window
```

---

## Test Credentials

### Admin Account (Full Access)
- **Email**: `admin@test.com`
- **Password**: `admin123456`
- **Access**: All pages, edit/delete, system management

### User Account (Limited Access)
- **Email**: `user@space.com`
- **Password**: `user123`
- **Access**: Missions, satellites, research (read-only)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit login/signup form |
| `Tab` | Navigate between fields |
| `Ctrl/Cmd + K` | Global search (placeholder) |
| `?` | Show keyboard shortcuts |
| `Esc` | Close modals |

---

## Easter Eggs

### 1. Houston Message
- Type `houston` (when not in input field)
- Shows: "Houston, we have no problems!"

### 2. Rocket Launch
- Rapid-click logo or satellite icon (5 times fast)
- Animated rocket launches upward

---

## File Structure

```
Key files you might need to edit:

📄 app.py                    # Main app, routing, callbacks
📄 requirements.txt          # Python dependencies
📄 .env                      # Environment variables (create this!)

📁 assets/
   📄 styles.css             # All custom styling
   📄 custom.js              # JavaScript features

📁 pages/
   📄 login.py               # Login page
   📄 signup.py              # Signup page
   📄 dashboard.py           # Main dashboard
   📄 missions.py            # Mission management
   📄 satellites.py          # Satellite tracking
   📄 telemetry.py           # Telemetry data
   📄 employees.py           # Crew management
   📄 research.py            # Research facts
   📄 analytics.py           # Analytics (admin)

📁 config/
   📄 database.py            # Database operations

📁 utils/
   📄 auth.py                # Authentication logic
```

---

## Common Tasks

### Adding a New Page

1. **Create page file**: `pages/my_page.py`
   ```python
   from dash import html
   import dash_bootstrap_components as dbc
   
   def my_page():
       return dbc.Container([
           html.H1("My Page Title"),
           # Your content
       ], fluid=True)
   ```

2. **Import in app.py**:
   ```python
   from pages import my_page
   ```

3. **Add route** in `display_page()` callback:
   ```python
   elif pathname == '/my-page':
       return my_page(), dash.no_update
   ```

4. **Add navigation link** in `create_navbar()`:
   ```python
   dbc.NavItem(dbc.NavLink("My Page", href="/my-page"))
   ```

### Changing Colors

Edit `assets/styles.css`:
```css
:root {
    --nebula-purple: #6366f1;   /* Primary accent */
    --nebula-cyan: #06b6d4;     /* Interactive */
    --hologram-green: #00ff88;  /* Success */
}
```

### Adding Database Table

1. Create table in Supabase SQL editor
2. Add methods in `config/database.py`:
   ```python
   def get_my_data(self):
       return self.client.table('my_table').select('*').execute().data
   ```
3. Use in page:
   ```python
   from config.database import db
   data = db.get_my_data()
   ```

### Adding a Callback

In `app.py`:
```python
@app.callback(
    Output('output-id', 'children'),
    Input('input-id', 'n_clicks')
)
def my_callback(n_clicks):
    return f"Clicked {n_clicks} times"
```

---

## Troubleshooting Quick Fixes

### Problem: Module not found
```powershell
# Solution:
.\venv311\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problem: Port already in use
```powershell
# Solution:
netstat -ano | findstr :8050
taskkill /PID <PID> /F
```

### Problem: Database connection error
```
# Solution:
# 1. Check .env file exists
# 2. Verify SUPABASE_URL and SUPABASE_KEY
# 3. Test connection in Python:
python -c "from config.database import db; print(db.get_all_missions())"
```

### Problem: CSS not loading
```
# Solution:
# 1. Clear browser cache (Ctrl+Shift+R)
# 2. Check assets/styles.css exists
# 3. Check browser console for errors
```

### Problem: Login not working
```
# Solution:
# 1. Check Supabase Auth is enabled
# 2. Verify user exists in database
# 3. Check browser console (F12)
# 4. Try creating new account via signup
```

---

## Environment Variables (.env)

```env
# Required
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here

# Optional
FLASK_ENV=development
SECRET_KEY=generate_random_string
PORT=8050
DEBUG=True
```

Get from: Supabase Dashboard → Settings → API

---

## Database Tables

| Table | Purpose |
|-------|---------|
| `user` | User accounts & roles |
| `department` | Organization departments |
| `employee` | Crew members |
| `mission` | Space missions |
| `satellite` | Satellite inventory |
| `telemetry` | Satellite data |
| `research_fact` | Research contributions |
| `equipment` | Mission equipment |
| `location` | Launch locations |

---

## CSS Classes Reference

### Layout
- `.glass-card` - Glassmorphic card
- `.stat-card` - Statistic display card
- `.dashboard-header` - Dashboard header section

### Animations
- `.fade-in` - Fade in animation
- `.slide-up` - Slide up animation
- `.stagger-1/2/3/4` - Staggered delays

### Typography
- `.glow-text` - Text with glow effect
- `.login-title` - Login page title style
- `.utc-clock` - UTC clock styling

### States
- `.btn-loading` - Button loading state
- `.status-indicator` - Status dot

---

## API Routes (Future)

Not implemented yet, but structure ready:

| Route | Method | Access |
|-------|--------|--------|
| `/api/missions` | GET | All users |
| `/api/missions` | POST | Admin only |
| `/api/satellites` | GET | All users |
| `/api/telemetry` | GET | Admin only |

---

## Performance Tips

1. **Limit data**: Use pagination (page_size=20)
2. **Cache results**: Implement Flask-Caching
3. **Lazy load**: Load charts on demand
4. **Optimize images**: Use WebP format
5. **CDN**: Serve static assets from CDN

---

## Security Checklist

- [ ] Never commit .env file
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production
- [ ] Implement rate limiting
- [ ] Sanitize user inputs
- [ ] Keep dependencies updated
- [ ] Enable Supabase RLS (Row Level Security)
- [ ] Use strong passwords
- [ ] Set up 2FA for admin accounts

---

## Deployment Checklist

- [ ] Update .env with production values
- [ ] Set FLASK_ENV=production
- [ ] Disable DEBUG mode
- [ ] Set up logging
- [ ] Configure backups
- [ ] Test all features
- [ ] Enable monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure domain and SSL
- [ ] Update Supabase site URL

---

## Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Supported |
| Firefox | 88+ | ✅ Supported |
| Safari | 14+ | ✅ Supported |
| Edge | 90+ | ✅ Supported |
| Opera | 76+ | ✅ Supported |
| IE 11 | - | ❌ Not supported |

---

## Mobile Support

| Device | Status |
|--------|--------|
| iOS (iPhone) | ✅ Supported |
| iOS (iPad) | ✅ Supported |
| Android (Phone) | ✅ Supported |
| Android (Tablet) | ✅ Supported |

Minimum screen width: 320px

---

## Resources

### Documentation
- **This Project**: README.md, SETUP_GUIDE.md, ENHANCEMENTS.md
- **Dash**: https://dash.plotly.com
- **Plotly**: https://plotly.com/python
- **Supabase**: https://supabase.com/docs
- **Bootstrap**: https://getbootstrap.com

### Community
- **Dash Forum**: https://community.plotly.com
- **Supabase Discord**: https://discord.supabase.com
- **Stack Overflow**: Tag: plotly-dash, supabase

### Tools
- **VS Code**: Code editor
- **Supabase Studio**: Database GUI
- **Browser DevTools**: F12 for debugging
- **Postman**: API testing

---

## Support

### Getting Help

1. **Check documentation**: README.md, SETUP_GUIDE.md
2. **Browser console**: F12 → Console tab
3. **Network tab**: Check API calls
4. **Check logs**: Terminal output
5. **Verify config**: .env file

### Reporting Issues

When reporting issues, include:
- Error message (full text)
- Steps to reproduce
- Browser and version
- Screenshot (if UI issue)
- Terminal logs

---

## Version Information

**Application**: Space Research Mission Control
**Version**: 2.0.0
**Last Updated**: November 2025
**Tech Stack**: Python 3.11, Dash 2.14, Supabase
**Status**: ✅ Production Ready

---

## Quick Commands Cheat Sheet

```powershell
# Activate environment
.\venv311\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Run app
python app.py

# Install single package
pip install package-name

# Update package
pip install --upgrade package-name

# List installed packages
pip list

# Save dependencies
pip freeze > requirements.txt

# Check Python version
python --version

# Deactivate environment
deactivate
```

---

## Color Palette Quick Reference

```css
/* Copy-paste these for consistency */

/* Backgrounds */
--space-black: #0a0e27;
--space-dark: #1a1f3a;
--space-purple: #2d1b4e;

/* Accents */
--nebula-purple: #6366f1;
--nebula-cyan: #06b6d4;
--hologram-green: #00ff88;

/* Status */
--success-green: #10b981;
--warning-amber: #f59e0b;
--alert-red: #ef4444;

/* Text */
--text-primary: #e5e7eb;
--text-secondary: #9ca3af;
--text-muted: #6b7280;
```

---

## Icon Classes (Font Awesome)

Commonly used icons:
```html
<i className="fas fa-rocket"></i>         <!-- Mission -->
<i className="fas fa-satellite"></i>       <!-- Satellite -->
<i className="fas fa-users"></i>           <!-- Crew -->
<i className="fas fa-chart-bar"></i>       <!-- Analytics -->
<i className="fas fa-globe"></i>           <!-- Global -->
<i className="fas fa-terminal"></i>        <!-- Terminal -->
<i className="fas fa-clock"></i>           <!-- Time -->
<i className="fas fa-check-circle"></i>    <!-- Success -->
<i className="fas fa-exclamation-triangle"></i> <!-- Warning -->
```

---

**📋 Keep this guide handy for quick reference!**

**🚀 Happy coding and exploring the cosmos!**

