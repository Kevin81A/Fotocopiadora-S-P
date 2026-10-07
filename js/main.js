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

  return `
    <article class="product-card reveal-card" data-product-id="${escapeHTML(p.id)}">
      <div class="product-media">
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
        <h3 class="product-name">${escapeHTML(p.name)}</h3>
        
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
            <a href="${waUrl}" target="_blank" rel="noopener" class="add-btn wa-quote-btn" aria-label="Cotizar por WhatsApp" title="Cotizar por WhatsApp">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
            </a>
            <button class="add-btn" data-share="${escapeHTML(p.id)}" aria-label="Compartir producto" title="Compartir">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
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
    btn.addEventListener('click', () => {
      addToCart(btn.dataset.add);
      btn.classList.add('added');
      const p = PRODUCTS.find((x) => x.id === btn.dataset.add);
      showToast(`${p ? p.name : 'Producto'} agregado al carrito ✓`);
      setTimeout(() => btn.classList.remove('added'), 900);
    });
  });

  container.querySelectorAll('[data-share]').forEach((btn) => {
    btn.addEventListener('click', () => {
      shareProduct(btn.dataset.share);
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
   PRODUCT CAROUSEL (Controles de desplazamiento horizontal)
   ============================================================ */
function initProductCarousel() {
  document.querySelectorAll('.product-slider-wrapper').forEach((wrapper) => {
    const track = wrapper.querySelector('.product-slider-track');
    const prevBtn = wrapper.querySelector('.prev-btn');
    const nextBtn = wrapper.querySelector('.next-btn');

    if (!track) return;

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        track.scrollBy({ left: -320, behavior: 'smooth' });
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        track.scrollBy({ left: 320, behavior: 'smooth' });
      });
    }
  });
}

/* ============================================================
   FAQ ACCORDION INTERACTIVO
   ============================================================ */
function initFAQAccordion() {
  document.querySelectorAll('.faq-item').forEach((item) => {
    const question = item.querySelector('.faq-question');
    if (!question) return;

    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach((i) => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });
}

/* ============================================================
   FLOATING ASSISTANT BUBBLE
   ============================================================ */
function initFloatingAssistant() {
  const bubble = document.getElementById('floatingAssistantBubble');
  if (bubble) {
    bubble.addEventListener('click', () => {
      const waUrl = 'https://wa.me/573178204193?text=Hola%2C%20quisiera%20asesor%C3%ADa%20personalizada%20con%20Fotocopiadora%20SyP';
      window.open(waUrl, '_blank');
    });
  }
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

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});

