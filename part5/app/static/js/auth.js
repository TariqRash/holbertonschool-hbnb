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
                <a href="/favorites"><i data-lucide="heart" class="icon-sm"></i> المفضلة</a>
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

        // Check for missing profile info (only once per session)
        if (typeof checkOnboarding === 'function' && !window._onboardingChecked) {
            window._onboardingChecked = true;
            checkOnboarding();
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
        dd.classList.add('hidden');
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
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    // Auto-load favorites when Auth loads
    if (Auth.isLoggedIn()) loadFavorites();
});

// Global logout function (called from onclick in HTML)
function logout() {
    Auth.logout();
}

// Close dropdown on outside click
document.addEventListener('click', e => {
    const dd = document.getElementById('userDropdown');
    const menu = document.getElementById('userMenu');
    if (dd && menu && !menu.contains(e.target)) {
        dd.classList.remove('show');
        dd.classList.add('hidden');
    }
});

// Onboarding Logic
function injectOnboardingModal() {
    if (document.getElementById('onboardingModal')) return;
    const div = document.createElement('div');
    div.id = 'onboardingModal';
    div.className = 'modal';
    div.innerHTML = `
        <div class="modal__backdrop" onclick="dismissOnboarding()"></div>
        <div class="modal__content" style="max-width:400px;">
            <h2 style="margin-bottom:1rem;">إكمال الملف الشخصي</h2>
            <p style="color:var(--text-secondary);margin-bottom:1.5rem;">يرجى إكمال بياناتك للاستمرار</p>
            <div class="form-group">
                <label>الاسم الأول First Name</label>
                <input type="text" id="obFirstName" class="form-input" placeholder="أحمد / Ahmed">
            </div>
            <div class="form-group">
                <label>اسم العائلة Last Name</label>
                <input type="text" id="obLastName" class="form-input" placeholder="القحطاني / Al-Qahtani">
            </div>
            <div class="form-group">
                <label>رقم الجوال Mobile Number</label>
                <div style="display:flex;gap:8px;align-items:center;">
                    <span style="background:var(--bg-secondary);padding:10px 12px;border-radius:8px;font-size:0.9rem;white-space:nowrap;">🇸🇦 +966</span>
                    <input type="tel" id="obPhone" class="form-input" placeholder="5xxxxxxxx" dir="ltr" style="flex:1;">
                </div>
            </div>
            <div class="form-group">
                <label>الجنس Gender</label>
                <select id="obSex" class="form-input">
                    <option value="">اختر / Select</option>
                    <option value="male">ذكر — Male</option>
                    <option value="female">أنثى — Female</option>
                </select>
            </div>
            <button class="btn btn--primary btn--block" onclick="saveOnboarding()">حفظ / Save</button>
            <button class="btn btn--text btn--block" onclick="dismissOnboarding()" style="margin-top:0.5rem;font-size:0.85rem;">لاحقاً / Later</button>
        </div>
    `;
    document.body.appendChild(div);
}

async function checkOnboarding() {
    if (!Auth.isLoggedIn()) return;
    try {
        const res = await api.get('/auth/me');
        // Show onboarding if phone, sex, or proper name is missing
        const nameIsDefault = !res.first_name || res.first_name === res.email?.split('@')[0];
        if (res && (!res.phone || !res.sex || nameIsDefault)) {
            injectOnboardingModal();
            document.getElementById('onboardingModal').classList.add('show');
            document.getElementById('onboardingModal').style.display = 'flex';
            
            // Prefill existing values
            if (res.first_name && !nameIsDefault) document.getElementById('obFirstName').value = res.first_name;
            if (res.last_name) document.getElementById('obLastName').value = res.last_name;
            if (res.phone) {
                // Strip +966 or 0 prefix for display
                let ph = res.phone;
                if (ph.startsWith('+966')) ph = ph.slice(4);
                else if (ph.startsWith('00966')) ph = ph.slice(5);
                else if (ph.startsWith('0')) ph = ph.slice(1);
                document.getElementById('obPhone').value = ph;
            }
            if (res.sex) document.getElementById('obSex').value = res.sex;
        }
    } catch (e) { console.warn('Onboarding check failed', e); }
}

async function saveOnboarding() {
    const firstName = document.getElementById('obFirstName').value.trim();
    const lastName = document.getElementById('obLastName').value.trim();
    let phone = document.getElementById('obPhone').value.trim();
    const sex = document.getElementById('obSex').value;
    
    if (!firstName || !phone || !sex) return showToast('جميع الحقول مطلوبة (ما عدا اسم العائلة)', 'error');
    
    // Normalize phone: strip leading 0, prepend +966
    phone = phone.replace(/\s+/g, '');
    if (phone.startsWith('0')) phone = phone.slice(1);
    if (!phone.startsWith('+966') && !phone.startsWith('00966')) {
        phone = '+966' + phone;
    }
    
    // Basic Saudi phone validation: +9665xxxxxxxx (12 digits total)
    if (!/^\+9665\d{8}$/.test(phone)) {
        return showToast('رقم الجوال غير صحيح (5xxxxxxxx)', 'error');
    }

    try {
        const updateData = { first_name: firstName, phone, sex };
        if (lastName) updateData.last_name = lastName;
        const res = await api.put('/auth/me', updateData);
        if (res.error) throw res;
        
        showToast('تم تحديث البيانات', 'success');
        document.getElementById('onboardingModal').style.display = 'none';
        document.getElementById('onboardingModal').classList.remove('show');
        
        // Update local user cache (NOT Auth.login — that's an API call!)
        const currentUser = Auth.getUser();
        if (currentUser) {
            currentUser.first_name = firstName;
            if (lastName) currentUser.last_name = lastName;
            currentUser.phone = phone;
            currentUser.sex = sex;
            localStorage.setItem(Auth.USER_KEY, JSON.stringify(currentUser));
        }
        // If server returned updated user, prefer that
        if (res.user) {
            localStorage.setItem(Auth.USER_KEY, JSON.stringify(res.user));
        }
        // Refresh navbar with new name
        updateAuthUI();
    } catch (e) {
        showToast(e.error || 'فشل التحديث', 'error');
    }
}

function dismissOnboarding() {
    const m = document.getElementById('onboardingModal');
    if (m) { m.style.display = 'none'; m.classList.remove('show'); }
}

/* ═══════════════════ FAVORITES ═══════════════════ */
let favoriteIds = new Set();
let favoritesLoaded = false;

async function loadFavorites() {
    if (!Auth.isLoggedIn()) return;
    if (favoritesLoaded) return; // unnecessary call
    try {
        const res = await api.get('/users/favorites');
        if (res && res.favorites) {
            favoriteIds = new Set(res.favorites.map(p => p.id));
            favoritesLoaded = true;
            updateFavoriteIcons();
        }
    } catch (e) {
        console.warn('Failed to load favorites', e);
    }
}

function updateFavoriteIcons() {
    document.querySelectorAll('.place-card').forEach(card => {
        const href = card.getAttribute('href');
        if (!href) return;
        const id = href.split('/').pop();
        const btn = card.querySelector('.place-card-fav i');
        if (!btn) return;
        
        if (favoriteIds.has(id)) {
            btn.setAttribute('fill', 'currentColor');
            btn.style.color = '#e11d48';
        } else {
            btn.setAttribute('fill', 'none');
            btn.style.color = '';
        }
    });
}

window.toggleFavorite = async function(id, btn) {
    if (!Auth.isLoggedIn()) {
        showToast('سجل الدخول لإضافة للمفضلة', 'info');
        // window.location.href = '/login'; // Optional: Redirect or just toast
        return;
    }
    
    // Optimistic UI update
    const isFav = favoriteIds.has(id);
    const icon = btn.querySelector('i');
    
    if (isFav) {
        favoriteIds.delete(id);
        icon.setAttribute('fill', 'none');
        icon.style.color = '';
    } else {
        favoriteIds.add(id);
        icon.setAttribute('fill', 'currentColor');
        icon.style.color = '#e11d48';
    }

    try {
        const method = isFav ? 'DELETE' : 'POST';
        await api.request(method, `/users/favorites/${id}`);
        showToast(isFav ? 'تم الحذف من المفضلة' : 'تم الإضافة للمفضلة', 'success');
    } catch (e) {
        // Revert on error
        if (isFav) {
            favoriteIds.add(id);
            icon.setAttribute('fill', 'currentColor');
            icon.style.color = '#e11d48';
        } else {
            favoriteIds.delete(id);
            icon.setAttribute('fill', 'none');
            icon.style.color = '';
        }
        showToast('فشل تحديث المفضلة', 'error');
    }
};
