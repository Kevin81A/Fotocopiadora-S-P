/* =========================================================
   Fotocopiadora SyP — Autenticación y Solicitudes de Servicio
   (simulado con localStorage mientras no existe back-end)

   IMPORTANTE PARA LA FASE DE BACK-END (PHP + MySQL):
   Este archivo concentra TODA la lógica que debería vivir en
   el servidor. Cuando exista la API en PHP, solo hay que
   reemplazar el cuerpo de cada función por un fetch() a los
   endpoints correspondientes (ej. /api/login.php,
   /api/solicitudes.php) sin tocar el resto del sitio, ya que
   las demás páginas solo llaman a estas funciones.

   Tablas que esto simula:
     - usuarios            (SyP.getUsers / SyP.registerUser)
     - solicitudes_servicio(SyP.getRequests / SyP.addRequest)
     - sesión actual        (SyP.getSession / SyP.login / SyP.logout)
   ========================================================= */

const SyP = (() => {
  const KEYS = {
    USERS: 'syp_users',
    SESSION: 'syp_session',
    REQUESTS: 'syp_maintenance_requests',
  };

  // Credenciales de administrador "pre-provisionadas" (así funciona
  // en un sistema real: el rol admin no se auto-asigna en el registro).
  const ADMIN_ACCOUNT = {
    email: 'admin@sypfotocopiadoras.com',
    password: 'admin123',
    name: 'Administración SyP',
    role: 'admin',
  };

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

  /* ---------- Usuarios ---------- */
  function getUsers() {
    return readJSON(KEYS.USERS, []);
  }
  function saveUsers(users) {
    writeJSON(KEYS.USERS, users);
  }
  function findUserByEmail(email) {
    return getUsers().find((u) => u.email.toLowerCase() === email.toLowerCase());
  }

  function registerUser({ name, email, phone, password }) {
    const emailNorm = email.trim().toLowerCase();
    if (emailNorm === ADMIN_ACCOUNT.email || findUserByEmail(emailNorm)) {
      return { ok: false, error: 'Ya existe una cuenta registrada con ese correo.' };
    }
    const user = {
      id: 'u_' + Date.now(),
      name: name.trim(),
      email: emailNorm,
      phone: phone.trim(),
      password, // Demo: en el back-end esto se guarda con hash (password_hash de PHP), nunca en texto plano.
      role: 'cliente',
      createdAt: new Date().toISOString(),
    };
    const users = getUsers();
    users.push(user);
    saveUsers(users);
    setSession(toSessionShape(user));
    return { ok: true, user };
  }

  function login({ email, password }) {
    const emailNorm = email.trim().toLowerCase();
    if (emailNorm === ADMIN_ACCOUNT.email && password === ADMIN_ACCOUNT.password) {
      const session = toSessionShape(ADMIN_ACCOUNT);
      setSession(session);
      return { ok: true, session };
    }
    const user = findUserByEmail(emailNorm);
    if (!user || user.password !== password) {
      return { ok: false, error: 'Correo o contraseña incorrectos.' };
    }
    const session = toSessionShape(user);
    setSession(session);
    return { ok: true, session };
  }

  function toSessionShape(user) {
    return { name: user.name, email: user.email, role: user.role };
  }

  /* ---------- Sesión ---------- */
  function getSession() {
    return readJSON(KEYS.SESSION, null);
  }
  function setSession(session) {
    writeJSON(KEYS.SESSION, session);
  }
  function logout() {
    localStorage.removeItem(KEYS.SESSION);
  }

  /* ---------- Solicitudes de servicio técnico ---------- */
  function getRequests() {
    return readJSON(KEYS.REQUESTS, []);
  }
  function saveRequests(list) {
    writeJSON(KEYS.REQUESTS, list);
  }
  function addRequest(data) {
    const list = getRequests();
    const request = {
      id: 'sol_' + Date.now(),
      estado: 'Pendiente',
      createdAt: new Date().toISOString(),
      ...data,
    };
    list.unshift(request);
    saveRequests(list);

    // Sincronizar con API Django en tiempo real
    try {
      fetch('http://127.0.0.1:8000/api/v1/services/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_name: data.clienteNombre,
          client_email: data.clienteEmail,
          client_phone: data.clientePhone || '3143804967',
          equipment: data.equipo,
          service_type: data.tipo,
          scheduled_date: data.fecha,
          scheduled_time: data.hora,
          description: data.descripcion || '',
        })
      }).catch(() => {});
    } catch (e) {}

    return request;
  }
  function getRequestsByEmail(email) {
    return getRequests().filter((r) => r.clienteEmail.toLowerCase() === email.toLowerCase());
  }
  function updateRequestStatus(id, estado) {
    const list = getRequests();
    const item = list.find((r) => r.id === id);
    if (item) {
      item.estado = estado;
      saveRequests(list);
    }
    return item;
  }

  return {
    ADMIN_ACCOUNT,
    registerUser,
    login,
    logout,
    getSession,
    setSession,
    getRequests,
    addRequest,
    getRequestsByEmail,
    updateRequestStatus,
  };
})();
