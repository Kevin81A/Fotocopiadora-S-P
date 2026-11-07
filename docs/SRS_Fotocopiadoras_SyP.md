# Especificación de Requisitos de Software (SRS)
## Proyecto: Plataforma Web E-commerce — Fotocopiadoras SyP

**Versión:** 1.0
**Fecha:** 16 de agosto de 2026
**Basado en el análisis de:** [COPY CAESS S.A.S.](https://copycaess.com/) (sitio de referencia, empresa del mismo sector: venta de fotocopiadoras, insumos y servicio técnico)
**Estándar de referencia:** IEEE 830 (adaptado)

---

## 1. Introducción

### 1.1 Propósito
Este documento especifica los requisitos funcionales y no funcionales para el desarrollo de un sitio web de comercio electrónico para **Fotocopiadoras SyP**, empresa dedicada a la venta de fotocopiadoras, impresoras, insumos de impresión (tóners, tintas), repuestos, accesorios y servicio técnico. El documento sirve como guía para el equipo de desarrollo y como acuerdo de alcance con el cliente (propietaria del negocio).

### 1.2 Alcance del producto
El sistema, denominado en este documento **"SyP Web"**, será una plataforma web que permitirá:
- Mostrar un catálogo de productos (fotocopiadoras, impresoras, tóners/tintas, repuestos, accesorios, kits de mantenimiento).
- Permitir a los clientes agregar productos a un carrito de compras y realizar pedidos (checkout).
- Gestionar cuentas de usuario (registro/login) para clientes.
- Ofrecer un módulo de solicitud de servicio técnico.
- Brindar información de contacto, ubicación y canales de atención (WhatsApp, redes sociales).
- Incluir un **panel administrativo** para que el personal del negocio gestione productos, categorías, inventario, pedidos y contenido del sitio, sin depender de un programador.

El sistema NO incluirá en esta primera versión (fuera de alcance):
- Aplicación móvil nativa (solo sitio web responsive).
- Pasarela de pago con tarjeta a través de plataformas internacionales complejas (se evaluará una pasarela local colombiana, ver sección 2.5).
- Sistema de facturación electrónica DIAN integrado (se deja como mejora futura, ver sección 6).
- Módulo de contabilidad o nómina.

### 1.3 Definiciones, acrónimos y abreviaturas
| Término | Definición |
|---|---|
| SRS | Software Requirements Specification (Especificación de Requisitos de Software) |
| SKU | Código único de identificación de un producto |
| Admin | Usuario administrador del sitio (dueña del negocio o personal autorizado) |
| Cliente/Usuario | Persona que navega y compra en el sitio |
| CMS | Sistema de gestión de contenido (panel administrativo) |
| Checkout | Proceso final de compra (revisión de carrito, datos de envío, pago) |
| Responsive | Diseño que se adapta a distintos tamaños de pantalla (móvil, tablet, escritorio) |

### 1.4 Referencias
- Sitio web de referencia analizado: https://copycaess.com/ (empresa Copy Caess S.A.S., Neiva, Colombia).
- Estándar IEEE 830-1998 para especificación de requisitos de software.

### 1.5 Visión general del documento
Este SRS está organizado en: descripción general del producto, requisitos específicos (funcionales, no funcionales, de interfaz), modelo de datos preliminar, y recomendaciones de evolución futura.

---

## 2. Descripción General

### 2.1 Contexto del negocio
Fotocopiadoras SyP es una empresa que, según el modelo de negocio observado en la referencia del sector, se dedica a:
1. **Venta de equipos**: fotocopiadoras multifuncionales e impresoras (nuevas y/o reacondicionadas), con variantes por modelo, velocidad de impresión (ppm) y capacidad mensual de páginas.
2. **Venta de insumos y repuestos**: tóners, cartuchos, cilindros, bandas de transferencia, cuchillas de limpieza, kits de mantenimiento, recargas de tóner, chips, fusoras, etc.
3. **Servicio técnico**: mantenimiento preventivo y correctivo de los equipos vendidos o de terceros.
4. **Atención personalizada**: por WhatsApp, teléfono, y en tienda física.

### 2.2 Perspectiva del producto
SyP Web será un sistema nuevo e independiente (no se integra con sistemas legados existentes), compuesto por:
- **Frontend público**: catálogo, carrito, checkout, autenticación, contacto, servicio técnico.
- **Backend / Panel administrativo**: gestión de productos, categorías, pedidos, usuarios e información del sitio.
- **Base de datos**: almacenamiento de productos, usuarios, pedidos y configuración.

### 2.3 Funciones principales del producto
1. Catálogo de productos navegable y filtrable por categoría y búsqueda por texto.
2. Ficha de producto con variantes (ej. modelo, color de tóner, gramaje).
3. Carrito de compras persistente durante la sesión.
4. Proceso de checkout con captura de datos de envío/facturación.
5. Registro e inicio de sesión de usuarios (clientes).
6. Formulario/flujo de solicitud de servicio técnico.
7. Página de contacto con mapa de ubicación, horarios y enlaces directos a WhatsApp y redes sociales.
8. Panel administrativo con gestión CRUD de productos, categorías, pedidos y mensajes de contacto.

### 2.4 Características de los usuarios
| Tipo de usuario | Descripción | Nivel técnico esperado |
|---|---|---|
| Visitante | Navega el catálogo sin cuenta | Básico |
| Cliente registrado | Se registra, compra, consulta histórico de pedidos | Básico |
| Administrador | Dueña del negocio o personal designado; gestiona catálogo, precios, pedidos e inventario | Básico–medio (requiere panel simple e intuitivo) |
| Técnico de soporte (opcional) | Recibe y gestiona solicitudes de servicio técnico | Básico |

### 2.5 Restricciones generales
- El sitio debe operar en español (Colombia) y mostrar precios en pesos colombianos (COP).
- Debe ser responsive (funcional en móvil, tablet y escritorio), dado que gran parte del tráfico esperado provendrá de WhatsApp y redes sociales.
- El panel administrativo debe ser utilizable por personal sin conocimientos técnicos avanzados.
- Se recomienda evaluar una pasarela de pagos colombiana (ej. Wompi, PayU, Mercado Pago) para checkout con pago en línea; alternativamente, contraentrega o pago por transferencia/WhatsApp como fue observado en el sitio de referencia (que prioriza atención por WhatsApp).
- Presupuesto y tiempo de desarrollo deben ser acordados en un documento aparte (no es objeto de este SRS).

### 2.6 Supuestos y dependencias
- Se asume que la empresa cuenta con un catálogo real de productos (nombres, descripciones, precios, fotos) para poblar el sitio.
- Se asume disponibilidad de un número de WhatsApp Business para integración de contacto directo.
- Se asume que el hosting/dominio serán contratados por el cliente o el equipo de desarrollo, según se acuerde.

---

## 3. Requisitos Específicos

### 3.1 Requisitos Funcionales

#### RF-01 — Página de inicio
El sistema debe mostrar una página de inicio con: mensaje de bienvenida/propuesta de valor de la empresa, productos destacados o en promoción, accesos directos a categorías principales (Fotocopiadoras, Equipos y Suministros, Mantenimiento) y sección de servicios ofrecidos (entrega a domicilio, atención personalizada, productos premium).

#### RF-02 — Catálogo de productos
El sistema debe permitir:
- RF-02.1: Listar todos los productos disponibles con imagen, nombre, categoría y precio.
- RF-02.2: Filtrar productos por categoría (ej. Fotocopiadoras, Impresoras, Tintas y Tóneres, Repuestos, Accesorios, Mantenimiento).
- RF-02.3: Buscar productos por texto (nombre o palabra clave, ej. modelo de impresora).
- RF-02.4: Mostrar el número total de productos encontrados según el filtro/búsqueda aplicado.

#### RF-03 — Ficha de producto
- RF-03.1: Mostrar imagen(es), nombre, categoría, descripción detallada y precio del producto.
- RF-03.2: Permitir selección de variantes cuando aplique (ej. distintos modelos compatibles, gramaje de tóner, nivel premium/estándar).
- RF-03.3: Mostrar disponibilidad de stock (ej. "Pocas unidades", "Agotado").
- RF-03.4: Permitir agregar el producto al carrito desde la ficha.
- RF-03.5: Para fotocopiadoras/equipos, permitir adjuntar o enlazar un brochure/ficha técnica descargable (PDF).

#### RF-04 — Carrito de compras
- RF-04.1: Permitir agregar, modificar cantidad y eliminar productos del carrito.
- RF-04.2: Mostrar el total acumulado en tiempo real.
- RF-04.3: Persistir el contenido del carrito durante la sesión del usuario.
- RF-04.4: Mostrar un contador visible de artículos en el carrito en la cabecera del sitio.

#### RF-05 — Checkout (proceso de compra)
- RF-05.1: Solicitar datos de envío (nombre, dirección, teléfono, ciudad) y datos de facturación básicos.
- RF-05.2: Mostrar resumen del pedido antes de confirmar (productos, cantidades, subtotal, envío si aplica, total).
- RF-05.3: Ofrecer al menos un método de pago (a definir: pasarela en línea, transferencia bancaria, contraentrega, o coordinación por WhatsApp).
- RF-05.4: Generar un número de pedido único y enviar confirmación al cliente (por correo y/o WhatsApp).

#### RF-06 — Cuentas de usuario
- RF-06.1: Permitir registro de nuevos clientes (nombre, correo, contraseña, teléfono).
- RF-06.2: Permitir inicio y cierre de sesión.
- RF-06.3: Permitir recuperación de contraseña.
- RF-06.4: Mostrar al usuario registrado su historial de pedidos.
- RF-06.5 (opcional v1): Permitir compra como invitado (sin necesidad de registro).

#### RF-07 — Página "Nosotros"
Mostrar información institucional: historia de la empresa, años de experiencia, misión/visión (si aplica), y valores diferenciales (ej. atención personalizada, garantía, productos premium).

#### RF-08 — Página de contacto
- RF-08.1: Mostrar dirección física, horarios de atención y teléfonos.
- RF-08.2: Incluir mapa embebido (Google Maps) con la ubicación del local.
- RF-08.3: Incluir enlace directo a WhatsApp con mensaje predeterminado.
- RF-08.4: Incluir enlaces a redes sociales (Facebook, Instagram, u otras que aplique).
- RF-08.5: Incluir un formulario de contacto que envíe el mensaje al correo/panel del administrador.

#### RF-09 — Servicio técnico
- RF-09.1: Página dedicada donde el cliente pueda describir el problema del equipo y solicitar una visita o diagnóstico.
- RF-09.2: El formulario debe capturar: nombre, teléfono, marca/modelo del equipo, descripción del problema.
- RF-09.3: Las solicitudes deben quedar registradas en el panel administrativo para su gestión y seguimiento (ej. estados: recibida, en proceso, resuelta).

#### RF-10 — Panel administrativo
- RF-10.1: Acceso restringido mediante autenticación (usuario/contraseña) solo para roles autorizados.
- RF-10.2: CRUD (crear, leer, actualizar, eliminar) de productos: nombre, descripción, categoría, precio, imágenes, variantes, stock/disponibilidad.
- RF-10.3: CRUD de categorías de productos.
- RF-10.4: Gestión de pedidos: ver detalle, cambiar estado (pendiente, confirmado, en camino, entregado, cancelado).
- RF-10.5: Gestión de solicitudes de servicio técnico (ver RF-09.3).
- RF-10.6: Visualización de mensajes recibidos por el formulario de contacto.
- RF-10.7 (opcional v1): Panel de estadísticas básicas (productos más vendidos, pedidos por mes).

#### RF-11 — Carrito visible y navegación global
El sistema debe mostrar en todas las páginas: menú de navegación (Inicio, Productos, Nosotros, Contacto, Servicio Técnico), acceso a login/cuenta, ícono/contador de carrito, y pie de página con enlaces a categorías, servicios, datos de contacto y redes sociales.

### 3.2 Requisitos No Funcionales

| ID | Requisito | Descripción |
|---|---|---|
| RNF-01 | Usabilidad | El sitio debe ser intuitivo, con máximo 3 clics para llegar a cualquier producto desde la página de inicio. |
| RNF-02 | Responsividad | El diseño debe adaptarse correctamente a dispositivos móviles, tablets y escritorio. |
| RNF-03 | Rendimiento | Las páginas principales deben cargar en menos de 3 segundos con conexión estándar. |
| RNF-04 | Disponibilidad | El sitio debe estar disponible al menos el 99% del tiempo (uptime), sujeto al proveedor de hosting. |
| RNF-05 | Seguridad | Las contraseñas deben almacenarse cifradas (hash). Las comunicaciones deben usar HTTPS. Los datos de pago (si se integra pasarela) no deben almacenarse directamente en el servidor propio. |
| RNF-06 | Escalabilidad | El sistema debe soportar el crecimiento del catálogo (se observó un caso de referencia con 177+ productos) sin degradar el rendimiento. |
| RNF-07 | Mantenibilidad | El panel administrativo debe permitir actualizar productos y precios sin intervención de un desarrollador. |
| RNF-08 | Compatibilidad | El sitio debe funcionar correctamente en los navegadores más usados (Chrome, Safari, Firefox, Edge) en sus versiones recientes. |
| RNF-09 | SEO básico | Las páginas deben incluir metadatos (título, descripción) para facilitar el posicionamiento en buscadores. |
| RNF-10 | Localización | Moneda en pesos colombianos (COP), formato de fecha DD/MM/AAAA, idioma español. |
| RNF-11 | Copias de seguridad | La base de datos debe respaldarse periódicamente (mínimo diario) para evitar pérdida de información de pedidos e inventario. |

### 3.3 Requisitos de Interfaz

#### 3.3.1 Interfaces de usuario
- Header fijo con logo, menú de navegación, acceso a cuenta y carrito.
- Página de catálogo con filtro lateral o superior por categoría y campo de búsqueda.
- Tarjetas de producto (imagen, nombre, categoría, precio, botón de acción).
- Footer con información de productos, servicios, contacto y redes sociales, replicando el patrón observado en el sitio de referencia analizado.

#### 3.3.2 Interfaces de hardware
No aplica (sistema 100% web, sin requerimientos de hardware específico más allá de un dispositivo con navegador y conexión a internet).

#### 3.3.3 Interfaces de software
- Integración con Google Maps (embebido) para mostrar ubicación.
- Integración con WhatsApp (enlace `wa.me` con mensaje predefinido).
- Integración con pasarela de pagos (a definir en fase de diseño técnico).
- Integración con servicio de envío de correos (para confirmaciones de pedido y recuperación de contraseña).

#### 3.3.4 Interfaces de comunicación
- Protocolo HTTPS para todas las comunicaciones cliente-servidor.
- API REST (o equivalente) entre frontend y backend/panel administrativo.

---

## 4. Modelo de Datos Preliminar (Entidades Principales)

| Entidad | Atributos principales |
|---|---|
| **Producto** | id, nombre, descripción, categoría, precio, imágenes, variantes, stock/disponibilidad, estado (activo/agotado) |
| **Categoría** | id, nombre (ej. Fotocopiadoras, Impresoras, Tintas y Tóneres, Repuestos, Accesorios, Mantenimiento) |
| **Usuario** | id, nombre, correo, contraseña (hash), teléfono, rol (cliente/administrador) |
| **Pedido** | id, usuario, productos (detalle), cantidades, subtotal, total, estado, dirección de envío, fecha |
| **Solicitud de Servicio Técnico** | id, nombre del cliente, teléfono, equipo/modelo, descripción del problema, estado, fecha |
| **Mensaje de Contacto** | id, nombre, correo/teléfono, mensaje, fecha, estado (leído/no leído) |

---

## 5. Categorías de Producto Identificadas (referencia de mercado)

Basado en el análisis del sitio de referencia del sector, se recomienda que el catálogo de Fotocopiadoras SyP contemple, como mínimo, las siguientes categorías:
1. **Fotocopiadoras** (equipos multifuncionales nuevos/reacondicionados)
2. **Impresoras**
3. **Tintas y Tóneres** (cartuchos originales, compatibles, recargas)
4. **Repuestos** (cilindros, bandas de transferencia, cuchillas de limpieza, chips, fusoras, kits)
5. **Accesorios**
6. **Mantenimiento** (kits y servicios asociados)

Cada producto puede tener **variantes** (ej. compatibilidad con distintos modelos de equipo, presentación en gramos, calidad estándar/premium), tal como se identificó en el catálogo analizado.

---

## 6. Recomendaciones y Mejoras Futuras (fuera del alcance v1)

- Integración de facturación electrónica DIAN.
- Aplicación móvil nativa para clientes frecuentes.
- Sistema de suscripción/recompra automática de insumos (ej. recordatorio de recarga de tóner).
- Chat en vivo integrado además del enlace a WhatsApp.
- Programa de fidelización o descuentos para clientes recurrentes.
- Módulo de cotizaciones para clientes empresariales (compras al por mayor).
- Panel de reportes avanzados (ventas por categoría, rotación de inventario).

---

## 7. Aprobación

| Rol | Nombre | Firma/Visto bueno | Fecha |
|---|---|---|---|
| Cliente (propietaria del negocio) | | | |
| Desarrollador(a) responsable | | | |

---

*Documento generado a partir del análisis del sitio web público de Copy Caess S.A.S. (https://copycaess.com/) como referencia de mercado para definir funcionalidades típicas del sector de venta de fotocopiadoras e insumos de impresión en Colombia. La información de productos y precios de dicha empresa fue usada únicamente como caso de estudio de estructura funcional, no como contenido a copiar literalmente en el sitio final de Fotocopiadoras SyP.*
