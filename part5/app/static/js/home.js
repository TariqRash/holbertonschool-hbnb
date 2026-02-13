/**
 * HBnB V2 — Home Page Logic
 * Loads data and renders all home sections.
 */

let map = null;
let markers = [];

document.addEventListener('DOMContentLoaded', () => {
    applyTranslations();
    loadHomeData();
    initMap();
    initSearchBox();
});

/* ─── LOAD ALL HOME DATA ─── */
async function loadHomeData() {
    const lang = getLang();
    try {
        const data = await api.get(`/home?lang=${lang}`);
        if (data) {
            renderCities(data.cities || []);
            renderFeatured(data.featured || []);
            renderPropertyTypes(data.property_types || []);
            renderBudget(data.budget || []);
            renderMonthly(data.monthly || []);
            loadMapMarkers();
        }
    } catch {
        // Fallback: load sections individually
        loadCities();
        loadFeatured();
        loadPropertyTypes();
        loadBudget();
        loadMonthly();
        loadMapMarkers();
    }
}

/* ─── CITIES SECTION ─── */
async function loadCities() {
    const data = await api.get('/cities?featured=true');
    if (data) renderCities(data);
}

function renderCities(cities) {
    const grid = document.getElementById('citiesGrid');
    if (!grid) return;

    if (!cities.length) {
        // Show placeholder Saudi cities
        const placeholders = [
            { name_ar: 'الرياض', name_en: 'Riyadh', image: CONFIG.PLACEHOLDER_IMAGES.riyadh },
            { name_ar: 'جدة', name_en: 'Jeddah', image: CONFIG.PLACEHOLDER_IMAGES.jeddah },
            { name_ar: 'مكة', name_en: 'Makkah', image: CONFIG.PLACEHOLDER_IMAGES.makkah },
            { name_ar: 'المدينة', name_en: 'Madinah', image: CONFIG.PLACEHOLDER_IMAGES.madinah },
            { name_ar: 'الدمام', name_en: 'Dammam', image: CONFIG.PLACEHOLDER_IMAGES.dammam },
            { name_ar: 'أبها', name_en: 'Abha', image: CONFIG.PLACEHOLDER_IMAGES.abha },
        ];
        cities = placeholders;
    }

    const lang = getLang();
    grid.innerHTML = cities.map(c => `
        <a href="/search?city=${c.id || ''}" class="city-card">
            <img src="${c.image_url || c.image || CONFIG.PLACEHOLDER_IMAGES.riyadh}" 
                 alt="${lang === 'ar' ? c.name_ar : c.name_en}" loading="lazy">
            <div class="city-card__overlay">
                <h3>${lang === 'ar' ? c.name_ar : c.name_en}</h3>
                ${c.places_count ? `<span>${c.places_count} ${t('property_types')}</span>` : ''}
            </div>
        </a>
    `).join('');
}

/* ─── FEATURED / ELITE PLACES ─── */
async function loadFeatured() {
    const data = await api.get('/places/featured');
    if (data) renderFeatured(data);
}

function renderFeatured(places) {
    const slider = document.getElementById('featuredSlider');
    if (!slider) return;
    slider.innerHTML = places.map(p => createPlaceCard(p)).join('');
}

/* ─── PROPERTY TYPES ─── */
async function loadPropertyTypes() {
    const data = await api.get('/property-types');
    if (data) renderPropertyTypes(data);
}

function renderPropertyTypes(types) {
    const grid = document.getElementById('typesGrid');
    if (!grid) return;

    if (!types.length) {
        const defaults = [
            { name_ar: 'شقق', name_en: 'Apartments', icon: '🏢' },
            { name_ar: 'شاليهات', name_en: 'Chalets', icon: '🏠' },
            { name_ar: 'استديوهات', name_en: 'Studios', icon: '🏬' },
            { name_ar: 'استراحات', name_en: 'Retreats', icon: '⛱️' },
            { name_ar: 'منتجعات', name_en: 'Resorts', icon: '🏖️' },
            { name_ar: 'فلل', name_en: 'Villas', icon: '🏡' },
            { name_ar: 'مزارع', name_en: 'Farms', icon: '🌾' },
            { name_ar: 'مخيمات', name_en: 'Camps', icon: '⛺' },
        ];
        types = defaults;
    }

    const lang = getLang();
    grid.innerHTML = types.map(tp => `
        <a href="/search?type=${tp.id || ''}" class="type-card">
            <span class="type-card__icon">${tp.icon || CONFIG.PROPERTY_TYPE_ICONS[tp.name_en?.toLowerCase()] || '🏠'}</span>
            <span class="type-card__name">${lang === 'ar' ? tp.name_ar : tp.name_en}</span>
        </a>
    `).join('');
}

/* ─── BUDGET FRIENDLY ─── */
async function loadBudget() {
    const data = await api.get('/places/budget');
    if (data) renderBudget(data);
}

function renderBudget(places) {
    const grid = document.getElementById('budgetGrid');
    if (!grid) return;
    grid.innerHTML = places.map(p => createPlaceCard(p)).join('');
}

/* ─── MONTHLY STAYS ─── */
async function loadMonthly() {
    const data = await api.get('/places/monthly');
    if (data) renderMonthly(data);
}

function renderMonthly(places) {
    const grid = document.getElementById('monthlyGrid');
    if (!grid) return;
    grid.innerHTML = places.map(p => {
        const card = createPlaceCard(p, true);
        return card;
    }).join('');
}

/* ─── PLACE CARD GENERATOR ─── */
function createPlaceCard(place, showMonthly = false) {
    const lang = getLang();
    const title = lang === 'ar' ? (place.title_ar || place.title_en) : (place.title_en || place.title_ar);
    const city = lang === 'ar' ? (place.city_name_ar || place.city_name_en || '') : (place.city_name_en || place.city_name_ar || '');
    const image = place.cover_image || place.image_url || CONFIG.PLACEHOLDER_IMAGES.riyadh;
    const price = showMonthly && place.monthly_price
        ? formatPrice(place.monthly_price)
        : formatPrice(place.price_per_night);
    const unit = showMonthly ? t('per_month') : t('per_night');
    const rating = place.average_rating ? place.average_rating.toFixed(1) : '—';

    return `
        <a href="/place/${place.id}" class="place-card">
            <div class="place-card__image">
                <img src="${image}" alt="${title}" loading="lazy">
                ${place.is_featured ? '<span class="place-card__badge">⭐ Elite</span>' : ''}
                <button class="place-card__fav" onclick="event.preventDefault();">
                    <i data-lucide="heart"></i>
                </button>
            </div>
            <div class="place-card__body">
                <div class="place-card__title">${title}</div>
                <div class="place-card__city">${city}</div>
            </div>
            <div class="place-card__footer">
                <span class="place-card__price">${price} <small>${unit}</small></span>
                <span class="place-card__rating">★ ${rating}</span>
            </div>
        </a>
    `;
}

/* ─── MAP ─── */
function initMap() {
    const container = document.getElementById('homeMap');
    if (!container || typeof L === 'undefined') return;

    map = L.map('homeMap').setView(CONFIG.MAP_CENTER, 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
        maxZoom: 18,
    }).addTo(map);
}

async function loadMapMarkers() {
    if (!map) return;
    try {
        const data = await api.get('/maps/places');
        if (!data || !data.length) return;

        // Clear existing
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        data.forEach(p => {
            if (!p.latitude || !p.longitude) return;
            const marker = L.marker([p.latitude, p.longitude])
                .addTo(map)
                .bindPopup(`
                    <strong>${p.title || ''}</strong><br>
                    ${formatPrice(p.price_per_night)} ${t('per_night')}
                `);
            markers.push(marker);
        });

        // Fit map to markers
        if (markers.length) {
            const group = L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        }
    } catch (err) {
        console.warn('Map markers failed:', err);
    }
}

/* ─── SEARCH BOX ─── */
function initSearchBox() {
    const form = document.getElementById('heroSearchForm');
    if (!form) return;

    form.addEventListener('submit', e => {
        e.preventDefault();
        const city = document.getElementById('searchCity')?.value || '';
        const checkIn = document.getElementById('searchCheckIn')?.value || '';
        const checkOut = document.getElementById('searchCheckOut')?.value || '';
        const guests = document.getElementById('searchGuests')?.value || '';

        const params = new URLSearchParams();
        if (city) params.set('city', city);
        if (checkIn) params.set('check_in', checkIn);
        if (checkOut) params.set('check_out', checkOut);
        if (guests) params.set('guests', guests);

        window.location.href = `/search?${params.toString()}`;
    });

    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    const ci = document.getElementById('searchCheckIn');
    const co = document.getElementById('searchCheckOut');
    if (ci) ci.min = today;
    if (co) co.min = today;
    if (ci) ci.addEventListener('change', () => { if (co) co.min = ci.value; });
}

/* ─── QUICK FILTERS ─── */
function filterByType(type) {
    window.location.href = `/search?type=${type}`;
}

/* ─── SCROLL TO TOP ─── */
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
