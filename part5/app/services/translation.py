"""
HBnB V2 — Translation Service
Auto-translate using Google Translate API (free tier).
"""
import logging

logger = logging.getLogger(__name__)

# Translations dictionary — used as fallback
TRANSLATIONS = {
    'ar': {
        # Navigation
        'home': 'الرئيسية',
        'search': 'بحث',
        'bookings': 'حجوزاتي',
        'favorites': 'المفضلة',
        'profile': 'الملف الشخصي',
        'login': 'تسجيل الدخول',
        'logout': 'تسجيل الخروج',
        'register': 'إنشاء حساب',

        # Home
        'search_placeholder': 'ابحث عن وجهتك المثالية...',
        'cities': 'المدن',
        'featured_places': 'عقارات مميزة',
        'business_trip': 'رحلة عمل',
        'family_trip': 'رحلة عائلية',
        'monthly_stays': 'إقامة شهرية',
        'property_types': 'أنواع العقارات',
        'budget_friendly': 'أسعار مناسبة',
        'less_than_average': 'أقل من متوسط الأسعار',
        'per_night': 'لليلة',
        'per_month': 'للشهر',

        # Property Types
        'apartments': 'شقق',
        'chalets': 'شاليهات',
        'studios': 'استديوهات',
        'rest_houses': 'استراحات',
        'resorts': 'منتجعات',
        'villas': 'فلل',
        'farms': 'مزارع',
        'camps': 'مخيمات',
        'hotels': 'فنادق',
        'hostels': 'نُزل',

        # Booking
        'book_now': 'احجز الآن',
        'check_in': 'تاريخ الوصول',
        'check_out': 'تاريخ المغادرة',
        'guests': 'الضيوف',
        'adults': 'بالغين',
        'children': 'أطفال',
        'infants': 'رضّع',
        'total': 'الإجمالي',
        'subtotal': 'المجموع الفرعي',
        'service_fee': 'رسوم الخدمة',
        'discount': 'خصم',
        'confirm_booking': 'تأكيد الحجز',
        'cancel_booking': 'إلغاء الحجز',
        'booking_confirmed': 'تم تأكيد الحجز',

        # Auth
        'enter_email': 'أدخل بريدك الإلكتروني',
        'enter_otp': 'أدخل رمز التحقق',
        'send_otp': 'إرسال رمز التحقق',
        'send_magic_link': 'إرسال رابط الدخول',
        'verify': 'تحقق',
        'or': 'أو',
        'owner_register': 'سجّل كمالك عقار',

        # Place
        'amenities': 'المرافق',
        'reviews': 'التقييمات',
        'location': 'الموقع',
        'house_rules': 'قواعد المنزل',
        'access_info': 'معلومات الوصول',
        'write_review': 'اكتب تقييم',
        'bedrooms': 'غرف نوم',
        'bathrooms': 'حمامات',
        'max_guests': 'الحد الأقصى للضيوف',

        # Footer
        'about': 'عن المنصة',
        'contact': 'تواصل معنا',
        'privacy': 'سياسة الخصوصية',
        'terms': 'الشروط والأحكام',
        'built_by': 'تم التطوير بواسطة',

        # General
        'loading': 'جاري التحميل...',
        'error': 'خطأ',
        'success': 'تم بنجاح',
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'delete': 'حذف',
        'edit': 'تعديل',
        'view': 'عرض',
        'no_results': 'لا توجد نتائج',
        'sar': 'ر.س',
    },
    'en': {
        # Navigation
        'home': 'Home',
        'search': 'Search',
        'bookings': 'My Bookings',
        'favorites': 'Favorites',
        'profile': 'Profile',
        'login': 'Login',
        'logout': 'Logout',
        'register': 'Register',

        # Home
        'search_placeholder': 'Search for your perfect stay...',
        'cities': 'Cities',
        'featured_places': 'Featured Properties',
        'business_trip': 'Business Trip',
        'family_trip': 'Family Trip',
        'monthly_stays': 'Monthly Stays',
        'property_types': 'Property Types',
        'budget_friendly': 'Budget Friendly',
        'less_than_average': 'Below Average Price',
        'per_night': '/night',
        'per_month': '/month',

        # Property Types
        'apartments': 'Apartments',
        'chalets': 'Chalets',
        'studios': 'Studios',
        'rest_houses': 'Rest Houses',
        'resorts': 'Resorts',
        'villas': 'Villas',
        'farms': 'Farms',
        'camps': 'Camps',
        'hotels': 'Hotels',
        'hostels': 'Hostels',

        # Booking
        'book_now': 'Book Now',
        'check_in': 'Check-in',
        'check_out': 'Check-out',
        'guests': 'Guests',
        'adults': 'Adults',
        'children': 'Children',
        'infants': 'Infants',
        'total': 'Total',
        'subtotal': 'Subtotal',
        'service_fee': 'Service Fee',
        'discount': 'Discount',
        'confirm_booking': 'Confirm Booking',
        'cancel_booking': 'Cancel Booking',
        'booking_confirmed': 'Booking Confirmed',

        # Auth
        'enter_email': 'Enter your email',
        'enter_otp': 'Enter verification code',
        'send_otp': 'Send OTP',
        'send_magic_link': 'Send Magic Link',
        'verify': 'Verify',
        'or': 'or',
        'owner_register': 'Register as Property Owner',

        # Place
        'amenities': 'Amenities',
        'reviews': 'Reviews',
        'location': 'Location',
        'house_rules': 'House Rules',
        'access_info': 'Access Information',
        'write_review': 'Write Review',
        'bedrooms': 'Bedrooms',
        'bathrooms': 'Bathrooms',
        'max_guests': 'Max Guests',

        # Footer
        'about': 'About',
        'contact': 'Contact Us',
        'privacy': 'Privacy Policy',
        'terms': 'Terms & Conditions',
        'built_by': 'Built by',

        # General
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'edit': 'Edit',
        'view': 'View',
        'no_results': 'No results found',
        'sar': 'SAR',
    }
}


def t(key, lang='ar'):
    """Get translation for a key"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ar']).get(key, key)


def translate_text(text, target_lang='ar', source_lang='auto'):
    """Translate text using Google Translate (free tier)"""
    if not text:
        return text

    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(text, dest=target_lang, src=source_lang)
        return result.text
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return text  # Return original on failure


def get_all_translations(lang='ar'):
    """Get all translations for a language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ar'])
