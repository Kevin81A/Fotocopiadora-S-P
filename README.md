# Fotocopiadora SyP — Web App

> **"Precisión de planta. Servicio de barrio."**
> A modern, fully functional front-end web application for **Fotocopiadora SyP**, a photocopier and printer sales & repair shop based in **Neiva, Huila, Colombia**.

---

## 🖥️ Live Preview

> Open `index.html` with [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) in VS Code, or run the included PowerShell server:
> ```powershell
> powershell -ExecutionPolicy Bypass -File servidor.ps1
> ```
> Then navigate to **http://localhost:5500**

---

## 📸 Features

- **Full multi-page website** — 7 pages, all internally linked
- **Product catalog** with category filters, live search, and 16+ products
- **Shopping cart** — persists across pages using `localStorage`
- **WhatsApp Checkout** — cart generates a pre-filled WhatsApp message to confirm orders
- **Technical Service booking** — logged-in clients can schedule maintenance visits
- **Auth system** — login/register (simulated with `localStorage`), admin & client roles
- **Admin panel** — view all service requests, filter by status, update status, export CSV, and send WhatsApp reminders to clients
- **Contact page** — embedded Google Maps, contact form that builds a WhatsApp message
- **Scroll reveal animations** — Intersection Observer API, no external libraries
- **Fully responsive** — mobile-first, works on all screen sizes
- **No dependencies** — pure HTML, CSS, and vanilla JavaScript

---

## 📁 Project Structure

```
syp-web/
├── .vscode/
│   ├── settings.json        # Live Server config (port 5500)
│   └── launch.json          # Chrome debug config
├── css/
│   └── style.css            # Complete design system (~1300 lines)
├── js/
│   ├── products.js          # Product data + SVG icons + formatCOP()
│   ├── auth.js              # Auth & service requests (localStorage)
│   └── main.js              # Cart, checkout modal, nav, animations
├── index.html               # Homepage — hero, categories, featured products
├── nosotros.html            # About — history, values, stats
├── contacto.html            # Contact — map, hours, WhatsApp form
├── productos.html           # Catalog — filters + search
├── servicio-tecnico.html    # Service booking (requires login)
├── login.html               # Login / Register
├── admin.html               # Admin panel (requires admin role)
├── servidor.ps1             # PowerShell static HTTP server (no Node needed)
└── README.md
```

---

## 🚀 Getting Started

### Option 1 — VS Code + Live Server (recommended)

1. Install [VS Code](https://code.visualstudio.com/)
2. Install the [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
3. Open the `syp-web/` folder in VS Code
4. Right-click `index.html` → **"Open with Live Server"**

### Option 2 — PowerShell server (no Node.js required)

```powershell
cd syp-web
powershell -ExecutionPolicy Bypass -File servidor.ps1
```

Opens automatically at **http://localhost:5500/index.html**

### Option 3 — Any static server

```bash
# Python 3
python -m http.server 5500

# Node.js (if available)
npx live-server --port=5500
```

---

## 🔐 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@fotocopiadorasyp.com` | `admin123` |
| **Client** | Register a new account on `/login.html` | — |

> ⚠️ Auth is simulated with `localStorage`. No real backend — passwords are **not** hashed. Do not use real credentials.

---

## 🛒 How the Cart Works

1. Add products from any page (cart persists across navigation via `localStorage`)
2. Click the **Cart** button in the header
3. Click **"Proceder al pago"** — a confirmation modal opens
4. Click **"Confirmar por WhatsApp"** — opens WhatsApp with the order pre-filled
5. Cart clears automatically after confirmation

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Markup | HTML5 (semantic) |
| Styles | CSS3 — custom design system, CSS Variables, Grid, Flexbox |
| Scripts | Vanilla JavaScript (ES6+) |
| Fonts | Google Fonts — Archivo Black, Inter, IBM Plex Mono |
| Storage | `localStorage` (cart, auth, service requests) |
| Server | PowerShell `System.Net.HttpListener` (dev only) |

---

## 📄 Pages

| Page | File | Description |
|------|------|-------------|
| Home | `index.html` | Hero, product categories, featured products, services |
| Products | `productos.html` | Full catalog with search and category filters |
| About | `nosotros.html` | Company history, values, stats |
| Contact | `contacto.html` | Address, hours, Google Maps, WhatsApp form |
| Service | `servicio-tecnico.html` | Schedule maintenance visits (client login required) |
| Login | `login.html` | Login / register with tab switching |
| Admin | `admin.html` | Service request management (admin login required) |

---

## 🎨 Design System

The site uses a custom **"Registration Mark"** design concept inspired by print press marks (the ⊕ symbol).

**Color palette:**
- `--ink: #0B0B0C` — Primary black
- `--red: #E4002B` — Brand red
- `--paper: #FAFAF8` — Background off-white
- `--steel: #6B6D70` — Secondary text

**Typography:**
- `Archivo Black` — Display headings
- `Inter` — Body text
- `IBM Plex Mono` — Labels, prices, codes

---

## 🗺️ Roadmap (Backend Phase)

- [ ] PHP + MySQL backend (`api/` folder)
- [ ] Real authentication with password hashing (`password_hash`)
- [ ] Product database with images
- [ ] Online payments (Wompi / PayU for Colombia)
- [ ] Email notifications for service requests
- [ ] WhatsApp Business API integration

---

## 🤝 Business

**Fotocopiadora SyP**
- 📍 Av La Toma # 3-30, Neiva, Huila, Colombia
- 📞 +57 314 380 4967 (Gladys) / +57 317 820 4193 (Juan)
- 📘 [Facebook](https://web.facebook.com/copycaes/)
- 📸 [Instagram](https://www.instagram.com/copycaess/)
- 🕐 Mon–Fri: 8am–12pm · 2pm–6pm | Sat: 8am–12pm

---

## 📝 License

This project is proprietary software developed for **Fotocopiadora SyP**.
All rights reserved © 2026 Fotocopiadora SyP.
