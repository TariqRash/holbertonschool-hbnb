/* ============================================
   HBnB - Currency Converter Module
   Uses Frankfurter API (free, no key required)
   Base currency: USD
   ============================================ */

(function () {
  'use strict';

  const CACHE_KEY = 'hbnb-currency-rates';
  const CACHE_TTL = 3600000; // 1 hour in ms
  const PREF_KEY = 'hbnb-currency';
  const API_URL = 'https://api.frankfurter.app/latest?from=USD';

  // Supported currencies with symbols
  const CURRENCIES = {
    USD: { symbol: '$', name: 'US Dollar', nameAr: 'دولار أمريكي' },
    EUR: { symbol: '€', name: 'Euro', nameAr: 'يورو' },
    GBP: { symbol: '£', name: 'British Pound', nameAr: 'جنيه إسترليني' },
    SAR: { symbol: '﷼', name: 'Saudi Riyal', nameAr: 'ريال سعودي' },
    AED: { symbol: 'د.إ', name: 'UAE Dirham', nameAr: 'درهم إماراتي' },
    JPY: { symbol: '¥', name: 'Japanese Yen', nameAr: 'ين ياباني' },
    TRY: { symbol: '₺', name: 'Turkish Lira', nameAr: 'ليرة تركية' }
  };

  let rates = { USD: 1 };
  let currentCurrency = 'USD';

  /**
   * Get saved currency preference
   */
  function getSavedCurrency() {
    return localStorage.getItem(PREF_KEY) || 'USD';
  }

  /**
   * Save currency preference
   */
  function saveCurrency(code) {
    localStorage.setItem(PREF_KEY, code);
  }

  /**
   * Try to load rates from localStorage cache
   */
  function loadCachedRates() {
    try {
      const cached = JSON.parse(localStorage.getItem(CACHE_KEY));
      if (cached && cached.timestamp && (Date.now() - cached.timestamp < CACHE_TTL)) {
        return cached.rates;
      }
    } catch (e) { /* ignore */ }
    return null;
  }

  /**
   * Save rates to localStorage cache
   */
  function cacheRates(ratesObj) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        rates: ratesObj,
        timestamp: Date.now()
      }));
    } catch (e) { /* ignore */ }
  }

  /**
   * Fetch latest exchange rates from Frankfurter API
   */
  async function fetchRates() {
    // Try cache first
    const cached = loadCachedRates();
    if (cached) {
      rates = cached;
      rates.USD = 1;
      return;
    }

    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error('API error');
      const data = await response.json();
      rates = data.rates || {};
      rates.USD = 1;
      cacheRates(rates);
    } catch (e) {
      // Fallback — keep USD = 1, others won't convert
      console.warn('Currency API unavailable, using USD only.');
      rates = { USD: 1 };
    }
  }

  /**
   * Convert a USD amount to the target currency
   * @param {number} usdAmount - The amount in USD
   * @param {string} [targetCode] - Target currency code (defaults to current)
   * @returns {string} Formatted price string
   */
  function convertPrice(usdAmount, targetCode) {
    const code = targetCode || currentCurrency;
    const rate = rates[code] || 1;
    const converted = usdAmount * rate;
    const info = CURRENCIES[code] || { symbol: code + ' ' };

    // Format with 2 decimal places (JPY gets 0)
    const decimals = (code === 'JPY') ? 0 : 2;
    return info.symbol + converted.toFixed(decimals);
  }

  /**
   * Get currency symbol for current selection
   */
  function getCurrencySymbol(code) {
    const info = CURRENCIES[code || currentCurrency];
    return info ? info.symbol : '$';
  }

  /**
   * Build the currency selector <select> element
   * @returns {HTMLSelectElement}
   */
  function buildCurrencySelector() {
    const select = document.createElement('select');
    select.id = 'currency-selector';
    select.className = 'currency-selector';
    select.setAttribute('aria-label', 'Select currency');

    const lang = (typeof getSavedLanguage === 'function') ? getSavedLanguage() : 'en';

    Object.keys(CURRENCIES).forEach(function (code) {
      const opt = document.createElement('option');
      opt.value = code;
      const info = CURRENCIES[code];
      opt.textContent = code + ' (' + info.symbol + ')';
      if (code === currentCurrency) opt.selected = true;
      select.appendChild(opt);
    });

    select.addEventListener('change', function () {
      currentCurrency = this.value;
      saveCurrency(currentCurrency);
      // Re-render prices on the page
      if (typeof window.onCurrencyChange === 'function') {
        window.onCurrencyChange(currentCurrency);
      }
    });

    return select;
  }

  /**
   * Initialize currency module
   */
  async function initCurrency() {
    currentCurrency = getSavedCurrency();
    await fetchRates();

    // Inject selector into filter section (index page) or place info
    const filterSection = document.getElementById('filter');
    if (filterSection && !document.getElementById('currency-selector')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'currency-wrapper';
      const label = document.createElement('label');
      label.setAttribute('for', 'currency-selector');
      label.className = 'currency-label';
      label.innerHTML = '<i data-lucide="banknote" style="width:16px;height:16px;vertical-align:-2px;margin-right:4px;"></i>';
      label.appendChild(document.createTextNode(
        (typeof t === 'function') ? t('currency.label') : 'Currency:'
      ));
      wrapper.appendChild(label);
      wrapper.appendChild(buildCurrencySelector());
      filterSection.appendChild(wrapper);

      // Re-render Lucide icons
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    // Also inject on place details page
    const placeInfo = document.querySelector('.place-info');
    if (placeInfo && !document.getElementById('currency-selector')) {
      // Will be handled after place loads via onCurrencyChange
    }
  }

  // Expose globally
  window.initCurrency = initCurrency;
  window.convertPrice = convertPrice;
  window.getCurrencySymbol = getCurrencySymbol;
  window.CURRENCIES = CURRENCIES;
})();
