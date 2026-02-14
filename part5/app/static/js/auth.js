/**
 * HBnB V2 — Authentication
 * JWT-based auth with OTP + Magic Link support.
 */

const Auth = {
    TOKEN_KEY: 'hbnb_token',
    REFRESH_KEY: 'hbnb_refresh',
    USER_KEY: 'hbnb_user',

    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    },

    getRefresh() {
        return localStorage.getItem(this.REFRESH_KEY);
    },

    getUser() {
        const u = localStorage.getItem(this.USER_KEY);
        return u ? JSON.parse(u) : null;
    },

    setAuth(data) {
        if (data.access_token) localStorage.setItem(this.TOKEN_KEY, data.access_token);
        if (data.refresh_token) localStorage.setItem(this.REFRESH_KEY, data.refresh_token);
        if (data.user) localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
    },

    clear() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.REFRESH_KEY);
        localStorage.removeItem(this.USER_KEY);
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    isOwner() {
        const u = this.getUser();
        return u && (u.role === 'owner' || u.role === 'admin');
    },

    isAdmin() {
        const u = this.getUser();
        return u && u.role === 'admin';
    },

    /* --- OTP flow --- */
    async requestOTP(email) {
        return api.post('/auth/otp/request', { email });
    },

    async verifyOTP(email, code) {
        const res = await api.post('/auth/otp/verify', { email, code });
        if (res.access_token) this.setAuth(res);
        return res;
    },

    /* --- Magic Link flow --- */
    async requestMagicLink(email) {
        return api.post('/auth/magic-link/request', { email });
    },

    async verifyMagicLink(token) {
        const res = await api.post('/auth/magic-link/verify', { token });
        if (res.access_token) this.setAuth(res);
        return res;
    },

    /* --- Password login (fallback) --- */
    async login(email, password) {
        const res = await api.post('/auth/login', { email, password });
        if (res.access_token) this.setAuth(res);
        return res;
    },

    /* --- Owner registration --- */
    async registerOwner(data) {
        const res = await api.post('/auth/register/owner', data);
        if (res.access_token) this.setAuth(res);
        return res;
    },

    /* --- Refresh --- */
    async refresh() {
        const token = this.getRefresh();
        if (!token) return null;
        try {
            const res = await fetch(`${CONFIG.API_URL}/auth/refresh`, {
                method: 'POST',
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await res.json();
            if (data.access_token) {
                localStorage.setItem(this.TOKEN_KEY, data.access_token);
            }
            return data;
        } catch { return null; }
    },

    /* --- Profile --- */
    async getProfile() {
        return api.get('/auth/me');
    },

    async updateProfile(data) {
        return api.put('/auth/me', data);
    },

    /* --- Logout --- */
    logout() {
        this.clear();
        updateAuthUI();
        showToast(t('logout'), 'info');
        window.location.href = '/';
    }
};

/**
 * Update navbar based on auth state
 * Works with both home page (class="hidden") and inner pages (style.display)
 */
function updateAuthUI() {
    const loginBtn = document.getElementById('loginBtn');
    const userMenu = document.getElementById('userMenu');
    const userAvatar = document.getElementById('userAvatar');
    const userName = document.getElementById('userName');
    const ownerLink = document.getElementById('ownerLink');

    if (Auth.isLoggedIn()) {
        const user = Auth.getUser();
        if (loginBtn) { loginBtn.style.display = 'none'; loginBtn.classList.add('hidden'); }
        if (userMenu) { userMenu.style.display = 'flex'; userMenu.classList.remove('hidden'); }
        if (userName) userName.textContent = user?.first_name || 'User';
        if (userAvatar) {
            if (user?.avatar_url) {
                userAvatar.src = user.avatar_url;
            } else {
                // Generate initials avatar
                const name = user?.first_name || 'U';
                userAvatar.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=6C63FF&color=fff&size=36&bold=true`;
            }
        }
        // Show owner link if owner/admin
        if (ownerLink) {
            if (Auth.isOwner()) { ownerLink.style.display = ''; ownerLink.classList.remove('hidden'); }
            else { ownerLink.style.display = 'none'; ownerLink.classList.add('hidden'); }
        }

        // If the dropdown doesn't exist in inner pages, inject it
        if (userMenu && !document.getElementById('userDropdown')) {
            const dropdown = document.createElement('div');
            dropdown.id = 'userDropdown';
            dropdown.className = 'dropdown hidden';
            dropdown.innerHTML = `
                <a href="/bookings"><i data-lucide="calendar" class="icon-sm"></i> حجوزاتي</a>
                ${Auth.isOwner() ? '<a href="/owner"><i data-lucide="home" class="icon-sm"></i> لوحة المالك</a>' : ''}
                ${Auth.isAdmin() ? '<a href="/admin"><i data-lucide="shield" class="icon-sm"></i> لوحة الإدارة</a>' : ''}
                <hr>
                <button onclick="Auth.logout()"><i data-lucide="log-out" class="icon-sm"></i> تسجيل الخروج</button>
            `;
            userMenu.style.position = 'relative';
            userMenu.style.cursor = 'pointer';
            userMenu.appendChild(dropdown);
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } else {
        if (loginBtn) { loginBtn.style.display = ''; loginBtn.classList.remove('hidden'); }
        if (userMenu) { userMenu.style.display = 'none'; userMenu.classList.add('hidden'); }
    }
}

/**
 * Toggle user dropdown
 */
function toggleUserDropdown() {
    const dd = document.getElementById('userDropdown');
    if (dd) {
        dd.classList.toggle('hidden');
        dd.classList.toggle('show');
    }
}

// Close dropdown on outside click
document.addEventListener('click', e => {
    const dd = document.getElementById('userDropdown');
    const menu = document.getElementById('userMenu');
    if (dd && menu && !menu.contains(e.target)) {
        dd.classList.remove('show');
    }
});

// Check magic-link token from URL
(function checkMagicLink() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token && window.location.pathname === '/auth/verify') {
        Auth.verifyMagicLink(token).then(res => {
            if (res.access_token) {
                showToast('تم تسجيل الدخول بنجاح', 'success');
                window.location.href = '/';
            } else {
                showToast(res.error || 'Verification failed', 'error');
            }
        });
    }
})();

// Init auth UI on page load
document.addEventListener('DOMContentLoaded', updateAuthUI);

// Global logout function (called from onclick in HTML)
function logout() {
    Auth.logout();
}
