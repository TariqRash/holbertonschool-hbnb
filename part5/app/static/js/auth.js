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
 */
function updateAuthUI() {
    const loginBtn = document.getElementById('loginBtn');
    const userMenu = document.getElementById('userMenu');
    const userAvatar = document.getElementById('userAvatar');
    const userName = document.getElementById('userName');

    if (Auth.isLoggedIn()) {
        const user = Auth.getUser();
        if (loginBtn) loginBtn.style.display = 'none';
        if (userMenu) userMenu.style.display = 'flex';
        if (userName) userName.textContent = user?.first_name || 'User';
        if (userAvatar && user?.avatar_url) {
            userAvatar.src = user.avatar_url;
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'flex';
        if (userMenu) userMenu.style.display = 'none';
    }
}

/**
 * Toggle user dropdown
 */
function toggleUserDropdown() {
    const dd = document.getElementById('userDropdown');
    if (dd) dd.classList.toggle('show');
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
