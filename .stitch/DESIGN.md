# Design System: SYP (Fotocopiadora SyP)
**Project Title:** Fotocopiadora SyP — Web Platform & Equipment Management  
**Design Philosophy:** "Precisión de planta. Servicio de barrio." (Industrial Print-Press Precision with Local Neighborhood Trust & Modern Interactive Polish)

---

## 1. Visual Theme & Atmosphere

The design system for **Fotocopiadora SyP** fuses an **Editorial Industrial / Print-Shop Aesthetic** (registration marks ⊕, CMYK calibration accents, precise hairline dividers) with **modern dynamic engagement** (hero sliders, smooth product carousels, infinite brand marquee tickers, and interactive floating assistance).

* **Tone:** High-precision, energetic, trustworthy, transparent, accessible.
* **Density:** Balanced grid density with generous typographic breathing room, high contrast, and tactile card feedback.
* **Geometry:** Modern industrial corners (`border-radius: 4px` / `8px` for cards; `999px` for pills and floating widgets).
* **Elevation:** Multi-layer depth with diffuse shadows (`box-shadow: 0 10px 30px rgba(0,0,0,0.08)`), glassmorphism (`backdrop-filter: blur(12px)`), and subtle ambient gradient lighting.

---

## 2. Color Palette & Roles

| Semantic Token | Light Mode Hex | Dark Mode Hex | Functional Role |
| :--- | :--- | :--- | :--- |
| **`--ink` (Primary Deep)** | `#0B0B0C` | `#F4F4F2` | Main headlines, high-emphasis text, dark hero slider background, primary buttons. |
| **`--paper` (Background Surface)**| `#FAFAF8` | `#121214` | Clean canvas background reminiscent of heavy bond paper. |
| **`--paper-dim` (Card Surface)**| `#F1F0EC` | `#1A1A1E` | Secondary container fill, category filter chips, search bars, marquee strip. |
| **`--red` (Brand Accent)** | `#E4002B` | `#E4002B` | Brand signature color (magenta/red registration mark), primary CTA buttons, focus rings, status highlights. |
| **`--red-dark` (Active Crimson)**| `#B4001F` | `#FF2D55` | Button hover/pressed states, discount badges. |
| **`--steel` (Technical Neutral)**| `#6B6D70` | `#9D9EA3` | Secondary descriptions, technical specs, breadcrumbs, placeholder labels. |
| **`--line` (Hairline Border)** | `#E3E2DF` | `#2B2B30` | 1px grid dividers, card outlines, input borders. |

---

## 3. Dynamic & Interactive Components

### 3.1 Hero Carousel / Slider (`.hero-slider-wrap`)
* **Slides Track:** 3 feature slides with autoplay (6s interval), smooth slide transition (`cubic-bezier(0.16, 1, 0.3, 1)`), pause on hover, and manual arrow controls.
* **Slide 1:** Fotocopiadoras & Multifuncionales Láser Ricoh (Línea Exclusiva MP, IM y Pro Series).
* **Slide 2:** Servicio Técnico Especializado a Domicilio en Neiva.
* **Slide 3:** Tóneres, Insumos y Recargas Certificadas Grado A+ para equipos Ricoh.
* **Indicators:** Progress-bar animated bullets with active length expansion (`width: 56px`).

### 3.2 Infinite Ricoh Ecosystem Marquee (`.marquee-container`)
* **Continuous Loop:** Seamless marquee ticker displaying the full Ricoh ecosystem (RICOH, RICOH MP SERIES, RICOH IM COLOR, RICOH AFICIO, RICOH PRO INDUSTRIAL, TÓNER GRADO A+ RICOH, REPUESTOS ORIGINALES RICOH, SOPORTE TÉCNICO OFICIAL NEIVA).
* **Hover State:** Pauses animation and scales hovered brand logos with high-contrast color reveal.

### 3.3 Product Carousel (`.product-slider-wrapper`)
* **Horizontal Scroll:** Smooth-scrolling snap track (`scroll-snap-type: x mandatory`) with left/right control arrows and touch swipe support.
* **Cards:** Glassmorphism headers, discount tags (`-15%`), stock alerts (`Pocas unidades` / `Nuevo`), and one-click WhatsApp quote buttons.

### 3.4 Floating WhatsApp Assistant Widget (`.floating-assistant-wrap`)
* **Notification Pulse:** Floating green WhatsApp button with active message badge (`1`) and gentle floating animation (`@keyframes float-pulse`).
* **Advisor Bubble:** Interactive bubble with avatar and personal greeting: *"Gladys Solano · SyP: ¿Buscas tóner o mantenimiento hoy?"*.

---

## 4. Typography Rules

* **Display / Headings (`--font-display`):** `Archivo Black, sans-serif`
  * *Usage:* Page titles (`h1`), section titles (`h2`), hero slide headlines.
  * *Characteristics:* Heavy grotesque weight, tight tracking (`-0.02em`), authoritative presence.
* **Body & Interface (`--font-body`):** `Inter, sans-serif`
  * *Usage:* Paragraphs, descriptions, navigation links, form labels.
  * *Weights:* 400 (regular), 500 (medium), 600 (semibold), 700 (bold).
* **Technical & Data Mono (`--font-mono`):** `IBM Plex Mono, monospace`
  * *Usage:* Product prices, model codes, SKUs, timestamps, eyebrows, status badges (`.eyebrow`, `.product-price`).
