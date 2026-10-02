/* =========================================================
   FOTOCOPIADORAS SyP — Datos de productos (demo front-end)
   En la fase de back-end, este arreglo será reemplazado por
   una consulta a la base de datos MySQL vía PHP (ej. fetch
   a api/productos.php que devuelva JSON).
   ========================================================= */

const CATEGORIES = [
  { id: 'fotocopiadoras', label: 'Fotocopiadoras' },
  { id: 'impresoras', label: 'Impresoras' },
  { id: 'tintas', label: 'Tintas y Tóneres' },
  { id: 'repuestos', label: 'Repuestos' },
  { id: 'accesorios', label: 'Accesorios' },
  { id: 'mantenimiento', label: 'Mantenimiento' },
];

/* Íconos de línea (originales, trazo simple) por categoría */
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
    name: 'Multifuncional Láser Color 2554',
    cat: 'fotocopiadoras',
    price: 3400000,
    spec: '35 ppm · copia, imprime y escanea · hasta 20.000 pág/mes',
    stock: 'ok',
  },
  {
    id: 'sp-600bn',
    name: 'Multifuncional Láser B/N 600',
    cat: 'fotocopiadoras',
    price: 3600000,
    spec: '60 ppm · equipo de escritorio compacto',
    stock: 'low',
  },
  {
    id: 'sp-c306',
    name: 'Multifuncional Color Compacta 306',
    cat: 'fotocopiadoras',
    price: 2600000,
    spec: '30 ppm · ideal para oficina pequeña',
    stock: 'ok',
  },
  {
    id: 'sp-p400',
    name: 'Impresora Láser Monocromática P400',
    cat: 'impresoras',
    price: 980000,
    spec: '40 ppm · dúplex automático',
    stock: 'ok',
  },
  {
    id: 'sp-p220c',
    name: 'Impresora Láser Color P220',
    cat: 'impresoras',
    price: 1450000,
    spec: '22 ppm color · red inalámbrica integrada',
    stock: 'ok',
  },
  {
    id: 'sp-ton301',
    name: 'Tóner Compatible Serie 301',
    cat: 'tintas',
    price: 34000,
    spec: 'Rendimiento aprox. 9.000 páginas',
    stock: 'ok',
  },
  {
    id: 'sp-ton4501c',
    name: 'Tóner Color Compatible Serie 4501',
    cat: 'tintas',
    price: 216000,
    spec: '23.000 pág. negro / 17.000 pág. color',
    stock: 'ok',
  },
  {
    id: 'sp-recarga1000',
    name: 'Recarga de Tóner 1000gr Premium',
    cat: 'tintas',
    price: 100000,
    spec: 'Alta densidad · compatible OEM y aftermarket',
    stock: 'low',
  },
  {
    id: 'sp-cil2554',
    name: 'Cilindro OPC Universal 2554',
    cat: 'repuestos',
    price: 61000,
    spec: 'Compatible con múltiples modelos',
    stock: 'ok',
  },
  {
    id: 'sp-banda',
    name: 'Banda de Transferencia Heavy Duty',
    cat: 'repuestos',
    price: 300000,
    spec: 'Vida útil 150.000–200.000 impresiones',
    stock: 'ok',
  },
  {
    id: 'sp-chip',
    name: 'Chip de Tóner Reset Universal',
    cat: 'repuestos',
    price: 15000,
    spec: 'Compatible con múltiples series',
    stock: 'ok',
  },
  {
    id: 'sp-correa',
    name: 'Correa ADF Universal',
    cat: 'accesorios',
    price: 35000,
    spec: 'Alimentador automático de documentos',
    stock: 'ok',
  },
  {
    id: 'sp-bandeja',
    name: 'Bandeja de Papel Adicional 500h',
    cat: 'accesorios',
    price: 420000,
    spec: 'Amplía capacidad de alimentación',
    stock: 'low',
  },
  {
    id: 'sp-kitstd',
    name: 'Kit de Mantenimiento Preventivo Estándar',
    cat: 'mantenimiento',
    price: 180000,
    spec: 'Cauchos, cuchillas y sellos de repuesto',
    stock: 'ok',
  },
  {
    id: 'sp-kitpremium',
    name: 'Kit de Mantenimiento Preventivo Premium',
    cat: 'mantenimiento',
    price: 260000,
    spec: 'Incluye cilindro y film de fusora',
    stock: 'ok',
  },
  {
    id: 'sp-visita',
    name: 'Visita Técnica de Diagnóstico',
    cat: 'mantenimiento',
    price: 45000,
    spec: 'Revisión completa en sitio · Neiva y alrededores',
    stock: 'ok',
  },
];

function formatCOP(value) {
  return '$' + value.toLocaleString('es-CO');
}
