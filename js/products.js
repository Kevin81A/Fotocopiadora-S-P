/* =========================================================
   Fotocopiadora SyP — Catálogo y Matriz de Compatibilidad
   ========================================================= */

const CATEGORIES = [
  { id: 'fotocopiadoras', label: 'Fotocopiadoras' },
  { id: 'impresoras', label: 'Impresoras' },
  { id: 'tintas', label: 'Tintas y Tóneres' },
  { id: 'repuestos', label: 'Repuestos' },
  { id: 'accesorios', label: 'Accesorios' },
  { id: 'mantenimiento', label: 'Mantenimiento' },
];

/* Marcas y Modelos soportados para el Buscador de Compatibilidad */
const BRAND_MODELS = {
  Ricoh: [
    'Aficio MP 301',
    'MP 2554 / 3054 / 3554',
    'MP 4501 / 5001',
    'MP C306 / C406 Color',
    'MP C2003 / C2503 Color',
    'Pro 8100 / 8200'
  ],
  Kyocera: [
    'Ecosys M2040dn',
    'Ecosys M2135dn',
    'TaskAlfa 3011i / 3511i',
    'TaskAlfa 2552ci Color'
  ],
  Canon: [
    'imageRUNNER 2206 / 2520',
    'imageRUNNER ADVANCE C3525i',
    'imageRUNNER 1643i'
  ],
  HP: [
    'LaserJet Pro M404 / M428',
    'LaserJet Enterprise M607 / M608',
    'Color LaserJet Pro MFP M479'
  ]
};

const ICONS = {
  fotocopiadoras: `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="16" width="32" height="18" rx="1.5"/><rect x="13" y="6" width="22" height="10" rx="1"/><rect x="17" y="28" width="14" height="10" rx="0.5"/><circle cx="13" cy="21" r="1.4" fill="currentColor" stroke="none"/><line x1="18" y1="21" x2="30" y2="21"/></svg>`,
  impresoras: `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="10" y="17" width="28" height="14" rx="1.5"/><rect x="14" y="7" width="20" height="10"/><rect x="15" y="31" width="18" height="10"/><circle cx="32" cy="23" r="1.4" fill="currentColor" stroke="none"/></svg>`,
  tintas: `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M24 6 L32 20 A8 8 0 1 1 16 20 Z"/><line x1="19" y1="24" x2="29" y2="24"/></svg>`,
  repuestos: `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="24" cy="24" r="8"/><path d="M24 10v4M24 34v4M38 24h-4M14 24h-4M33.6 14.4l-2.8 2.8M17.2 30.8l-2.8 2.8M33.6 33.6l-2.8-2.8M17.2 17.2l-2.8-2.8"/></svg>`,
  accesorios: `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="14" height="14" rx="1.5"/><rect x="25" y="9" width="14" height="14" rx="1.5"/><rect x="9" y="25" width="14" height="14" rx="1.5"/><rect x="25" y="25" width="14" height="14" rx="1.5"/></svg>`,
  mantenimiento: `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M31 9a8 8 0 0 0-10.9 9.1L9 29.2V39h9.8l11.1-11.1A8 8 0 0 0 39 17a7.9 7.9 0 0 0-1.3-4.4L31.9 18.4 29.6 16 35.4 10.3A8 8 0 0 0 31 9Z"/></svg>`,
};

const PRODUCTS = [
  {
    id: 'sp-2554c',
    name: 'Multifuncional Láser Ricoh MP 2554',
    cat: 'fotocopiadoras',
    price: 3400000,
    spec: '35 ppm · copia, imprime y escanea · hasta 20.000 pág/mes',
    stock: 'ok',
    models: ['MP 2554 / 3054 / 3554'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-600bn',
    name: 'Multifuncional Láser B/N MP 301',
    cat: 'fotocopiadoras',
    price: 1850000,
    spec: '31 ppm · dúplex automático · escáner a color',
    stock: 'ok',
    models: ['Aficio MP 301'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-c306',
    name: 'Multifuncional Color Compacta C306',
    cat: 'fotocopiadoras',
    price: 2600000,
    spec: '30 ppm · pantalla táctil 10.1" · red gigabit',
    stock: 'ok',
    models: ['MP C306 / C406 Color'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-m2040',
    name: 'Kyocera Ecosys M2040dn Multifuncional',
    cat: 'fotocopiadoras',
    price: 2100000,
    spec: '40 ppm B/N · tambor de larga duración (100.000 pág)',
    stock: 'ok',
    models: ['Ecosys M2040dn'],
    brand: 'Kyocera',
  },
  {
    id: 'sp-p400',
    name: 'Impresora Láser Monocromática HP M404',
    cat: 'impresoras',
    price: 980000,
    spec: '40 ppm · dúplex automático · bajo consumo',
    stock: 'ok',
    models: ['LaserJet Pro M404 / M428'],
    brand: 'HP',
  },
  {
    id: 'sp-p220c',
    name: 'Impresora Color Ricoh SP C250',
    cat: 'impresoras',
    price: 1450000,
    spec: '22 ppm color · WiFi y Ethernet integrados',
    stock: 'ok',
    models: ['MP C2003 / C2503 Color'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-ton301',
    name: 'Tóner Compatible Ricoh MP 301 (Tipo 301)',
    cat: 'tintas',
    price: 34000,
    spec: 'Rendimiento aprox. 8.000 páginas al 5%',
    stock: 'ok',
    models: ['Aficio MP 301'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-ton2554',
    name: 'Tóner Negro Ricoh MP 2554 / 3054 / 3554',
    cat: 'tintas',
    price: 78000,
    spec: 'Rendimiento aprox. 24.000 páginas',
    stock: 'ok',
    models: ['MP 2554 / 3054 / 3554'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-ton2040',
    name: 'Tóner Kyocera TK-1175 Compatible',
    cat: 'tintas',
    price: 65000,
    spec: 'Rendimiento aprox. 12.000 páginas',
    stock: 'ok',
    models: ['Ecosys M2040dn', 'Ecosys M2135dn'],
    brand: 'Kyocera',
  },
  {
    id: 'sp-ton4501c',
    name: 'Kit Tóner Color Ricoh MP C306 / C406 (CMYK)',
    cat: 'tintas',
    price: 216000,
    spec: '17.000 pág. negro / 12.000 pág. colores',
    stock: 'ok',
    models: ['MP C306 / C406 Color'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-recarga1000',
    name: 'Polvo de Tóner Universal 1000gr Premium',
    cat: 'tintas',
    price: 95000,
    spec: 'Micro-filtrado de alta densidad · negro profundo',
    stock: 'ok',
    models: ['Aficio MP 301', 'MP 2554 / 3054 / 3554', 'Ecosys M2040dn', 'imageRUNNER 2206 / 2520'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-cil2554',
    name: 'Cilindro Tambor OPC Ricoh MP 2554 / 3554',
    cat: 'repuestos',
    price: 61000,
    spec: 'Duración certificada 60.000 páginas',
    stock: 'ok',
    models: ['MP 2554 / 3054 / 3554'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-cil301',
    name: 'Cilindro OPC + Cuchilla Ricoh MP 301',
    cat: 'repuestos',
    price: 48000,
    spec: 'Kit completo de revelado y limpieza',
    stock: 'ok',
    models: ['Aficio MP 301'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-banda',
    name: 'Banda de Transferencia Ricoh MP C2503 / C306',
    cat: 'repuestos',
    price: 280000,
    spec: 'Vida útil 120.000–150.000 copias',
    stock: 'ok',
    models: ['MP C306 / C406 Color', 'MP C2003 / C2503 Color'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-correa',
    name: 'Gomas de Alimentación de Papel (Pick Up Rollers)',
    cat: 'repuestos',
    price: 28000,
    spec: 'Set x3 unidades antideslizantes',
    stock: 'ok',
    models: ['Aficio MP 301', 'MP 2554 / 3054 / 3554', 'Ecosys M2040dn'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-kitstd',
    name: 'Mantenimiento Preventivo Completo en Taller',
    cat: 'mantenimiento',
    price: 120000,
    spec: 'Desarme, soplado, lubricación y calibración óptica',
    stock: 'ok',
    models: ['Aficio MP 301', 'MP 2554 / 3054 / 3554', 'Ecosys M2040dn'],
    brand: 'Ricoh',
  },
  {
    id: 'sp-visita',
    name: 'Visita Técnica de Emergencia / Diagnóstico',
    cat: 'mantenimiento',
    price: 45000,
    spec: 'Atención prioritaria en sitio · Neiva y perímetro',
    stock: 'ok',
    models: ['Aficio MP 301', 'MP 2554 / 3054 / 3554', 'Ecosys M2040dn', 'imageRUNNER 2206 / 2520'],
    brand: 'Ricoh',
  },
];

function formatCOP(value) {
  return '$' + Number(value).toLocaleString('es-CO');
}
