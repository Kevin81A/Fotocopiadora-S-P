# Design System: SYP (Fotocopiadora SyP)
**Project Title:** Fotocopiadora SyP — Web Platform & Equipment Management  
**Design Philosophy:** "Precisión de planta. Servicio de barrio." (Industrial Print-Press Precision with Local Neighborhood Trust)

---

## 1. Visual Theme & Atmosphere

The design system for **Fotocopiadora SyP** is built around an **Editorial Industrial / Print-Shop Aesthetic** inspired by printing press registration marks (⊕), CMYK calibration targets, and technical machinery documentation.

* **Tone:** Utilitarian, reliable, high-precision, honest, accessible.
* **Density:** Balanced grid density with generous typographic breathing room, high contrast, and crisp hairline dividers.
* **Geometry:** Sharp, squared-off corners (`border-radius: 2px`) evoking physical paper sheets, laser toner cartridges, and heavy-duty copier hardware.
* **Elevation:** Minimalist elevation relying on 1px precision borders rather than heavy blur shadows, providing an authentic blueprint feel.

---

## 2. Color Palette & Roles

| Semantic Token | Hex Code | Dark Mode Hex | Functional Role |
| :--- | :--- | :--- | :--- |
| **`--ink` (Primary Black)** | `#0B0B0C` | `#F4F4F2` | Main headlines, high-emphasis text, dark hero sections, primary buttons. |
| **`--paper` (Background Paper)**| `#FAFAF8` | `#121214` | Clean background canvas reminiscent of premium bond paper. |
| **`--paper-dim` (Card Surface)**| `#F1F0EC` | `#1A1A1E` | Secondary backgrounds, category filter chips, search bars, table headers. |
| **`--red` (Brand Accent)** | `#E4002B` | `#E4002B` | Brand signature color (magenta/red registration mark), primary CTA buttons, focus rings, status highlights. |
| **`--red-dark` (Active Crimson)**| `#B4001F` | `#FF2D55` | Button hover/pressed states, discount badges. |
| **`--steel` (Technical Neutral)**| `#6B6D70` | `#9D9EA3` | Secondary descriptions, technical specs, breadcrumbs, placeholder labels. |
| **`--line` (Hairline Border)** | `#E3E2DF` | `#2B2B30` | 1px grid dividers, card outlines, input borders. |

---

## 3. Typography Rules

* **Display / Headings (`--font-display`):** `Archivo Black, sans-serif`
  * *Usage:* Page titles (`h1`), section titles (`h2`), high-impact banners.
  * *Characteristics:* Heavy grotesque weight, tight tracking (`-0.01em`), authoritative presence.
* **Body & Interface (`--font-body`):** `Inter, sans-serif`
  * *Usage:* Paragraphs, descriptions, navigation links, form labels.
  * *Weights:* 400 (regular), 500 (medium), 600 (semibold), 700 (bold).
* **Technical & Data Mono (`--font-mono`):** `IBM Plex Mono, monospace`
  * *Usage:* Product prices, model codes, SKUs, timestamps, eyebrows, status badges (`.eyebrow`, `.product-price`).
  * *Characteristics:* Monospace alignment for numbers and technical data.

---

## 4. Component Patterns & Styling

### 4.1 Buttons
* **Primary Button (`.btn-primary`):** Background `--red` (`#E4002B`), text `#FFFFFF`, font-weight 600, border-radius 2px, subtle translateY on hover.
* **Secondary / Outline (`.btn-outline`):** Background transparent, 1px solid `--line`, text `--ink`, hover border `--ink`.
* **Add to Cart / Share Button (`.add-btn`):** 36x36px square icon button, hairline border, hover fill with smooth micro-interaction.

### 4.2 Cards & Containers
* **Product Cards (`.product-card`):** Flat background `--paper-dim`, 1px border `--line`, sharp 2px radius, top media box with category vector icons, bottom pricing bar.
* **Feature / Service Cards (`.service-card`):** Border `--line`, eyebrow in mono red, bold headline, generous internal padding (32px).
* **Compatibility Finder Box (`.compat-finder`):** Highlight container with 3px solid red left border, dual-column select grid.

### 4.3 Inputs & Forms
* **Input Fields (`input`, `select`, `textarea`):** 1px border `--line`, background `--paper`, text `--ink`, padding `12px 14px`, 2px radius. Focus state produces a 2px outline in `--red`.
* **Filter Chips (`.chip`):** Pill-shaped toggle chips (`border-radius: 999px`), inactive border `--line`, active state fills `--ink` with `--paper` text.

### 4.4 Status Badges
* **Pendiente:** Yellow/Orange background (`#f57c00`), white mono text.
* **Confirmada / En Proceso:** Blue/Purple background (`#0288d1` / `#7b1fa2`), white mono text.
* **Completada:** Green background (`#2e7d32`), white mono text.

---

## 5. Layout & Grid Principles

* **Max Width:** `--max-w: 1200px` centered with `24px` horizontal gutters.
* **Header Height:** Fixed `76px` with sticky navigation bar and registration mark logo.
* **Product Grid:** Responsive CSS Grid (`repeat(auto-fill, minmax(270px, 1fr))` on desktop, 2 columns on tablet, 1 column on mobile).
* **Motion & Animation:** `IntersectionObserver` scroll reveals with staggered entry delays (0.06s), cart count pulse (`@keyframes bump`), and registration crosshair snap (`@keyframes reg-snap`).
