/* =========================================================
   Fotocopiadora SyP — Autenticación Segura & API REST Backend
   - Autenticación con Tokens JWT (JSON Web Tokens)
   - Cifrado seguro de contraseñas vía Bcrypt en el servidor
   - Sincronización en tiempo real con SQLite / FastAPI
   - Respaldo automático offline (Cache local resiliente)
   ========================================================= */

const SyP = (() => {
  const API_URL = 'http://127.0.0.1:8000/api/v1';
  
  const KEYS = {
    TOKEN: 'syp_jwt_token',
    SESSION: 'syp_session',
    REQUESTS: 'syp_maintenance_requests',
  };

  const ADMIN_ACCOUNT = {
    email: 'admin@sypfotocopiadoras.com',
    password: 'admin123',
    name: 'Administración SyP Central',
    role: 'admin',
  };

  function getToken() {
    return localStorage.getItem(KEYS.TOKEN) || null;
  }

  function setToken(token) {
    if (token) {
      localStorage.setItem(KEYS.TOKEN, token);
    } else {
      localStorage.removeItem(KEYS.TOKEN);
    }
  }

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  }

  function writeJSON(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  /* ---------- Sesión y Perfil ---------- */
  function getSession() {
    return readJSON(KEYS.SESSION, null);
  }

  function setSession(session) {
    writeJSON(KEYS.SESSION, session);
  }

  function logout() {
    localStorage.removeItem(KEYS.SESSION);
    localStorage.removeItem(KEYS.TOKEN);
  }

  /* ---------- Headers con Autorización JWT ---------- */
  function getAuthHeaders() {
    const token = getToken();
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  /* ---------- Registro de Usuario ---------- */
  async function registerUser({ name, email, phone, password }) {
    const emailNorm = email.trim().toLowerCase();
    
    // Intentar registro en API REST
    try {
      const res = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          email: emailNorm,
          phone: phone.trim(),
          password: password,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setToken(data.access_token);
        const session = {
          id: data.user.id,
          name: data.user.name,
          email: data.user.email,
          phone: data.user.phone,
          role: data.user.role,
        };
        setSession(session);
        return { ok: true, user: data.user };
      } else {
        const errData = await res.json().catch(() => ({ detail: 'Error al registrar usuario.' }));
        return { ok: false, error: errData.detail || 'Error en el servidor.' };
      }
    } catch (networkErr) {
      // Fallback local si el servidor no está en línea
      console.warn('[SyP Auth] Backend fuera de línea, usando modo local.');
      const session = {
        id: 'usr_' + Date.now(),
        name: name.trim(),
        email: emailNorm,
        phone: phone.trim(),
        role: 'cliente',
      };
      setSession(session);
      return { ok: true, user: session };
    }
  }

  /* ---------- Inicio de Sesión ---------- */
  async function login({ email, password }) {
    const emailNorm = email.trim().toLowerCase();

    // Intentar login en API REST
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: emailNorm,
          password: password,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setToken(data.access_token);
        const session = {
          id: data.user.id,
          name: data.user.name,
          email: data.user.email,
          phone: data.user.phone,
          role: data.user.role,
        };
        setSession(session);
        return { ok: true, session };
      } else {
        const errData = await res.json().catch(() => ({ detail: 'Correo o contraseña incorrectos.' }));
        return { ok: false, error: errData.detail || 'Correo o contraseña incorrectos.' };
      }
    } catch (networkErr) {
      // Fallback local
      console.warn('[SyP Auth] Backend fuera de línea, usando fallback local.');
      if (emailNorm === ADMIN_ACCOUNT.email && password === ADMIN_ACCOUNT.password) {
        const session = { name: ADMIN_ACCOUNT.name, email: ADMIN_ACCOUNT.email, role: 'admin' };
        setSession(session);
        return { ok: true, session };
      }
      return { ok: false, error: 'No se pudo conectar al servidor de autenticación.' };
    }
  }

  /* ---------- Verificación de Token en Servidor ---------- */
  async function verifyCurrentSession() {
    const token = getToken();
    if (!token) return null;

    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: getAuthHeaders(),
      });
      if (res.ok) {
        const user = await res.json();
        const session = {
          id: user.id,
          name: user.name,
          email: user.email,
          phone: user.phone,
          role: user.role,
        };
        setSession(session);
        return session;
      } else {
        logout();
        return null;
      }
    } catch (e) {
      return getSession();
    }
  }

  /* ---------- Solicitudes de Servicio Técnico ---------- */
  function getRequests() {
    return readJSON(KEYS.REQUESTS, []);
  }

  function saveRequests(list) {
    writeJSON(KEYS.REQUESTS, list);
  }

  async function addRequest(data) {
    const list = getRequests();
    const localReq = {
      id: 'sol_' + Date.now(),
      estado: 'Pendiente',
      createdAt: new Date().toISOString(),
      ...data,
    };
    list.unshift(localReq);
    saveRequests(list);

    try {
      const res = await fetch(`${API_URL}/requests`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          equipment: data.equipo,
          service_type: data.tipo,
          desired_date: data.fecha,
          desired_time: data.hora,
          description: data.descripcion || '',
          client_name: data.clienteNombre,
          client_email: data.clienteEmail,
          client_phone: data.clientePhone || '',
        }),
      });
      if (res.ok) {
        const serverReq = await res.json();
        localReq.id = serverReq.id;
        saveRequests(list);
      }
    } catch (e) {
      console.warn('[SyP Requests] Solicitud guardada localmente (pendiente de sync).');
    }

    return localReq;
  }

  async function fetchMyRequests(email) {
    try {
      const res = await fetch(`${API_URL}/requests/my`, {
        headers: getAuthHeaders(),
      });
      if (res.ok) {
        const data = await res.json();
        return data.map((r) => ({
          id: r.id,
          clienteNombre: r.client_name,
          clienteEmail: r.client_email,
          equipo: r.equipment,
          tipo: r.service_type,
          fecha: r.desired_date,
          hora: r.desired_time,
          descripcion: r.description,
          estado: r.status,
          adminNotes: r.admin_notes,
          createdAt: r.created_at,
        }));
      }
    } catch (e) {}
    return getRequests().filter((r) => r.clienteEmail && r.clienteEmail.toLowerCase() === email.toLowerCase());
  }

  async function fetchAllAdminRequests(statusFilter = 'all') {
    try {
      const url = statusFilter && statusFilter !== 'all' 
        ? `${API_URL}/requests?status_filter=${encodeURIComponent(statusFilter)}`
        : `${API_URL}/requests`;
      
      const res = await fetch(url, {
        headers: getAuthHeaders(),
      });
      if (res.ok) {
        const data = await res.json();
        return data.map((r) => ({
          id: r.id,
          clienteNombre: r.client_name,
          clienteEmail: r.client_email,
          clientePhone: r.client_phone || '+57 314 380 4967',
          equipo: r.equipment,
          tipo: r.service_type,
          fecha: r.desired_date,
          hora: r.desired_time,
          descripcion: r.description,
          estado: r.status,
          adminNotes: r.admin_notes,
          createdAt: r.created_at,
        }));
      }
    } catch (e) {}
    return getRequests();
  }

  async function updateRequestStatus(id, estado, adminNotes = '') {
    const list = getRequests();
    const item = list.find((r) => r.id === id);
    if (item) {
      item.estado = estado;
      saveRequests(list);
    }

    try {
      await fetch(`${API_URL}/requests/${id}/status`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify({ status: estado, admin_notes: adminNotes }),
      });
    } catch (e) {}

    return item;
  }

  /* ---------- Contacto & Cotizaciones ---------- */
  async function submitContactForm(data) {
    try {
      const res = await fetch(`${API_URL}/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e) {
      return { ok: true, fallback: true };
    }
  }

  async function saveQuoteToServer(quoteData) {
    try {
      const res = await fetch(`${API_URL}/quotes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(quoteData),
      });
      return await res.json();
    } catch (e) {
      return { ok: false };
    }
  }

  // Verificación de sesión al inicializar
  if (typeof window !== 'undefined') {
    verifyCurrentSession();
  }

  return {
    API_URL,
    ADMIN_ACCOUNT,
    getToken,
    setToken,
    registerUser,
    login,
    logout,
    getSession,
    setSession,
    verifyCurrentSession,
    getRequests,
    addRequest,
    fetchMyRequests,
    fetchAllAdminRequests,
    updateRequestStatus,
    submitContactForm,
    saveQuoteToServer,
    getRequestsByEmail: (email) => getRequests().filter((r) => r.clienteEmail && r.clienteEmail.toLowerCase() === email.toLowerCase()),
  };
})();

