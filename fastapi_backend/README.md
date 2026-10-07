# Fotocopiadora SyP — Backend REST API & Autenticación JWT

Servidor backend robusto desarrollado con **FastAPI**, **SQLite (WAL mode)**, **Bcrypt** y **JSON Web Tokens (JWT)** para la plataforma de comercio electrónico y soporte técnico de **Fotocopiadora SyP** (Neiva, Huila).

---

## 🔒 Arquitectura de Seguridad Implementada

1. **Autenticación con JWT:** Tokens firmados con algoritmo `HS256`, expiración programada y validación de roles en cada endpoint protegido.
2. **Cifrado de Contraseñas:** Hashing unidireccional con **Bcrypt (12 rondas de salt)** en el servidor antes de persistir en base de datos.
3. **Control de Acceso Basado en Roles (RBAC):**
   - **Administrador:** Acceso completo al panel administrativo, gestión de solicitudes de servicio, actualización de estados y edición de productos.
   - **Cliente:** Acceso a su historial personal de mantenimientos, cotizaciones y perfil.
4. **Validación Estricta de Datos:** Esquemas **Pydantic v2** para prevenir inyecciones y datos corruptos.
5. **CORS Seguro:** Configurado para admitir peticiones del frontend web en localhost y producción.

---

## 🚀 Cómo Iniciar el Servidor

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Inicializar y poblar la base de datos
python seed_data.py

# 3. Iniciar servidor FastAPI en puerto 8000
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 📡 Endpoints Principales

- `GET /api/v1/health` — Estado de salud y métricas de base de datos.
- `POST /api/v1/auth/register` — Registro de nuevos clientes.
- `POST /api/v1/auth/login` — Inicio de sesión y emisión de token JWT.
- `GET /api/v1/auth/me` — Perfil del usuario autenticado (requiere `Bearer <token>`).
- `GET /api/v1/products` — Catálogo de productos y repuestos Ricoh.
- `POST /api/v1/requests` — Creación de solicitudes de servicio técnico.
- `GET /api/v1/requests/my` — Historial de solicitudes del cliente.
- `GET /api/v1/requests` — (Admin) Listado de todas las solicitudes con filtros.
- `PATCH /api/v1/requests/{id}/status` — (Admin) Actualización de estado y notas técnicas.
- `POST /api/v1/contact` — Recepción y persistencia de mensajes de contacto.
- `POST /api/v1/quotes` — Registro de cotizaciones comerciales formales.
- `POST /api/v1/counters` — Reporte mensual de contadores de copias para clientes de renting.

---

## 👤 Cuentas de Acceso Pre-provisionadas

- **Administrador Central:** `admin@sypfotocopiadoras.com` / `admin123`
- **Gladys Solano (Ventas & Renting):** `gladys.solano@sypfotocopiadoras.com` / `gladys2026`
- **Juan Sebastián (Taller & Soporte):** `juan.portela@sypfotocopiadoras.com` / `juan2026`
- **Cliente Demo (Notaría 2):** `cliente@notaria2neiva.com` / `cliente123`
