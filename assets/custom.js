/**
 * Space Research Mission Control - Custom JavaScript
 * Adds interactivity, animations, and enhanced UX
 */

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Mission Control Systems Initializing...');
    
    // Initialize all features
    initCountUpAnimations();
    initLiveClock();
    initKeyboardShortcuts();
    initPasswordStrengthMeter();
    initPasswordToggle();
    initEnterKeyHandlers();
    
    // Easter eggs
    initEasterEggs();
    
    console.log('✅ All systems operational');
});

// ============================================
// COUNT-UP ANIMATIONS FOR STATS
// ============================================

function initCountUpAnimations() {
    const statElements = document.querySelectorAll('.stat-value[data-target]');
    
    statElements.forEach(element => {
        const target = parseInt(element.getAttribute('data-target')) || 0;
        animateCountUp(element, target);
    });
}

function animateCountUp(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16); // 60fps
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// ============================================
// LIVE UTC CLOCK
// ============================================

function initLiveClock() {
    function updateClock() {
        const clockElement = document.getElementById('live-utc-clock');
        if (clockElement) {
            const now = new Date();
            const utcString = now.toISOString().substr(11, 8);
            clockElement.textContent = utcString;
        }
    }
    
    // Update immediately and then every second
    updateClock();
    setInterval(updateClock, 1000);
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for global search (placeholder)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            console.log('🔍 Global search shortcut triggered');
            // Add search modal here in future
            showNotification('Global search: Ctrl+K', 'info');
        }
        
        // ? for keyboard shortcuts help
        if (e.key === '?' && !isInputFocused()) {
            e.preventDefault();
            showKeyboardShortcutsModal();
        }
        
        // Esc to close modals
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

function isInputFocused() {
    const activeElement = document.activeElement;
    return activeElement && (
        activeElement.tagName === 'INPUT' ||
        activeElement.tagName === 'TEXTAREA' ||
        activeElement.isContentEditable
    );
}

function showKeyboardShortcutsModal() {
    console.log('⌨️ Keyboard shortcuts:');
    console.log('Ctrl+K: Global search');
    console.log('?: Show shortcuts');
    console.log('Esc: Close modals');
    showNotification('Press Ctrl+K for search, ? for help', 'info');
}

function closeAllModals() {
    // Close any open modals
    const modals = document.querySelectorAll('.modal.show');
    modals.forEach(modal => {
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.remove();
        modal.classList.remove('show');
        modal.style.display = 'none';
    });
}

// ============================================
// PASSWORD STRENGTH METER
// ============================================

function initPasswordStrengthMeter() {
    const passwordInput = document.getElementById('signup-password');
    if (!passwordInput) return;
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strength = calculatePasswordStrength(password);
        updatePasswordStrengthUI(strength);
    });
}

function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (!password) return { level: 0, text: '', color: '' };
    
    // Length check
    if (password.length >= 6) strength += 20;
    if (password.length >= 10) strength += 20;
    if (password.length >= 14) strength += 10;
    
    // Character variety
    if (/[a-z]/.test(password)) strength += 15;
    if (/[A-Z]/.test(password)) strength += 15;
    if (/[0-9]/.test(password)) strength += 10;
    if (/[^a-zA-Z0-9]/.test(password)) strength += 10;
    
    // Determine level
    let level, text, color;
    if (strength < 30) {
        level = 1;
        text = 'Weak - Add more characters';
        color = '#ef4444';
    } else if (strength < 50) {
        level = 2;
        text = 'Fair - Add variety';
        color = '#f59e0b';
    } else if (strength < 70) {
        level = 3;
        text = 'Good - Almost there';
        color = '#06b6d4';
    } else {
        level = 4;
        text = 'Strong - Excellent!';
        color = '#10b981';
    }
    
    return { level, text, color, strength: Math.min(strength, 100) };
}

function updatePasswordStrengthUI(strengthData) {
    const progressBar = document.getElementById('password-strength-progress');
    const strengthText = document.getElementById('password-strength-text');
    
    if (!progressBar || !strengthText) return;
    
    progressBar.style.width = `${strengthData.strength}%`;
    progressBar.style.backgroundColor = strengthData.color;
    strengthText.textContent = strengthData.text;
    strengthText.style.color = strengthData.color;
}

// ============================================
// PASSWORD TOGGLE (SHOW/HIDE)
// ============================================

function initPasswordToggle() {
    // Login password toggle
    const loginToggle = document.getElementById('password-toggle');
    const loginPassword = document.getElementById('login-password');
    
    if (loginToggle && loginPassword) {
        loginToggle.addEventListener('click', function() {
            togglePasswordVisibility(loginPassword, 'password-toggle-icon');
        });
    }
    
    // Signup password toggle
    const signupToggle = document.getElementById('signup-password-toggle');
    const signupPassword = document.getElementById('signup-password');
    
    if (signupToggle && signupPassword) {
        signupToggle.addEventListener('click', function() {
            togglePasswordVisibility(signupPassword, 'signup-password-toggle-icon');
        });
    }
}

function togglePasswordVisibility(inputElement, iconId) {
    const icon = document.getElementById(iconId);
    
    if (inputElement.type === 'password') {
        inputElement.type = 'text';
        if (icon) icon.className = 'fas fa-eye-slash';
    } else {
        inputElement.type = 'password';
        if (icon) icon.className = 'fas fa-eye';
    }
}

// ============================================
// ENTER KEY HANDLERS FOR FORMS
// ============================================

function initEnterKeyHandlers() {
    // Login form
    const loginEmail = document.getElementById('login-email');
    const loginPassword = document.getElementById('login-password');
    const loginButton = document.getElementById('login-button');
    
    if (loginEmail && loginPassword && loginButton) {
        [loginEmail, loginPassword].forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    loginButton.click();
                }
            });
        });
    }
    
    // Signup form
    const signupInputs = [
        'signup-username',
        'signup-email',
        'signup-password',
        'signup-password-confirm'
    ];
    const signupButton = document.getElementById('signup-button');
    
    if (signupButton) {
        signupInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        signupButton.click();
                    }
                });
            }
        });
    }
}

// ============================================
// PASSWORD MATCH INDICATOR
// ============================================

// Auto-check password match
setInterval(function() {
    const password = document.getElementById('signup-password');
    const confirm = document.getElementById('signup-password-confirm');
    const indicator = document.getElementById('password-match-indicator');
    
    if (!password || !confirm || !indicator) return;
    
    if (confirm.value.length > 0) {
        if (password.value === confirm.value) {
            indicator.innerHTML = '<small class="text-success"><i class="fas fa-check-circle me-1"></i>Passwords match</small>';
        } else {
            indicator.innerHTML = '<small class="text-danger"><i class="fas fa-times-circle me-1"></i>Passwords do not match</small>';
        }
    } else {
        indicator.innerHTML = '';
    }
}, 500);

// ============================================
// BUTTON LOADING STATE
// ============================================

function setButtonLoading(buttonId, loading = true) {
    const button = document.getElementById(buttonId);
    if (!button) return;
    
    if (loading) {
        button.classList.add('btn-loading');
        button.disabled = true;
        const textSpan = button.querySelector('span');
        if (textSpan) {
            textSpan.setAttribute('data-original-text', textSpan.textContent);
            textSpan.textContent = 'PROCESSING...';
        }
    } else {
        button.classList.remove('btn-loading');
        button.disabled = false;
        const textSpan = button.querySelector('span');
        if (textSpan) {
            const originalText = textSpan.getAttribute('data-original-text');
            if (originalText) {
                textSpan.textContent = originalText;
            }
        }
    }
}

// ============================================
// NOTIFICATIONS
// ============================================

function showNotification(message, type = 'info', duration = 3000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getIconForType(type)} me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Remove after duration
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ============================================
// EASTER EGGS
// ============================================

function initEasterEggs() {
    let typedText = '';
    const easterEggCode = 'houston';
    
    document.addEventListener('keypress', function(e) {
        if (isInputFocused()) return;
        
        typedText += e.key.toLowerCase();
        
        // Keep only last N characters
        if (typedText.length > easterEggCode.length) {
            typedText = typedText.slice(-easterEggCode.length);
        }
        
        // Check for easter egg
        if (typedText === easterEggCode) {
            triggerHoustonEasterEgg();
            typedText = '';
        }
    });
    
    // Logo rapid click easter egg
    const logos = document.querySelectorAll('.navbar-brand, .fa-satellite');
    logos.forEach(logo => {
        let clickCount = 0;
        let clickTimer;
        
        logo.addEventListener('click', function() {
            clickCount++;
            clearTimeout(clickTimer);
            
            if (clickCount >= 5) {
                triggerRocketEasterEgg(logo);
                clickCount = 0;
            }
            
            clickTimer = setTimeout(() => {
                clickCount = 0;
            }, 2000);
        });
    });
}

function triggerHoustonEasterEgg() {
    console.log('🚀 Houston, we have no problems!');
    
    // Create floating message
    const message = document.createElement('div');
    message.innerHTML = `
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(10, 14, 39, 0.95);
            border: 2px solid #00ff88;
            border-radius: 16px;
            padding: 2rem;
            z-index: 10000;
            text-align: center;
            box-shadow: 0 0 60px rgba(0, 255, 136, 0.5);
        ">
            <i class="fas fa-rocket fa-3x mb-3" style="color: #00ff88;"></i>
            <h3 style="color: #00ff88; margin: 0;">Houston, we have no problems!</h3>
            <p style="color: #9ca3af; margin-top: 0.5rem;">All systems nominal 🚀</p>
        </div>
    `;
    
    document.body.appendChild(message);
    
    setTimeout(() => {
        message.style.transition = 'opacity 0.5s';
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 500);
    }, 3000);
}

function triggerRocketEasterEgg(element) {
    console.log('🚀 Rocket launch sequence initiated!');
    
    // Create rocket
    const rocket = document.createElement('i');
    rocket.className = 'fas fa-rocket';
    rocket.style.position = 'fixed';
    rocket.style.fontSize = '3rem';
    rocket.style.color = '#00ff88';
    rocket.style.zIndex = '10000';
    rocket.style.transform = 'rotate(-45deg)';
    rocket.style.textShadow = '0 0 20px rgba(0, 255, 136, 0.8)';
    
    const rect = element.getBoundingClientRect();
    rocket.style.left = rect.left + 'px';
    rocket.style.top = rect.top + 'px';
    
    document.body.appendChild(rocket);
    
    // Animate rocket
    let pos = rect.top;
    const interval = setInterval(() => {
        pos -= 10;
        rocket.style.top = pos + 'px';
        rocket.style.opacity = (pos / rect.top);
        
        if (pos < -100) {
            clearInterval(interval);
            rocket.remove();
        }
    }, 20);
    
    showNotification('🚀 Liftoff!', 'success');
}

// ============================================
// SMOOTH SCROLL
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================
// CARD HOVER EFFECTS
// ============================================

document.querySelectorAll('.glass-card, .stat-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ============================================
// AUTO-FOCUS FIRST INPUT
// ============================================

setTimeout(function() {
    const firstInput = document.querySelector('input[type="email"][autofocus], input[type="text"][autofocus]');
    if (firstInput) {
        firstInput.focus();
    }
}, 100);

// ============================================
// REMEMBER EMAIL FUNCTIONALITY
// ============================================

const rememberCheckbox = document.getElementById('remember-me');
const loginEmail = document.getElementById('login-email');

if (rememberCheckbox && loginEmail) {
    // Load saved email on page load
    const savedEmail = localStorage.getItem('rememberedEmail');
    if (savedEmail) {
        loginEmail.value = savedEmail;
        rememberCheckbox.checked = true;
    }
    
    // Save email when checkbox is checked
    rememberCheckbox.addEventListener('change', function() {
        if (this.checked && loginEmail.value) {
            localStorage.setItem('rememberedEmail', loginEmail.value);
        } else {
            localStorage.removeItem('rememberedEmail');
        }
    });
    
    // Update saved email when input changes
    loginEmail.addEventListener('change', function() {
        if (rememberCheckbox.checked) {
            localStorage.setItem('rememberedEmail', this.value);
        }
    });
}

// ============================================
// GLOBAL UTILITY FUNCTIONS
// ============================================

window.missionControl = {
    showNotification,
    setButtonLoading,
    animateCountUp,
    showKeyboardShortcutsModal
};

console.log('🎯 Mission Control JavaScript loaded successfully');
