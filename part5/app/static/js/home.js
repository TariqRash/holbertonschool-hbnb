/**
 * HBnB V2 — Home Page Logic
 * Loads data and renders all home sections.
 */

let map = null;
let markers = [];

document.addEventListener('DOMContentLoaded', () => {
    applyTranslations();
    showSkeletons();
    loadHomeData();
    initMap();
    initSearchBox();
});

/* ─── SKELETON LOADING STATES ─── */
function showSkeletons() {
    // Cities skeleton
    const citiesGrid = document.getElementById('citiesGrid');
    if (citiesGrid) {
        citiesGrid.innerHTML = Array(6).fill('').map(() => `
            <div class="city-card skeleton-card">
                <div class="skeleton" style="width:100%;height:100%;border-radius:var(--radius-lg);"></div>
            </div>
        `).join('');
    }
    // Featured skeleton
    const featuredSlider = document.getElementById('featuredSlider');
    if (featuredSlider) {
        featuredSlider.innerHTML = Array(4).fill('').map(() => `
            <div class="place-card" style="min-width:300px;">
                <div class="skeleton" style="aspect-ratio:4/3;"></div>
                <div style="padding:16px;">
                    <div class="skeleton" style="height:1rem;width:70%;margin-bottom:8px;"></div>
                    <div class="skeleton" style="height:0.8rem;width:40%;"></div>
                </div>
            </div>
        `).join('');
    }
    // Types skeleton
    const typesGrid = document.getElementById('typesGrid');
    if (typesGrid) {
        typesGrid.innerHTML = Array(8).fill('').map(() => `
            <div class="type-card" style="pointer-events:none;">
                <div class="skeleton" style="width:48px;height:48px;border-radius:50%;margin:0 auto 8px;"></div>
                <div class="skeleton" style="height:0.8rem;width:60%;margin:0 auto;"></div>
            </div>
        `).join('');
    }
}

/* ─── LOAD ALL HOME DATA ─── */
async function loadHomeData() {
    const lang = getLang();
    try {
        const data = await api.get(`/home?lang=${lang}`);
        if (data) {
            renderCities(data.cities || []);
            renderFeatured(data.featured || []);
            renderPropertyTypes(data.property_types || []);
            renderBudget(data.budget_places || data.budget || []);
            renderMonthly(data.monthly_deals || data.monthly || []);
            if (data.average_price) {
                const el = document.getElementById('avgPrice');
                if (el) el.textContent = Math.round(data.average_price).toLocaleString('ar-SA');
            }
            loadMapMarkers();
        }
    } catch {
        // Fallback: load sections individually with error isolation
        await Promise.allSettled([
            loadCities(),
            loadFeatured(),
            loadPropertyTypes(),
            loadBudget(),
            loadMonthly(),
            loadMapMarkers(),
        ]);
    }
    // Reinitialize icons after all sections rendered
    if (typeof lucide !== 'undefined') lucide.createIcons();
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
        grid.innerHTML = `
            <div class="empty-state" style="grid-column:1/-1;text-align:center;padding:2rem;">
                <i data-lucide="map-pin-off" style="width:48px;height:48px;margin:0 auto 12px;display:block;opacity:0.3;"></i>
                <p style="color:var(--text-secondary);">لا توجد مدن متاحة حالياً</p>
            </div>`;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }

    const lang = getLang();
    grid.innerHTML = cities.map(c => {
        const name = lang === 'ar' ? c.name_ar : c.name_en;
        const image = c.image_url || c.image || CONFIG.CITY_IMAGES[c.name_en?.toLowerCase()] || CONFIG.PLACEHOLDER_IMAGE;
        return `
            <a href="/search?city=${c.id || ''}" class="city-card">
                <img src="${image}" 
                     alt="${name}" loading="lazy" class="city-card-bg">
                <div class="city-card-overlay"></div>
                <div class="city-card-content">
                    <h3 class="city-card-name">${name}</h3>
                    ${c.places_count ? `<span class="city-card-count">${c.places_count} عقار</span>` : ''}
                </div>
            </a>
        `;
    }).join('');
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
        grid.innerHTML = '<p style="text-align:center;color:var(--text-secondary);grid-column:1/-1;">لا توجد أنواع</p>';
        return;
    }

    const lang = getLang();
    grid.innerHTML = types.map(tp => {
        const iconName = tp.icon || CONFIG.TYPE_ICONS[tp.name_en?.toLowerCase()] || 'home';
        return `
            <a href="/search?type=${tp.id || ''}" class="type-card">
                <span class="type-card__icon"><i data-lucide="${iconName}"></i></span>
                <span class="type-card__name">${lang === 'ar' ? tp.name_ar : tp.name_en}</span>
            </a>
        `;
    }).join('');
    if (typeof lucide !== 'undefined') lucide.createIcons();
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
    const title = lang === 'ar' ? (place.title_ar || place.title_en || place.title) : (place.title_en || place.title_ar || place.title);
    const cityName = place.city
        ? (lang === 'ar' ? (place.city.name_ar || place.city.name_en || '') : (place.city.name_en || place.city.name_ar || ''))
        : '';
    const typeName = place.property_type
        ? (lang === 'ar' ? (place.property_type.name_ar || place.property_type.name_en || '') : (place.property_type.name_en || ''))
        : '';
    const image = place.image_url || place.cover_image || CONFIG.PLACEHOLDER_IMAGE;
    const price = showMonthly && place.monthly_price
        ? formatPrice(place.monthly_price)
        : formatPrice(place.price_per_night);
    const unit = showMonthly ? t('per_month') : t('per_night');
    const rating = place.average_rating ? place.average_rating.toFixed(1) : null;
    const reviewCount = place.review_count || 0;

    return `
        <a href="/place/${place.id}" class="place-card">
            <div class="place-card-image">
                <img src="${image}" alt="${title}" loading="lazy">
                ${place.is_featured ? '<span class="place-card-badge"><i data-lucide="crown" style="width:12px;height:12px;display:inline;"></i> Elite</span>' : ''}
                <button class="place-card-fav" onclick="event.preventDefault();event.stopPropagation();">
                    <i data-lucide="heart" style="width:18px;height:18px;"></i>
                </button>
            </div>
            <div class="place-card-body">
                ${cityName ? `<div class="place-card-location"><i data-lucide="map-pin" style="width:14px;height:14px;flex-shrink:0;"></i> ${cityName}</div>` : ''}
                <div class="place-card-title">${title}</div>
                <div class="place-card-info">
                    ${place.bedrooms ? `<span><i data-lucide="bed-double" style="width:14px;height:14px;"></i> ${place.bedrooms}</span>` : ''}
                    ${place.max_guests ? `<span><i data-lucide="users" style="width:14px;height:14px;"></i> ${place.max_guests}</span>` : ''}
                    ${typeName ? `<span>${typeName}</span>` : ''}
                </div>
            </div>
            <div class="place-card-footer">
                <span class="place-card-price">${price} <small>${unit}</small></span>
                <span class="place-card-rating">${rating ? `<span class="star">★</span> ${rating}` : '<span style="opacity:0.4;">جديد</span>'} ${reviewCount ? `<small>(${reviewCount})</small>` : ''}</span>
            </div>
        </a>
    `;
}

/* ─── MAP ─── */
function initMap() {
    const container = document.getElementById('homeMap');
    if (!container) return;

    const useGoogle = CONFIG.MAP_PROVIDER === 'google' && typeof google !== 'undefined' && google.maps;

    if (useGoogle) {
        map = new google.maps.Map(container, {
            center: { lat: CONFIG.MAP_CENTER[0], lng: CONFIG.MAP_CENTER[1] },
            zoom: CONFIG.MAP_ZOOM,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: false,
            styles: [
                { featureType: 'poi', stylers: [{ visibility: 'off' }] },
                { featureType: 'transit', stylers: [{ visibility: 'off' }] }
            ]
        });
        map._provider = 'google';
    } else if (typeof L !== 'undefined') {
        map = L.map('homeMap').setView(CONFIG.MAP_CENTER, CONFIG.MAP_ZOOM);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap',
            maxZoom: 18,
        }).addTo(map);
        map._provider = 'osm';
    }
}

async function loadMapMarkers() {
    if (!map) return;
    try {
        const res = await api.get('/maps/places');
        // API returns { markers: [...] }
        const data = res?.markers || (Array.isArray(res) ? res : []);
        if (!data.length) return;

        const isGoogle = map._provider === 'google';

        // Clear existing
        markers.forEach(m => {
            if (isGoogle) m.setMap(null);
            else map.removeLayer(m);
        });
        markers = [];

        const bounds = isGoogle ? new google.maps.LatLngBounds() : null;

        data.forEach(p => {
            if (!p.latitude || !p.longitude) return;
            const price = p.price_per_night || p.price || 0;

            if (isGoogle) {
                const marker = new google.maps.Marker({
                    position: { lat: p.latitude, lng: p.longitude },
                    map: map,
                    title: p.title || '',
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        fillColor: '#6C63FF',
                        fillOpacity: 0.9,
                        strokeColor: '#fff',
                        strokeWeight: 2,
                        scale: 8
                    }
                });
                const info = new google.maps.InfoWindow({
                    content: `<div style="font-family:Cairo,sans-serif;padding:4px;">
                        <strong>${p.title || ''}</strong><br>
                        <span style="color:#6C63FF;font-weight:700;">${formatPrice(price)}</span> ${t('per_night')}
                    </div>`
                });
                marker.addListener('click', () => info.open(map, marker));
                markers.push(marker);
                bounds.extend(marker.getPosition());
            } else {
                const marker = L.marker([p.latitude, p.longitude])
                    .addTo(map)
                    .bindPopup(`
                        <strong>${p.title || ''}</strong><br>
                        ${formatPrice(price)} ${t('per_night')}
                    `);
                markers.push(marker);
            }
        });

        // Fit bounds
        if (markers.length) {
            if (isGoogle) {
                map.fitBounds(bounds, { padding: 50 });
            } else {
                const group = L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.1));
            }
        }
    } catch (err) {
        console.warn('Map markers failed:', err);
    }
}

/* ─── SEARCH BOX ─── */
function initSearchBox() {
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    const ci = document.getElementById('searchCheckIn');
    const co = document.getElementById('searchCheckOut');
    if (ci) ci.min = today;
    if (co) co.min = today;
    if (ci) ci.addEventListener('change', () => { if (co) co.min = ci.value; });

    // Quick filter chips
    document.querySelectorAll('.filter-chip[data-filter]').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
        });
    });

    // City autocomplete
    initCityAutocomplete();
}

/* ─── CITY AUTOCOMPLETE ─── */
let acDebounce = null;

function initCityAutocomplete() {
    const input = document.getElementById('searchCityInput');
    const dropdown = document.getElementById('cityAutocomplete');
    const hidden = document.getElementById('searchCity');
    if (!input || !dropdown) return;

    input.addEventListener('input', () => {
        clearTimeout(acDebounce);
        const q = input.value.trim();
        if (q.length < 2) {
            dropdown.style.display = 'none';
            hidden.value = '';
            return;
        }
        acDebounce = setTimeout(() => searchCityAutocomplete(q), 300);
    });

    input.addEventListener('focus', () => {
        if (input.value.trim().length >= 2) {
            dropdown.style.display = 'block';
        }
    });

    document.addEventListener('click', e => {
        if (!e.target.closest('.search-field')) {
            dropdown.style.display = 'none';
        }
    });
}

async function searchCityAutocomplete(q) {
    const dropdown = document.getElementById('cityAutocomplete');
    const hidden = document.getElementById('searchCity');
    const lang = getLang();

    try {
        const results = await api.get(`/cities/search?q=${encodeURIComponent(q)}&lang=${lang}`);

        if (!results || !results.length) {
            dropdown.innerHTML = '<div class="ac-empty">لا توجد نتائج</div>';
            dropdown.style.display = 'block';
            return;
        }

        dropdown.innerHTML = results.map(c => `
            <div class="ac-item" data-id="${c.id || ''}" data-name="${c.name || c.description || ''}">
                <i data-lucide="map-pin"></i>
                <span>${c.name || c.description || ''}</span>
            </div>
        `).join('');

        dropdown.querySelectorAll('.ac-item').forEach(item => {
            item.addEventListener('click', () => {
                const input = document.getElementById('searchCityInput');
                input.value = item.dataset.name;
                hidden.value = item.dataset.id;
                dropdown.style.display = 'none';
            });
        });

        dropdown.style.display = 'block';
        lucide.createIcons();
    } catch (e) {
        dropdown.style.display = 'none';
    }
}

/* ─── QUICK FILTERS ─── */
function filterByType(type) {
    window.location.href = `/search?type=${type}`;
}

function filterByTrip(type) {
    window.location.href = `/search?trip_type=${type}`;
}

/* ─── HOME SEARCH ─── */
function doSearch() {
    const city = document.getElementById('searchCity')?.value || '';
    const cityInput = document.getElementById('searchCityInput')?.value || '';
    const checkIn = document.getElementById('searchCheckIn')?.value || '';
    const checkOut = document.getElementById('searchCheckOut')?.value || '';
    const guests = document.getElementById('searchGuests')?.value || '';

    const params = new URLSearchParams();
    if (city) params.set('city', city);
    else if (cityInput) params.set('q', cityInput);
    if (checkIn) params.set('check_in', checkIn);
    if (checkOut) params.set('check_out', checkOut);
    if (guests) params.set('guests', guests);

    // Check active filter chip
    const activeChip = document.querySelector('.filter-chip.active[data-filter]');
    if (activeChip && activeChip.dataset.filter !== 'all') {
        params.set('type', activeChip.dataset.filter);
    }

    window.location.href = `/search?${params.toString()}`;
}

/* ─── SCROLL TO TOP ─── */
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
