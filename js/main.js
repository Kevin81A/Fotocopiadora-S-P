/* =========================================================
   FOTOCOPIADORAS SyP — Lógica principal (front-end puro)
   MEJORAS v2:
   - Carrito persistente en localStorage (sobrevive navegación)
   - Checkout real: abre WhatsApp con resumen del pedido
   - Modal de checkout con resumen antes de confirmar
   - Animaciones de entrada al hacer scroll (Intersection Observer)
   ========================================================= */

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

// Estado global del carrito (cargado desde localStorage)
const state = {
  cart: loadCartFromStorage(),
};

/* ---------- Menú móvil ---------- */
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    toggle.classList.toggle('open');
    nav.classList.toggle('mobile-open');
  });
  nav.querySelectorAll('a').forEach((a) =>
    a.addEventListener('click', () => {
      toggle.classList.remove('open');
      nav.classList.remove('mobile-open');
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
    // Pulso visual al cambiar
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
            <div class="cart-item-name">${p.name}</div>
            <div class="cart-item-price">${formatCOP(p.price)}</div>
            <div class="qty-control">
              <button aria-label="Restar" data-action="dec" data-id="${p.id}">−</button>
              <span>${item.qty}</span>
              <button aria-label="Sumar" data-action="inc" data-id="${p.id}">+</button>
            </div>
          </div>
          <button class="cart-item-remove" data-action="remove" data-id="${p.id}">Quitar</button>
        </div>`;
    })
    .join('');

  const totalEl = document.getElementById('cartTotalValue');
  if (totalEl) totalEl.textContent = formatCOP(cartTotal());

  // listeners de los controles
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
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
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

  /* ---------- Checkout: abre modal con resumen + WhatsApp ---------- */
  const checkoutBtn = document.getElementById('checkoutBtn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      if (state.cart.length === 0) return;
      close(); // cerrar drawer primero
      openCheckoutModal();
    });
  }

  renderCart();
  updateCartCount();
}

/* ============================================================
   CHECKOUT MODAL + WHATSAPP
   ============================================================ */
function buildWhatsAppMessage() {
  const lines = ['🛒 *Pedido SyP Fotocopiadoras*\n'];
  state.cart.forEach((item) => {
    const p = PRODUCTS.find((x) => x.id === item.id);
    if (p) lines.push(`• ${p.name} x${item.qty} — ${formatCOP(p.price * item.qty)}`);
  });
  lines.push(`\n*Total: ${formatCOP(cartTotal())}*`);
  lines.push('\nHola, me gustaría confirmar este pedido. ¿Tienen disponibilidad?');
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
          <div class="checkout-item-name">${p.name}</div>
          <div class="checkout-item-sub">x${item.qty} — ${formatCOP(p.price)} c/u</div>
        </div>
        <div class="checkout-item-total">${formatCOP(p.price * item.qty)}</div>
      </div>`;
  }).join('');

  modal.innerHTML = `
    <div class="modal-head">
      <h2>Confirmar pedido</h2>
      <button class="modal-close" id="modalClose" aria-label="Cerrar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <div class="modal-body">
      <p class="modal-note">Revisa tu pedido. Al confirmar te redirigiremos a WhatsApp con un resumen listo para enviarnos.</p>
      <div class="checkout-items">${itemsHTML}</div>
      <div class="checkout-total-row">
        <span>Total</span>
        <span class="checkout-total-val">${formatCOP(cartTotal())}</span>
      </div>
    </div>
    <div class="modal-foot">
      <button class="btn btn-outline" id="modalCancel">Volver al carrito</button>
      <a href="https://wa.me/573145046459?text=${buildWhatsAppMessage()}" target="_blank" rel="noopener" class="btn btn-primary" id="confirmWA">
        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
        Confirmar por WhatsApp
      </a>
    </div>`;

  overlay.style.display = 'block';
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  requestAnimationFrame(() => {
    overlay.classList.add('open');
    modal.classList.add('open');
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
  document.getElementById('modalCancel').addEventListener('click', () => {
    closeModal();
    // Reabrir carrito
    setTimeout(() => {
      document.getElementById('cartDrawer').classList.add('open');
      document.getElementById('cartOverlay').classList.add('open');
      document.body.style.overflow = 'hidden';
    }, 300);
  });
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });
  // Tras confirmar → limpiar carrito
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

/* ---------- Render de tarjetas de producto (reutilizable) ---------- */
function productCardHTML(p) {
  const catLabel = CATEGORIES.find((c) => c.id === p.cat)?.label ?? p.cat;
  const stockTag =
    p.stock === 'low'
      ? '<span class="stock-tag low">Pocas unidades</span>'
      : p.stock === 'new'
      ? '<span class="stock-tag" style="background:var(--red)">Nuevo</span>'
      : '';
  const discountBadge = p.discount
    ? `<span class="discount-badge">-${p.discount}%</span>`
    : '';
  const originalPrice = p.discount
    ? `<span class="product-price-original">${formatCOP(Math.round(p.price / (1 - p.discount / 100)))}</span>`
    : '';
  return `
    <article class="product-card reveal-card">
      <div class="product-media">
        ${stockTag}
        ${discountBadge}
        ${ICONS[p.cat]}
      </div>
      <div class="product-body">
        <span class="product-cat">${catLabel}</span>
        <h3 class="product-name">${p.name}</h3>
        <p class="product-spec">${p.spec}</p>
        <div class="product-foot">
          <div>
            ${originalPrice}
            <span class="product-price">${formatCOP(p.price)}</span>
          </div>
          <button class="add-btn" data-add="${p.id}" aria-label="Agregar al carrito">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>
          </button>
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
      showToast(`${p.name} agregado al carrito ✓`);
      setTimeout(() => btn.classList.remove('added'), 900);
    });
  });
  // Aplicar animaciones de entrada
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

/* ---------- Animación de marca de registro al cargar ---------- */
function triggerRegMarks() {
  document.querySelectorAll('.reg-mark, .hero-mark, .about-big-mark').forEach((el) => {
    requestAnimationFrame(() => el.classList.add('animate'));
  });
}

/* ---------- Área de cuenta en el header (login / rol) ---------- */
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
    <button class="account-btn" id="accountToggle">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
      <span class="label">${session.name.split(' ')[0]}</span>
    </button>
    <div class="account-dropdown" id="accountDropdown">
      <div class="who">
        <div class="name">${session.name}</div>
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
    dropdown.classList.toggle('open');
  });
  document.addEventListener('click', () => dropdown.classList.remove('open'));

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

/* ---------- Init ---------- */
document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  markActiveNav();
  initCartDrawer();
  triggerRegMarks();
  initAccountArea();
  initScrollReveal();
  initRevealCards();

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
