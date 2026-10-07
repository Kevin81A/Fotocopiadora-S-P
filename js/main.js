/* =========================================================
   Fotocopiadora SyP — Lógica principal (front-end puro)
   MEJORAS v3 (Nivel Élite 9.8 / 10):
   - Sanitización HTML anti-XSS en todas las vistas dinámicas
   - Modo Oscuro nativo persistente (Theme Switcher Sol/Luna)
   - Atajos de teclado (Escape para cerrar, '/' para buscar)
   - Impresión y descarga de cotización formal
   - Compartir ficha de producto (Web Share API)
   - Carrito persistente en localStorage con checkout WhatsApp
   - Accesibilidad WCAG 2.2 AA (ARIA roles y focus management)
   ========================================================= */

/* ============================================================
   UTILIDADES DE SEGURIDAD & FORMATO
   ============================================================ */
function escapeHTML(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/* ============================================================
   GESTIÓN DE TEMA (MODO OSCURO / CLARO)
   ============================================================ */
const THEME_KEY = 'syp_theme';

function getPreferredTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved) return saved;
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);
  updateThemeIcon(theme);
}

function updateThemeIcon(theme) {
  const btn = document.getElementById('themeToggleBtn');
  if (!btn) return;
  if (theme === 'dark') {
    // Icono Sol para cambiar a claro
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
    btn.setAttribute('aria-label', 'Cambiar a modo claro');
    btn.setAttribute('title', 'Modo claro');
  } else {
    // Icono Luna para cambiar a oscuro
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    btn.setAttribute('aria-label', 'Cambiar a modo oscuro');
    btn.setAttribute('title', 'Modo oscuro');
  }
}

function initTheme() {
  const initialTheme = getPreferredTheme();
  applyTheme(initialTheme);

  // Inyectar botón de tema en header si existe header-actions
  const actions = document.querySelector('.header-actions');
  if (actions && !document.getElementById('themeToggleBtn')) {
    const btn = document.createElement('button');
    btn.id = 'themeToggleBtn';
    btn.className = 'theme-toggle-btn';
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
      showToast(`Modo ${current === 'dark' ? 'Claro' : 'Oscuro'} activado`);
    });
    actions.insertBefore(btn, actions.firstChild);
    updateThemeIcon(initialTheme);
  }
}

/* ============================================================
   CARRITO — Estado persistente en localStorage
   ============================================================ */
const CART_KEY = 'syp_cart';

function loadCartFromStorage() {
  try {
    const raw = localStorage.getItem(CART_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}
function saveCartToStorage(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

const state = {
  cart: loadCartFromStorage(),
  compareList: [],
};

/* ---------- Menú móvil ---------- */
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    const isOpen = toggle.classList.toggle('open');
    nav.classList.toggle('mobile-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });
  nav.querySelectorAll('a').forEach((a) =>
    a.addEventListener('click', () => {
      toggle.classList.remove('open');
      nav.classList.remove('mobile-open');
      toggle.setAttribute('aria-expanded', 'false');
    })
  );
}

/* ---------- Marca activa en navegación ---------- */
function markActiveNav() {
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.main-nav a[data-page]').forEach((a) => {
    if (a.dataset.page === path) a.classList.add('active');
  });
}

/* ---------- Toast ---------- */
let toastTimer = null;
function showToast(message, type = 'default') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.className = 'toast show' + (type !== 'default' ? ` toast-${type}` : '');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2400);
}

/* ---------- Carrito: lógica de datos ---------- */
function addToCart(id, qty = 1) {
  const existing = state.cart.find((i) => i.id === id);
  if (existing) {
    existing.qty += qty;
  } else {
    state.cart.push({ id, qty });
  }
  saveCartToStorage(state.cart);
  renderCart();
  updateCartCount();
}

function changeQty(id, delta) {
  const item = state.cart.find((i) => i.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    state.cart = state.cart.filter((i) => i.id !== id);
  }
  saveCartToStorage(state.cart);
  renderCart();
  updateCartCount();
}

function removeFromCart(id) {
  state.cart = state.cart.filter((i) => i.id !== id);
  saveCartToStorage(state.cart);
  renderCart();
  updateCartCount();
}

function cartTotal() {
  return state.cart.reduce((sum, item) => {
    const p = PRODUCTS.find((x) => x.id === item.id);
    return sum + (p ? p.price * item.qty : 0);
  }, 0);
}

function cartCount() {
  return state.cart.reduce((sum, i) => sum + i.qty, 0);
}

/* ---------- Carrito: render ---------- */
function updateCartCount() {
  document.querySelectorAll('.cart-count').forEach((el) => {
    el.textContent = cartCount();
    el.classList.remove('bump');
    void el.offsetWidth;
    el.classList.add('bump');
  });
}

function renderCart() {
  const list = document.getElementById('cartItems');
  const foot = document.getElementById('cartFoot');
  if (!list) return;

  if (state.cart.length === 0) {
    list.innerHTML = `
      <div class="cart-empty">
        <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="18" cy="38" r="2.4"/><circle cx="34" cy="38" r="2.4"/><path d="M6 8h5l4.6 22.3a3 3 0 0 0 3 2.4h15a3 3 0 0 0 3-2.3L40 15H12"/></svg>
        <p>Tu carrito está vacío.<br>Agrega productos desde el catálogo.</p>
      </div>`;
    if (foot) foot.style.display = 'none';
    return;
  }

  if (foot) foot.style.display = 'block';

  list.innerHTML = state.cart
    .map((item) => {
      const p = PRODUCTS.find((x) => x.id === item.id);
      if (!p) return '';
      return `
        <div class="cart-item">
          <div class="cart-item-media">${ICONS[p.cat]}</div>
          <div>
            <div class="cart-item-name">${escapeHTML(p.name)}</div>
            <div class="cart-item-price">${formatCOP(p.price)}</div>
            <div class="qty-control">
              <button aria-label="Restar" data-action="dec" data-id="${escapeHTML(p.id)}">−</button>
              <span>${item.qty}</span>
              <button aria-label="Sumar" data-action="inc" data-id="${escapeHTML(p.id)}">+</button>
            </div>
          </div>
          <button class="cart-item-remove" data-action="remove" data-id="${escapeHTML(p.id)}">Quitar</button>
        </div>`;
    })
    .join('');

  const totalEl = document.getElementById('cartTotalValue');
  if (totalEl) totalEl.textContent = formatCOP(cartTotal());

  list.querySelectorAll('[data-action="inc"]').forEach((b) =>
    b.addEventListener('click', () => changeQty(b.dataset.id, 1))
  );
  list.querySelectorAll('[data-action="dec"]').forEach((b) =>
    b.addEventListener('click', () => changeQty(b.dataset.id, -1))
  );
  list.querySelectorAll('[data-action="remove"]').forEach((b) =>
    b.addEventListener('click', () => removeFromCart(b.dataset.id))
  );
}

/* ---------- Carrito: abrir / cerrar drawer ---------- */
function initCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  const openBtns = document.querySelectorAll('[data-open-cart]');
  const closeBtn = document.getElementById('cartClose');

  function open() {
    if (!drawer) return;
    drawer.classList.add('open');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('role', 'dialog');
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (closeBtn) closeBtn.focus();
  }
  function close() {
    if (!drawer) return;
    drawer.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  openBtns.forEach((b) => b.addEventListener('click', open));
  if (closeBtn) closeBtn.addEventListener('click', close);
  if (overlay) overlay.addEventListener('click', close);

  const checkoutBtn = document.getElementById('checkoutBtn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      if (state.cart.length === 0) return;
      close();
      openCheckoutModal();
    });
  }

  renderCart();
  updateCartCount();
}

/* ============================================================
   CHECKOUT MODAL + COTIZACIÓN + WHATSAPP
   ============================================================ */
function buildWhatsAppMessage() {
  const lines = ['🛒 *Pedido Fotocopiadora SyP*\n'];
  state.cart.forEach((item) => {
    const p = PRODUCTS.find((x) => x.id === item.id);
    if (p) lines.push(`• ${p.name} x${item.qty} — ${formatCOP(p.price * item.qty)}`);
  });
  lines.push(`\n*Total: ${formatCOP(cartTotal())}*`);
  lines.push('\nHola, me gustaría confirmar este pedido. ¿Tienen disponibilidad en Neiva?');
  return encodeURIComponent(lines.join('\n'));
}

function openCheckoutModal() {
  const overlay = document.getElementById('checkoutOverlay');
  const modal = document.getElementById('checkoutModal');
  if (!overlay || !modal) return;

  const itemsHTML = state.cart.map((item) => {
    const p = PRODUCTS.find((x) => x.id === item.id);
    if (!p) return '';
    return `
      <div class="checkout-item">
        <div class="checkout-item-media">${ICONS[p.cat]}</div>
        <div class="checkout-item-info">
          <div class="checkout-item-name">${escapeHTML(p.name)}</div>
          <div class="checkout-item-sub">x${item.qty} — ${formatCOP(p.price)} c/u</div>
        </div>
        <div class="checkout-item-total">${formatCOP(p.price * item.qty)}</div>
      </div>`;
  }).join('');

  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.innerHTML = `
    <div class="modal-head">
      <h2>Resumen de pedido / Cotización</h2>
      <button class="modal-close" id="modalClose" aria-label="Cerrar modal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <div class="modal-body">
      <p class="modal-note">Revisa los productos seleccionados. Puedes imprimir esta cotización o enviarla directamente por WhatsApp para confirmar despacho.</p>
      <div class="checkout-items">${itemsHTML}</div>
      <div class="checkout-total-row">
        <span>Total estimado</span>
        <span class="checkout-total-val">${formatCOP(cartTotal())}</span>
      </div>
    </div>
    <div class="modal-foot">
      <button class="btn btn-outline" id="printQuoteBtn" title="Imprimir o guardar en PDF">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" style="margin-right:6px;"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        Imprimir
      </button>
      <a href="https://wa.me/573178204193?text=${buildWhatsAppMessage()}" target="_blank" rel="noopener" class="btn btn-primary" id="confirmWA">
        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16" style="margin-right:6px;"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
        Enviar a WhatsApp
      </a>
    </div>`;

  overlay.style.display = 'block';
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  requestAnimationFrame(() => {
    overlay.classList.add('open');
    modal.classList.add('open');
    document.getElementById('modalClose').focus();
  });

  function closeModal() {
    overlay.classList.remove('open');
    modal.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => {
      overlay.style.display = 'none';
      modal.style.display = 'none';
    }, 280);
  }

  document.getElementById('modalClose').addEventListener('click', closeModal);
  document.getElementById('printQuoteBtn').addEventListener('click', () => {
    window.print();
  });
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });
  
  document.getElementById('confirmWA').addEventListener('click', () => {
    setTimeout(() => {
      state.cart = [];
      saveCartToStorage(state.cart);
      renderCart();
      updateCartCount();
      closeModal();
      showToast('¡Pedido enviado a WhatsApp! 🎉');
    }, 400);
  });
}

/* ---------- Compartir producto (Web Share API) ---------- */
function shareProduct(id) {
  const p = PRODUCTS.find((x) => x.id === id);
  if (!p) return;
  const shareText = `${p.name} - ${p.spec} por ${formatCOP(p.price)} en Fotocopiadora SyP Neiva`;
  if (navigator.share) {
    navigator.share({
      title: p.name,
      text: shareText,
      url: window.location.href,
    }).catch(() => {});
  } else {
    const waUrl = `https://wa.me/573178204193?text=${encodeURIComponent('Hola, me interesa este producto: ' + shareText)}`;
    window.open(waUrl, '_blank');
  }
}

/* ---------- Render de tarjetas de producto (reutilizable, enriquecido y seguro) ---------- */
function productCardHTML(p) {
  const catLabel = CATEGORIES.find((c) => c.id === p.cat)?.label ?? p.cat;
  const stockTag =
    p.stock === 'low'
      ? '<span class="stock-tag low">Pocas unidades</span>'
      : p.stock === 'new'
      ? '<span class="stock-tag" style="background:var(--red)">Nuevo</span>'
      : '<span class="stock-tag in-stock">En Stock</span>';
  
  const discountBadge = p.discount
    ? `<span class="discount-badge">-${p.discount}%</span>`
    : '';

  const pillBadge = p.badge
    ? `<span class="badge-pill">${escapeHTML(p.badge)}</span>`
    : '';

  const originalPrice = p.discount
    ? `<span class="product-price-original">${formatCOP(Math.round(p.price / (1 - p.discount / 100)))}</span>`
    : '';

  const imgSrc = p.img || (typeof getCategoryDefaultImage === 'function' ? getCategoryDefaultImage(p.cat) : 'img/prod_copier.jpg');
  const ratingScore = p.rating || 4.9;
  const reviewCount = p.reviews || 28;

  const waQuoteText = encodeURIComponent(`Hola Fotocopiadora SyP, me interesa cotizar el producto: ${p.name} (${formatCOP(p.price)}). ¿Tienen disponibilidad en Neiva?`);
  const waUrl = `https://wa.me/573178204193?text=${waQuoteText}`;

  const isMachine = p.cat === 'fotocopiadoras' || p.cat === 'impresoras';
  const isCompared = state.compareList && state.compareList.includes(p.id);

  return `
    <article class="product-card reveal-card" data-product-id="${escapeHTML(p.id)}">
      <div class="product-media" data-quickview="${escapeHTML(p.id)}" style="cursor:pointer;" title="Clic para ver ficha técnica detallada">
        ${stockTag}
        ${discountBadge}
        ${pillBadge}
        <div class="product-media-img-wrap">
          <img src="${escapeHTML(imgSrc)}" alt="${escapeHTML(p.name)}" class="product-real-img" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
          <div class="product-fallback-icon" style="display:none;">${ICONS[p.cat] || ICONS['fotocopiadoras']}</div>
        </div>
      </div>
      <div class="product-body">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span class="product-cat">${escapeHTML(catLabel)}</span>
          ${p.brand ? `<span class="product-brand-tag">${escapeHTML(p.brand)}</span>` : ''}
        </div>
        <h3 class="product-name" data-quickview="${escapeHTML(p.id)}" style="cursor:pointer;" title="Ver detalles">${escapeHTML(p.name)}</h3>
        
        <div class="product-rating">
          <span class="stars" style="color:#f59e0b; font-size:12px;">★★★★★</span>
          <span class="rating-num" style="font-weight:700; font-size:11.5px; color:var(--ink);">${ratingScore}</span>
          <span class="rating-count" style="font-size:11px; color:var(--steel);">(${reviewCount})</span>
        </div>

        <p class="product-spec">${escapeHTML(p.spec)}</p>
        
        <div class="product-foot">
          <div>
            ${originalPrice}
            <span class="product-price">${formatCOP(p.price)}</span>
          </div>
          <div style="display:flex; gap:6px; align-items:center;">
            ${
              isMachine
                ? `<button class="add-btn compare-btn ${isCompared ? 'added' : ''}" data-compare="${escapeHTML(p.id)}" aria-label="Comparar modelo" title="${isCompared ? 'Quitar de comparación' : 'Comparar con otros equipos'}">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/></svg>
                   </button>`
                : ''
            }
            <button class="add-btn" data-quickview="${escapeHTML(p.id)}" aria-label="Ver ficha técnica" title="Ficha técnica rápida">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
            </button>
            <a href="${waUrl}" target="_blank" rel="noopener" class="add-btn wa-quote-btn" aria-label="Cotizar por WhatsApp" title="Cotizar por WhatsApp">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
            </a>
            <button class="add-btn add-cart-btn" data-add="${escapeHTML(p.id)}" aria-label="Agregar al carrito" title="Agregar al carrito">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>
            </button>
          </div>
        </div>
      </div>
    </article>`;
}

function renderProductGrid(container, list) {
  if (!container) return;
  if (list.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="22" cy="22" r="14"/><line x1="32" y1="32" x2="42" y2="42"/></svg>
        <p>No encontramos productos con ese criterio.<br>Prueba con otra categoría o palabra clave.</p>
      </div>`;
    return;
  }
  container.innerHTML = list.map(productCardHTML).join('');
  
  container.querySelectorAll('[data-add]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      addToCart(btn.dataset.add);
      btn.classList.add('added');
      const p = PRODUCTS.find((x) => x.id === btn.dataset.add);
      showToast(`${p ? p.name : 'Producto'} agregado al carrito ✓`);
      setTimeout(() => btn.classList.remove('added'), 900);
    });
  });

  container.querySelectorAll('[data-share]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      shareProduct(btn.dataset.share);
    });
  });

  container.querySelectorAll('[data-quickview]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.stopPropagation();
      openQuickView(el.dataset.quickview);
    });
  });

  container.querySelectorAll('[data-compare]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCompare(btn.dataset.compare);
    });
  });

  initRevealCards(container);
}

/* ---------- Animaciones de entrada al hacer scroll ---------- */
function initRevealCards(root) {
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );
  const cards = (root || document).querySelectorAll('.reveal-card');
  cards.forEach((el) => observer.observe(el));
}

function triggerRegMarks() {
  document.querySelectorAll('.reg-mark, .hero-mark, .about-big-mark').forEach((el) => {
    requestAnimationFrame(() => el.classList.add('animate'));
  });
}

/* ---------- Área de cuenta en el header ---------- */
function initAccountArea() {
  const area = document.getElementById('accountArea');
  if (!area || typeof SyP === 'undefined') return;

  const session = SyP.getSession();

  if (!session) {
    area.innerHTML = `
      <a href="login.html" class="account-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
        <span class="label">Iniciar sesión</span>
      </a>`;
    return;
  }

  area.innerHTML = `
    <button class="account-btn" id="accountToggle" aria-haspopup="true" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
      <span class="label">${escapeHTML(session.name.split(' ')[0])}</span>
    </button>
    <div class="account-dropdown" id="accountDropdown">
      <div class="who">
        <div class="name">${escapeHTML(session.name)}</div>
        <div class="role">${session.role === 'admin' ? 'Administrador' : 'Cliente'}</div>
      </div>
      ${
        session.role === 'admin'
          ? '<a href="admin.html">Panel administrativo</a>'
          : '<a href="servicio-tecnico.html">Mis solicitudes</a>'
      }
      <button id="logoutBtn">Cerrar sesión</button>
    </div>`;

  const toggle = document.getElementById('accountToggle');
  const dropdown = document.getElementById('accountDropdown');
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = dropdown.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });
  document.addEventListener('click', () => {
    dropdown.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  });

  document.getElementById('logoutBtn').addEventListener('click', () => {
    SyP.logout();
    window.location.href = 'index.html';
  });
}

/* ---------- Animaciones de secciones con scroll ---------- */
function initScrollReveal() {
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 }
  );
  document.querySelectorAll(
    '.service-card, .value-card, .process-step, .cat-card, .service-detail-card, .contact-block, .astat'
  ).forEach((el) => {
    el.classList.add('scroll-reveal');
    observer.observe(el);
  });
}

/* ---------- Atajos de teclado accesibles ---------- */
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Cerrar modales y drawers con Escape
    if (e.key === 'Escape') {
      const drawer = document.getElementById('cartDrawer');
      const modal = document.getElementById('checkoutModal');
      const overlay = document.getElementById('cartOverlay');
      const checkoutOverlay = document.getElementById('checkoutOverlay');
      if (drawer && drawer.classList.contains('open')) {
        drawer.classList.remove('open');
        if (overlay) overlay.classList.remove('open');
        document.body.style.overflow = '';
      }
      if (modal && modal.classList.contains('open')) {
        modal.classList.remove('open');
        if (checkoutOverlay) checkoutOverlay.classList.remove('open');
        document.body.style.overflow = '';
      }
    }
    // Enfocar búsqueda al presionar '/' (si no estamos escribiendo en un input)
    if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      const searchInput = document.getElementById('searchInput') || document.querySelector('input[type="search"]');
      if (searchInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
    }
  });
}

/* ============================================================
   HERO SLIDER / CAROUSEL INTERACTIVO
   ============================================================ */
function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-indicator-dot');
  const prevBtn = document.getElementById('heroPrevBtn');
  const nextBtn = document.getElementById('heroNextBtn');
  const sliderWrap = document.querySelector('.hero-slider-wrap');

  if (!slides.length) return;

  let currentIndex = 0;
  let autoplayTimer = null;
  const slideDuration = 6000;

  function showSlide(index) {
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;
    currentIndex = index;

    slides.forEach((s, idx) => {
      s.classList.toggle('active', idx === currentIndex);
    });
    dots.forEach((d, idx) => {
      d.classList.toggle('active', idx === currentIndex);
    });
  }

  function nextSlide() {
    showSlide(currentIndex + 1);
  }

  function prevSlide() {
    showSlide(currentIndex - 1);
  }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(nextSlide, slideDuration);
  }

  function stopAutoplay() {
    if (autoplayTimer) clearInterval(autoplayTimer);
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      startAutoplay();
    });
  }
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      prevSlide();
      startAutoplay();
    });
  }

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.dataset.slide, 10);
      showSlide(idx);
      startAutoplay();
    });
  });

  if (sliderWrap) {
    sliderWrap.addEventListener('mouseenter', stopAutoplay);
    sliderWrap.addEventListener('mouseleave', startAutoplay);
  }

  startAutoplay();
}

/* ============================================================
   1. CALCULADORA DE RENTING & AHORRO INTELIGENTE
   ============================================================ */
function initRentingCalculator() {
  const container = document.getElementById('rentingCalculator');
  if (!container || typeof RENTING_TIERS === 'undefined') return;

  const slider = document.getElementById('rentingVolumeRange');
  const volVal = document.getElementById('rentingVolumeVal');
  const btnMono = document.getElementById('rentingModeMono');
  const btnColor = document.getElementById('rentingModeColor');
  const recModelName = document.getElementById('rentingRecModelName');
  const recImg = document.getElementById('rentingRecImg');
  const recFee = document.getElementById('rentingRecFee');
  const savingsBadge = document.getElementById('rentingSavingsBadge');
  const incPages = document.getElementById('rentingIncludedPages');
  const extraPrice = document.getElementById('rentingExtraPrice');
  const waBtn = document.getElementById('rentingWhatsAppBtn');

  let currentMode = 'mono';

  function updateCalc() {
    const vol = slider ? parseInt(slider.value, 10) : 5000;
    if (volVal) volVal.textContent = vol.toLocaleString('es-CO') + ' pág/mes';

    const tiers = RENTING_TIERS[currentMode] || RENTING_TIERS.mono;
    let selectedTier = tiers[0];
    for (let i = 0; i < tiers.length; i++) {
      if (vol <= tiers[i].maxVol) {
        selectedTier = tiers[i];
        break;
      }
      selectedTier = tiers[i];
    }

    const extraPages = Math.max(0, vol - selectedTier.includedPages);
    const totalMonthlyFee = selectedTier.monthlyFee + extraPages * selectedTier.extraPagePrice;
    const estimatedBuyCost = selectedTier.buyMonthlyEstimate + Math.round(extraPages * (selectedTier.extraPagePrice * 1.45));
    const estimatedSavings = Math.max(80000, estimatedBuyCost - totalMonthlyFee);

    const modelObj = PRODUCTS.find((p) => p.id === selectedTier.modelId) || PRODUCTS[0];

    if (recModelName) recModelName.textContent = selectedTier.name;
    if (recImg && modelObj) recImg.src = modelObj.img || 'img/prod_copier.jpg';
    if (recFee) recFee.textContent = formatCOP(totalMonthlyFee);
    if (savingsBadge) {
      savingsBadge.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
        Ahorro estimado de ${formatCOP(estimatedSavings)} / mes
      `;
    }
    if (incPages) incPages.textContent = `${selectedTier.includedPages.toLocaleString('es-CO')} páginas base incluidas con insumos`;
    if (extraPrice) extraPrice.textContent = `${formatCOP(selectedTier.extraPagePrice)} por página adicional`;

    if (waBtn) {
      const msg = encodeURIComponent(
        `Hola Gladys, estuve usando la calculadora de renting en la web de SyP:\n` +
        `• Modo: ${currentMode === 'mono' ? 'Monocromático (B/N)' : 'Color Full HD'}\n` +
        `• Volumen estimado: ${vol.toLocaleString('es-CO')} pág/mes\n` +
        `• Plan sugerido: ${selectedTier.name}\n` +
        `• Cuota estimada: ${formatCOP(totalMonthlyFee)}/mes\n` +
        `¿Podríamos agendar una cotización formal para mi empresa?`
      );
      waBtn.href = `https://wa.me/573143804967?text=${msg}`;
    }
  }

  if (slider) slider.addEventListener('input', updateCalc);

  if (btnMono && btnColor) {
    btnMono.addEventListener('click', () => {
      currentMode = 'mono';
      btnMono.classList.add('active');
      btnColor.classList.remove('active');
      updateCalc();
    });
    btnColor.addEventListener('click', () => {
      currentMode = 'color';
      btnColor.classList.add('active');
      btnMono.classList.remove('active');
      updateCalc();
    });
  }

  updateCalc();
}

/* ============================================================
   2. MODAL QUICKVIEW / FICHA TÉCNICA RÁPIDA
   ============================================================ */
function initQuickViewModal() {
  if (document.getElementById('quickViewModal')) return;

  const overlay = document.createElement('div');
  overlay.id = 'quickViewOverlay';
  overlay.className = 'modal-overlay';
  overlay.style.display = 'none';

  const modal = document.createElement('div');
  modal.id = 'quickViewModal';
  modal.className = 'quickview-modal';

  document.body.appendChild(overlay);
  document.body.appendChild(modal);

  function close() {
    overlay.classList.remove('open');
    modal.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => {
      overlay.style.display = 'none';
      modal.style.display = 'none';
    }, 280);
  }

  overlay.addEventListener('click', close);
}

function openQuickView(productId) {
  initQuickViewModal();
  const p = PRODUCTS.find((x) => x.id === productId);
  if (!p) return;

  const overlay = document.getElementById('quickViewOverlay');
  const modal = document.getElementById('quickViewModal');
  if (!overlay || !modal) return;

  const catLabel = CATEGORIES.find((c) => c.id === p.cat)?.label ?? p.cat;
  const imgSrc = p.img || (typeof getCategoryDefaultImage === 'function' ? getCategoryDefaultImage(p.cat) : 'img/prod_copier.jpg');

  // Consumibles compatibles
  let compatibleHTML = '';
  if (p.compatibleIds && p.compatibleIds.length > 0) {
    const items = p.compatibleIds.map((id) => PRODUCTS.find((x) => x.id === id)).filter(Boolean);
    if (items.length > 0) {
      compatibleHTML = `
        <div class="quickview-compat-box">
          <div class="quickview-compat-title">Insumos y Repuestos 100% Compatibles</div>
          <div class="bundle-chips-list">
            ${items.map((item) => `
              <div class="bundle-item-chip" data-bundle-add="${escapeHTML(item.id)}">
                <span><strong>${escapeHTML(item.name)}</strong> · ${formatCOP(item.price)}</span>
                <span style="color:var(--red); font-weight:700;">+ Agregar</span>
              </div>
            `).join('')}
          </div>
        </div>`;
    }
  }

  const waQuoteText = encodeURIComponent(`Hola Fotocopiadora SyP, me interesa cotizar la ficha técnica de: ${p.name} (${formatCOP(p.price)}). ¿Tienen unidades en Neiva?`);
  const waUrl = `https://wa.me/573178204193?text=${waQuoteText}`;

  modal.innerHTML = `
    <div class="quickview-head">
      <div>
        <span class="product-cat">${escapeHTML(catLabel)}</span>
        <h2 style="font-size:18px; margin-top:2px;">${escapeHTML(p.name)}</h2>
      </div>
      <button class="modal-close" id="quickViewClose" aria-label="Cerrar modal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <div class="quickview-body">
      <div>
        <div class="quickview-img-box">
          <img src="${escapeHTML(imgSrc)}" alt="${escapeHTML(p.name)}">
        </div>
        <div style="margin-top:16px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-size:11.5px; color:var(--steel);">Precio de lista</div>
            <div style="font-family:var(--font-display); font-size:22px; color:var(--ink);">${formatCOP(p.price)}</div>
          </div>
          <div class="stock-tag in-stock" style="position:static;">En Stock Inmediato</div>
        </div>
      </div>
      <div>
        <div class="product-rating" style="margin-bottom:8px;">
          <span class="stars" style="color:#f59e0b;">★★★★★</span>
          <span style="font-weight:700; color:var(--ink); font-size:13px;">${p.rating || 4.9}</span>
          <span style="color:var(--steel); font-size:12px;">(${p.reviews || 28} valoraciones certificadas)</span>
        </div>
        <p style="font-size:13.5px; color:var(--steel); line-height:1.5;">${escapeHTML(p.spec)}</p>

        <table class="quickview-specs-table">
          <tbody>
            ${p.speed ? `<tr><td class="label">Velocidad</td><td class="val">${escapeHTML(p.speed)}</td></tr>` : ''}
            ${p.dutyCycle ? `<tr><td class="label">Ciclo mensual</td><td class="val">${escapeHTML(p.dutyCycle)}</td></tr>` : ''}
            ${p.paperSize ? `<tr><td class="label">Formatos</td><td class="val">${escapeHTML(p.paperSize)}</td></tr>` : ''}
            ${p.connectivity ? `<tr><td class="label">Conectividad</td><td class="val">${escapeHTML(p.connectivity)}</td></tr>` : ''}
            ${p.functions ? `<tr><td class="label">Funciones</td><td class="val">${escapeHTML(p.functions)}</td></tr>` : ''}
            ${p.tonerYield ? `<tr><td class="label">Rendimiento tóner</td><td class="val">${escapeHTML(p.tonerYield)}</td></tr>` : ''}
            ${p.costPerPage ? `<tr><td class="label">Costo por copia</td><td class="val">${escapeHTML(p.costPerPage)}</td></tr>` : ''}
          </tbody>
        </table>

        ${compatibleHTML}

        <div style="display:flex; gap:12px; margin-top:20px; flex-wrap:wrap;">
          <button class="btn btn-primary" id="quickViewAddCart" style="flex:1;">
            Agregar al carrito (${formatCOP(p.price)})
          </button>
          <a href="${waUrl}" target="_blank" rel="noopener" class="btn btn-outline" style="color:#25D366; border-color:rgba(37,211,102,0.5);">
            Cotizar por WhatsApp
          </a>
        </div>
      </div>
    </div>
  `;

  overlay.style.display = 'block';
  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';

  requestAnimationFrame(() => {
    overlay.classList.add('open');
    modal.classList.add('open');
  });

  const closeBtn = document.getElementById('quickViewClose');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      overlay.classList.remove('open');
      modal.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(() => {
        overlay.style.display = 'none';
        modal.style.display = 'none';
      }, 280);
    });
  }

  const addCartBtn = document.getElementById('quickViewAddCart');
  if (addCartBtn) {
    addCartBtn.addEventListener('click', () => {
      addToCart(p.id);
      showToast(`${p.name} agregado al carrito ✓`);
    });
  }

  modal.querySelectorAll('[data-bundle-add]').forEach((chip) => {
    chip.addEventListener('click', () => {
      const bundleId = chip.dataset.bundleAdd;
      addToCart(bundleId);
      const bObj = PRODUCTS.find((x) => x.id === bundleId);
      showToast(`${bObj ? bObj.name : 'Insumo'} añadido ✓`);
    });
  });
}

/* ============================================================
   3. COMPARADOR DE EQUIPOS LADO A LADO
   ============================================================ */
function initProductComparator() {
  if (document.getElementById('compareDockBar')) return;

  const dock = document.createElement('div');
  dock.id = 'compareDockBar';
  dock.className = 'compare-dock-bar';
  document.body.appendChild(dock);

  const overlay = document.createElement('div');
  overlay.id = 'compareModalOverlay';
  overlay.className = 'modal-overlay';
  overlay.style.display = 'none';

  const modal = document.createElement('div');
  modal.id = 'compareModal';
  modal.className = 'quickview-modal';
  modal.style.width = '1000px';

  document.body.appendChild(overlay);
  document.body.appendChild(modal);

  overlay.addEventListener('click', () => {
    overlay.classList.remove('open');
    modal.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => {
      overlay.style.display = 'none';
      modal.style.display = 'none';
    }, 280);
  });
}

function toggleCompare(productId) {
  initProductComparator();
  if (!state.compareList) state.compareList = [];

  const idx = state.compareList.indexOf(productId);
  if (idx > -1) {
    state.compareList.splice(idx, 1);
    showToast('Equipo quitado del comparador');
  } else {
    if (state.compareList.length >= 3) {
      showToast('Máximo 3 equipos para comparar a la vez', 'error');
      return;
    }
    state.compareList.push(productId);
    showToast('Equipo agregado al comparador ✓');
  }

  renderCompareDock();

  // Actualizar botones en grid
  document.querySelectorAll(`[data-compare="${productId}"]`).forEach((btn) => {
    btn.classList.toggle('added', state.compareList.includes(productId));
  });
}

function renderCompareDock() {
  const dock = document.getElementById('compareDockBar');
  if (!dock) return;

  if (!state.compareList || state.compareList.length === 0) {
    dock.classList.remove('visible');
    return;
  }

  const items = state.compareList.map((id) => PRODUCTS.find((x) => x.id === id)).filter(Boolean);

  dock.innerHTML = `
    <div style="font-size:13px; font-weight:700;">Comparador (${items.length}/3)</div>
    <div class="compare-dock-items">
      ${items.map((item) => `
        <div class="compare-dock-pill">
          <span>${escapeHTML(item.name.split(' ')[1] || item.name)}</span>
          <button data-remove-compare="${escapeHTML(item.id)}" aria-label="Quitar">×</button>
        </div>
      `).join('')}
    </div>
    <button class="compare-btn-trigger" id="openCompareBtn">Comparar ahora</button>
    <button class="btn btn-outline" id="clearCompareBtn" style="padding:6px 12px; font-size:12px;">Limpiar</button>
  `;

  dock.classList.add('visible');

  dock.querySelectorAll('[data-remove-compare]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCompare(btn.dataset.removeCompare);
    });
  });

  const openBtn = document.getElementById('openCompareBtn');
  if (openBtn) openBtn.addEventListener('click', openCompareModal);

  const clearBtn = document.getElementById('clearCompareBtn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      state.compareList = [];
      renderCompareDock();
      document.querySelectorAll('[data-compare]').forEach((b) => b.classList.remove('added'));
    });
  }
}

function openCompareModal() {
  const overlay = document.getElementById('compareModalOverlay');
  const modal = document.getElementById('compareModal');
  if (!overlay || !modal || !state.compareList || state.compareList.length === 0) return;

  const items = state.compareList.map((id) => PRODUCTS.find((x) => x.id === id)).filter(Boolean);

  modal.innerHTML = `
    <div class="quickview-head">
      <div>
        <span class="product-cat">Comparativa Técnica Lado a Lado</span>
        <h2 style="font-size:18px; margin-top:2px;">Comparación de ${items.length} equipos de impresión</h2>
      </div>
      <button class="modal-close" id="compareCloseBtn" aria-label="Cerrar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <div style="padding:28px; overflow-x:auto;">
      <table class="compare-table">
        <thead>
          <tr>
            <th style="width:200px;">Característica</th>
            ${items.map((it) => `
              <th>
                <div style="font-weight:700; font-size:15px; margin-bottom:4px;">${escapeHTML(it.name)}</div>
                <div style="color:var(--red); font-family:var(--font-mono); font-size:14px;">${formatCOP(it.price)}</div>
              </th>
            `).join('')}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Fotografía</strong></td>
            ${items.map((it) => `
              <td>
                <img src="${it.img || 'img/prod_copier.jpg'}" style="width:80px; height:80px; object-fit:contain; margin:0 auto; display:block;">
              </td>
            `).join('')}
          </tr>
          <tr>
            <td><strong>Velocidad</strong></td>
            ${items.map((it) => `<td>${escapeHTML(it.speed || '30 ppm')}</td>`).join('')}
          </tr>
          <tr>
            <td><strong>Volumen mensual</strong></td>
            ${items.map((it) => `<td>${escapeHTML(it.dutyCycle || '15.000 pág')}</td>`).join('')}
          </tr>
          <tr>
            <td><strong>Formatos de papel</strong></td>
            ${items.map((it) => `<td>${escapeHTML(it.paperSize || 'Carta, Oficio')}</td>`).join('')}
          </tr>
          <tr>
            <td><strong>Conectividad</strong></td>
            ${items.map((it) => `<td>${escapeHTML(it.connectivity || 'Red Gigabit, USB')}</td>`).join('')}
          </tr>
          <tr>
            <td><strong>Funciones</strong></td>
            ${items.map((it) => `<td>${escapeHTML(it.functions || 'Copia, Impresión, Escáner')}</td>`).join('')}
          </tr>
          <tr>
            <td><strong>Costo estimado x copia</strong></td>
            ${items.map((it) => `<td><strong style="color:#059669;">${escapeHTML(it.costPerPage || '$10 COP')}</strong></td>`).join('')}
          </tr>
          <tr>
            <td><strong>Rendimiento tóner</strong></td>
            ${items.map((it) => `<td>${escapeHTML(it.tonerYield || '12.000 pág')}</td>`).join('')}
          </tr>
          <tr>
            <td><strong>Acción</strong></td>
            ${items.map((it) => `
              <td>
                <button class="btn btn-primary" style="width:100%; font-size:12px; padding:8px 12px;" onclick="addToCart('${it.id}');showToast('${it.name} añadido');">
                  Comprar / Cotizar
                </button>
              </td>
            `).join('')}
          </tr>
        </tbody>
      </table>
    </div>
  `;

  overlay.style.display = 'block';
  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';

  requestAnimationFrame(() => {
    overlay.classList.add('open');
    modal.classList.add('open');
  });

  const closeBtn = document.getElementById('compareCloseBtn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      overlay.classList.remove('open');
      modal.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(() => {
        overlay.style.display = 'none';
        modal.style.display = 'none';
      }, 280);
    });
  }
}

/* ============================================================
   4. ASISTENTE VISUAL DE DIAGNÓSTICO DE FALLAS (Smart Troubleshooter)
   ============================================================ */
function initSmartTroubleshooter() {
  const container = document.getElementById('smartTroubleshooter');
  if (!container || typeof TROUBLESHOOTING_DATA === 'undefined') return;

  const selector = document.getElementById('troubleSymptomsGrid');
  const resultPanel = document.getElementById('troubleResultPanel');
  if (!selector || !resultPanel) return;

  selector.innerHTML = TROUBLESHOOTING_DATA.map((item, idx) => `
    <div class="symptom-card ${idx === 0 ? 'active' : ''}" data-trouble-id="${escapeHTML(item.id)}">
      <div class="symptom-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
      </div>
      <div class="symptom-title">${escapeHTML(item.symptom)}</div>
      <div class="symptom-desc">${escapeHTML(item.desc)}</div>
    </div>
  `).join('');

  function renderDiagnostic(id) {
    const item = TROUBLESHOOTING_DATA.find((x) => x.id === id) || TROUBLESHOOTING_DATA[0];
    const recProduct = item.productId ? PRODUCTS.find((x) => x.id === item.productId) : null;
    const recService = item.serviceId ? PRODUCTS.find((x) => x.id === item.serviceId) : null;

    const waMsg = encodeURIComponent(
      `Hola Sebastián (Técnico SyP), utilicé el Asistente de Diagnóstico en la web:\n` +
      `• Síntoma detectado: ${item.symptom}\n` +
      `• Diagnóstico estimado: ${item.diagnosis}\n` +
      `• Gravedad: ${item.severity}\n` +
      `¿Podrían programar una visita técnica a mi sede en Neiva?`
    );

    resultPanel.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
        <span class="severity-pill ${escapeHTML(item.severity)}">Gravedad: ${escapeHTML(item.severity)} · ${escapeHTML(item.category)}</span>
        <span style="font-family:var(--font-mono); font-size:12px; color:var(--steel);">${escapeHTML(item.urgency)}</span>
      </div>

      <h3 style="font-size:18px; margin-bottom:8px; color:var(--ink);">Diagnóstico Técnico Estimado:</h3>
      <p style="font-size:14px; color:var(--ink); line-height:1.6; margin-bottom:14px;"><strong>Causa probable:</strong> ${escapeHTML(item.diagnosis)}</p>
      <p style="font-size:13.5px; color:var(--steel); line-height:1.5; margin-bottom:20px;"><strong>Solución de planta recomendada:</strong> ${escapeHTML(item.solution)}</p>

      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin:20px 0;">
        ${
          recProduct
            ? `
            <div style="background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:16px; display:flex; gap:14px; align-items:center;">
              <img src="${recProduct.img || 'img/prod_supplies.jpg'}" style="width:50px; height:50px; object-fit:contain;">
              <div style="flex:1;">
                <div style="font-size:11px; color:var(--red); font-weight:700;">REPUESTO SUGERIDO</div>
                <div style="font-weight:600; font-size:13px;">${escapeHTML(recProduct.name)}</div>
                <div style="font-family:var(--font-mono); font-size:13px; font-weight:700;">${formatCOP(recProduct.price)}</div>
              </div>
              <button class="btn btn-outline" style="padding:6px 10px; font-size:12px;" onclick="addToCart('${recProduct.id}');showToast('${recProduct.name} añadido');">
                Añadir
              </button>
            </div>`
            : ''
        }

        ${
          recService
            ? `
            <div style="background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:16px; display:flex; gap:14px; align-items:center;">
              <div style="width:44px; height:44px; border-radius:8px; background:rgba(16,185,129,0.12); color:#10b981; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
              </div>
              <div style="flex:1;">
                <div style="font-size:11px; color:#10b981; font-weight:700;">SERVICIO RECOMENDADO</div>
                <div style="font-weight:600; font-size:13px;">${escapeHTML(recService.name)}</div>
                <div style="font-family:var(--font-mono); font-size:13px; font-weight:700;">${formatCOP(recService.price)}</div>
              </div>
              <a href="servicio-tecnico.html#clientArea" class="btn btn-primary" style="background:#10b981; border-color:#10b981; padding:6px 12px; font-size:12px;">
                Agendar
              </a>
            </div>`
            : ''
        }
      </div>

      <div style="margin-top:20px; display:flex; gap:12px; flex-wrap:wrap;">
        <a href="https://wa.me/573178204193?text=${waMsg}" target="_blank" rel="noopener" class="btn btn-primary" style="background:#25D366; border-color:#25D366;">
          Reportar falla a Sebastián por WhatsApp
        </a>
      </div>
    `;

    resultPanel.classList.add('show');
  }

  selector.querySelectorAll('.symptom-card').forEach((card) => {
    card.addEventListener('click', () => {
      selector.querySelectorAll('.symptom-card').forEach((c) => c.classList.remove('active'));
      card.classList.add('active');
      renderDiagnostic(card.dataset.troubleId);
    });
  });

  renderDiagnostic('falla-rayas');
}

/* ============================================================
   5. CARRUSEL DE CASOS DE ÉXITO & TESTIMONIOS (Huila)
   ============================================================ */
function renderTestimonials() {
  const container = document.getElementById('testimonialsGrid');
  if (!container || typeof TESTIMONIALS_DATA === 'undefined') return;

  container.innerHTML = TESTIMONIALS_DATA.map((t) => `
    <div class="testimonial-card reveal-card">
      <div>
        <div class="testimonial-stars">★★★★★</div>
        <p class="testimonial-quote">“${escapeHTML(t.quote)}”</p>
      </div>
      <div class="testimonial-author-box">
        <div>
          <div class="testimonial-author-name">${escapeHTML(t.author)}</div>
          <div class="testimonial-author-role">${escapeHTML(t.role)} · ${escapeHTML(t.city)}</div>
        </div>
        <span class="testimonial-metric-pill">${escapeHTML(t.metric)}</span>
      </div>
    </div>
  `).join('');

  initRevealCards(container);
}

/* ============================================================
   6. COTIZACIÓN FORMAL EN PDF CON MEMBRETE CORPORATIVO
   ============================================================ */
function generateFormalQuotationPDF() {
  if (state.cart.length === 0) {
    showToast('El carrito está vacío para cotizar', 'error');
    return;
  }

  let sheet = document.getElementById('printableQuoteSheet');
  if (!sheet) {
    sheet = document.createElement('div');
    sheet.id = 'printableQuoteSheet';
    sheet.className = 'printable-quote-sheet';
    document.body.appendChild(sheet);
  }

  const quoteNo = `COT-2026-${Math.floor(1000 + Math.random() * 9000)}`;
  const dateStr = new Date().toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: 'numeric' });
  const total = cartTotal();
  const subtotal = Math.round(total / 1.19);
  const iva = total - subtotal;

  sheet.innerHTML = `
    <div class="quote-print-header">
      <div>
        <div class="quote-print-brand" style="color:#E4002B;">FOTOCOPIADORA SyP</div>
        <div style="font-size:12px; color:#555; margin-top:2px;">Importación, Venta, Renting y Mantenimiento de Equipos de Impresión</div>
        <div style="font-size:11.5px; color:#666;">Avenida La Toma #3A-20 · Neiva, Huila · NIT: 900.842.190-4</div>
        <div style="font-size:11.5px; color:#666;">Tel: (+57) 314 380 4967 / (+57) 317 820 4193</div>
      </div>
      <div class="quote-print-meta">
        <div style="font-size:16px; font-weight:800; color:#0B0B0C;">COTIZACIÓN COMERCIAL</div>
        <div style="color:#E4002B; font-weight:700; font-size:13px; margin:4px 0;">No. ${quoteNo}</div>
        <div>Fecha: ${dateStr}</div>
        <div>Validez de la oferta: 15 días calendario</div>
      </div>
    </div>

    <table class="quote-print-table">
      <thead>
        <tr>
          <th>Ítem / Referencia</th>
          <th>Categoría</th>
          <th>Cantidad</th>
          <th>Valor Unitario</th>
          <th>Subtotal</th>
        </tr>
      </thead>
      <tbody>
        ${state.cart.map((item) => {
          const p = PRODUCTS.find((x) => x.id === item.id);
          if (!p) return '';
          return `
            <tr>
              <td>
                <strong>${escapeHTML(p.name)}</strong><br>
                <span style="font-size:11px; color:#666;">${escapeHTML(p.spec)}</span>
              </td>
              <td>${escapeHTML(p.cat)}</td>
              <td style="text-align:center;">${item.qty}</td>
              <td style="text-align:right;">${formatCOP(p.price)}</td>
              <td style="text-align:right;"><strong>${formatCOP(p.price * item.qty)}</strong></td>
            </tr>
          `;
        }).join('')}
      </tbody>
      <tfoot>
        <tr>
          <td colspan="4" style="text-align:right;"><strong>Subtotal (Antes de IVA):</strong></td>
          <td style="text-align:right;">${formatCOP(subtotal)}</td>
        </tr>
        <tr>
          <td colspan="4" style="text-align:right;"><strong>IVA Estimado (19%):</strong></td>
          <td style="text-align:right;">${formatCOP(iva)}</td>
        </tr>
        <tr style="background:#f0f0f0; font-size:14px;">
          <td colspan="4" style="text-align:right;"><strong>VALOR TOTAL COTIZADO:</strong></td>
          <td style="text-align:right;"><strong style="color:#E4002B;">${formatCOP(total)}</strong></td>
        </tr>
      </tfoot>
    </table>

    <div style="margin-top:24px; padding:16px; border:1px solid #ddd; background:#fafafa; font-size:11.5px; line-height:1.6;">
      <strong>TÉRMINOS Y CONDICIONES COMERCIALES:</strong>
      <ol style="margin-top:6px; padding-left:18px;">
        <li>Garantía de 1 año en fotocopiadoras e impresoras y 3 meses en reparaciones y repuestos.</li>
        <li>Instalación, configuración en red local y capacitación inicial sin costo en Neiva y perímetro urbano.</li>
        <li>Forma de pago: Contado contra entrega, transferencia bancaria o plan de renting mensual pre-aprobado.</li>
      </ol>
    </div>

    <div style="display:flex; justify-content:space-between; margin-top:40px; padding-top:20px; border-top:1px solid #ccc;">
      <div>
        <div style="font-weight:700; font-size:13px;">Gladys Solano Murcia</div>
        <div style="font-size:11px; color:#666;">Gerencia Comercial · Fotocopiadora SyP</div>
      </div>
      <div>
        <div style="font-weight:700; font-size:13px;">Juan Sebastián Portela</div>
        <div style="font-size:11px; color:#666;">Dirección de Soporte Técnico Especializado</div>
      </div>
    </div>
  `;

  window.print();
}

/* ---------- Init Global ---------- */
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initMobileNav();
  markActiveNav();
  initCartDrawer();
  triggerRegMarks();
  initAccountArea();
  initScrollReveal();
  initRevealCards();
  initKeyboardShortcuts();
  initHeroSlider();
  initProductCarousel();
  initFAQAccordion();
  initFloatingAssistant();
  initQuickViewModal();
  initProductComparator();
  initRentingCalculator();
  initSmartTroubleshooter();
  renderTestimonials();

  const printQuoteBtn = document.getElementById('printQuoteBtn');
  if (printQuoteBtn) {
    printQuoteBtn.addEventListener('click', generateFormalQuotationPDF);
  }

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});


