# 🖨️ Plataforma Web & Backend — Fotocopiadora SyP

> **"Precisión de planta. Servicio de barrio."**  
> Aplicación web integral de comercio electrónico, gestión de servicio técnico y administración comercial para **Fotocopiadoras SyP** (Neiva, Huila, Colombia).

---

## 🌐 Enlaces Oficiales del Proyecto

| Recurso | Enlace Directo | Descripción |
|---|---|---|
| 🚀 **Sitio Web Funcional en Vivo** | **[https://kevin81a.github.io/Fotocopiadora-S-P/](https://kevin81a.github.io/Fotocopiadora-S-P/)** | **Despliegue activo en GitHub Pages** (acceso directo e interactivo) |
| 💻 **Repositorio en GitHub** | **[https://github.com/Kevin81A/Fotocopiadora-S-P](https://github.com/Kevin81A/Fotocopiadora-S-P)** | Código fuente consolidado en la rama `main` |

---

## 📑 Paquete Documental Completo para Revisión del Instructor

Toda la documentación técnica y metodológica oficial exigida para el proyecto se encuentra en la carpeta [`docs/`](./docs/):

1. **`01_SRS_Fotocopiadoras_SyP.docx`**: Especificación de Requisitos de Software bajo estándar IEEE 830 adaptado.
2. **`02_Manual_de_Usuario_SyP.docx`**: Manual integral para clientes y personal administrativo.
3. **`03_Manual_Tecnico_y_Arquitectura.docx`**: Arquitectura del sistema, capas de software y diagramas C4/UML.
4. **`04_Diccionario_y_Modelo_Base_Datos.docx`**: Modelo relacional, tablas, tipos de datos, restricciones e índices.
5. **`05_Manual_de_Instalacion_y_Despliegue.docx`**: Guía paso a paso para despliegue local y producción.
6. **`06_Plan_y_Matriz_de_Pruebas.docx`**: Casos de prueba unitarios, de integración, seguridad y validación E2E.
7. **`07_Acta_de_Entrega_y_Cierre.docx`**: Documento formal de entrega, hitos y conformidad del producto.
8. **Auditorías Técnicas**:
   - `docs/AUDITORIA_DISENO_FUNCIONALIDAD.md`: Auditoría de experiencia de usuario y funcionalidad.
   - `docs/AUDITORIA_SEGURIDAD_STRIX.md`: Análisis de vulnerabilidades y hardening de seguridad.

---

## 📁 Estructura Consolidada del Proyecto (`main`)

```
Fotocopiadora-S-P/
├── css/
│   └── style.css                     # Sistema de diseño completo (Variables CSS, Grid, Flexbox, Dark Mode)
├── js/
│   ├── products.js                   # Catálogo de productos, compatibilidades e iconos
│   ├── auth.js                       # Autenticación JWT, sesiones y lógica de cliente/admin
│   └── main.js                       # Carrito, checkout WhatsApp/PSE, diagnóstico SC y PWA
├── img/                              # Galería optimizada de equipos, insumos y repuestos
├── docs/                             # Documentación formal completa (7 DOCX + Diagramas + Auditorías)
├── fastapi_backend/                  # Backend REST API en Python FastAPI
│   ├── main.py                       # Endpoints de autenticación, productos, pedidos, cotizaciones
│   ├── models.py                     # Esquemas Pydantic y modelos relacionales
│   ├── database.py                   # Conexión SQLite y pool de sesiones SQLAlchemy
│   ├── security.py                   # Hashing Bcrypt, tokens JWT y control de acceso RBAC
│   ├── seed_data.py                  # Script de sembrado de datos iniciales
│   ├── test_api.py                   # Suite de pruebas automatizadas
│   ├── requirements.txt              # Dependencias de Python
│   └── syp.db                        # Base de datos pre-configurada
├── index.html                        # Página de inicio (Hero, catálogo destacado, cotizador rápido)
├── productos.html                    # Catálogo interactivo con filtros por categoría y búsqueda en vivo
├── servicio-tecnico.html             # Módulo de solicitud de servicio, errores SC Ricoh y renting
├── contacto.html                     # Información de contacto, mapa y canal WhatsApp
├── nosotros.html                     # Historia empresarial, equipo y valores
├── login.html                        # Portal de autenticación y registro de usuarios
├── admin.html                        # Panel de control administrativo y analíticas
├── cotizacion.html                   # Módulo de cotizaciones con desglose detallado
├── offline.html                      # Vista de contingencia para navegación sin conexión
├── sw.js                             # Service Worker v6 para soporte PWA y cache offline
├── manifest.json                     # Manifiesto para instalación como aplicación web progresiva
├── iniciar_servidores.ps1            # Script para iniciar Frontend y Backend en paralelo
├── servidor.ps1                      # Servidor HTTP estático nativo en PowerShell
└── README.md                         # Este documento de referencia
```

---

## 🔐 Credenciales de Demostración

| Rol | Correo Electrónico | Contraseña | Acceso |
|---|---|---|---|
| **Administrador** | `admin@fotocopiadorasyp.com` | `admin123` | Panel administrativo (`admin.html`), gestión de pedidos, clientes y solicitudes |
| **Cliente Demo** | `cliente@ejemplo.com` | `cliente123` | Solicitudes de servicio técnico, cotizaciones y pedidos |

---

## 🚀 Guía de Ejecución Local

### Opción 1: Inicio Rápido con PowerShell (Frontend + Backend)
Ejecute el script automatizado que levanta ambos entornos simultáneamente:
```powershell
powershell -ExecutionPolicy Bypass -File iniciar_servidores.ps1
```

### Opción 2: Solo Frontend (Servidor Ligero)
```powershell
powershell -ExecutionPolicy Bypass -File servidor.ps1
```
El navegador abrirá automáticamente **http://localhost:5500/index.html**.

### Opción 3: Backend FastAPI Manual
```powershell
cd fastapi_backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
- Documentación interactiva Swagger: **http://localhost:8000/docs**
- Documentación alternativa ReDoc: **http://localhost:8000/redoc**

---

## 🛠️ Tecnologías Empleadas

- **Frontend**: HTML5 Semántico, CSS3 moderno (Custom Properties, CSS Grid, Flexbox), JavaScript ES6+ Vanilla (sin frameworks pesados para máxima velocidad).
- **PWA (Progressive Web App)**: Service Worker v6 con caché híbrida (Stale-While-Revalidate) y manifiesto para instalación en móviles y escritorio.
- **Backend API**: Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic v2.
- **Seguridad**: Autenticación Bearer JWT, algoritmos de hashing Bcrypt, sanitización de entradas, protección contra IDOR y cabeceras de seguridad.
- **Despliegue**: GitHub Pages (Frontend en producción) y Git para versionamiento.

---

## 🏢 Contacto y Soporte Comercial

**Fotocopiadora SyP**  
- **Dirección**: Avenida La Toma #3A-20, Neiva, Huila, Colombia  
- **Atención al Cliente**: +57 314 380 4967 / +57 317 820 4193  
- **Correo**: `Fotocopiadorassp@outlook.com`
