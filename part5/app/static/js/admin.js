/**
 * Rizi Admin Panel — JavaScript
 * Full CRUD operations for all entities.
 */

/* ─── Initialization ─── */
document.addEventListener('DOMContentLoaded', () => {
    if (!Auth.isLoggedIn()) {
        // Show inline admin login form instead of redirecting
        document.getElementById('adminLoginOverlay').style.display = 'flex';
        document.getElementById('sidebar').style.display = 'none';
        document.getElementById('adminMain').style.display = 'none';
        document.getElementById('adminEmail')?.focus();
        return;
    }

    const user = Auth.getUser();
    if (!user || user.role !== 'admin') {
        showToast('صلاحية المدير مطلوبة', 'error');
        document.getElementById('adminLoginOverlay').style.display = 'flex';
        document.getElementById('sidebar').style.display = 'none';
        document.getElementById('adminMain').style.display = 'none';
        Auth.clear();
        return;
    }

    document.getElementById('adminName').textContent = user.first_name || user.email;
    loadDashboard();
});

/* ─── Debounce Utility ─── */
function debounce(fn, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

/* ─── Section Navigation ─── */
const sectionTitles = {
    dashboard: 'لوحة التحكم',
    users: 'المستخدمون',
    places: 'الوحدات السكنية',
    bookings: 'الحجوزات',
    reviews: 'التقييمات',
    amenities: 'المرافق',
    cities: 'المدن',
    types: 'أنواع الوحدات',
    settings: 'الإعدادات',
};

function showSection(name, btn) {
    document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));

    const section = document.getElementById('section' + name.charAt(0).toUpperCase() + name.slice(1));
    if (section) section.classList.add('active');
    if (btn) btn.classList.add('active');

    document.getElementById('sectionTitle').textContent = sectionTitles[name] || name;

    // Load data for section
    const loaders = {
        dashboard: loadDashboard,
        users: loadUsers,
        places: loadPlaces,
        bookings: loadBookings,
        reviews: loadReviews,
        amenities: loadAmenities,
        cities: loadCities,
        types: loadTypes,
        settings: loadSettings,
    };
    if (loaders[name]) loaders[name]();

    // Close sidebar on mobile
    document.getElementById('sidebar')?.classList.remove('open');
}

function toggleSidebar() {
    document.getElementById('sidebar')?.classList.toggle('open');
}

/* ─── Modal Helpers ─── */
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('show');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

function closeModal(id) {
    document.getElementById(id)?.classList.remove('show');
}

// Close modals on ESC
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.show').forEach(m => m.classList.remove('show'));
    }
});

/* ─── Theme Toggle ─── */
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

(function () {
    const saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
})();

/* ═══════════════════════════════════════════════════
   DASHBOARD
   ═══════════════════════════════════════════════════ */
async function loadDashboard() {
    try {
        const data = await api.get('/admin/dashboard');
        document.getElementById('dUsers').textContent = data.users || 0;
        document.getElementById('dPlaces').textContent = data.places || 0;
        document.getElementById('dBookings').textContent = data.bookings || 0;
        document.getElementById('dReviews').textContent = data.reviews || 0;
        document.getElementById('dPending').textContent = data.pending_bookings || 0;
        document.getElementById('dRevenue').textContent = (data.total_revenue || 0).toLocaleString('ar-SA');
    } catch (e) {
        console.error('Dashboard load error:', e);
    }
}

/* ═══════════════════════════════════════════════════
   USERS
   ═══════════════════════════════════════════════════ */
let usersPage = 1;

async function loadUsers(page = 1) {
    usersPage = page;
    const search = document.getElementById('userSearch')?.value || '';
    const role = document.getElementById('userRoleFilter')?.value || '';

    try {
        const data = await api.get('/admin/users', { search, role, page, per_page: 20 });
        const tbody = document.getElementById('usersBody');
        tbody.innerHTML = (data.users || []).map(u => `
            <tr>
                <td>${u.first_name || ''} ${u.last_name || ''}</td>
                <td>${u.email}</td>
                <td><span class="badge badge--${u.role}">${u.role}</span></td>
                <td><span class="badge badge--${u.is_active ? 'active' : 'inactive'}">${u.is_active ? 'نشط' : 'معطل'}</span></td>
                <td>${u.created_at ? new Date(u.created_at).toLocaleDateString('ar-SA') : ''}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--edit" onclick='editUser(${JSON.stringify(u)})'><i data-lucide="pencil"></i></button>
                        <button class="action-btn action-btn--delete" onclick="deleteUser('${u.id}')"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="6" style="text-align:center;padding:40px;">لا يوجد مستخدمون</td></tr>';

        renderPagination('usersPagination', data.pages, data.page, loadUsers);
        lucide.createIcons();
    } catch (e) {
        console.error('Users load error:', e);
    }
}

function editUser(u) {
    document.getElementById('editUserId').value = u.id;
    document.getElementById('userModalTitle').textContent = 'تعديل مستخدم';
    document.getElementById('uFirstName').value = u.first_name || '';
    document.getElementById('uLastName').value = u.last_name || '';
    document.getElementById('uEmail').value = u.email || '';
    document.getElementById('uPhone').value = u.phone || '';
    document.getElementById('uPassword').value = '';
    document.getElementById('uRole').value = u.role || 'guest';
    openModal('userModal');
}

async function saveUser() {
    const id = document.getElementById('editUserId').value;
    const data = {
        first_name: document.getElementById('uFirstName').value,
        last_name: document.getElementById('uLastName').value,
        email: document.getElementById('uEmail').value,
        phone: document.getElementById('uPhone').value || null,
        role: document.getElementById('uRole').value,
    };
    const password = document.getElementById('uPassword').value;
    if (password) data.password = password;

    try {
        if (id) {
            await api.put(`/admin/users/${id}`, data);
            showToast('تم تحديث المستخدم', 'success');
        } else {
            if (!data.email) return showToast('البريد مطلوب', 'error');
            await api.post('/admin/users', data);
            showToast('تم إنشاء المستخدم', 'success');
        }
        closeModal('userModal');
        document.getElementById('editUserId').value = '';
        document.getElementById('userModalTitle').textContent = 'إضافة مستخدم';
        loadUsers(usersPage);
    } catch (e) {
        showToast(e.error || 'حدث خطأ', 'error');
    }
}

async function deleteUser(id) {
    if (!confirm('هل تريد تعطيل هذا المستخدم?')) return;
    try {
        await api.delete(`/admin/users/${id}`);
        showToast('تم تعطيل المستخدم', 'success');
        loadUsers(usersPage);
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   PLACES
   ═══════════════════════════════════════════════════ */
let placesPage = 1;

async function loadPlaces(page = 1) {
    placesPage = page;
    const search = document.getElementById('placeSearch')?.value || '';

    try {
        const data = await api.get('/admin/places', { search, page, per_page: 20 });
        const tbody = document.getElementById('placesBody');
        tbody.innerHTML = (data.places || []).map(p => `
            <tr>
                <td>${p.title_ar || p.title_en || ''}</td>
                <td>${p.city_name_ar || p.city_name_en || ''}</td>
                <td>${p.price_per_night || 0} ر.س</td>
                <td>${p.property_type || ''}</td>
                <td>${p.is_featured ? '<i data-lucide="check" style="color:#16a34a;width:16px;height:16px;"></i>' : '<i data-lucide="x" style="color:#aaa;width:16px;height:16px;"></i>'}</td>
                <td>${p.is_active !== false ? '<span class="badge badge--active">نشط</span>' : '<span class="badge badge--inactive">معطل</span>'}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--edit" title="تعديل" onclick="editPlace('${p.id}')"><i data-lucide="pencil"></i></button>
                        <button class="action-btn action-btn--edit" onclick="togglePlaceFeatured('${p.id}', ${!p.is_featured})" title="${p.is_featured ? 'إلغاء التمييز' : 'تمييز'}"><i data-lucide="${p.is_featured ? 'star-off' : 'star'}"></i></button>
                        <button class="action-btn action-btn--delete" onclick="deletePlace('${p.id}')" title="تعطيل"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="7" style="text-align:center;padding:40px;">لا يوجد عقارات</td></tr>';

        renderPagination('placesPagination', data.pages, data.page, loadPlaces);
        lucide.createIcons();
    } catch (e) {
        console.error('Places load error:', e);
    }
}

async function togglePlaceFeatured(id, featured) {
    try {
        await api.put(`/admin/places/${id}`, { is_featured: featured });
        showToast(featured ? 'تم تمييز العقار' : 'تم إلغاء التمييز', 'success');
        loadPlaces(placesPage);
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

async function deletePlace(id) {
    if (!confirm('هل تريد تعطيل هذا العقار?')) return;
    try {
        await api.delete(`/admin/places/${id}`);
        showToast('تم تعطيل العقار', 'success');
        loadPlaces(placesPage);
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

let placeDropdownsLoaded = false;

async function loadPlaceDropdowns() {
    if (placeDropdownsLoaded) return;
    try {
        const [cities, types] = await Promise.all([
            api.get('/cities'),
            api.get('/property-types')
        ]);
        const citySelect = document.getElementById('pCityId');
        const typeSelect = document.getElementById('pTypeId');
        citySelect.innerHTML = '<option value="">اختر المدينة</option>' +
            (cities || []).map(c => `<option value="${c.id}">${c.name_ar || c.name_en}</option>`).join('');
        typeSelect.innerHTML = '<option value="">اختر النوع</option>' +
            (types || []).map(t => `<option value="${t.id}">${t.name_ar || t.name_en}</option>`).join('');
        placeDropdownsLoaded = true;
    } catch (e) {
        console.error('Failed to load place dropdowns:', e);
    }
}

async function editPlace(id) {
    await loadPlaceDropdowns();
    try {
        const p = await api.get(`/admin/places/${id}`);
        if (!p) return showToast('عقار غير موجود', 'error');

        document.getElementById('editPlaceId').value = p.id;
        document.getElementById('placeModalTitle').textContent = 'تعديل العقار';
        document.getElementById('pTitleAr').value = p.title_ar || '';
        document.getElementById('pTitleEn').value = p.title_en || '';
        document.getElementById('pDescAr').value = p.description_ar || p.description || '';
        document.getElementById('pDescEn').value = p.description_en || (p.description && getLang() === 'en' ? p.description : '') || '';
        document.getElementById('pPrice').value = p.price_per_night || '';
        document.getElementById('pMonthlyDiscount').value = p.monthly_discount || '';
        document.getElementById('pCityId').value = p.city_id || (p.city?.id) || '';
        document.getElementById('pTypeId').value = p.property_type_id || (p.property_type?.id) || '';
        document.getElementById('pBedrooms').value = p.bedrooms ?? '';
        document.getElementById('pBathrooms').value = p.bathrooms ?? '';
        document.getElementById('pBeds').value = p.beds ?? '';
        document.getElementById('pMaxGuests').value = p.max_guests ?? '';
        document.getElementById('pTripType').value = p.trip_type || 'both';
        document.getElementById('pAddress').value = p.address || '';
        document.getElementById('pLatitude').value = p.latitude ?? '';
        document.getElementById('pLongitude').value = p.longitude ?? '';
        document.getElementById('pCheckInTime').value = p.check_in_time || '';
        document.getElementById('pCheckOutTime').value = p.check_out_time || '';
        document.getElementById('pIsActive').checked = p.is_active !== false;
        document.getElementById('pIsFeatured').checked = !!p.is_featured;
        document.getElementById('pInstantBook').checked = !!(p.instant_book || p.is_instant_book);

        openModal('placeModal');
    } catch (e) {
        showToast('فشل تحميل بيانات العقار', 'error');
    }
}

async function savePlace() {
    const id = document.getElementById('editPlaceId').value;
    if (!id) return showToast('لا يوجد عقار للتعديل', 'error');

    const data = {
        title_ar: document.getElementById('pTitleAr').value,
        title_en: document.getElementById('pTitleEn').value,
        description_ar: document.getElementById('pDescAr').value,
        description_en: document.getElementById('pDescEn').value,
        price_per_night: parseFloat(document.getElementById('pPrice').value) || 0,
        monthly_discount: parseInt(document.getElementById('pMonthlyDiscount').value) || 0,
        city_id: document.getElementById('pCityId').value || null,
        property_type_id: document.getElementById('pTypeId').value || null,
        bedrooms: parseInt(document.getElementById('pBedrooms').value) || 0,
        bathrooms: parseInt(document.getElementById('pBathrooms').value) || 0,
        beds: parseInt(document.getElementById('pBeds').value) || 0,
        max_guests: parseInt(document.getElementById('pMaxGuests').value) || 1,
        trip_type: document.getElementById('pTripType').value,
        address: document.getElementById('pAddress').value,
        latitude: parseFloat(document.getElementById('pLatitude').value) || null,
        longitude: parseFloat(document.getElementById('pLongitude').value) || null,
        check_in_time: document.getElementById('pCheckInTime').value || null,
        check_out_time: document.getElementById('pCheckOutTime').value || null,
        is_active: document.getElementById('pIsActive').checked,
        is_featured: document.getElementById('pIsFeatured').checked,
        instant_book: document.getElementById('pInstantBook').checked,
    };

    try {
        await api.put(`/admin/places/${id}`, data);
        showToast('تم تحديث العقار بنجاح', 'success');
        closeModal('placeModal');
        loadPlaces(placesPage);
    } catch (e) {
        showToast(e.error || 'فشل تحديث العقار', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   BOOKINGS
   ═══════════════════════════════════════════════════ */
let bookingsPage = 1;

async function loadBookings(page = 1) {
    bookingsPage = page;
    const status = document.getElementById('bookingStatusFilter')?.value || '';

    try {
        const data = await api.get('/admin/bookings', { status, page, per_page: 20 });
        const tbody = document.getElementById('bookingsBody');
        tbody.innerHTML = (data.bookings || []).map(b => `
            <tr>
                <td>${b.guest_name || b.guest_id?.slice(0, 8) || ''}</td>
                <td>${b.place?.title_ar || b.place_id?.slice(0, 8) || ''}</td>
                <td>${b.check_in ? new Date(b.check_in).toLocaleDateString('ar-SA') : ''}</td>
                <td>${b.check_out ? new Date(b.check_out).toLocaleDateString('ar-SA') : ''}</td>
                <td><span class="badge badge--${b.status}">${b.status}</span></td>
                <td>${b.total_price || 0} ر.س</td>
                <td>
                    <div class="action-btns">
                        ${b.status === 'pending' ? `<button class="action-btn action-btn--approve" onclick="updateBookingStatus('${b.id}', 'confirmed')"><i data-lucide="check"></i></button>` : ''}
                        ${b.status === 'confirmed' ? `<button class="action-btn action-btn--approve" title="Mark Completed" onclick="updateBookingStatus('${b.id}', 'completed')"><i data-lucide="check-circle"></i></button>` : ''}
                        <button class="action-btn action-btn--delete" onclick="updateBookingStatus('${b.id}', 'cancelled')"><i data-lucide="x"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="7" style="text-align:center;padding:40px;">لا يوجد حجوزات</td></tr>';

        renderPagination('bookingsPagination', data.pages, data.page, loadBookings);
        lucide.createIcons();
    } catch (e) {
        console.error('Bookings load error:', e);
    }
}

async function updateBookingStatus(id, status) {
    try {
        await api.put(`/admin/bookings/${id}`, { status });
        showToast('تم تحديث الحجز', 'success');
        loadBookings(bookingsPage);
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   REVIEWS
   ═══════════════════════════════════════════════════ */
async function loadReviews() {
    const approved = document.getElementById('reviewFilter')?.value || '';
    try {
        const data = await api.get('/admin/reviews', { approved });
        const tbody = document.getElementById('reviewsBody');
        tbody.innerHTML = (data.reviews || []).map(r => `
            <tr>
                <td>${r.author?.first_name || ''} ${r.author?.last_name || ''}</td>
                <td>${r.place_id?.slice(0, 8) || ''}</td>
                <td>${'<i data-lucide="star" style="width:14px;height:14px;color:#f59e0b;display:inline;"></i>'.repeat(r.rating)}</td>
                <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${r.comment || '—'}</td>
                <td><span class="badge badge--${r.is_approved ? 'active' : 'pending'}">${r.is_approved ? 'معتمد' : 'معلق'}</span></td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--approve" onclick="toggleReviewApproval('${r.id}', ${!r.is_approved})"><i data-lucide="${r.is_approved ? 'eye-off' : 'check'}"></i></button>
                        <button class="action-btn action-btn--delete" onclick="deleteReview('${r.id}')"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="6" style="text-align:center;padding:40px;">لا يوجد تقييمات</td></tr>';
        lucide.createIcons();
    } catch (e) {
        console.error('Reviews load error:', e);
    }
}

async function toggleReviewApproval(id, approved) {
    try {
        await api.put(`/admin/reviews/${id}`, { is_approved: approved });
        showToast(approved ? 'تم اعتماد التقييم' : 'تم إلغاء الاعتماد', 'success');
        loadReviews();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

async function deleteReview(id) {
    if (!confirm('حذف هذا التقييم?')) return;
    try {
        await api.delete(`/admin/reviews/${id}`);
        showToast('تم حذف التقييم', 'success');
        loadReviews();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   AMENITIES
   ═══════════════════════════════════════════════════ */
async function loadAmenities() {
    try {
        const data = await api.get('/admin/amenities');
        const tbody = document.getElementById('amenitiesBody');
        tbody.innerHTML = (data || []).map(a => `
            <tr>
                <td>${a.name_ar}</td>
                <td>${a.name_en}</td>
                <td><i data-lucide="${a.icon || 'circle'}" style="width:18px;height:18px;"></i> ${a.icon || ''}</td>
                <td>${a.category || ''}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--edit" onclick='editAmenity(${JSON.stringify(a)})'><i data-lucide="pencil"></i></button>
                        <button class="action-btn action-btn--delete" onclick="deleteAmenity('${a.id}')"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="5" style="text-align:center;padding:40px;">لا يوجد مرافق</td></tr>';
        lucide.createIcons();
    } catch (e) {
        console.error('Amenities load error:', e);
    }
}

function editAmenity(a) {
    document.getElementById('editAmenityId').value = a.id;
    document.getElementById('amenityModalTitle').textContent = 'تعديل مرفق';
    document.getElementById('aNameAr').value = a.name_ar || '';
    document.getElementById('aNameEn').value = a.name_en || '';
    document.getElementById('aIcon').value = a.icon || '';
    document.getElementById('aCategory').value = a.category || 'essentials';
    openModal('amenityModal');
}

async function saveAmenity() {
    const id = document.getElementById('editAmenityId').value;
    const data = {
        name_ar: document.getElementById('aNameAr').value,
        name_en: document.getElementById('aNameEn').value,
        icon: document.getElementById('aIcon').value,
        category: document.getElementById('aCategory').value,
    };

    try {
        if (id) {
            await api.put(`/admin/amenities/${id}`, data);
            showToast('تم تحديث المرفق', 'success');
        } else {
            await api.post('/admin/amenities', data);
            showToast('تم إضافة المرفق', 'success');
        }
        closeModal('amenityModal');
        document.getElementById('editAmenityId').value = '';
        document.getElementById('amenityModalTitle').textContent = 'إضافة مرفق';
        loadAmenities();
    } catch (e) {
        showToast(e.error || 'حدث خطأ', 'error');
    }
}

async function deleteAmenity(id) {
    if (!confirm('حذف هذا المرفق?')) return;
    try {
        await api.delete(`/admin/amenities/${id}`);
        showToast('تم حذف المرفق', 'success');
        loadAmenities();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   CITIES
   ═══════════════════════════════════════════════════ */
async function loadCities() {
    try {
        const data = await api.get('/admin/cities');
        const tbody = document.getElementById('citiesBody');
        tbody.innerHTML = (data || []).map(c => `
            <tr>
                <td>${c.name_ar}</td>
                <td>${c.name_en}</td>
                <td>${c.region_ar || c.region_en || ''}</td>
                <td>${c.is_featured ? '<i data-lucide="check" style="color:#16a34a;width:16px;height:16px;"></i>' : '<i data-lucide="x" style="color:#aaa;width:16px;height:16px;"></i>'}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--edit" onclick='editCity(${JSON.stringify(c)})'><i data-lucide="pencil"></i></button>
                        <button class="action-btn action-btn--delete" onclick="deleteCity('${c.id}')"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="5" style="text-align:center;padding:40px;">لا يوجد مدن</td></tr>';
        lucide.createIcons();
    } catch (e) {
        console.error('Cities load error:', e);
    }
}

function editCity(c) {
    document.getElementById('editCityId').value = c.id;
    document.getElementById('cityModalTitle').textContent = 'تعديل مدينة';
    document.getElementById('cNameAr').value = c.name_ar || '';
    document.getElementById('cNameEn').value = c.name_en || '';
    document.getElementById('cRegionAr').value = c.region_ar || '';
    document.getElementById('cRegionEn').value = c.region_en || '';
    document.getElementById('cLat').value = c.latitude || '';
    document.getElementById('cLng').value = c.longitude || '';
    document.getElementById('cFeatured').checked = c.is_featured || false;
    openModal('cityModal');
}

async function saveCity() {
    const id = document.getElementById('editCityId').value;
    const data = {
        name_ar: document.getElementById('cNameAr').value,
        name_en: document.getElementById('cNameEn').value,
        region_ar: document.getElementById('cRegionAr').value,
        region_en: document.getElementById('cRegionEn').value,
        latitude: parseFloat(document.getElementById('cLat').value) || null,
        longitude: parseFloat(document.getElementById('cLng').value) || null,
        is_featured: document.getElementById('cFeatured').checked,
    };

    try {
        if (id) {
            await api.put(`/admin/cities/${id}`, data);
            showToast('تم تحديث المدينة', 'success');
        } else {
            await api.post('/admin/cities', data);
            showToast('تم إضافة المدينة', 'success');
        }
        closeModal('cityModal');
        document.getElementById('editCityId').value = '';
        document.getElementById('cityModalTitle').textContent = 'إضافة مدينة';
        loadCities();
    } catch (e) {
        showToast(e.error || 'حدث خطأ', 'error');
    }
}

async function deleteCity(id) {
    if (!confirm('حذف هذه المدينة?')) return;
    try {
        await api.delete(`/admin/cities/${id}`);
        showToast('تم حذف المدينة', 'success');
        loadCities();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   PROPERTY TYPES
   ═══════════════════════════════════════════════════ */
async function loadTypes() {
    try {
        const data = await api.get('/admin/property-types');
        const tbody = document.getElementById('typesBody');
        tbody.innerHTML = (data || []).map(t => `
            <tr>
                <td>${t.name_ar}</td>
                <td>${t.name_en}</td>
                <td><i data-lucide="${t.icon || 'circle'}" style="width:18px;height:18px;"></i> ${t.icon || ''}</td>
                <td>${t.sort_order || 0}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--edit" onclick='editType(${JSON.stringify(t)})'><i data-lucide="pencil"></i></button>
                        <button class="action-btn action-btn--delete" onclick="deleteType('${t.id}')"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="5" style="text-align:center;padding:40px;">لا يوجد أنواع</td></tr>';
        lucide.createIcons();
    } catch (e) {
        console.error('Types load error:', e);
    }
}

function editType(t) {
    document.getElementById('editTypeId').value = t.id;
    document.getElementById('typeModalTitle').textContent = 'تعديل نوع عقار';
    document.getElementById('tNameAr').value = t.name_ar || '';
    document.getElementById('tNameEn').value = t.name_en || '';
    document.getElementById('tIcon').value = t.icon || '';
    document.getElementById('tOrder').value = t.sort_order || 0;
    openModal('typeModal');
}

async function saveType() {
    const id = document.getElementById('editTypeId').value;
    const data = {
        name_ar: document.getElementById('tNameAr').value,
        name_en: document.getElementById('tNameEn').value,
        icon: document.getElementById('tIcon').value,
        sort_order: parseInt(document.getElementById('tOrder').value) || 0,
    };

    try {
        if (id) {
            await api.put(`/admin/property-types/${id}`, data);
            showToast('تم تحديث نوع العقار', 'success');
        } else {
            await api.post('/admin/property-types', data);
            showToast('تم إضافة نوع العقار', 'success');
        }
        closeModal('typeModal');
        document.getElementById('editTypeId').value = '';
        document.getElementById('typeModalTitle').textContent = 'إضافة نوع عقار';
        loadTypes();
    } catch (e) {
        showToast(e.error || 'حدث خطأ', 'error');
    }
}

async function deleteType(id) {
    if (!confirm('حذف هذا النوع?')) return;
    try {
        await api.delete(`/admin/property-types/${id}`);
        showToast('تم حذف النوع', 'success');
        loadTypes();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ═══════════════════════════════════════════════════
   SETTINGS
   ═══════════════════════════════════════════════════ */
async function loadSettings() {
    try {
        const data = await api.get('/admin/settings');
        const tbody = document.getElementById('settingsBody');

        // Fill in known keys
        const keysMap = {};
        (data || []).forEach(s => { keysMap[s.key] = s; });

        if (keysMap['google_maps_api_key']) document.getElementById('settingGoogleMaps').value = keysMap['google_maps_api_key'].value || '';
        if (keysMap['resend_api_key']) document.getElementById('settingResend').value = keysMap['resend_api_key'].value || '';
        if (keysMap['bank_name']) document.getElementById('settingBankName').value = keysMap['bank_name'].value || '';
        if (keysMap['bank_iban']) document.getElementById('settingBankIban').value = keysMap['bank_iban'].value || '';
        if (keysMap['account_holder']) document.getElementById('settingAccountHolder').value = keysMap['account_holder'].value || '';
        if (keysMap['check_in_time']) document.getElementById('settingCheckIn').value = keysMap['check_in_time'].value || '16:00';
        if (keysMap['check_out_time']) document.getElementById('settingCheckOut').value = keysMap['check_out_time'].value || '12:00';
        if (keysMap['cleaning_hours']) document.getElementById('settingCleaning').value = keysMap['cleaning_hours'].value || '4';

        // Render custom settings table
        const custom = (data || []).filter(s => !['google_maps_api_key', 'resend_api_key', 'bank_name', 'bank_iban', 'account_holder', 'check_in_time', 'check_out_time', 'cleaning_hours'].includes(s.key));
        tbody.innerHTML = custom.map(s => `
            <tr>
                <td><code>${s.key}</code></td>
                <td>${s.is_secret ? '****' : (s.value || '—')}</td>
                <td>${s.category || ''}</td>
                <td>${s.description_en || s.description_ar || ''}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn action-btn--delete" onclick="deleteSetting('${s.id}')"><i data-lucide="trash-2"></i></button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="5" style="text-align:center;padding:20px;">لا يوجد إعدادات مخصصة</td></tr>';

        lucide.createIcons();
    } catch (e) {
        console.error('Settings load error:', e);
    }
}

async function saveApiKeys() {
    const keys = [
        { key: 'google_maps_api_key', value: document.getElementById('settingGoogleMaps').value, category: 'api_keys', description_en: 'Google Maps API Key', is_secret: false },
        { key: 'resend_api_key', value: document.getElementById('settingResend').value, category: 'api_keys', description_en: 'Resend Email API Key', is_secret: true },
        { key: 'bank_name', value: document.getElementById('settingBankName').value, category: 'payment', description_en: 'Bank Name', is_secret: false },
        { key: 'bank_iban', value: document.getElementById('settingBankIban').value, category: 'payment', description_en: 'Bank IBAN', is_secret: false },
        { key: 'account_holder', value: document.getElementById('settingAccountHolder').value, category: 'payment', description_en: 'Account Holder', is_secret: false },
    ];

    try {
        for (const k of keys) {
            if (k.value) await api.post('/admin/settings', k);
        }
        showToast('تم حفظ مفاتيح API', 'success');
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

async function saveBookingRules() {
    const rules = [
        { key: 'check_in_time', value: document.getElementById('settingCheckIn').value, category: 'booking', description_en: 'Check-in time', description_ar: 'وقت تسجيل الدخول' },
        { key: 'check_out_time', value: document.getElementById('settingCheckOut').value, category: 'booking', description_en: 'Check-out time', description_ar: 'وقت تسجيل الخروج' },
        { key: 'cleaning_hours', value: document.getElementById('settingCleaning').value, category: 'booking', description_en: 'Cleaning hours between guests', description_ar: 'ساعات التنظيف بين الضيوف' },
    ];

    try {
        for (const r of rules) {
            await api.post('/admin/settings', r);
        }
        showToast('تم حفظ قواعد الحجز', 'success');
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

async function saveSetting() {
    const data = {
        key: document.getElementById('sKey').value,
        value: document.getElementById('sValue').value,
        category: document.getElementById('sCategory').value,
        description_en: document.getElementById('sDesc').value,
        is_secret: document.getElementById('sSecret').checked,
    };

    try {
        await api.post('/admin/settings', data);
        showToast('تم حفظ الإعداد', 'success');
        closeModal('settingModal');
        loadSettings();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

async function deleteSetting(id) {
    if (!confirm('حذف هذا الإعداد?')) return;
    try {
        await api.delete(`/admin/settings/${id}`);
        showToast('تم حذف الإعداد', 'success');
        loadSettings();
    } catch (e) {
        showToast('حدث خطأ', 'error');
    }
}

/* ─── Pagination Helper ─── */
function renderPagination(containerId, totalPages, currentPage, loadFn) {
    const container = document.getElementById(containerId);
    if (!container || totalPages <= 1) { if (container) container.innerHTML = ''; return; }

    let html = '';
    for (let i = 1; i <= totalPages; i++) {
        html += `<button class="${i === currentPage ? 'active' : ''}" onclick="${loadFn.name}(${i})">${i}</button>`;
    }
    container.innerHTML = html;
}

/* ─── Logout ─── */
function logout() {
    Auth.clear();
    window.location.reload();
}
