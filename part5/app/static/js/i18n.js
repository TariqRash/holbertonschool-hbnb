/**
 * HBnB V2 — Internationalization (i18n)
 * Arabic/English language switcher with RTL support.
 */

const TRANSLATIONS = {
    ar: {
        // Nav
        home: 'الرئيسية',
        search: 'بحث',
        search_placeholder: 'ابحث عن وجهتك المثالية...',
        bookings: 'حجوزاتي',
        favorites: 'المفضلة',
        profile: 'الملف الشخصي',
        login: 'تسجيل الدخول',
        logout: 'تسجيل الخروج',

        // Home
        cities: 'المدن',
        featured_places: 'عقارات مميزة',
        business_trip: 'رحلة عمل',
        family_trip: 'رحلة عائلية',
        monthly_stays: 'إقامة شهرية',
        property_types: 'أنواع العقارات',
        budget_friendly: 'أسعار مناسبة',
        less_than_average: 'أقل من متوسط الأسعار',
        per_night: 'لليلة',
        per_month: 'للشهر',

        // Booking
        check_in: 'الوصول',
        check_out: 'المغادرة',
        guests: 'الضيوف',
        book_now: 'احجز الآن',
        confirm_booking: 'تأكيد الحجز',

        // Auth
        enter_email: 'أدخل بريدك الإلكتروني',
        enter_otp: 'أدخل رمز التحقق',
        send_otp: 'إرسال رمز التحقق',
        send_magic_link: 'إرسال رابط الدخول',
        or: 'أو',
        owner_register: 'سجّل كمالك عقار',

        // Place
        amenities: 'المرافق',
        reviews: 'التقييمات',
        location: 'الموقع',
        write_review: 'اكتب تقييم',
        bedrooms: 'غرف نوم',
        bathrooms: 'حمامات',
        max_guests: 'الحد الأقصى',

        // Footer
        built_by: 'تم التطوير بواسطة',

        // General
        loading: 'جاري التحميل...',
        no_results: 'لا توجد نتائج',
        sar: 'ر.س',
    },
    en: {
        home: 'Home',
        search: 'Search',
        search_placeholder: 'Search for your perfect stay...',
        bookings: 'My Bookings',
        favorites: 'Favorites',
        profile: 'Profile',
        login: 'Login',
        logout: 'Logout',
        cities: 'Cities',
        featured_places: 'Featured Properties',
        business_trip: 'Business Trip',
        family_trip: 'Family Trip',
        monthly_stays: 'Monthly Stays',
        property_types: 'Property Types',
        budget_friendly: 'Budget Friendly',
        less_than_average: 'Below Average Price',
        per_night: '/night',
        per_month: '/month',
        check_in: 'Check-in',
        check_out: 'Check-out',
        guests: 'Guests',
        book_now: 'Book Now',
        confirm_booking: 'Confirm Booking',
        enter_email: 'Enter your email',
        enter_otp: 'Enter verification code',
        send_otp: 'Send OTP',
        send_magic_link: 'Send Magic Link',
        or: 'or',
        owner_register: 'Register as Property Owner',
        amenities: 'Amenities',
        reviews: 'Reviews',
        location: 'Location',
        write_review: 'Write Review',
        bedrooms: 'Bedrooms',
        bathrooms: 'Bathrooms',
        max_guests: 'Max Guests',
        built_by: 'Built by',
        loading: 'Loading...',
        no_results: 'No results found',
        sar: 'SAR',
    }
};

/**
 * Get translation
 */
function t(key) {
    const lang = getLang();
    return TRANSLATIONS[lang]?.[key] || TRANSLATIONS.ar[key] || key;
}

/**
 * Toggle language
 */
function toggleLanguage() {
    const current = getLang();
    const next = current === 'ar' ? 'en' : 'ar';
    localStorage.setItem('lang', next);

    // Update direction
    document.documentElement.setAttribute('dir', next === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', next);

    // Update label
    const label = document.getElementById('langLabel');
    if (label) label.textContent = next === 'ar' ? 'EN' : 'AR';

    // Update all [data-t] elements
    applyTranslations();

    // Reload data with new language
    if (typeof loadHomeData === 'function') loadHomeData();
}

/**
 * Apply translations to DOM
 */
function applyTranslations() {
    document.querySelectorAll('[data-t]').forEach(el => {
        const key = el.getAttribute('data-t');
        const translated = t(key);
        if (el.tagName === 'INPUT' && el.type !== 'submit') {
            el.placeholder = translated;
        } else {
            el.textContent = translated;
        }
    });
}

/**
 * Initialize language
 */
(function initLang() {
    const lang = getLang();
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);

    const label = document.getElementById('langLabel');
    if (label) label.textContent = lang === 'ar' ? 'EN' : 'AR';
})();
