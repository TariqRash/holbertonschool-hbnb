/* ============================================
   HBnB Admin Panel - JavaScript
   Handles admin auth, dashboard stats, CRUD
   ============================================ */

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ==================== AUTH HELPERS ====================

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

function getAdminToken() {
    return getCookie('token');
}

/**
 * Decode JWT payload to check is_admin
 */
function decodeJWT(token) {
    try {
        const base64 = token.split('.')[1];
        const payload = atob(base64.replace(/-/g, '+').replace(/_/g, '/'));
        return JSON.parse(payload);
    } catch (e) {
        return null;
    }
}

/**
 * Ensure user is admin, redirect to admin login otherwise
 */
function requireAdmin() {
    const token = getAdminToken();
    if (!token) {
        window.location.href = 'login.html';
        return null;
    }

    const payload = decodeJWT(token);
    if (!payload || !payload.sub || !payload.is_admin) {
        window.location.href = 'login.html';
        return null;
    }

    return token;
}

/**
 * Logout admin
 */
function adminLogout() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC';
    window.location.href = 'login.html';
}

/**
 * Escape HTML
 */
function esc(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ==================== ADMIN LOGIN ====================

function initAdminLogin() {
    const form = document.getElementById('admin-login-form');
    if (!form) return;

    // If already admin, go to dashboard
    const token = getAdminToken();
    if (token) {
        const payload = decodeJWT(token);
        if (payload && payload.is_admin) {
            window.location.href = 'index.html';
            return;
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorEl = document.getElementById('login-error');
        const btn = form.querySelector('button[type="submit"]');

        btn.textContent = 'Signing in…';
        btn.disabled = true;

        try {
            const res = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (res.ok) {
                const data = await res.json();
                const payload = decodeJWT(data.access_token);

                if (!payload || !payload.is_admin) {
                    errorEl.textContent = 'Access denied. Admin account required.';
                    errorEl.style.display = 'block';
                    btn.textContent = 'Sign In';
                    btn.disabled = false;
                    return;
                }

                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = 'index.html';
            } else {
                errorEl.textContent = 'Invalid credentials. Please try again.';
                errorEl.style.display = 'block';
                btn.textContent = 'Sign In';
                btn.disabled = false;
            }
        } catch (err) {
            errorEl.textContent = 'Network error. Is the API server running?';
            errorEl.style.display = 'block';
            btn.textContent = 'Sign In';
            btn.disabled = false;
        }
    });
}

// ==================== DASHBOARD ====================

async function initDashboard() {
    const token = requireAdmin();
    if (!token) return;

    const headers = { 'Authorization': `Bearer ${token}` };

    try {
        // Fetch all data in parallel
        const [usersRes, placesRes, amenitiesRes] = await Promise.all([
            fetch(`${API_BASE_URL}/users/`, { headers }),
            fetch(`${API_BASE_URL}/places/`, { headers }),
            fetch(`${API_BASE_URL}/amenities/`, { headers })
        ]);

        const users = usersRes.ok ? await usersRes.json() : [];
        const places = placesRes.ok ? await placesRes.json() : [];
        const amenities = amenitiesRes.ok ? await amenitiesRes.json() : [];

        // Count reviews across all places
        let reviewCount = 0;
        places.forEach(p => {
            if (p.reviews) reviewCount += p.reviews.length;
        });

        // Update stats
        const su = document.getElementById('stat-users');
        const sp = document.getElementById('stat-places');
        const sr = document.getElementById('stat-reviews');
        const sa = document.getElementById('stat-amenities');
        if (su) su.textContent = users.length;
        if (sp) sp.textContent = places.length;
        if (sr) sr.textContent = reviewCount;
        if (sa) sa.textContent = amenities.length;

        // Recent users (last 5)
        const recentUsersEl = document.getElementById('recent-users');
        if (recentUsersEl) {
            if (users.length === 0) {
                recentUsersEl.innerHTML = '<tr><td colspan="3" class="admin-empty">No users found</td></tr>';
            } else {
                recentUsersEl.innerHTML = users.slice(0, 5).map(u => `
                    <tr>
                        <td>${esc(u.first_name)} ${esc(u.last_name)}</td>
                        <td>${esc(u.email)}</td>
                        <td><span class="badge ${u.is_admin ? 'badge-admin' : 'badge-user'}">${u.is_admin ? 'Admin' : 'User'}</span></td>
                    </tr>
                `).join('');
            }
        }

        // Recent places (last 5)
        const recentPlacesEl = document.getElementById('recent-places');
        if (recentPlacesEl) {
            if (places.length === 0) {
                recentPlacesEl.innerHTML = '<tr><td colspan="3" class="admin-empty">No places found</td></tr>';
            } else {
                recentPlacesEl.innerHTML = places.slice(0, 5).map(p => {
                    const ownerName = p.owner ? `${esc(p.owner.first_name)} ${esc(p.owner.last_name)}` : 'Unknown';
                    return `
                        <tr>
                            <td>${esc(p.title)}</td>
                            <td>$${Number(p.price).toFixed(2)}</td>
                            <td>${ownerName}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

    } catch (err) {
        console.error('Dashboard error:', err);
        if (typeof showToast === 'function') {
            showToast('error', 'Error', 'Failed to load dashboard data');
        }
    }
}

// ==================== USERS MANAGEMENT ====================

async function initUsersPage() {
    const token = requireAdmin();
    if (!token) return;

    await loadUsers(token);

    const form = document.getElementById('user-form');
    if (form) {
        form.addEventListener('submit', (e) => handleUserSubmit(e, token));
    }
}

async function loadUsers(token) {
    const tbody = document.getElementById('users-table');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE_URL}/users/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed to fetch users');
        const users = await res.json();

        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="admin-empty">No users found</td></tr>';
            return;
        }

        tbody.innerHTML = users.map(u => `
            <tr>
                <td>${esc(u.first_name)} ${esc(u.last_name)}</td>
                <td>${esc(u.email)}</td>
                <td><span class="badge ${u.is_admin ? 'badge-admin' : 'badge-user'}">${u.is_admin ? 'Admin' : 'User'}</span></td>
                <td class="actions">
                    <button class="btn-edit" onclick="editUser('${u.id}', '${esc(u.first_name)}', '${esc(u.last_name)}', '${esc(u.email)}')">
                        <i data-lucide="pencil" style="width:14px;height:14px;"></i> Edit
                    </button>
                </td>
            </tr>
        `).join('');

        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="4" class="admin-empty">Error loading users</td></tr>';
    }
}

function openUserModal(title) {
    document.getElementById('user-modal-title').textContent = title || 'Add User';
    document.getElementById('user-modal').classList.add('active');
}

function closeUserModal() {
    document.getElementById('user-modal').classList.remove('active');
    document.getElementById('user-form').reset();
    document.getElementById('user-id').value = '';
}

function editUser(id, firstName, lastName, email) {
    document.getElementById('user-id').value = id;
    document.getElementById('user-first-name').value = firstName;
    document.getElementById('user-last-name').value = lastName;
    document.getElementById('user-email').value = email;
    openUserModal('Edit User');
}

async function handleUserSubmit(e, token) {
    e.preventDefault();
    const userId = document.getElementById('user-id').value;
    const data = {
        first_name: document.getElementById('user-first-name').value,
        last_name: document.getElementById('user-last-name').value,
        email: document.getElementById('user-email').value
    };

    const password = document.getElementById('user-password').value;
    if (password) data.password = password;

    try {
        const url = userId ? `${API_BASE_URL}/users/${userId}` : `${API_BASE_URL}/users/`;
        const method = userId ? 'PUT' : 'POST';

        if (!userId) data.password = password || 'default123';

        const res = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showToast('success', 'Success', userId ? 'User updated successfully' : 'User created successfully');
            closeUserModal();
            await loadUsers(token);
        } else {
            const err = await res.json().catch(() => ({}));
            showToast('error', 'Error', err.error || err.message || 'Failed to save user');
        }
    } catch (err) {
        showToast('error', 'Error', 'Network error');
    }
}

// ==================== PLACES MANAGEMENT ====================

async function initPlacesPage() {
    const token = requireAdmin();
    if (!token) return;

    await loadPlaces(token);
}

async function loadPlaces(token) {
    const tbody = document.getElementById('places-table');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed');
        const places = await res.json();

        if (places.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="admin-empty">No places found</td></tr>';
            return;
        }

        tbody.innerHTML = places.map(p => {
            const owner = p.owner ? `${esc(p.owner.first_name)} ${esc(p.owner.last_name)}` : 'Unknown';
            const reviewCount = p.reviews ? p.reviews.length : 0;
            return `
                <tr>
                    <td>${esc(p.title)}</td>
                    <td>$${Number(p.price).toFixed(2)}</td>
                    <td>${owner}</td>
                    <td>${reviewCount}</td>
                    <td class="actions">
                        <a href="../place.html?id=${p.id}" class="btn-edit" target="_blank">
                            <i data-lucide="external-link" style="width:14px;height:14px;"></i> View
                        </a>
                        <button class="btn-delete" onclick="deletePlace('${p.id}')">
                            <i data-lucide="trash-2" style="width:14px;height:14px;"></i> Delete
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="5" class="admin-empty">Error loading places</td></tr>';
    }
}

async function deletePlace(placeId) {
    if (!confirm('Are you sure you want to delete this place?')) return;

    const token = getAdminToken();
    try {
        const res = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok || res.status === 204) {
            showToast('success', 'Deleted', 'Place deleted successfully');
            await loadPlaces(token);
        } else {
            showToast('error', 'Error', 'Failed to delete place');
        }
    } catch (err) {
        showToast('error', 'Error', 'Network error');
    }
}

// ==================== REVIEWS MANAGEMENT ====================

async function initReviewsPage() {
    const token = requireAdmin();
    if (!token) return;

    await loadReviews(token);
}

async function loadReviews(token) {
    const tbody = document.getElementById('reviews-table');
    if (!tbody) return;

    try {
        // Fetch all places to get reviews
        const res = await fetch(`${API_BASE_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed');
        const places = await res.json();

        // Collect all reviews with place info
        const allReviews = [];
        for (const place of places) {
            // Fetch each place details to get reviews
            const detailRes = await fetch(`${API_BASE_URL}/places/${place.id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (detailRes.ok) {
                const detail = await detailRes.json();
                if (detail.reviews) {
                    detail.reviews.forEach(r => {
                        allReviews.push({ ...r, place_title: detail.title, place_id: detail.id });
                    });
                }
            }
        }

        if (allReviews.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="admin-empty">No reviews found</td></tr>';
            return;
        }

        tbody.innerHTML = allReviews.map(r => {
            const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
            const text = r.text && r.text.length > 60 ? esc(r.text.slice(0, 60)) + '…' : esc(r.text);
            return `
                <tr>
                    <td>${esc(r.place_title)}</td>
                    <td>${esc(r.user_name || 'Unknown')}</td>
                    <td><span class="table-stars">${stars}</span></td>
                    <td>${text}</td>
                    <td class="actions">
                        <button class="btn-delete" onclick="deleteReview('${r.id}')">
                            <i data-lucide="trash-2" style="width:14px;height:14px;"></i> Delete
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="5" class="admin-empty">Error loading reviews</td></tr>';
    }
}

async function deleteReview(reviewId) {
    if (!confirm('Are you sure you want to delete this review?')) return;

    const token = getAdminToken();
    try {
        const res = await fetch(`${API_BASE_URL}/reviews/${reviewId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok || res.status === 204) {
            showToast('success', 'Deleted', 'Review deleted successfully');
            await loadReviews(token);
        } else {
            showToast('error', 'Error', 'Failed to delete review');
        }
    } catch (err) {
        showToast('error', 'Error', 'Network error');
    }
}

// ==================== AMENITIES MANAGEMENT ====================

async function initAmenitiesPage() {
    const token = requireAdmin();
    if (!token) return;

    await loadAmenities(token);

    const form = document.getElementById('amenity-form');
    if (form) {
        form.addEventListener('submit', (e) => handleAmenitySubmit(e, token));
    }
}

async function loadAmenities(token) {
    const tbody = document.getElementById('amenities-table');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE_URL}/amenities/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed');
        const amenities = await res.json();

        if (amenities.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="admin-empty">No amenities found</td></tr>';
            return;
        }

        tbody.innerHTML = amenities.map(a => `
            <tr>
                <td>${esc(a.name)}</td>
                <td style="font-size:0.8rem;color:var(--admin-text-muted);font-family:monospace;">${a.id}</td>
                <td class="actions">
                    <button class="btn-edit" onclick="editAmenity('${a.id}', '${esc(a.name)}')">
                        <i data-lucide="pencil" style="width:14px;height:14px;"></i> Edit
                    </button>
                    <button class="btn-delete" onclick="deleteAmenity('${a.id}')">
                        <i data-lucide="trash-2" style="width:14px;height:14px;"></i> Delete
                    </button>
                </td>
            </tr>
        `).join('');

        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="3" class="admin-empty">Error loading amenities</td></tr>';
    }
}

function openAmenityModal(title) {
    document.getElementById('amenity-modal-title').textContent = title || 'Add Amenity';
    document.getElementById('amenity-modal').classList.add('active');
}

function closeAmenityModal() {
    document.getElementById('amenity-modal').classList.remove('active');
    document.getElementById('amenity-form').reset();
    document.getElementById('amenity-id').value = '';
}

function editAmenity(id, name) {
    document.getElementById('amenity-id').value = id;
    document.getElementById('amenity-name').value = name;
    openAmenityModal('Edit Amenity');
}

async function handleAmenitySubmit(e, token) {
    e.preventDefault();
    const amenityId = document.getElementById('amenity-id').value;
    const data = { name: document.getElementById('amenity-name').value };

    try {
        const url = amenityId ? `${API_BASE_URL}/amenities/${amenityId}` : `${API_BASE_URL}/amenities/`;
        const method = amenityId ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        if (res.ok || res.status === 201) {
            showToast('success', 'Success', amenityId ? 'Amenity updated' : 'Amenity created');
            closeAmenityModal();
            await loadAmenities(token);
        } else {
            const err = await res.json().catch(() => ({}));
            showToast('error', 'Error', err.error || err.message || 'Failed to save amenity');
        }
    } catch (err) {
        showToast('error', 'Error', 'Network error');
    }
}

async function deleteAmenity(amenityId) {
    if (!confirm('Are you sure you want to delete this amenity?')) return;

    const token = getAdminToken();
    try {
        const res = await fetch(`${API_BASE_URL}/amenities/${amenityId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok || res.status === 204) {
            showToast('success', 'Deleted', 'Amenity deleted');
            await loadAmenities(token);
        } else {
            showToast('error', 'Error', 'Failed to delete amenity');
        }
    } catch (err) {
        showToast('error', 'Error', 'Network error');
    }
}

// ==================== PAGE INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const page = window.location.pathname.split('/').pop() || 'index.html';

    switch (page) {
        case 'login.html':
            initAdminLogin();
            break;
        case 'index.html':
        case '':
            initDashboard();
            break;
        case 'users.html':
            initUsersPage();
            break;
        case 'places.html':
            initPlacesPage();
            break;
        case 'reviews.html':
            initReviewsPage();
            break;
        case 'amenities.html':
            initAmenitiesPage();
            break;
    }
});
