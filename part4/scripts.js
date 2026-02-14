/* ============================================
   HBnB Simple Web Client - Main JavaScript
   ============================================ */

// API base URL - change this to match your back-end server
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ==================== DARK MODE ====================

/**
 * Get saved theme or default to 'light'
 */
function getSavedTheme() {
    return localStorage.getItem('hbnb-theme') || 'light';
}

/**
 * Apply the given theme to the page
 * @param {string} theme - 'light' or 'dark'
 */
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('hbnb-theme', theme);

    // Update toggle button icon
    const btn = document.getElementById('theme-toggle');
    if (btn) {
        btn.innerHTML = theme === 'dark'
            ? '<i data-lucide="sun"></i>'
            : '<i data-lucide="moon"></i>';
        // Re-render Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
    const current = getSavedTheme();
    const next = current === 'light' ? 'dark' : 'light';
    applyTheme(next);
}

/**
 * Initialize theme on page load
 */
function initTheme() {
    applyTheme(getSavedTheme());
}

// ==================== COOKIE HELPERS ====================

/**
 * Get a cookie value by its name
 * @param {string} name - The cookie name
 * @returns {string|null} The cookie value or null
 */
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

/**
 * Set a cookie
 * @param {string} name - The cookie name
 * @param {string} value - The cookie value
 * @param {number} days - Expiration in days (default: 1)
 */
function setCookie(name, value, days = 1) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + value + '; path=/; expires=' + expires;
}

// ==================== FAVORITES (localStorage) ====================

function getFavorites() {
    try { return JSON.parse(localStorage.getItem('hbnb-favorites')) || []; }
    catch (e) { return []; }
}

function saveFavorites(favs) {
    localStorage.setItem('hbnb-favorites', JSON.stringify(favs));
}

function isFavorite(placeId) {
    return getFavorites().includes(placeId);
}

function toggleFavorite(placeId) {
    let favs = getFavorites();
    if (favs.includes(placeId)) {
        favs = favs.filter(id => id !== placeId);
    } else {
        favs.push(placeId);
    }
    saveFavorites(favs);
    return favs.includes(placeId);
}

// ==================== AUTHENTICATION ====================

/**
 * Check if user is authenticated and return the token
 * @returns {string|null} The JWT token or null
 */
function getToken() {
    return getCookie('token');
}

/**
 * Check authentication and toggle login/logout link visibility
 */
function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');
    const logoutBtn = document.getElementById('logout-btn');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }
    if (logoutBtn) {
        logoutBtn.style.display = token ? 'inline-flex' : 'none';
    }

    return token;
}

/**
 * Log out by clearing the token cookie and redirecting
 */
function handleLogout() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    window.location.href = 'index.html';
}

// ==================== URL HELPERS ====================

/**
 * Extract the place ID from URL query parameters
 * @returns {string|null} The place ID or null
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// ==================== LOGIN PAGE ====================

/**
 * Handle the login form submission
 * @param {Event} event - The form submit event
 */
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('login-error');
    const submitBtn = event.target.querySelector('button[type="submit"]');

    // Loading state
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Signing in…';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Store the JWT token in a cookie
            document.cookie = `token=${data.access_token}; path=/`;
            // Redirect to the main page
            window.location.href = 'index.html';
        } else {
            const errData = await response.json().catch(() => null);
            const msg = errData && errData.error ? errData.error : 'Login failed. Please check your credentials.';
            if (errorEl) {
                errorEl.textContent = msg;
                errorEl.style.display = 'block';
            } else {
                showToast('error', t('toast.error'), msg);
            }
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    } catch (error) {
        const msg = t('login.error.network');
        if (errorEl) {
            errorEl.textContent = msg;
            errorEl.style.display = 'block';
        } else {
            showToast('error', t('toast.error'), msg);
        }
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}

// ==================== REGISTER PAGE ====================

/**
 * Toggle between login and register forms
 * @param {string} form - 'login' or 'register'
 */
function toggleAuthForm(form) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    if (!loginForm || !registerForm) return;

    if (form === 'register') {
        loginForm.style.display = 'none';
        registerForm.style.display = 'flex';
    } else {
        registerForm.style.display = 'none';
        loginForm.style.display = 'flex';
    }
}

/**
 * Handle the register form submission
 * @param {Event} event - The form submit event
 */
async function handleRegister(event) {
    event.preventDefault();

    const firstName = document.getElementById('reg-first-name').value.trim();
    const lastName = document.getElementById('reg-last-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value;
    const errorEl = document.getElementById('register-error');
    const submitBtn = event.target.querySelector('button[type="submit"]');

    // Loading state
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Creating account…';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password
            })
        });

        if (response.ok) {
            // Registration successful - auto login
            const loginRes = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (loginRes.ok) {
                const data = await loginRes.json();
                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = 'index.html';
            } else {
                // Registered but auto-login failed, switch to login form
                showToast('success', 'Success', 'Account created! Please sign in.');
                toggleAuthForm('login');
            }
        } else {
            const errData = await response.json().catch(() => null);
            const msg = errData && errData.error ? errData.error : 'Registration failed. Please try again.';
            if (errorEl) {
                errorEl.textContent = msg;
                errorEl.style.display = 'block';
            } else {
                showToast('error', t('toast.error'), msg);
            }
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    } catch (error) {
        const msg = 'Network error. Please check your connection.';
        if (errorEl) {
            errorEl.textContent = msg;
            errorEl.style.display = 'block';
        } else {
            showToast('error', t('toast.error'), msg);
        }
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}

// ==================== INDEX PAGE - PLACES LIST ====================

// Store places data globally so filtering can access it
let allPlaces = [];

/**
 * Fetch all places from the API
 * @param {string|null} token - JWT token (optional)
 */
async function fetchPlaces(token) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places;
            displayPlaces(places);
        } else {
            document.getElementById('places-list').innerHTML =
                '<p class="error-message">Failed to load places.</p>';
        }
    } catch (error) {
        document.getElementById('places-list').innerHTML =
            '<p class="error-message">Network error. Could not load places.</p>';
    }
}

/**
 * Display places as cards in the places-list section
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<div class="empty-state"><p>' + t('index.empty') + '</p></div>';
        return;
    }

    places.forEach((place, index) => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.style.animationDelay = `${index * 0.08}s`;

        const desc = place.description
            ? (place.description.length > 120 ? escapeHTML(place.description.slice(0, 120)) + '…' : escapeHTML(place.description))
            : 'No description available.';

        const priceStr = (typeof convertPrice === 'function')
            ? convertPrice(place.price)
            : '$' + Number(place.price).toFixed(2);

        const favClass = isFavorite(place.id) ? ' favorited' : '';

        card.innerHTML = `
            <button class="favorite-btn${favClass}" data-place-id="${place.id}" aria-label="Toggle favorite" onclick="handleFavoriteClick(event, this, '${place.id}')">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </button>
            <h3>${escapeHTML(place.title)}</h3>
            <p class="price">${priceStr} <span style="font-weight:400;font-size:0.85rem;color:#999">/ ${t('index.card.perNight')}</span></p>
            <p>${desc}</p>
            <a href="place.html?id=${place.id}" class="details-button">${t('index.card.viewDetails')}</a>
        `;

        placesList.appendChild(card);
    });
}

/**
 * Handle favorite button click
 */
function handleFavoriteClick(evt, btn, placeId) {
    if (evt) { evt.preventDefault(); evt.stopPropagation(); }
    const nowFav = toggleFavorite(placeId);
    if (nowFav) {
        btn.classList.add('favorited');
        if (typeof showToast === 'function') showToast('info', t('toast.info'), t('favorites.added'));
    } else {
        btn.classList.remove('favorited');
        if (typeof showToast === 'function') showToast('info', t('toast.info'), t('favorites.removed'));
    }
}

/**
 * Filter displayed places by maximum price and search query
 * @param {string} maxPrice - Maximum price value or "all"
 * @param {string} [searchQuery] - Optional text search
 */
function filterPlacesByPrice(maxPrice, searchQuery) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    let filtered = allPlaces;

    // Price filter
    if (maxPrice && maxPrice !== 'all') {
        const max = parseFloat(maxPrice);
        filtered = filtered.filter(place => place.price <= max);
    }

    // Search filter
    const query = searchQuery || (document.getElementById('search-input') ? document.getElementById('search-input').value : '');
    if (query && query.trim().length > 0) {
        const q = query.trim().toLowerCase();
        filtered = filtered.filter(place =>
            (place.title && place.title.toLowerCase().includes(q)) ||
            (place.description && place.description.toLowerCase().includes(q))
        );
    }

    displayPlaces(filtered);
}

// ==================== PLACE DETAILS PAGE ====================

/**
 * Fetch and display details for a specific place
 * @param {string|null} token - JWT token (optional)
 * @param {string} placeId - The place ID
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            document.getElementById('place-details').innerHTML =
                '<p class="error-message">Place not found.</p>';
        }
    } catch (error) {
        document.getElementById('place-details').innerHTML =
            '<p class="error-message">Network error. Could not load place details.</p>';
    }
}

/**
 * Display place details in the place-details section
 * @param {Object} place - The place data object
 */
function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    if (!detailsSection) return;

    // Build amenities list
    let amenitiesHTML = '';
    if (place.amenities && place.amenities.length > 0) {
        amenitiesHTML = `
            <div class="amenities-list">
                ${place.amenities.map(a => `<span class="amenity-tag">${escapeHTML(a.name)}</span>`).join('')}
            </div>
        `;
    } else {
        amenitiesHTML = '<p style="color:#999;font-style:italic;">' + t('place.noAmenities') + '</p>';
    }

    // Build owner info
    let ownerName = 'Unknown';
    if (place.owner) {
        ownerName = `${escapeHTML(place.owner.first_name)} ${escapeHTML(place.owner.last_name)}`;
    }

    // Price with currency conversion
    const priceStr = (typeof convertPrice === 'function')
        ? convertPrice(place.price)
        : '$' + Number(place.price).toFixed(2);

    detailsSection.innerHTML = `
        <button class="back-btn" onclick="history.back()">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
            ${t('place.back')}
        </button>
        <div class="place-details">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                <h1>${escapeHTML(place.title)}</h1>
                <button class="share-btn" onclick="sharePage()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                    ${t('place.share')}
                </button>
            </div>
            <div class="place-info">
                <p><strong>🏠 ${t('place.host')}</strong> ${ownerName}</p>
                <p><strong>💰 ${t('place.price')}</strong> ${priceStr} / ${t('index.card.perNight')}</p>
                <p><strong>📍 ${t('place.location')}</strong> ${place.latitude}, ${place.longitude}</p>
            </div>
            <p class="description">${escapeHTML(place.description || t('place.noDescription'))}</p>
            <h3>🛎️ ${t('place.amenities')}</h3>
            ${amenitiesHTML}
        </div>
    `;

    // Display reviews
    displayReviews(place.reviews || []);
}

/**
 * Share the current page URL
 */
function sharePage() {
    const url = window.location.href;
    if (navigator.share) {
        navigator.share({ title: document.title, url: url }).catch(() => {});
    } else if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
            if (typeof showToast === 'function') showToast('success', t('toast.success'), t('place.share.copied'));
        });
    }
}

/**
 * Display reviews in the reviews section
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    // Keep the heading, clear the rest
    reviewsSection.innerHTML = '<h2>Reviews</h2>';

    if (reviews.length === 0) {
        reviewsSection.innerHTML += '<p style="color:#999;font-style:italic;padding:1rem 0;">No reviews yet. Be the first to share your experience!</p>';
        return;
    }

    reviews.forEach((review, index) => {
        const card = document.createElement('div');
        card.className = 'review-card';
        card.style.animationDelay = `${index * 0.1}s`;

        // Build star rating display
        const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);

        card.innerHTML = `
            <p class="reviewer"><strong>${escapeHTML(review.user_name || 'Anonymous')}</strong></p>
            <p class="rating">${stars}</p>
            <p>${escapeHTML(review.text)}</p>
        `;

        reviewsSection.appendChild(card);
    });
}

// ==================== ADD REVIEW ====================

/**
 * Submit a review for a place
 * @param {string} token - JWT token
 * @param {string} placeId - The place ID
 * @param {string} reviewText - The review text
 * @param {number} rating - The rating value (1-5)
 */
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating)
            })
        });

        return response;
    } catch (error) {
        return null;
    }
}

/**
 * Handle the review form submission on the place details page
 * @param {Event} event - The form submit event
 * @param {string} token - JWT token
 * @param {string} placeId - The place ID
 */
async function handlePlaceReviewSubmit(event, token, placeId) {
    event.preventDefault();

    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;
    const messageEl = document.getElementById('review-message');
    const submitBtn = event.target.querySelector('button[type="submit"]');

    if (!rating) {
        if (messageEl) {
            messageEl.textContent = 'Please select a rating.';
            messageEl.className = 'error-message';
        }
        return;
    }

    // Loading state
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting…';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';

    const response = await submitReview(token, placeId, reviewText, rating);

    if (response && response.ok) {
        if (messageEl) {
            messageEl.textContent = 'Review submitted successfully!';
            messageEl.className = 'success-message';
        }
        // Clear form
        document.getElementById('review-text').value = '';
        document.getElementById('rating').value = '';
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        // Reload place details to show the new review
        setTimeout(() => {
            fetchPlaceDetails(token, placeId);
        }, 1000);
    } else {
        let errorMsg = 'Failed to submit review.';
        if (response) {
            const errData = await response.json().catch(() => null);
            if (errData && errData.error) {
                errorMsg = errData.error;
            }
        }
        if (messageEl) {
            messageEl.textContent = errorMsg;
            messageEl.className = 'error-message';
        }
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}

/**
 * Handle the review form submission on the add_review.html page
 * @param {Event} event - The form submit event
 * @param {string} token - JWT token
 * @param {string} placeId - The place ID
 */
async function handleAddReviewSubmit(event, token, placeId) {
    event.preventDefault();

    const reviewText = document.getElementById('review').value;
    const rating = document.getElementById('rating').value;
    const messageEl = document.getElementById('review-message');

    if (!rating) {
        if (messageEl) {
            messageEl.textContent = 'Please select a rating.';
            messageEl.className = 'error-message';
        }
        return;
    }

    const response = await submitReview(token, placeId, reviewText, rating);

    if (response && response.ok) {
        showToast('success', t('toast.success'), t('reviews.add.success'));
        // Clear form
        document.getElementById('review').value = '';
        document.getElementById('rating').value = '';
        // Redirect back to the place page
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 1200);
    } else {
        let errorMsg = t('reviews.add.error');
        if (response) {
            const errData = await response.json().catch(() => null);
            if (errData && errData.error) {
                errorMsg = errData.error;
            }
        }
        if (messageEl) {
            messageEl.textContent = errorMsg;
            messageEl.className = 'error-message';
        } else {
            showToast('error', t('toast.error'), errorMsg);
        }
    }
}

// ==================== UTILITY ====================

/**
 * Escape HTML to prevent XSS
 * @param {string} str - The string to escape
 * @returns {string} The escaped string
 */
function escapeHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ==================== PAGE INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize dark mode
    initTheme();

    // Initialize i18n
    if (typeof initI18n === 'function') {
        initI18n();
    }

    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Initialize currency converter
    if (typeof initCurrency === 'function') {
        initCurrency();
    }

    // Setup logout button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Create scroll-to-top button
    createScrollToTop();

    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    // --- LOGIN PAGE ---
    if (currentPage === 'login.html') {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', handleLogin);
        }
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', handleRegister);
        }
    }

    // --- INDEX PAGE ---
    if (currentPage === 'index.html' || currentPage === '') {
        const token = checkAuthentication();
        // Fetch places regardless of authentication (public endpoint)
        fetchPlaces(token);

        // Setup price filter
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                filterPlacesByPrice(event.target.value);
            });
        }

        // Setup search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                const priceVal = document.getElementById('price-filter') ? document.getElementById('price-filter').value : 'all';
                filterPlacesByPrice(priceVal, searchInput.value);
            });
        }

        // Currency change callback — re-render cards
        window.onCurrencyChange = function () {
            const priceVal = document.getElementById('price-filter') ? document.getElementById('price-filter').value : 'all';
            const searchVal = document.getElementById('search-input') ? document.getElementById('search-input').value : '';
            filterPlacesByPrice(priceVal, searchVal);
        };
    }

    // --- PLACE DETAILS PAGE ---
    if (currentPage === 'place.html') {
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();

        if (!placeId) {
            document.getElementById('place-details').innerHTML =
                '<p class="error-message">' + t('place.error.noId') + '</p>';
            return;
        }

        // Fetch place details (public endpoint, token optional)
        fetchPlaceDetails(token, placeId);

        // Show or hide the add review section
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) {
            if (!token) {
                addReviewSection.style.display = 'none';
            } else {
                addReviewSection.style.display = 'block';
            }
        }

        // Setup review form on place page
        const reviewForm = document.getElementById('review-form');
        if (reviewForm && token) {
            reviewForm.addEventListener('submit', (event) => {
                handlePlaceReviewSubmit(event, token, placeId);
            });
        }

        // Setup character counter for review textarea
        setupCharCounter('review-text', 1000);

        // Currency change callback — re-fetch to re-render
        window.onCurrencyChange = function () {
            fetchPlaceDetails(token, placeId);
        };
    }

    // --- ADD REVIEW PAGE ---
    if (currentPage === 'add_review.html') {
        const token = getToken();

        // Redirect to index if not authenticated
        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        const placeId = getPlaceIdFromURL();

        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', (event) => {
                handleAddReviewSubmit(event, token, placeId);
            });
        }

        // Setup character counter for review textarea
        setupCharCounter('review', 1000);
    }
});

// ==================== SCROLL TO TOP ====================

function createScrollToTop() {
    const btn = document.createElement('button');
    btn.className = 'scroll-to-top';
    btn.setAttribute('aria-label', 'Scroll to top');
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>';
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });
}

// ==================== CHARACTER COUNTER ====================

function setupCharCounter(textareaId, maxChars) {
    const textarea = document.getElementById(textareaId);
    if (!textarea) return;

    const counter = document.createElement('div');
    counter.className = 'char-counter';
    counter.textContent = '0 / ' + maxChars;
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);

    textarea.addEventListener('input', () => {
        const len = textarea.value.length;
        counter.textContent = len + ' / ' + maxChars;
        counter.classList.remove('warn', 'limit');
        if (len > maxChars * 0.9) counter.classList.add('warn');
        if (len >= maxChars) counter.classList.add('limit');
        if (len > maxChars) {
            textarea.value = textarea.value.slice(0, maxChars);
            counter.textContent = maxChars + ' / ' + maxChars;
        }
    });
}
