/**
 * HBnB V2 — Configuration
 */
const CONFIG = {
    API_URL: window.location.origin + '/api/v1',
    DEFAULT_LANG: 'ar',
    DEFAULT_COUNTRY: 'SA',
    CURRENCY: 'SAR',
    PRIVACY_RADIUS: 500,  // miles

    // Map defaults (Saudi Arabia center)
    MAP_CENTER: [24.7136, 46.6753],  // Riyadh
    MAP_ZOOM: 6,

    // Placeholder images
    PLACEHOLDER_IMAGE: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop',
    CITY_IMAGES: {
        'riyadh': 'https://images.unsplash.com/photo-1586724237569-f3d0c1dee8c6?w=400&h=500&fit=crop',
        'jeddah': 'https://images.unsplash.com/photo-1578895101408-1a36b834405b?w=400&h=500&fit=crop',
        'makkah': 'https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=400&h=500&fit=crop',
        'madinah': 'https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=400&h=500&fit=crop',
        'dammam': 'https://images.unsplash.com/photo-1578895101408-1a36b834405b?w=400&h=500&fit=crop',
        'abha': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=500&fit=crop',
        'taif': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=500&fit=crop',
        'tabuk': 'https://images.unsplash.com/photo-1682687982501-1e58ab814714?w=400&h=500&fit=crop',
    },

    // Property type icons
    TYPE_ICONS: {
        'apartments': '🏢',
        'chalets': '🏖️',
        'studios': '🎨',
        'rest_houses': '🏡',
        'resorts': '🏨',
        'villas': '🏛️',
        'farms': '🌳',
        'camps': '⛺',
        'hotels': '🏩',
        'hostels': '🛏️',
    },
};

/**
 * API Helper
 */
const api = {
    async get(endpoint, params = {}) {
        const url = new URL(CONFIG.API_URL + endpoint);
        Object.entries(params).forEach(([k, v]) => {
            if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v);
        });

        const headers = {};
        const token = localStorage.getItem('token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(url, { headers });
        if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
        return res.json();
    },

    async post(endpoint, data = {}) {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(CONFIG.API_URL + endpoint, {
            method: 'POST',
            headers,
            body: JSON.stringify(data),
        });
        const json = await res.json();
        if (!res.ok) throw { status: res.status, ...json };
        return json;
    },

    async put(endpoint, data = {}) {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(CONFIG.API_URL + endpoint, {
            method: 'PUT',
            headers,
            body: JSON.stringify(data),
        });
        const json = await res.json();
        if (!res.ok) throw { status: res.status, ...json };
        return json;
    },

    async delete(endpoint) {
        const headers = {};
        const token = localStorage.getItem('token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(CONFIG.API_URL + endpoint, {
            method: 'DELETE',
            headers,
        });
        if (!res.ok) throw new Error(`API ${res.status}`);
        return res.json();
    },

    async upload(endpoint, formData) {
        const headers = {};
        const token = localStorage.getItem('token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(CONFIG.API_URL + endpoint, {
            method: 'POST',
            headers,
            body: formData,
        });
        const json = await res.json();
        if (!res.ok) throw { status: res.status, ...json };
        return json;
    },
};

/**
 * Toast Notifications
 */
function showToast(message, type = 'info', duration = 3000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = { success: '✅', error: '❌', info: 'ℹ️' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${icons[type] || ''}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Theme Toggle
 */
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);

    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.setAttribute('data-lucide', next === 'dark' ? 'sun' : 'moon');
        lucide.createIcons();
    }
}

// Apply saved theme
(function () {
    const saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
})();

/**
 * Scroll effects
 */
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    const scrollTop = document.getElementById('scrollTop');
    const navSearch = document.getElementById('navSearch');

    if (navbar) {
        navbar.classList.toggle('scrolled', window.scrollY > 10);
    }
    if (scrollTop) {
        scrollTop.classList.toggle('hidden', window.scrollY < 400);
    }
    if (navSearch) {
        navSearch.classList.toggle('visible', window.scrollY > 400);
    }
});

/**
 * Format currency
 */
function formatPrice(amount, currency = 'SAR') {
    const lang = getLang();
    if (lang === 'ar') {
        return `${amount.toLocaleString('ar-SA')} ر.س`;
    }
    return `${currency} ${amount.toLocaleString('en-US')}`;
}

/**
 * Get current language
 */
function getLang() {
    return localStorage.getItem('lang') || CONFIG.DEFAULT_LANG;
}
