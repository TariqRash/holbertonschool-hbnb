/**
 * HBnB V2 — Configuration
 */
const CONFIG = {
    API_URL: window.location.origin + '/api/v1',
    DEFAULT_LANG: 'ar',
    DEFAULT_COUNTRY: 'SA',
    CURRENCY: 'SAR',
    PRIVACY_RADIUS: 500,  // miles

    // Google Maps
    GOOGLE_MAPS_API_KEY: 'AIzaSyDKXY_py-Ku0hm_EKZAYV5A86PTpzdNSSY',
    MAP_PROVIDER: 'google', // 'google' or 'osm'

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
    // Alias for backward compatibility (used in home.js, place.html, booking templates)
    get PLACEHOLDER_IMAGES() {
        return this.CITY_IMAGES;
    },

    // Property type icons (Lucide icon names)
    TYPE_ICONS: {
        'apartments': 'building-2',
        'chalets': 'house',
        'studios': 'square',
        'rest_houses': 'umbrella',
        'resorts': 'palm-tree',
        'villas': 'home',
        'farms': 'wheat',
        'camps': 'tent',
        'hotels': 'hotel',
        'hostels': 'bed',
    },
};

/**
 * API Helper — with retry, error handling, loading indicators
 */
const api = {
    _retries: 1,
    _timeout: 15000,

    async _fetch(url, options = {}, retries = api._retries) {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), api._timeout);
        options.signal = controller.signal;

        for (let attempt = 0; attempt <= retries; attempt++) {
            try {
                const res = await fetch(url, options);
                clearTimeout(timer);

                if (res.status === 401) {
                    // Token expired — clear and redirect
                    localStorage.removeItem('hbnb_token');
                    localStorage.removeItem('hbnb_user');
                    if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/admin')) {
                        window.location.href = '/login';
                    }
                    throw { status: 401, error: 'انتهت صلاحية الجلسة' };
                }

                if (!res.ok) {
                    const errData = await res.json().catch(() => ({}));
                    throw { status: res.status, ...errData };
                }

                return await res.json();
            } catch (e) {
                clearTimeout(timer);
                if (e.name === 'AbortError') {
                    if (attempt < retries) continue;
                    throw { error: 'انتهت مهلة الاتصال' };
                }
                if (attempt < retries && (!e.status || e.status >= 500)) {
                    await new Promise(r => setTimeout(r, 1000 * (attempt + 1)));
                    continue;
                }
                throw e;
            }
        }
    },

    async get(endpoint, params = {}) {
        const url = new URL(CONFIG.API_URL + endpoint);
        Object.entries(params).forEach(([k, v]) => {
            if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v);
        });

        const headers = {};
        const token = localStorage.getItem('hbnb_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        return api._fetch(url.toString(), { headers });
    },

    async post(endpoint, data = {}) {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('hbnb_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        return api._fetch(CONFIG.API_URL + endpoint, {
            method: 'POST',
            headers,
            body: JSON.stringify(data),
        });
    },

    async put(endpoint, data = {}) {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('hbnb_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        return api._fetch(CONFIG.API_URL + endpoint, {
            method: 'PUT',
            headers,
            body: JSON.stringify(data),
        });
    },

    async delete(endpoint) {
        const headers = {};
        const token = localStorage.getItem('hbnb_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        return api._fetch(CONFIG.API_URL + endpoint, {
            method: 'DELETE',
            headers,
        });
    },

    /** Generic request method — for dynamic HTTP methods (e.g. favorites toggle) */
    async request(method, endpoint, data = null) {
        const headers = {};
        const token = localStorage.getItem('hbnb_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;
        if (data) headers['Content-Type'] = 'application/json';

        const options = { method, headers };
        if (data) options.body = JSON.stringify(data);

        return api._fetch(CONFIG.API_URL + endpoint, options);
    },

    async upload(endpoint, formData) {
        const headers = {};
        const token = localStorage.getItem('hbnb_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        return api._fetch(CONFIG.API_URL + endpoint, {
            method: 'POST',
            headers,
            body: formData,
        }, 0); // no retry for uploads
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

    const iconNames = { success: 'check-circle', error: 'alert-circle', info: 'info' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i data-lucide="${iconNames[type] || 'info'}" style="width:18px;height:18px;"></i><span>${message}</span>`;
    container.appendChild(toast);
    if (typeof lucide !== 'undefined') lucide.createIcons();

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
    if (amount === null || amount === undefined || isNaN(amount)) amount = 0;
    const lang = getLang();
    if (lang === 'ar') {
        return `${Number(amount).toLocaleString('ar-SA')} ر.س`;
    }
    return `${currency} ${Number(amount).toLocaleString('en-US')}`;
}

/**
 * Get current language
 */
function getLang() {
    return localStorage.getItem('lang') || CONFIG.DEFAULT_LANG;
}

/**
 * Global image error handler — fallback to placeholder
 */
document.addEventListener('error', e => {
    if (e.target.tagName === 'IMG' && !e.target.dataset.fallback) {
        e.target.dataset.fallback = '1';
        e.target.src = CONFIG.PLACEHOLDER_IMAGE;
    }
}, true);

/**
 * Debounce utility
 */
function debounce(fn, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}