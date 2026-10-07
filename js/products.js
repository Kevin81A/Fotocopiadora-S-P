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
    img: 'img/prod_copier.jpg',
    rating: 4.9,
    reviews: 42,
    badge: 'Más Vendido',
    discount: 10,
    speed: '35 ppm',
    dutyCycle: '20.000 pág/mes',
    paperSize: 'Carta, Oficio, Doble Carta (A3 / A4)',
    connectivity: 'Red Gigabit Ethernet, USB 2.0, SD Card',
    functions: 'Copia, Impresión de Red, Escáner Dúplex Color',
    tonerYield: '24.000 páginas al 5%',
    costPerPage: '$8 COP / página',
    compatibleIds: ['sp-ton2554', 'sp-cil2554', 'sp-correa'],
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
    img: 'img/prod_copier.jpg',
    rating: 4.8,
    reviews: 36,
    badge: 'Recomendado',
    speed: '31 ppm',
    dutyCycle: '10.000 pág/mes',
    paperSize: 'Carta, Oficio, Legal (A4)',
    connectivity: 'Red Ethernet 10/100, USB 2.0',
    functions: 'Copia, Impresión, Escáner a Color, Dúplex',
    tonerYield: '8.000 páginas',
    costPerPage: '$9 COP / página',
    compatibleIds: ['sp-ton301', 'sp-cil301', 'sp-correa'],
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
    img: 'img/prod_copier.jpg',
    rating: 5.0,
    reviews: 19,
    badge: 'Color HD',
    speed: '30 ppm Color / B&N',
    dutyCycle: '15.000 pág/mes',
    paperSize: 'Carta, Oficio, Folio',
    connectivity: 'Pantalla Smart 10.1", Gigabit LAN, WiFi opcional',
    functions: 'Multifuncional Color Láser, Escáner de Alta Definición',
    tonerYield: '17.000 pág (Negro) / 12.000 (Color)',
    costPerPage: '$35 COP / pág color',
    compatibleIds: ['sp-ton4501c', 'sp-banda'],
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
    img: 'img/prod_copier.jpg',
    rating: 4.9,
    reviews: 58,
    badge: 'Alto Rendimiento',
    discount: 5,
    speed: '40 ppm',
    dutyCycle: '50.000 pág/mes',
    paperSize: 'Carta, Oficio, Legal',
    connectivity: 'Red Gigabit, USB Host 2.0',
    functions: 'Copia, Impresión, Escaneo Dúplex simultáneo de 1 pasada',
    tonerYield: '12.000 páginas',
    costPerPage: '$7 COP / página',
    compatibleIds: ['sp-ton2040', 'sp-correa'],
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
    img: 'img/prod_printer.jpg',
    rating: 4.7,
    reviews: 24,
    badge: 'Económica',
    speed: '40 ppm',
    dutyCycle: '80.000 pág/mes',
    paperSize: 'Carta, Oficio, Ejecutivo',
    connectivity: 'Red Ethernet, USB 2.0 de alta velocidad',
    functions: 'Impresora Láser Monocromática de Red',
    tonerYield: '10.000 páginas',
    costPerPage: '$11 COP / página',
    compatibleIds: ['sp-recarga1000'],
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
    img: 'img/prod_printer.jpg',
    rating: 4.8,
    reviews: 15,
    badge: 'WiFi Direct',
    speed: '22 ppm Color / B&N',
    dutyCycle: '30.000 pág/mes',
    paperSize: 'Carta, Oficio, A4',
    connectivity: 'WiFi Direct, Ethernet, USB 2.0',
    functions: 'Impresión Láser Color inalámbrica',
    tonerYield: '6.000 páginas',
    costPerPage: '$38 COP / página',
    compatibleIds: ['sp-ton4501c'],
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
    img: 'img/prod_toner.jpg',
    rating: 4.9,
    reviews: 95,
    badge: 'Top Ventas',
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
    img: 'img/prod_toner.jpg',
    rating: 5.0,
    reviews: 73,
    badge: 'Original / Homologado',
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
    img: 'img/prod_toner.jpg',
    rating: 4.8,
    reviews: 31,
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
    img: 'img/hero_toner.jpg',
    rating: 4.9,
    reviews: 29,
    badge: 'Kit x4',
    discount: 8,
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
    img: 'img/prod_toner.jpg',
    rating: 4.9,
    reviews: 64,
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
    img: 'img/prod_supplies.jpg',
    rating: 4.9,
    reviews: 38,
    badge: 'Alta Duración',
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
    img: 'img/prod_supplies.jpg',
    rating: 4.8,
    reviews: 27,
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
    img: 'img/prod_supplies.jpg',
    rating: 5.0,
    reviews: 14,
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
    img: 'img/prod_supplies.jpg',
    rating: 4.7,
    reviews: 41,
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
    img: 'img/service_workshop.jpg',
    rating: 5.0,
    reviews: 83,
    badge: 'Garantizado',
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
    img: 'img/hero_service.jpg',
    rating: 4.9,
    reviews: 97,
    badge: 'Express &lt; 24h',
  },
];

/* ============================================================
   MATRIZ DE DIAGNÓSTICO DE FALLAS (Smart Troubleshooter)
   ============================================================ */
const TROUBLESHOOTING_DATA = [
  {
    id: 'falla-rayas',
    symptom: 'Líneas negras verticales o rayas repetitivas',
    category: 'Calidad de Copia',
    severity: 'Media',
    desc: 'La hoja sale con una o varias líneas negras continuas que manchan el documento a lo largo de la página.',
    diagnosis: 'Cilindro Tambor OPC rayado o cuchilla de limpieza (Cleaning Blade) con desgaste/muescas por residuos de grapas o polvo.',
    solution: 'Reemplazo del Cilindro OPC y Cuchilla de limpieza, más aspirado técnico de la tolva residual.',
    productId: 'sp-cil2554',
    serviceId: 'sp-kitstd',
    urgency: 'Atención en 24h para evitar contaminar la unidad reveladora',
  },
  {
    id: 'falla-atasco',
    symptom: 'Atasco continuo de papel en Bandeja 1 o Alimentador Dúplex',
    category: 'Mecánica de Alimentación',
    severity: 'Alta',
    desc: 'La máquina intenta tomar la hoja pero patina, se arruga en la entrada o reporta error "Atasco de Papel" de inmediato.',
    diagnosis: 'Gomas de arrastre (Pick-up Rollers) cristalizadas, lisas o con suciedad acumulada de papel bond.',
    solution: 'Cambio de set de gomas de alimentación (3 rodillos antideslizantes) y calibración de resorte de presión.',
    productId: 'sp-correa',
    serviceId: 'sp-visita',
    urgency: 'Solución rápida en sitio (< 30 min)',
  },
  {
    id: 'falla-codigo',
    symptom: 'Código de error SC en pantalla (ej. SC 542 / SC 320 / SC 401)',
    category: 'Electrónica y Fusor',
    severity: 'Crítica',
    desc: 'La fotocopiadora se bloquea con una pantalla roja o mensaje de servicio que impide realizar copias o impresiones.',
    diagnosis: 'Falla térmica en termistor/fusor o desincronización de motor poligonal láser. Bloqueo de seguridad preventivo.',
    solution: 'Diagnóstico con multímetro/código de servicio en taller o domicilio, reseteo SP y recambio de pieza averiada.',
    productId: null,
    serviceId: 'sp-visita',
    urgency: 'Prioridad de emergencia inmediata',
  },
  {
    id: 'falla-palido',
    symptom: 'Impresión muy clara, pálida o fondo grisáceo sucio',
    category: 'Densidad y Tóner',
    severity: 'Baja',
    desc: 'El texto no sale negro profundo o el fondo de la hoja queda con sombra de polvo residual.',
    diagnosis: 'Polvo de tóner descalibrado, rodillo magnético sucio o sensor ID de densidad óptico obstruido.',
    solution: 'Recarga con polvo microfiltrado Grado A+ y calibración óptica de sensor TD/ID.',
    productId: 'sp-ton2554',
    serviceId: 'sp-kitstd',
    urgency: 'Mantenimiento preventivo recomendado',
  },
  {
    id: 'falla-ruido',
    symptom: 'Ruido fuerte de carraca / chasquido de engranajes',
    category: 'Tracción Mecánica',
    severity: 'Media',
    desc: 'Al presionar botón de copia se escucha un sonido metálico o chasquido de piñones forzados.',
    diagnosis: 'Engranaje de fusión roto o buje de registro trabado por falta de lubricación de alta temperatura.',
    solution: 'Desarme de módulo de tracción, lubricación sintética y sustitución de piñón desgastado.',
    productId: null,
    serviceId: 'sp-kitstd',
    urgency: 'Requiere revisión para no romper el motor principal',
  },
];

/* ============================================================
   PRUEBA SOCIAL Y CASOS DE ÉXITO EN EL HUILA
   ============================================================ */
const TESTIMONIALS_DATA = [
  {
    id: 'test-1',
    author: 'Dra. Carmen Cecilia Andrade',
    role: 'Administradora · Notaría Segunda de Neiva',
    entity: 'Notaría Segunda de Neiva',
    quote: 'Llevamos más de 4 años con el servicio de renting de Ricoh MP 2554 con Fotocopiadora SyP. El soporte técnico cuando se requiere es inmediato y el suministro de tóner nunca falta.',
    rating: 5,
    city: 'Neiva, Huila',
    metric: '+45.000 copias notariales/mes sin interrupciones',
  },
  {
    id: 'test-2',
    author: 'Lic. Miller González',
    role: 'Coordinador Académico',
    entity: 'Colegio Cooperativo Campestre',
    quote: 'Para la época de exámenes y talleres escolares el volumen de copiado es altísimo. Gladys y Sebastián nos asesoraron con una Kyocera de alto rendimiento que redujo nuestros costos en más del 40%.',
    rating: 5,
    city: 'Neiva, Huila',
    metric: '40% de ahorro frente a compra tradicional',
  },
  {
    id: 'test-3',
    author: 'Ing. Fernando Perdomo',
    role: 'Director de Obra',
    entity: 'Constructora & Proyectos del Huila',
    quote: 'Imprimimos planos, memorias de cálculo y contratos a diario. La calidad de las recargas y el tóner compatible es indistinguible del original, con garantía total.',
    rating: 5,
    city: 'Neiva, Huila',
    metric: '100% de nitidez en planos y contratos',
  },
  {
    id: 'test-4',
    author: 'Sandra Milena Rojas',
    role: 'Propietaria',
    entity: 'Papelería & Centro de Copiado La Toma',
    quote: 'Excelente respaldo en la Av. La Toma. Si una máquina falla, el técnico llega el mismo día. La confianza y el trato familiar son incomparables.',
    rating: 5,
    city: 'Neiva, Huila',
    metric: 'Respuesta técnica en menos de 3 horas',
  },
];

/* ============================================================
   PARÁMETROS PARA LA CALCULADORA DE RENTING
   ============================================================ */
const RENTING_TIERS = {
  mono: [
    { maxVol: 4000, modelId: 'sp-600bn', name: 'Plan Básico Pyme (Ricoh MP 301)', monthlyFee: 190000, includedPages: 3000, extraPagePrice: 28, buyMonthlyEstimate: 290000 },
    { maxVol: 12000, modelId: 'sp-2554c', name: 'Plan Corporativo Pro (Ricoh MP 2554)', monthlyFee: 320000, includedPages: 8000, extraPagePrice: 22, buyMonthlyEstimate: 510000 },
    { maxVol: 50000, modelId: 'sp-m2040', name: 'Plan Alto Volumen Industrial (Kyocera 40ppm)', monthlyFee: 480000, includedPages: 16000, extraPagePrice: 18, buyMonthlyEstimate: 780000 },
  ],
  color: [
    { maxVol: 6000, modelId: 'sp-c306', name: 'Plan Color Studio (Ricoh C306 HD)', monthlyFee: 380000, includedPages: 2500, extraPagePrice: 75, buyMonthlyEstimate: 620000 },
    { maxVol: 50000, modelId: 'sp-c306', name: 'Plan Color Corporativo Pro (Ricoh C2503)', monthlyFee: 560000, includedPages: 6000, extraPagePrice: 65, buyMonthlyEstimate: 940000 },
  ]
};

function getCategoryDefaultImage(cat) {
  switch (cat) {
    case 'fotocopiadoras': return 'img/prod_copier.jpg';
    case 'impresoras': return 'img/prod_printer.jpg';
    case 'tintas': return 'img/prod_toner.jpg';
    case 'repuestos': return 'img/prod_supplies.jpg';
    case 'mantenimiento': return 'img/hero_service.jpg';
    default: return 'img/prod_copier.jpg';
  }
}

function formatCOP(value) {
  return '$' + Number(value).toLocaleString('es-CO');
}

/* ============================================================
   SINCRONIZACIÓN CON BACKEND DJANGO REST FRAMEWORK
   ============================================================ */
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

async function syncProductsFromBackend() {
  try {
    const res = await fetch(`${API_BASE_URL}/products/`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        PRODUCTS.length = 0;
        data.forEach((item) => {
          PRODUCTS.push({
            id: item.id_code,
            name: item.name,
            cat: item.category_slug,
            price: Number(item.price),
            spec: item.spec,
            stock: item.stock_status,
            brand: item.brand_name,
            models: item.compatible_models ? item.compatible_models.split(',').map((m) => m.trim()) : [],
            discount: item.discount_percent || 0,
            img: item.image_url || getCategoryDefaultImage(item.category_slug),
            rating: item.rating || 4.9,
            reviews: item.reviews_count || 25,
            badge: item.badge || '',
            speed: item.speed || '35 ppm',
            dutyCycle: item.duty_cycle || '20.000 pág/mes',
            paperSize: item.paper_size || 'Carta, Oficio, A4',
            connectivity: item.connectivity || 'Red Gigabit, USB 2.0',
            functions: item.functions || 'Copia, Impresión, Escáner',
            tonerYield: item.toner_yield || '15.000 páginas',
            costPerPage: item.cost_per_page || '$10 COP',
            compatibleIds: item.compatible_ids ? item.compatible_ids.split(',').map(s => s.trim()) : [],
          });
        });
        console.log('[SyP] ⚡ Conectado con Backend Django: ' + PRODUCTS.length + ' productos sincronizados.');
        if (typeof applyFilters === 'function') {
          applyFilters(false);
        }
      }
    }
  } catch (e) {
    // Si Django está apagado, continúa con los datos estáticos enriquecidos sin interrumpir
  }
}

// Intentar sincronización al cargar
if (typeof window !== 'undefined') {
  syncProductsFromBackend();
}
