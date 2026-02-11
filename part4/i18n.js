/* ============================================
   HBnB - Internationalization (i18n) Module
   Supports: English (en) & Arabic (ar)
   ============================================ */

const translations = {
  en: {
    // Header / Nav
    "nav.home": "Home",
    "nav.login": "Login",
    "nav.logout": "Logout",
    "nav.admin": "Admin",

    // Index Page
    "index.title": "HBnB - Places",
    "index.filter.label": "Max Price:",
    "index.filter.all": "All Prices",
    "index.filter.under10": "Under $10",
    "index.filter.under50": "Under $50",
    "index.filter.under100": "Under $100",
    "index.card.perNight": "/ night",
    "index.card.viewDetails": "View Details",
    "index.empty": "No places found matching your criteria.",
    "index.error.load": "Failed to load places.",
    "index.error.network": "Network error. Could not load places.",

    // Login Page
    "login.title": "Welcome Back",
    "login.subtitle": "Sign in to your HBnB account",
    "login.email.label": "Email",
    "login.email.placeholder": "you@example.com",
    "login.password.label": "Password",
    "login.password.placeholder": "Enter your password",
    "login.submit": "Sign In",
    "login.submitting": "Signing in…",
    "login.error.credentials": "Login failed. Please check your credentials.",
    "login.error.network": "Network error. Please try again.",

    // Place Details Page
    "place.title": "HBnB - Place Details",
    "place.host": "Host:",
    "place.price": "Price:",
    "place.location": "Location:",
    "place.amenities": "Amenities",
    "place.noAmenities": "No amenities listed.",
    "place.noDescription": "No description available.",
    "place.error.notFound": "Place not found.",
    "place.error.network": "Network error. Could not load place details.",
    "place.error.noId": "No place ID provided.",

    // Reviews
    "reviews.title": "Reviews",
    "reviews.empty": "No reviews yet. Be the first to share your experience!",
    "reviews.add.title": "Add a Review",
    "reviews.add.textLabel": "Your Review",
    "reviews.add.textPlaceholder": "Share your experience with this place...",
    "reviews.add.ratingLabel": "Rating",
    "reviews.add.ratingDefault": "Select a rating",
    "reviews.add.rating1": "★ 1 - Poor",
    "reviews.add.rating2": "★★ 2 - Fair",
    "reviews.add.rating3": "★★★ 3 - Good",
    "reviews.add.rating4": "★★★★ 4 - Great",
    "reviews.add.rating5": "★★★★★ 5 - Excellent",
    "reviews.add.submit": "Submit Review",
    "reviews.add.submitting": "Submitting…",
    "reviews.add.success": "Review submitted successfully!",
    "reviews.add.error": "Failed to submit review.",
    "reviews.add.errorRating": "Please select a rating.",

    // Footer
    "footer.copy": "© 2026 HBnB Evolution - All Rights Reserved",

    // Toast
    "toast.success": "Success",
    "toast.error": "Error",
    "toast.info": "Info",
    "toast.warning": "Warning",

    // Dark Mode
    "theme.light": "Light",
    "theme.dark": "Dark",

    // Language
    "lang.en": "EN",
    "lang.ar": "AR"
  },

  ar: {
    // Header / Nav
    "nav.home": "الرئيسية",
    "nav.login": "تسجيل الدخول",
    "nav.logout": "تسجيل الخروج",
    "nav.admin": "لوحة التحكم",

    // Index Page
    "index.title": "HBnB - الأماكن",
    "index.filter.label": "الحد الأقصى للسعر:",
    "index.filter.all": "جميع الأسعار",
    "index.filter.under10": "أقل من $10",
    "index.filter.under50": "أقل من $50",
    "index.filter.under100": "أقل من $100",
    "index.card.perNight": "/ ليلة",
    "index.card.viewDetails": "عرض التفاصيل",
    "index.empty": "لم يتم العثور على أماكن تطابق معاييرك.",
    "index.error.load": "فشل تحميل الأماكن.",
    "index.error.network": "خطأ في الشبكة. تعذر تحميل الأماكن.",

    // Login Page
    "login.title": "مرحباً بعودتك",
    "login.subtitle": "سجّل الدخول إلى حسابك في HBnB",
    "login.email.label": "البريد الإلكتروني",
    "login.email.placeholder": "you@example.com",
    "login.password.label": "كلمة المرور",
    "login.password.placeholder": "أدخل كلمة المرور",
    "login.submit": "تسجيل الدخول",
    "login.submitting": "جارٍ تسجيل الدخول…",
    "login.error.credentials": "فشل تسجيل الدخول. يرجى التحقق من بياناتك.",
    "login.error.network": "خطأ في الشبكة. يرجى المحاولة مرة أخرى.",

    // Place Details Page
    "place.title": "HBnB - تفاصيل المكان",
    "place.host": "المضيف:",
    "place.price": "السعر:",
    "place.location": "الموقع:",
    "place.amenities": "المرافق",
    "place.noAmenities": "لا توجد مرافق مدرجة.",
    "place.noDescription": "لا يوجد وصف متاح.",
    "place.error.notFound": "المكان غير موجود.",
    "place.error.network": "خطأ في الشبكة. تعذر تحميل تفاصيل المكان.",
    "place.error.noId": "لم يتم توفير معرّف المكان.",

    // Reviews
    "reviews.title": "التقييمات",
    "reviews.empty": "لا توجد تقييمات بعد. كن أول من يشارك تجربته!",
    "reviews.add.title": "أضف تقييماً",
    "reviews.add.textLabel": "تقييمك",
    "reviews.add.textPlaceholder": "شارك تجربتك مع هذا المكان...",
    "reviews.add.ratingLabel": "التقييم",
    "reviews.add.ratingDefault": "اختر تقييماً",
    "reviews.add.rating1": "★ ١ - سيء",
    "reviews.add.rating2": "★★ ٢ - مقبول",
    "reviews.add.rating3": "★★★ ٣ - جيد",
    "reviews.add.rating4": "★★★★ ٤ - ممتاز",
    "reviews.add.rating5": "★★★★★ ٥ - رائع",
    "reviews.add.submit": "إرسال التقييم",
    "reviews.add.submitting": "جارٍ الإرسال…",
    "reviews.add.success": "تم إرسال التقييم بنجاح!",
    "reviews.add.error": "فشل إرسال التقييم.",
    "reviews.add.errorRating": "يرجى اختيار تقييم.",

    // Footer
    "footer.copy": "© 2026 HBnB Evolution - جميع الحقوق محفوظة",

    // Toast
    "toast.success": "نجاح",
    "toast.error": "خطأ",
    "toast.info": "معلومات",
    "toast.warning": "تحذير",

    // Dark Mode
    "theme.light": "فاتح",
    "theme.dark": "داكن",

    // Language
    "lang.en": "EN",
    "lang.ar": "AR"
  }
};

/* ---------- i18n Engine ---------- */

/**
 * Get saved language or default to English
 */
function getSavedLanguage() {
  return localStorage.getItem('hbnb-lang') || 'en';
}

/**
 * Save language preference
 */
function saveLanguage(lang) {
  localStorage.setItem('hbnb-lang', lang);
}

/**
 * Translate a key to the current language
 * @param {string} key - The translation key
 * @param {object} [vars] - Variables to interpolate (e.g., {price: 50})
 * @returns {string}
 */
function t(key, vars) {
  const lang = getSavedLanguage();
  let str = (translations[lang] && translations[lang][key]) || (translations['en'] && translations['en'][key]) || key;
  if (vars) {
    Object.keys(vars).forEach(k => {
      str = str.replace(`{${k}}`, vars[k]);
    });
  }
  return str;
}

/**
 * Apply RTL/LTR direction based on current language
 */
function applyDirection() {
  const lang = getSavedLanguage();
  const html = document.documentElement;
  if (lang === 'ar') {
    html.setAttribute('dir', 'rtl');
    html.setAttribute('lang', 'ar');
    document.body.classList.add('rtl');
  } else {
    html.setAttribute('dir', 'ltr');
    html.setAttribute('lang', 'en');
    document.body.classList.remove('rtl');
  }
}

/**
 * Translate all elements with data-i18n attribute
 */
function translatePage() {
  applyDirection();

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const translated = t(key);
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.placeholder = translated;
    } else if (el.tagName === 'OPTION') {
      el.textContent = translated;
    } else {
      el.textContent = translated;
    }
  });

  // Update page title if there's a data-i18n-title on <html> or <head>
  const titleKey = document.querySelector('title')?.getAttribute('data-i18n');
  if (titleKey) {
    document.title = t(titleKey);
  }

  // Update lang toggle button text
  const langBtn = document.getElementById('lang-toggle');
  if (langBtn) {
    const lang = getSavedLanguage();
    langBtn.textContent = lang === 'en' ? 'AR' : 'EN';
    langBtn.setAttribute('aria-label', lang === 'en' ? 'Switch to Arabic' : 'Switch to English');
  }
}

/**
 * Toggle between EN and AR
 */
function toggleLanguage() {
  const current = getSavedLanguage();
  const next = current === 'en' ? 'ar' : 'en';
  saveLanguage(next);
  translatePage();
  // Re-render dynamic content if available
  if (typeof window.onLanguageChange === 'function') {
    window.onLanguageChange(next);
  }
}

/**
 * Initialize i18n on page load
 */
function initI18n() {
  applyDirection();
  translatePage();
}
