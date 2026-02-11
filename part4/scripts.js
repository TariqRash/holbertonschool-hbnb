/* ============================================
   HBnB Simple Web Client - Main JavaScript
   ============================================ */

// API base URL - change this to match your back-end server
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

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

// ==================== AUTHENTICATION ====================

/**
 * Check if user is authenticated and return the token
 * @returns {string|null} The JWT token or null
 */
function getToken() {
    return getCookie('token');
}

/**
 * Check authentication and toggle login link visibility
 */
function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
    }

    return token;
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
                alert(msg);
            }
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    } catch (error) {
        const msg = 'Network error. Please try again.';
        if (errorEl) {
            errorEl.textContent = msg;
            errorEl.style.display = 'block';
        } else {
            alert(msg);
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
        placesList.innerHTML = '<div class="empty-state"><p>No places found matching your criteria.</p></div>';
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

        card.innerHTML = `
            <h3>${escapeHTML(place.title)}</h3>
            <p class="price">$${Number(place.price).toFixed(2)} <span style="font-weight:400;font-size:0.85rem;color:#999">/ night</span></p>
            <p>${desc}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(card);
    });
}

/**
 * Filter displayed places by maximum price
 * @param {string} maxPrice - Maximum price value or "all"
 */
function filterPlacesByPrice(maxPrice) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    if (maxPrice === 'all') {
        displayPlaces(allPlaces);
        return;
    }

    const max = parseFloat(maxPrice);
    const filtered = allPlaces.filter(place => place.price <= max);
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
        amenitiesHTML = '<p style="color:#999;font-style:italic;">No amenities listed.</p>';
    }

    // Build owner info
    let ownerName = 'Unknown';
    if (place.owner) {
        ownerName = `${escapeHTML(place.owner.first_name)} ${escapeHTML(place.owner.last_name)}`;
    }

    detailsSection.innerHTML = `
        <div class="place-details">
            <h1>${escapeHTML(place.title)}</h1>
            <div class="place-info">
                <p><strong>🏠 Host:</strong> ${ownerName}</p>
                <p><strong>💰 Price:</strong> $${Number(place.price).toFixed(2)} / night</p>
                <p><strong>📍 Location:</strong> ${place.latitude}, ${place.longitude}</p>
            </div>
            <p class="description">${escapeHTML(place.description || 'No description available.')}</p>
            <h3>🛎️ Amenities</h3>
            ${amenitiesHTML}
        </div>
    `;

    // Display reviews
    displayReviews(place.reviews || []);
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
        alert('Review submitted successfully!');
        // Clear form
        document.getElementById('review').value = '';
        document.getElementById('rating').value = '';
        // Redirect back to the place page
        window.location.href = `place.html?id=${placeId}`;
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
        } else {
            alert(errorMsg);
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
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    // --- LOGIN PAGE ---
    if (currentPage === 'login.html') {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', handleLogin);
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
    }

    // --- PLACE DETAILS PAGE ---
    if (currentPage === 'place.html') {
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();

        if (!placeId) {
            document.getElementById('place-details').innerHTML =
                '<p class="error-message">No place ID provided.</p>';
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
    }
});
