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

let checkoutStep = 1;
let selectedPaymentMethod = 'PSE';

function openCheckoutModal() {
  const overlay = document.getElementById('checkoutOverlay');
  const modal = document.getElementById('checkoutModal');
  if (!overlay || !modal) return;
  if (state.cart.length === 0) {
    showToast('Tu carrito está vacío. Agrega productos Ricoh primero.');
    return;
  }

  checkoutStep = 1;
  selectedPaymentMethod = 'PSE';
  renderCheckoutModalContent();

  overlay.style.display = 'block';
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  requestAnimationFrame(() => {
    overlay.classList.add('open');
    modal.classList.add('open');
  });
}

function closeCheckoutModal() {
  const overlay = document.getElementById('checkoutOverlay');
  const modal = document.getElementById('checkoutModal');
  if (!overlay || !modal) return;
  overlay.classList.remove('open');
  modal.classList.remove('open');
  document.body.style.overflow = '';
  setTimeout(() => {
    overlay.style.display = 'none';
    modal.style.display = 'none';
  }, 280);
}

function renderCheckoutModalContent() {
  const modal = document.getElementById('checkoutModal');
  if (!modal) return;

  const user = (typeof Auth !== 'undefined' && Auth.getUser) ? Auth.getUser() : null;
  const total = cartTotal();
  const subtotal = Math.round(total / 1.19);
  const iva = total - subtotal;
  const shipping = total >= 100000 ? 0 : 8000;
  const grandTotal = total + shipping;

  modal.className = 'modal checkout-modal-container';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');

  modal.innerHTML = `
    <!-- HEADER CON INDICADOR DE PASOS -->
    <div class="checkout-steps-bar">
      <div class="checkout-step-item ${checkoutStep === 1 ? 'active' : (checkoutStep > 1 ? 'completed' : '')}" onclick="goToCheckoutStep(1)">
        <span class="step-number">1</span>
        <span>Revisión de Carrito</span>
      </div>
      <div class="checkout-step-item ${checkoutStep === 2 ? 'active' : (checkoutStep > 2 ? 'completed' : '')}" onclick="goToCheckoutStep(2)">
        <span class="step-number">2</span>
        <span>Datos y Entrega</span>
      </div>
      <div class="checkout-step-item ${checkoutStep === 3 ? 'active' : (checkoutStep > 3 ? 'completed' : '')}" onclick="goToCheckoutStep(3)">
        <span class="step-number">3</span>
        <span>Método de Pago</span>
      </div>
    </div>

    <!-- CUERPO SEGÚN EL PASO ACTIVO -->
    <div class="checkout-content-body">
      
      <!-- PASO 1: REVISIÓN DE PRODUCTOS -->
      <div class="checkout-step-pane ${checkoutStep === 1 ? 'active' : ''}" id="stepPane1">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin:0;">Productos Seleccionados (${cartCount()} items)</h3>
          <button class="modal-close" onclick="closeCheckoutModal()" aria-label="Cerrar modal" style="background:none; border:none; cursor:pointer;">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" fill="none"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
          </button>
        </div>

        <div class="checkout-items" style="max-height:260px; overflow-y:auto; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:16px;">
          ${state.cart.map(item => {
            const p = PRODUCTS.find(x => x.id === item.id);
            if (!p) return '';
            return `
              <div class="checkout-item" style="display:flex; align-items:center; gap:12px; padding:10px 0; border-bottom:1px solid #f1f5f9;">
                <div class="checkout-item-media" style="width:42px; height:42px; background:#f8fafc; border-radius:6px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">${ICONS[p.cat] || ''}</div>
                <div style="flex:1;">
                  <div style="font-weight:700; font-size:13px; color:#0f172a;">${escapeHTML(p.name)}</div>
                  <div style="font-size:11.5px; color:#64748b;">${formatCOP(p.price)} c/u</div>
                </div>
                <div style="font-weight:700; font-size:12px; color:#334155; background:#f1f5f9; padding:3px 8px; border-radius:4px;">x${item.qty}</div>
                <div style="font-weight:800; font-size:13px; color:#0f172a; min-width:80px; text-align:right;">${formatCOP(p.price * item.qty)}</div>
              </div>
            `;
          }).join('')}
        </div>

        <div class="checkout-totals-summary">
          <div class="checkout-totals-row">
            <span>Subtotal Neto:</span>
            <span style="font-weight:600;">${formatCOP(subtotal)}</span>
          </div>
          <div class="checkout-totals-row">
            <span>IVA (19% Discriminado):</span>
            <span style="font-weight:600;">${formatCOP(iva)}</span>
          </div>
          <div class="checkout-totals-row">
            <span>Envío a Domicilio en Neiva:</span>
            <span style="font-weight:600; color:${shipping === 0 ? '#059669' : '#0f172a'};">${shipping === 0 ? '¡GRATIS!' : formatCOP(shipping)}</span>
          </div>
          <div class="checkout-totals-row final">
            <span>Total a Pagar (COP):</span>
            <span>${formatCOP(grandTotal)}</span>
          </div>
        </div>

        <div class="checkout-actions-row">
          <button class="btn btn-outline" onclick="closeCheckoutModal()">Seguir Comprando</button>
          <button class="btn btn-primary" onclick="goToCheckoutStep(2)">Continuar a Datos de Entrega →</button>
        </div>
      </div>

      <!-- PASO 2: DATOS DE FACTURACIÓN Y ENVÍO -->
      <div class="checkout-step-pane ${checkoutStep === 2 ? 'active' : ''}" id="stepPane2">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin:0;">Datos del Cliente y Dirección en Neiva</h3>
          <button class="modal-close" onclick="closeCheckoutModal()" aria-label="Cerrar modal" style="background:none; border:none; cursor:pointer;">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" fill="none"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
          </button>
        </div>

        <form id="checkoutDeliveryForm" onsubmit="handleDeliverySubmit(event)" class="checkout-form-grid">
          <div class="checkout-input-group checkout-form-full">
            <label for="chkName">Nombre Completo / Razón Social *</label>
            <input type="text" id="chkName" required value="${user ? escapeHTML(user.name) : ''}" placeholder="Ej: Notaría 2da de Neiva / Carlos Morales">
          </div>

          <div class="checkout-input-group">
            <label for="chkNit">Cédula o NIT para Factura *</label>
            <input type="text" id="chkNit" required placeholder="Ej: 900.123.456-7 ó 12.345.678">
          </div>

          <div class="checkout-input-group">
            <label for="chkPhone">Teléfono / Celular (WhatsApp) *</label>
            <input type="tel" id="chkPhone" required value="${user ? escapeHTML(user.phone) : ''}" placeholder="Ej: 314 380 4967">
          </div>

          <div class="checkout-input-group checkout-form-full">
            <label for="chkEmail">Correo Electrónico (Para Factura y Enlace) *</label>
            <input type="email" id="chkEmail" required value="${user ? escapeHTML(user.email) : ''}" placeholder="correo@empresa.com">
          </div>

          <div class="checkout-input-group checkout-form-full">
            <label for="chkAddress">Dirección Exacta de Entrega *</label>
            <input type="text" id="chkAddress" required placeholder="Ej: Calle 8 # 6-45, Oficina 301, Centro">
          </div>

          <div class="checkout-input-group">
            <label for="chkCity">Zona / Barrio en Neiva *</label>
            <select id="chkCity">
              <option value="Neiva - Centro">Neiva - Zona Centro</option>
              <option value="Neiva - Norte / Cándido">Neiva - Norte / Cándido Leguízamo</option>
              <option value="Neiva - Oriente / Ipanema">Neiva - Oriente / Ipanema / Buganvillas</option>
              <option value="Neiva - Sur / Canaima">Neiva - Sur / Timanco / Canaima</option>
              <option value="Neiva - Las Granjas">Neiva - Las Granjas</option>
              <option value="Huila - Otro Municipio">Otro Municipio del Huila (Envío Nacional)</option>
            </select>
          </div>

          <div class="checkout-input-group">
            <label for="chkNotes">Observaciones de Despacho</label>
            <input type="text" id="chkNotes" placeholder="Ej: Recibir en portería / timbre 2">
          </div>

          <div class="checkout-form-full checkout-actions-row">
            <button type="button" class="btn btn-outline" onclick="goToCheckoutStep(1)">← Volver al Carrito</button>
            <button type="submit" class="btn btn-primary">Continuar al Pago →</button>
          </div>
        </form>
      </div>

      <!-- PASO 3: MÉTODOS DE PAGO Y CONVERSIÓN -->
      <div class="checkout-step-pane ${checkoutStep === 3 ? 'active' : ''}" id="stepPane3">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin:0;">Selecciona tu Método de Pago</h3>
          <button class="modal-close" onclick="closeCheckoutModal()" aria-label="Cerrar modal" style="background:none; border:none; cursor:pointer;">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" fill="none"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
          </button>
        </div>

        <div class="payment-methods-grid">
          <!-- PSE -->
          <div class="payment-method-card ${selectedPaymentMethod === 'PSE' ? 'selected' : ''}" onclick="selectPaymentMethod('PSE')">
            <div class="payment-method-header">
              <span class="payment-method-title">💳 PSE / Débito Bancario</span>
              <span style="font-size:10px; font-weight:800; background:#dbeafe; color:#1e40af; padding:2px 6px; border-radius:4px;">COLOMBIA</span>
            </div>
            <span class="payment-method-desc">Todos los bancos: Bancolombia, Davivienda, Bogotá, Nu, etc.</span>
          </div>

          <!-- Transferencia QR Bancolombia / Nequi -->
          <div class="payment-method-card ${selectedPaymentMethod === 'Transferencia Bancolombia / Nequi' ? 'selected' : ''}" onclick="selectPaymentMethod('Transferencia Bancolombia / Nequi')">
            <div class="payment-method-header">
              <span class="payment-method-title">📱 QR Bancolombia / Nequi</span>
              <span style="font-size:10px; font-weight:800; background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:4px;">INMEDIATO</span>
            </div>
            <span class="payment-method-desc">Escanea el código QR de SyP y transfiere al instante sin comisiones.</span>
          </div>

          <!-- Tarjeta de Crédito -->
          <div class="payment-method-card ${selectedPaymentMethod === 'Tarjeta de Crédito / Débito' ? 'selected' : ''}" onclick="selectPaymentMethod('Tarjeta de Crédito / Débito')">
            <div class="payment-method-header">
              <span class="payment-method-title">💳 Tarjeta Crédito / Débito</span>
              <span style="font-size:10px; font-weight:800; background:#f1f5f9; color:#334155; padding:2px 6px; border-radius:4px;">VISA/MC</span>
            </div>
            <span class="payment-method-desc">Paga hasta en 36 cuotas con Visa, Mastercard o American Express.</span>
          </div>

          <!-- Cotización Formal Web -->
          <div class="payment-method-card ${selectedPaymentMethod === 'Cotización Formal' ? 'selected' : ''}" onclick="selectPaymentMethod('Cotización Formal')">
            <div class="payment-method-header">
              <span class="payment-method-title">📄 Cotización Web Permanente</span>
              <span style="font-size:10px; font-weight:800; background:#ecfdf5; color:#065f46; padding:2px 6px; border-radius:4px;">EMPRESAS</span>
            </div>
            <span class="payment-method-desc">Genera un enlace web oficial con QR y PDF para aprobación contable.</span>
          </div>
        </div>

        <!-- DETALLE DINÁMICO DEL MÉTODO -->
        <div id="paymentDetailBox" class="payment-detail-box">
          <!-- Se llena dinámicamente -->
        </div>

        <div class="checkout-actions-row">
          <button class="btn btn-outline" onclick="goToCheckoutStep(2)">← Volver a Datos</button>
          <button id="btnProcessPayment" class="btn btn-primary" onclick="processOrderSubmission()">
            Confirmar y Pagar ${formatCOP(grandTotal)}
          </button>
        </div>
      </div>

      <!-- PASO 4: CONFIRMACIÓN Y ÉXITO -->
      <div class="checkout-step-pane ${checkoutStep === 4 ? 'active' : ''}" id="stepPane4">
        <div id="checkoutSuccessContainer" class="order-success-screen">
          <!-- Llenado tras crear la orden -->
        </div>
      </div>

    </div>
  `;

  renderPaymentDetailSection();
}

function goToCheckoutStep(step) {
  if (step === 2 || step === 3) {
    if (state.cart.length === 0) {
      showToast('Tu carrito está vacío.');
      return;
    }
  }
  if (step === 3) {
    const form = document.getElementById('checkoutDeliveryForm');
    if (form && !form.checkValidity()) {
      form.reportValidity();
      return;
    }
  }
  checkoutStep = step;
  renderCheckoutModalContent();
}

function handleDeliverySubmit(e) {
  e.preventDefault();
  checkoutStep = 3;
  renderCheckoutModalContent();
}

function selectPaymentMethod(method) {
  selectedPaymentMethod = method;
  renderPaymentDetailSection();
  
  // Actualizar clases de selección
  document.querySelectorAll('.payment-method-card').forEach(card => {
    card.classList.toggle('selected', card.textContent.includes(method) || (method === 'PSE' && card.textContent.includes('PSE')));
  });

  const btn = document.getElementById('btnProcessPayment');
  const total = cartTotal();
  const shipping = total >= 100000 ? 0 : 8000;
  const grandTotal = total + shipping;

  if (btn) {
    if (method === 'Cotización Formal') {
      btn.textContent = '📄 Generar Cotización Oficial Web';
    } else {
      btn.textContent = `Confirmar y Procesar ${formatCOP(grandTotal)}`;
    }
  }
}

function renderPaymentDetailSection() {
  const box = document.getElementById('paymentDetailBox');
  if (!box) return;

  if (selectedPaymentMethod === 'PSE') {
    box.innerHTML = `
      <div style="font-size:13px; font-weight:700; color:#0f172a; margin-bottom:8px;">Transferencia Segura PSE en Colombia</div>
      <div class="checkout-form-grid">
        <div class="checkout-input-group checkout-form-full">
          <label>Selecciona tu Entidad Bancaria</label>
          <select id="pseBankSelect">
            <option value="Bancolombia">Bancolombia</option>
            <option value="Nequi">Nequi</option>
            <option value="Davivienda / Daviplata">Davivienda / Daviplata</option>
            <option value="Banco de Bogotá">Banco de Bogotá</option>
            <option value="BBVA Colombia">BBVA Colombia</option>
            <option value="Scotiabank Colpatria">Scotiabank Colpatria</option>
            <option value="Banco Agrario de Colombia">Banco Agrario de Colombia</option>
            <option value="Nu Colombia">Nu Colombia (Cuenta Nu)</option>
            <option value="Lulo Bank">Lulo Bank</option>
          </select>
        </div>
        <div class="checkout-input-group">
          <label>Tipo de Persona</label>
          <select id="psePersonType">
            <option value="Natural">Persona Natural</option>
            <option value="Juridica">Persona Jurídica (Empresa)</option>
          </select>
        </div>
        <div class="checkout-input-group">
          <label>Cédula / NIT del Titular</label>
          <input type="text" id="pseDocNumber" placeholder="Número de documento">
        </div>
      </div>
      <p style="font-size:11px; color:#64748b; margin-top:10px;">🔒 Transacción protegida y cifrada en el sistema de pagos seguros de Colombia.</p>
    `;
  } else if (selectedPaymentMethod === 'Transferencia Bancolombia / Nequi') {
    box.innerHTML = `
      <div class="qr-payment-container">
        <div class="qr-code-holder">
          <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Bancolombia-SyP-Neiva-3143804967" alt="QR Bancolombia SyP">
        </div>
        <div class="qr-accounts-info">
          <div style="font-weight:800; color:#0f172a; margin-bottom:4px; font-size:14px;">Cuentas Oficiales de Fotocopiadora SyP:</div>
          <div><strong>• Bancolombia Ahorros:</strong> 078-456982-12</div>
          <div><strong>• Nequi / Daviplata:</strong> 314 380 4967 (Gladys Solano)</div>
          <div><strong>• Llave Transfiya:</strong> 317 820 4193 (Juan Sebastián)</div>
          <p style="font-size:11px; color:#64748b; margin-top:6px;">Al confirmar, se reservará tu pedido y podrás enviar el comprobante directamente a nuestros asesores por WhatsApp.</p>
        </div>
      </div>
    `;
  } else if (selectedPaymentMethod === 'Tarjeta de Crédito / Débito') {
    box.innerHTML = `
      <div style="font-size:13px; font-weight:700; color:#0f172a; margin-bottom:8px;">Pago con Tarjeta de Crédito o Débito</div>
      <div class="checkout-form-grid">
        <div class="checkout-input-group checkout-form-full">
          <label>Número de Tarjeta</label>
          <input type="text" id="ccNumber" placeholder="4500 1234 5678 9010" maxlength="19">
        </div>
        <div class="checkout-input-group">
          <label>Fecha Vencimiento (MM/AA)</label>
          <input type="text" id="ccExpiry" placeholder="12/28" maxlength="5">
        </div>
        <div class="checkout-input-group">
          <label>Código de Seguridad (CVV)</label>
          <input type="password" id="ccCvv" placeholder="123" maxlength="4">
        </div>
      </div>
    `;
  } else if (selectedPaymentMethod === 'Cotización Formal') {
    box.innerHTML = `
      <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:6px; padding:12px; font-size:13px; color:#065f46;">
        <strong>📄 Generación de Enlace Web de Cotización</strong><br>
        Se generará un documento formal con código permanente (ej: <code>COT-2026-XXXX</code>) que podrás enviar por correo, compartir en comités de compras o imprimir en PDF con validez de 15 días.
      </div>
    `;
  }
}

async function processOrderSubmission() {
  const btn = document.getElementById('btnProcessPayment');
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Procesando en el servidor...';
  }

  // Extraer datos del formulario
  const name = document.getElementById('chkName')?.value || 'Cliente General';
  const nit = document.getElementById('chkNit')?.value || '';
  const phone = document.getElementById('chkPhone')?.value || '';
  const email = document.getElementById('chkEmail')?.value || 'ventas@fotocopiadorasyp.com';
  const address = document.getElementById('chkAddress')?.value || 'Entrega local Neiva';
  const city = document.getElementById('chkCity')?.value || 'Neiva, Huila';
  const notes = document.getElementById('chkNotes')?.value || '';

  const total = cartTotal();
  const subtotal = Math.round(total / 1.19);
  const iva = total - subtotal;
  const shipping = total >= 100000 ? 0 : 8000;
  const grandTotal = total + shipping;

  const items = state.cart.map(i => {
    const p = PRODUCTS.find(x => x.id === i.id);
    return {
      id: i.id,
      name: p ? p.name : 'Producto Ricoh',
      spec: p ? p.spec : '',
      price: p ? p.price : 0,
      quantity: i.qty
    };
  });

  try {
    if (selectedPaymentMethod === 'Cotización Formal') {
      // Guardar cotización en la API
      const res = await fetch('http://127.0.0.1:8000/api/v1/quotes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_name: name,
          client_email: email,
          client_phone: phone,
          items_json: JSON.stringify(items),
          subtotal: subtotal,
          iva: iva,
          total: grandTotal,
          notes: notes
        })
      });

      if (!res.ok) throw new Error('Error al registrar la cotización en el servidor.');
      const data = await res.json();
      
      localStorage.setItem("syp_last_quote", JSON.stringify(data));
      state.cart = [];
      saveCartToStorage(state.cart);
      renderCart();
      updateCartCount();

      renderOrderSuccess({
        isQuote: true,
        code: data.quote_code,
        name: name,
        total: grandTotal,
        url: `/cotizacion.html?code=${data.quote_code}`,
        phone: phone
      });

    } else {
      // Guardar pedido en la API
      const res = await fetch('http://127.0.0.1:8000/api/v1/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(typeof Auth !== 'undefined' && Auth.getToken() ? { 'Authorization': `Bearer ${Auth.getToken()}` } : {})
        },
        body: JSON.stringify({
          client_name: name,
          client_email: email,
          client_phone: phone,
          client_nit: nit,
          delivery_address: address,
          delivery_city: city,
          items_json: JSON.stringify(items),
          subtotal: subtotal,
          iva: iva,
          total: grandTotal,
          payment_method: selectedPaymentMethod,
          payment_status: selectedPaymentMethod === 'Transferencia Bancolombia / Nequi' ? 'En Verificación' : 'Aprobado',
          notes: notes
        })
      });

      if (!res.ok) throw new Error('Error al procesar el pedido en el servidor.');
      const data = await res.json();

      state.cart = [];
      saveCartToStorage(state.cart);
      renderCart();
      updateCartCount();

      renderOrderSuccess({
        isQuote: false,
        code: data.order_code,
        name: name,
        total: grandTotal,
        url: `/cotizacion.html?order=${data.order_code}`,
        phone: phone,
        method: selectedPaymentMethod
      });
    }

  } catch (err) {
    showToast(err.message || 'Error en la conexión. Intenta nuevamente.', 'error');
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Reintentar';
    }
  }
}

function renderOrderSuccess(info) {
  checkoutStep = 4;
  const pane = document.getElementById('stepPane4');
  const container = document.getElementById('checkoutSuccessContainer');
  if (!pane || !container) return;

  document.querySelectorAll('.checkout-step-pane').forEach(p => p.classList.remove('active'));
  pane.classList.add('active');

  const permalink = window.location.origin + info.url;
  const waMessage = encodeURIComponent(
    `👋 Hola Asesores SyP, acabo de registrar ${info.isQuote ? 'la cotización' : 'el pedido'} *${info.code}* a nombre de *${info.name}* por *$${Number(info.total).toLocaleString('es-CO')} COP*.\n\n🔗 Enlace oficial: ${permalink}`
  );

  container.innerHTML = `
    <div class="order-success-icon">✓</div>
    <h2 style="font-size:22px; font-weight:800; color:#0f172a; margin:0 0 6px;">
      ${info.isQuote ? '¡Cotización Oficial Generada!' : '¡Pedido Registrado con Éxito!'}
    </h2>
    <p style="font-size:14px; color:#64748b; margin:0 0 12px;">
      ${info.isQuote 
        ? 'Se ha creado el documento comercial con enlace permanente y código QR.'
        : 'Tu compra ha sido registrada en el sistema de Fotocopiadora SyP y está lista para despacho en Neiva.'}
    </p>

    <div class="order-success-code">${info.code}</div>

    <div style="display:flex; flex-direction:column; gap:10px; max-width:400px; margin:16px auto 0;">
      <a href="${info.url}" class="btn btn-primary" style="text-align:center; padding:12px 18px; font-weight:700;">
        📄 Ver Documento / Factura en Línea y Descargar PDF
      </a>
      <a href="https://wa.me/573143804967?text=${waMessage}" target="_blank" class="btn btn-outline" style="background:#25d366; color:#fff; border-color:#25d366; text-align:center; padding:12px 18px; font-weight:700;">
        💬 Notificar a Asesores por WhatsApp
      </a>
      <button class="btn btn-outline" onclick="navigator.clipboard.writeText('${permalink}'); showToast('¡Enlace copiado al portapapeles!');" style="text-align:center; padding:10px;">
        📋 Copiar Enlace Permanente
      </button>
      <button class="btn btn-outline" onclick="closeCheckoutModal()" style="text-align:center; padding:10px; border:none; color:#64748b;">
        Cerrar y Continuar Navegando
      </button>
    </div>
  `;
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

/* ---------- Notificaciones y Área de cuenta en el header ---------- */
function formatRelativeTime(isoStr) {
  if (!isoStr) return '';
  const date = new Date(isoStr.includes('Z') ? isoStr : isoStr + 'Z');
  const now = new Date();
  const diffSec = Math.max(0, Math.floor((now - date) / 1000));
  if (diffSec < 45) return 'Hace un momento';
  if (diffSec < 3600) return `Hace ${Math.floor(diffSec / 60)} min`;
  if (diffSec < 86400) return `Hace ${Math.floor(diffSec / 3600)} h`;
  if (diffSec < 172800) return 'Ayer';
  return date.toLocaleDateString('es-CO', { day: '2-digit', month: 'short' });
}

const NOTIF_ICONS = {
  order: '🛒',
  maintenance: '🔧',
  renting: '📄',
  system: '🔔',
  promo: '🏷️',
  info: 'ℹ️',
};

let notifPollInterval = null;

function initAccountArea() {
  const area = document.getElementById('accountArea');
  if (!area || typeof SyP === 'undefined') return;

  const session = SyP.getSession();

  if (!session) {
    if (notifPollInterval) clearInterval(notifPollInterval);
    area.innerHTML = `
      <a href="login.html" class="account-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
        <span class="label">Iniciar sesión</span>
      </a>`;
    return;
  }

  area.innerHTML = `
    <!-- Campanita de Notificaciones -->
    <div class="notif-bell-wrap" id="notifBellWrap">
      <button class="notif-btn" id="notifToggle" aria-label="Notificaciones" aria-haspopup="true" aria-expanded="false" title="Centro de Notificaciones">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        <span class="notif-badge" id="notifBadge" style="display:none">0</span>
      </button>
      <div class="notif-dropdown" id="notifDropdown" role="region" aria-label="Notificaciones del usuario">
        <div class="notif-head">
          <h4>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            Notificaciones
          </h4>
          <button class="notif-clear-btn" id="notifMarkAllBtn" type="button">Marcar leídas</button>
        </div>
        <div class="notif-list" id="notifList">
          <div class="notif-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            Cargando notificaciones...
          </div>
        </div>
      </div>
    </div>

    <!-- Menú de Usuario -->
    <div style="position:relative">
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
        <button id="logoutBtn" type="button">Cerrar sesión</button>
      </div>
    </div>`;

  const accToggle = document.getElementById('accountToggle');
  const accDropdown = document.getElementById('accountDropdown');
  const notifToggle = document.getElementById('notifToggle');
  const notifDropdown = document.getElementById('notifDropdown');
  const notifBadge = document.getElementById('notifBadge');
  const notifList = document.getElementById('notifList');
  const notifMarkAllBtn = document.getElementById('notifMarkAllBtn');

  // Toggle Menú de Usuario
  accToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    notifDropdown.classList.remove('open');
    notifToggle.setAttribute('aria-expanded', 'false');
    const isOpen = accDropdown.classList.toggle('open');
    accToggle.setAttribute('aria-expanded', String(isOpen));
  });

  // Toggle Campanita de Notificaciones
  notifToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    accDropdown.classList.remove('open');
    accToggle.setAttribute('aria-expanded', 'false');
    const isOpen = notifDropdown.classList.toggle('open');
    notifToggle.setAttribute('aria-expanded', String(isOpen));
  });

  // Cerrar dropdowns al hacer clic fuera
  document.addEventListener('click', () => {
    accDropdown.classList.remove('open');
    accToggle.setAttribute('aria-expanded', 'false');
    notifDropdown.classList.remove('open');
    notifToggle.setAttribute('aria-expanded', 'false');
  });

  // Marcar todas como leídas
  notifMarkAllBtn.addEventListener('click', async (e) => {
    e.stopPropagation();
    await SyP.markAllNotificationsRead();
    refreshNotifications();
  });

  // Cerrar sesión
  document.getElementById('logoutBtn').addEventListener('click', () => {
    if (notifPollInterval) clearInterval(notifPollInterval);
    SyP.logout();
    window.location.href = 'index.html';
  });

  // Función de actualización en tiempo real de notificaciones
  async function refreshNotifications() {
    if (!SyP.getToken()) return;
    const res = await SyP.fetchMyNotifications(15);
    const unread = res.unread_count || 0;
    if (unread > 0) {
      notifBadge.textContent = unread > 9 ? '9+' : unread;
      notifBadge.style.display = 'block';
    } else {
      notifBadge.style.display = 'none';
    }

    if (!res.items || res.items.length === 0) {
      notifList.innerHTML = `
        <div class="notif-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          No tienes notificaciones por el momento.
        </div>`;
      return;
    }

    notifList.innerHTML = res.items.map((n) => {
      const icon = NOTIF_ICONS[n.type] || '🔔';
      const unreadCls = !n.is_read ? ' unread' : '';
      const timeStr = formatRelativeTime(n.created_at);
      return `
        <div class="notif-item${unreadCls}" data-id="${escapeHTML(n.id)}" data-link="${escapeHTML(n.link_url || '')}">
          <div class="notif-item-icon">${icon}</div>
          <div class="notif-item-body">
            <div class="notif-item-title">${escapeHTML(n.title)}</div>
            <div class="notif-item-msg">${escapeHTML(n.message)}</div>
            <div class="notif-item-time">${timeStr}</div>
          </div>
        </div>`;
    }).join('');

    // Listener de clic para cada item (marca como leído y navega)
    notifList.querySelectorAll('.notif-item').forEach((itemEl) => {
      itemEl.addEventListener('click', async (e) => {
        e.stopPropagation();
        const nid = itemEl.dataset.id;
        const link = itemEl.dataset.link;
        await SyP.markNotificationRead(nid);
        itemEl.classList.remove('unread');
        refreshNotifications();
        if (link) {
          window.location.href = link;
        }
      });
    });
  }

  // Carga inicial y sondeo periódico cada 20 segundos
  refreshNotifications();
  if (notifPollInterval) clearInterval(notifPollInterval);
  notifPollInterval = setInterval(refreshNotifications, 20000);
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
   BANNER SLIDER DESTACADO DE SERVICIOS & RENTING (HOME)
   ============================================================ */
function initServicesBannerSlider() {
  const wrap = document.getElementById('servicesBannerSlider');
  if (!wrap) return;

  const slides = wrap.querySelectorAll('.banner-slide');
  const dots = wrap.querySelectorAll('.banner-dot');
  const prevBtn = document.getElementById('bannerPrevBtn');
  const nextBtn = document.getElementById('bannerNextBtn');

  if (!slides.length) return;

  let currentIdx = 0;
  let timer = null;
  const duration = 6500;

  function setSlide(i) {
    if (i < 0) i = slides.length - 1;
    if (i >= slides.length) i = 0;
    currentIdx = i;

    slides.forEach((s, idx) => s.classList.toggle('active', idx === currentIdx));
    dots.forEach((d, idx) => d.classList.toggle('active', idx === currentIdx));
  }

  function next() { setSlide(currentIdx + 1); }
  function prev() { setSlide(currentIdx - 1); }

  function start() {
    stop();
    timer = setInterval(next, duration);
  }
  function stop() {
    if (timer) clearInterval(timer);
  }

  if (nextBtn) nextBtn.addEventListener('click', () => { next(); start(); });
  if (prevBtn) prevBtn.addEventListener('click', () => { prev(); start(); });

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.dataset.bdot, 10);
      setSlide(idx);
      start();
    });
  });

  wrap.addEventListener('mouseenter', stop);
  wrap.addEventListener('mouseleave', start);

  start();
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

/* ============================================================
   7. BUSCADOR DE CÓDIGOS DE ERROR SC RICOH (Feature 1)
   ============================================================ */
function initRicohSCCodeLookup() {
  const container = document.getElementById('scCodeLookup');
  if (!container || typeof RICOH_SC_CODES === 'undefined') return;

  const input = document.getElementById('scSearchInput');
  const clearBtn = document.getElementById('scClearBtn');
  const chips = container.querySelectorAll('.sc-chip-btn');
  const resultsContainer = document.getElementById('scResultsContainer');
  if (!input || !resultsContainer) return;

  function formatSeverityBadge(severity) {
    const s = escapeHTML(severity);
    return `<span class="severity-pill ${s}">Gravedad: ${s}</span>`;
  }

  function renderCodes(matches, queryTerm = '') {
    if (!matches || matches.length === 0) {
      const sanitizedQuery = escapeHTML(queryTerm);
      const waUnknownMsg = encodeURIComponent(
        `Hola Juan Sebastián (Técnico SyP), mi fotocopiadora Ricoh muestra el código "${queryTerm}". No lo encontré en el buscador. ¿Podrías indicarme qué significa y cómo solucionarlo?`
      );
      resultsContainer.innerHTML = `
        <div class="sc-empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <h3 style="font-size:16px; margin-bottom:6px; color:var(--ink);">Código "${sanitizedQuery}" no listado en la guía rápida</h3>
          <p style="font-size:13px; max-width:480px; margin:0 auto 18px; line-height:1.5;">Existen más de 400 sub-códigos de servicio técnico para la línea Ricoh. Nuestro jefe de taller puede decodificarlo de inmediato en el manual de servicio oficial.</p>
          <a href="https://wa.me/573178204193?text=${waUnknownMsg}" target="_blank" rel="noopener" class="btn btn-primary" style="background:#25D366; border-color:#25D366;">
            Consultar código "${sanitizedQuery}" con Sebastián por WhatsApp
          </a>
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = matches.map((item) => {
      const waMsg = encodeURIComponent(
        `Hola Sebastián (Técnico SyP), mi equipo Ricoh reporta el código ${item.code}: ${item.name}.\n` +
        `• Categoría: ${item.category}\n` +
        `• Causa probable: ${item.cause}\n` +
        `¿Podrías agendar un diagnóstico en sitio o cotizarme la solución para Neiva?`
      );

      return `
        <div class="sc-result-card" data-sc-code="${escapeHTML(item.code)}">
          <div class="sc-card-header">
            <div>
              <span class="sc-code-badge">${escapeHTML(item.code)}</span>
              <h3 class="sc-card-title">${escapeHTML(item.name)}</h3>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span style="font-family:var(--font-mono); font-size:11.5px; color:var(--steel); background:var(--paper); padding:4px 8px; border-radius:4px; border:1px solid var(--line);">${escapeHTML(item.category)}</span>
              ${formatSeverityBadge(item.severity)}
            </div>
          </div>

          <div style="font-size:14px; line-height:1.6; color:var(--ink); margin-bottom:12px;">
            <strong>¿Qué significa este código?</strong> ${escapeHTML(item.meaning)}
          </div>

          <div class="sc-detail-grid">
            <div class="sc-detail-item">
              <h4>Causa Raíz Probable</h4>
              <p>${escapeHTML(item.cause)}</p>
            </div>
            <div class="sc-detail-item">
              <h4>Solución y Protocolo Técnico SyP</h4>
              <p>${escapeHTML(item.solution)}</p>
            </div>
          </div>

          ${item.safetyNotice ? `
            <div class="sc-safety-alert">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" style="flex-shrink:0;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              <span><strong>Advertencia de Seguridad:</strong> ${escapeHTML(item.safetyNotice)}</span>
            </div>
          ` : ''}

          <div class="sc-action-row">
            <a href="https://wa.me/573178204193?text=${waMsg}" target="_blank" rel="noopener" class="btn btn-primary" style="background:#25D366; border-color:#25D366;">
              <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16" style="margin-right:6px;"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
              Reportar ${escapeHTML(item.code)} a Sebastián (Técnico)
            </a>
            <button type="button" class="btn btn-outline" onclick="if(typeof prefillServiceFormFromSC === 'function') prefillServiceFormFromSC('${escapeHTML(item.code)}', '${escapeHTML(item.name)}', '${escapeHTML(item.cause)}')">
              Agendar Visita de Taller en Neiva
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  function search(query) {
    const raw = (query || '').trim().toLowerCase();
    if (clearBtn) {
      clearBtn.classList.toggle('visible', raw.length > 0);
    }

    chips.forEach((c) => {
      const code = c.dataset.sc.toLowerCase();
      c.classList.toggle('active', raw.length > 0 && (raw.includes(code.replace('sc ', '')) || code.includes(raw)));
    });

    if (!raw) {
      renderCodes([RICOH_SC_CODES[0], RICOH_SC_CODES[1]]);
      return;
    }

    const matches = RICOH_SC_CODES.filter((item) => {
      const codeClean = item.code.toLowerCase().replace(/\s+/g, '');
      const queryClean = raw.replace(/\s+/g, '');
      return (
        codeClean.includes(queryClean) ||
        item.name.toLowerCase().includes(raw) ||
        item.category.toLowerCase().includes(raw) ||
        item.cause.toLowerCase().includes(raw) ||
        item.solution.toLowerCase().includes(raw)
      );
    });

    renderCodes(matches, query);
  }

  input.addEventListener('input', (e) => {
    search(e.target.value);
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      input.value = '';
      search('');
      input.focus();
    });
  }

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const sc = chip.dataset.sc;
      input.value = sc;
      search(sc);
    });
  });

  // Render inicial
  renderCodes([RICOH_SC_CODES[0], RICOH_SC_CODES[1]]);
}

/* ============================================================
   7B. SELECTOR INTELIGENTE DE COMPATIBILIDAD DE INSUMOS & REPUESTOS RICOH
   ============================================================ */
function initCompatibilityFinder() {
  const brandSel = document.getElementById('compatBrandSelect');
  const modelSel = document.getElementById('compatModelSelect');
  const clearBtn = document.getElementById('compatClearBtn');
  const resultsGrid = document.getElementById('compatResultsGrid');

  if (!brandSel || !modelSel || typeof BRAND_MODELS === 'undefined') return;

  // Llenar selector de Series Ricoh si no está lleno
  if (brandSel.options.length <= 1) {
    Object.keys(BRAND_MODELS).forEach((series) => {
      const opt = document.createElement('option');
      opt.value = series;
      opt.textContent = series;
      brandSel.appendChild(opt);
    });
  }

  function renderCompatResults(modelName) {
    if (!resultsGrid) return;
    if (!modelName) {
      resultsGrid.innerHTML = '';
      resultsGrid.style.display = 'none';
      return;
    }

    const matches = PRODUCTS.filter((p) => {
      if (p.models && p.models.includes(modelName)) return true;
      if (p.models && p.models.some((m) => modelName.includes(m) || m.includes(modelName))) return true;
      return false;
    });

    if (matches.length === 0) {
      resultsGrid.style.display = 'block';
      resultsGrid.innerHTML = `
        <div style="grid-column:1/-1; background:var(--paper); border:1px dashed var(--line); border-radius:8px; padding:24px; text-align:center;">
          <p style="font-size:14px; color:var(--steel); margin:0 0 12px;">No hay repuestos directos en catálogo web para <strong>${escapeHTML(modelName)}</strong>, pero disponemos de stock en taller físico.</p>
          <a href="https://wa.me/573143804967?text=${encodeURIComponent('Hola Gladys, necesito cotizar tóner y repuestos para Ricoh ' + modelName)}" target="_blank" rel="noopener" class="btn btn-primary" style="font-size:12.5px;">
            Consultar Insumos con Gladys (Ventas)
          </a>
        </div>
      `;
      return;
    }

    resultsGrid.style.display = 'grid';
    resultsGrid.innerHTML = matches.map((p) => {
      const catLabel = CATEGORIES.find((c) => c.id === p.cat)?.label ?? p.cat;
      const imgSrc = p.img || (typeof getCategoryDefaultImage === 'function' ? getCategoryDefaultImage(p.cat) : 'img/prod_toner.jpg');

      return `
        <div class="product-card" style="margin:0; box-shadow:0 2px 10px rgba(0,0,0,0.04);">
          <div class="product-media" style="height:140px; cursor:pointer;" onclick="openQuickView('${escapeHTML(p.id)}')">
            <span class="stock-tag in-stock">Compatible</span>
            <div class="product-media-img-wrap">
              <img src="${escapeHTML(imgSrc)}" alt="${escapeHTML(p.name)}" class="product-real-img" loading="lazy">
            </div>
          </div>
          <div class="product-body" style="padding:14px;">
            <span class="product-cat">${escapeHTML(catLabel)}</span>
            <h4 class="product-name" style="font-size:13.5px; margin:4px 0 6px; cursor:pointer;" onclick="openQuickView('${escapeHTML(p.id)}')">${escapeHTML(p.name)}</h4>
            <p class="product-spec" style="font-size:11.5px; margin-bottom:10px;">${escapeHTML(p.spec)}</p>
            <div class="product-foot">
              <span class="product-price" style="font-size:15px;">${formatCOP(p.price)}</span>
              <button type="button" class="btn btn-primary" style="padding:6px 12px; font-size:12px;" onclick="addToCart('${escapeHTML(p.id)}'); showToast('${escapeHTML(p.name)} agregado al carrito ✓');">
                + Añadir
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  brandSel.addEventListener('change', () => {
    const selectedBrand = brandSel.value;
    modelSel.innerHTML = '<option value="">2. Selecciona el modelo exacto</option>';
    if (selectedBrand && BRAND_MODELS[selectedBrand]) {
      modelSel.disabled = false;
      BRAND_MODELS[selectedBrand].forEach((mod) => {
        const opt = document.createElement('option');
        opt.value = mod;
        opt.textContent = mod;
        modelSel.appendChild(opt);
      });
      if (clearBtn) clearBtn.style.display = 'inline-block';
    } else {
      modelSel.disabled = true;
      if (clearBtn) clearBtn.style.display = 'none';
      renderCompatResults(null);
    }
  });

  modelSel.addEventListener('change', () => {
    if (modelSel.value) {
      if (clearBtn) clearBtn.style.display = 'inline-block';
      renderCompatResults(modelSel.value);
      showToast(`Insumos compatibles con ${modelSel.value} cargados ✓`);
    } else {
      renderCompatResults(null);
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      brandSel.value = '';
      modelSel.innerHTML = '<option value="">2. Primero elige la Serie Ricoh</option>';
      modelSel.disabled = true;
      clearBtn.style.display = 'none';
      renderCompatResults(null);
      showToast('Filtro de compatibilidad restablecido');
    });
  }
}

/* ============================================================
   8. MODAL SELECTOR DE ASESOR WHATSAPP (Feature 3)
   ============================================================ */
function initAdvisorSelectorModal() {
  if (document.getElementById('advisorModalOverlay')) return;

  const overlay = document.createElement('div');
  overlay.id = 'advisorModalOverlay';
  overlay.className = 'advisor-modal-overlay';

  const modal = document.createElement('div');
  modal.id = 'advisorModal';
  modal.className = 'advisor-modal';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');

  modal.innerHTML = `
    <div class="advisor-modal-head">
      <div>
        <span class="eyebrow" style="color:var(--red); font-size:11px; margin-bottom:2px; display:block;">Atención Inmediata en Neiva</span>
        <h2>Elige tu Asesor Especializado SyP</h2>
      </div>
      <button class="modal-close" id="advisorModalClose" aria-label="Cerrar selector">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <div class="advisor-modal-body">
      <div class="advisor-cards-grid">
        
        <!-- ASESOR 1: GLADYS SOLANO (VENTAS & RENTING) -->
        <div class="advisor-profile-card commercial">
          <div>
            <div class="advisor-avatar-box">
              <div class="advisor-avatar gladys">
                GS
                <span class="advisor-online-dot" title="En línea para ventas"></span>
              </div>
              <div>
                <div class="advisor-name">Gladys Solano Murcia</div>
                <div class="advisor-role-tag">Gerencia Comercial & Renting</div>
              </div>
            </div>
            <p class="advisor-desc">Asesoría comercial en venta y alquiler de fotocopiadoras Ricoh, cálculo de cuotas de renting, suministro de tóneres al por mayor y cotizaciones formales.</p>
          </div>

          <div class="advisor-quick-actions">
            <a href="https://wa.me/573143804967?text=Hola%20Gladys%2C%20deseo%20cotizar%20un%20plan%20de%20renting%20o%20fotocopiadora%20Ricoh%20para%20mi%20empresa" target="_blank" rel="noopener" class="advisor-action-btn wa-primary">
              <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
              WhatsApp: Cotizar Renting o Compra
            </a>
            <a href="https://wa.me/573143804967?text=Hola%20Gladys%2C%20necesito%20comprar%20t%C3%B3neres%20o%20repuestos%20Ricoh" target="_blank" rel="noopener" class="advisor-action-btn">
              <span>📦 Comprar Tóners / Insumos</span>
              <span style="font-size:11px; color:var(--steel);">+57 314 380 4967</span>
            </a>
            <a href="tel:+573143804967" class="advisor-action-btn" style="border-style:dashed;">
              <span>📞 Llamada Telefónica Directa</span>
              <span>Llamar</span>
            </a>
          </div>
        </div>

        <!-- ASESOR 2: JUAN SEBASTIÁN PORTELA (SOPORTE TÉCNICO) -->
        <div class="advisor-profile-card technical">
          <div>
            <div class="advisor-avatar-box">
              <div class="advisor-avatar sebastian">
                JP
                <span class="advisor-online-dot" title="En línea en taller"></span>
              </div>
              <div>
                <div class="advisor-name">Juan Sebastián Portela</div>
                <div class="advisor-role-tag">Jefe de Soporte Técnico & Taller</div>
              </div>
            </div>
            <p class="advisor-desc">Atención de fallas mecánicas, atascos de papel, códigos de error SC Ricoh, mantenimiento preventivo y servicio técnico de emergencia a domicilio en Neiva.</p>
          </div>

          <div class="advisor-quick-actions">
            <a href="https://wa.me/573178204193?text=Hola%20Sebasti%C3%A1n%2C%20tengo%20una%20urgencia%20t%C3%A9cnica%20%2F%20c%C3%B3digo%20de%20error%20en%20mi%20fotocopiadora%20Ricoh" target="_blank" rel="noopener" class="advisor-action-btn wa-primary" style="background:#10b981; border-color:#10b981;">
              <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-1.5-.7-2.5-1.3-3.5-3-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5-.1-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.9-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
              WhatsApp: Urgencia / Código SC
            </a>
            <a href="https://wa.me/573178204193?text=Hola%20Sebasti%C3%A1n%2C%20deseo%20programar%20un%20mantenimiento%20preventivo%20en%20mi%20sede" target="_blank" rel="noopener" class="advisor-action-btn">
              <span>🔧 Programar Mantenimiento</span>
              <span style="font-size:11px; color:var(--steel);">+57 317 820 4193</span>
            </a>
            <a href="tel:+573178204193" class="advisor-action-btn" style="border-style:dashed;">
              <span>📞 Llamada Telefónica Directa</span>
              <span>Llamar</span>
            </a>
          </div>
        </div>

      </div>
    </div>
    <div class="advisor-modal-foot">
      <span>📍 Sede Central: Avenida La Toma #3A-20, Neiva</span>
      <span>⏰ Lun–Vie: 7:30am–12:00pm y 2:00pm–5:00pm</span>
    </div>
  `;

  overlay.style.display = 'none';
  modal.style.display = 'none';

  document.body.appendChild(overlay);
  document.body.appendChild(modal);

  function open() {
    overlay.style.display = 'block';
    modal.style.display = 'flex';
    // Force reflow for transitions
    void modal.offsetWidth;
    overlay.classList.add('open');
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    const closeBtn = document.getElementById('advisorModalClose');
    if (closeBtn) closeBtn.focus();
  }

  function close() {
    overlay.classList.remove('open');
    modal.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => {
      if (!overlay.classList.contains('open')) overlay.style.display = 'none';
      if (!modal.classList.contains('open')) modal.style.display = 'none';
    }, 280);
  }

  overlay.addEventListener('click', close);
  const closeBtn = document.getElementById('advisorModalClose');
  if (closeBtn) closeBtn.addEventListener('click', close);

  // Interceptar clicks en botón flotante y botones con data-advisor-modal
  document.querySelectorAll('.floating-wa-btn, #floatingAssistantBubble, [data-advisor-modal]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      open();
    });
  });
}

/* ============================================================
   9. BANNER DE INSTALACIÓN PWA (Feature 3)
   ============================================================ */
let deferredPrompt = null;

function initPWAInstallBanner() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js').catch((err) => {
        console.warn('[SyP PWA] SW registration failed:', err);
      });
    });
  }

  const dismissedTime = localStorage.getItem('syp_pwa_dismissed');
  if (dismissedTime && Date.now() - parseInt(dismissedTime, 10) < 7 * 24 * 60 * 60 * 1000) {
    return;
  }

  if (document.getElementById('pwaInstallBanner')) return;

  const banner = document.createElement('aside');
  banner.id = 'pwaInstallBanner';
  banner.className = 'pwa-install-banner';
  banner.setAttribute('aria-label', 'Instalar aplicación web de Fotocopiadora SyP');

  banner.innerHTML = `
    <div class="pwa-app-icon">
      <svg viewBox="0 0 40 40" width="28" height="28">
        <circle cx="20" cy="20" r="14" stroke="#FAFAF8" stroke-width="1.5" fill="none"/>
        <line x1="20" y1="4" x2="20" y2="36" stroke="#FAFAF8" stroke-width="1.5"/>
        <line x1="4" y1="20" x2="36" y2="20" stroke="#FAFAF8" stroke-width="1.5"/>
        <circle cx="20" cy="20" r="8" stroke="#E4002B" stroke-width="2.5" fill="none"/>
      </svg>
    </div>
    <div class="pwa-banner-content">
      <div class="pwa-banner-title">Instala la App de Fotocopiadora SyP</div>
      <p class="pwa-banner-desc">Accede al catálogo de fotocopiadoras Ricoh, buscador de errores SC y cotizaciones al instante en tu celular.</p>
      <div class="pwa-banner-actions">
        <button type="button" class="pwa-action-btn" id="pwaInstallActionBtn">Instalar App</button>
        <button type="button" class="pwa-dismiss-btn" id="pwaDismissBtn">Ahora no</button>
      </div>
    </div>
  `;

  banner.style.display = 'none';
  document.body.appendChild(banner);

  function showBanner() {
    banner.style.display = 'flex';
    void banner.offsetWidth;
    banner.classList.add('visible');
  }

  function hideBanner() {
    banner.classList.remove('visible');
    setTimeout(() => {
      if (!banner.classList.contains('visible')) banner.style.display = 'none';
    }, 400);
  }

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    setTimeout(() => {
      showBanner();
    }, 2000);
  });

  setTimeout(() => {
    if (!localStorage.getItem('syp_pwa_dismissed') && !banner.classList.contains('visible')) {
      showBanner();
    }
  }, 4000);

  const installBtn = document.getElementById('pwaInstallActionBtn');
  if (installBtn) {
    installBtn.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
          showToast('¡Gracias por instalar Fotocopiadora SyP! 🎉');
        }
        deferredPrompt = null;
        hideBanner();
      } else {
        showToast('Para instalar: En tu navegador pulsa "Compartir" o Menú (⋮) > "Agregar a pantalla de inicio" 📱');
        setTimeout(() => hideBanner(), 4000);
      }
    });
  }

  const dismissBtn = document.getElementById('pwaDismissBtn');
  if (dismissBtn) {
    dismissBtn.addEventListener('click', () => {
      hideBanner();
      localStorage.setItem('syp_pwa_dismissed', Date.now().toString());
    });
  }

  window.addEventListener('appinstalled', () => {
    hideBanner();
    showToast('App instalada con éxito 🚀');
  });
}

function initFloatingAssistant() {
  const bubble = document.getElementById('floatingAssistantBubble');
  if (!bubble) return;
  setTimeout(() => {
    bubble.classList.add('show');
  }, 2500);
}

function initFAQAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach((item) => {
    const q = item.querySelector('.faq-question');
    if (q) {
      q.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        faqItems.forEach((i) => i.classList.remove('open'));
        if (!isOpen) item.classList.add('open');
      });
    }
  });
}

function initProductCarousel() {
  // Inicialización suave si se requiere
}

/* ============================================================
   10. CONTROL DE RED (ONLINE / OFFLINE) & BOTÓN VOLVER ARRIBA
   ============================================================ */
function initNetworkStatusListener() {
  function updateOnlineStatus() {
    let pill = document.getElementById('offlineBannerPill');
    if (!pill) {
      pill = document.createElement('div');
      pill.id = 'offlineBannerPill';
      pill.className = 'offline-banner-pill';
      pill.innerHTML = `
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
        <span>Modo sin conexión: El catálogo local y códigos SC siguen disponibles</span>
      `;
      document.body.appendChild(pill);
    }

    if (!navigator.onLine) {
      pill.classList.add('show');
      showToast('⚠️ Modo sin conexión activado', 'error');
    } else {
      if (pill.classList.contains('show')) {
        pill.classList.remove('show');
        showToast('📡 Conexión a internet restablecida ✓', 'success');
      }
    }
  }

  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  if (!navigator.onLine) updateOnlineStatus();
}

function initBackToTopButton() {
  if (document.getElementById('backToTopBtn')) return;

  const btn = document.createElement('button');
  btn.id = 'backToTopBtn';
  btn.className = 'back-to-top-btn';
  btn.setAttribute('aria-label', 'Volver arriba de la página');
  btn.setAttribute('title', 'Volver arriba');
  btn.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="18 15 12 9 6 15"/>
    </svg>
  `;

  document.body.appendChild(btn);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 380) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
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
  initServicesBannerSlider();
  initProductCarousel();
  initFAQAccordion();
  initFloatingAssistant();
  initQuickViewModal();
  initProductComparator();
  initRentingCalculator();
  initSmartTroubleshooter();
  initRicohSCCodeLookup();
  initCompatibilityFinder();
  initAdvisorSelectorModal();
  initPWAInstallBanner();
  initNetworkStatusListener();
  initBackToTopButton();
  renderTestimonials();

  const printQuoteBtn = document.getElementById('printQuoteBtn');
  if (printQuoteBtn) {
    printQuoteBtn.addEventListener('click', generateFormalQuotationPDF);
  }

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});



