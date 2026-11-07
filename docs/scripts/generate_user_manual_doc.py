import os
import sys
from PIL import Image, ImageDraw, ImageFont
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Docs")
os.makedirs(DOCS_DIR, exist_ok=True)
OUTPUT_DOCX = os.path.join(DOCS_DIR, "02_Manual_de_Usuario_SyP.docx")
DIAGRAM_PATH = os.path.join(DOCS_DIR, "user_manual_flowchart.png")

def generate_user_diagram():
    """Generates a User Experience & Navigation Flowchart using Pillow."""
    width, height = 1350, 880
    img = Image.new("RGB", (width, height), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 22)
        font_box_title = ImageFont.truetype("arialbd.ttf", 15)
        font_box_sub = ImageFont.truetype("arial.ttf", 12)
        font_item = ImageFont.truetype("arial.ttf", 11)
        font_badge = ImageFont.truetype("arialbd.ttf", 10)
    except Exception:
        font_title = font_box_title = font_box_sub = font_item = font_badge = ImageFont.load_default()

    # Header Banner
    draw.rectangle([0, 0, width, 65], fill="#0F4C81")
    draw.text((30, 20), "MAPA DE NAVEGACIÓN Y EXPERIENCIA DE USUARIO - FOTOCOPIADORAS SyP", fill="#FFFFFF", font=font_title)

    # 1. CLIENT PORTAL WORKFLOW (Left)
    draw.text((50, 95), "PARTE 1: FLUJOS DEL CLIENTE Y VISITANTE (TIENDA PWA)", fill="#0F4C81", font=font_box_title)

    client_steps = [
        ("1. Navegación & Búsqueda", "Exploración de index.html y productos.html con filtros facetados por modelo Ricoh."),
        ("2. Ficha Técnica & Carrito", "Consulta de ppm, conectividad, tóners compatibles y adición de ítems al carrito."),
        ("3. Cotización Formal en PDF", "Cálculo legal con IVA 19% en cotizacion.html y descarga de documento oficial."),
        ("4. Checkout & Transacción", "Selección de método de pago (PSE, Bancolombia, Nequi, Crédito a 30 días o WhatsApp)."),
        ("5. Agendamiento de Soporte", "Solicitud de mantenimiento preventivo o correctivo con fecha y franja horaria."),
        ("6. Reporte de Contadores", "Envío mensual de lecturas mecánicas de copias blanco y negro y color (Renting).")
    ]

    cy = 135
    for idx, (ctitle, cdesc) in enumerate(client_steps):
        draw.rounded_rectangle([50, cy, 620, cy + 65], radius=8, outline="#CBD5E1", width=2, fill="#FFFFFF")
        draw.rounded_rectangle([60, cy + 10, 90, cy + 40], radius=5, fill="#2563EB")
        draw.text((70, cy + 15), str(idx + 1), fill="#FFFFFF", font=font_box_title)
        draw.text((105, cy + 12), ctitle, fill="#1E40AF", font=font_box_title)
        draw.text((105, cy + 36), cdesc, fill="#475569", font=font_item)
        
        if idx < 5:
            draw.line([(335, cy + 65), (335, cy + 80)], fill="#2563EB", width=2)
            draw.polygon([(330, cy + 75), (340, cy + 75), (335, cy + 81)], fill="#2563EB")
        cy += 80

    # 2. ADMIN PORTAL WORKFLOW (Right)
    draw.text((710, 95), "PARTE 2: FLUJOS DE ADMINISTRACIÓN (PANEL ADMIN.HTML)", fill="#B91C1C", font=font_box_title)

    admin_steps = [
        ("1. Autenticación Restringida", "Acceso exclusivo con credenciales de administrador (Gladys Solano / Juan Portela)."),
        ("2. Dashboard & Analítica", "Monitoreo en tiempo real de ingresos en COP, pedidos y servicios activos."),
        ("3. Gestión de Catálogo Ricoh", "Creación, edición de precios, especificaciones técnicas y control de stock."),
        ("4. Control & Despacho", "Auditoría de pagos, aprobación de órdenes y actualización de guías de despacho."),
        ("5. Asignación de Soporte", "Revisión de órdenes técnicas, asignación de personal en campo y notas internas."),
        ("6. Auditoría Renting & Export", "Validación de lecturas de contadores mensuales y descarga de reportes en CSV.")
    ]

    ay = 135
    for idx, (atitle, adesc) in enumerate(admin_steps):
        draw.rounded_rectangle([710, ay, 1280, ay + 65], radius=8, outline="#CBD5E1", width=2, fill="#FFFFFF")
        draw.rounded_rectangle([720, ay + 10, 750, ay + 40], radius=5, fill="#DC2626")
        draw.text((730, ay + 15), str(idx + 1), fill="#FFFFFF", font=font_box_title)
        draw.text((765, ay + 12), atitle, fill="#991B1B", font=font_box_title)
        draw.text((765, ay + 36), adesc, fill="#475569", font=font_item)
        
        if idx < 5:
            draw.line([(995, ay + 65), (995, ay + 80)], fill="#DC2626", width=2)
            draw.polygon([(990, ay + 75), (1000, ay + 75), (995, ay + 81)], fill="#DC2626")
        ay += 80

    # Bottom Interaction Banner
    draw.rounded_rectangle([50, 645, 1280, 840], radius=10, outline="#0F4C81", width=2, fill="#FFFFFF")
    draw.rounded_rectangle([50, 645, 1280, 685], radius=10, outline="#0F4C81", width=1, fill="#0F4C81")
    draw.rectangle([50, 670, 1280, 685], fill="#0F4C81")
    draw.text((70, 655), "3. PUNTOS DE CONTACTO Y ASISTENCIA OMNICANAL AL USUARIO", fill="#FFFFFF", font=font_box_title)

    contact_pts = [
        ("WhatsApp Flotante", "Atención Inmediata", "Botón directo visible en todas las pantallas con mensaje preconfigurado."),
        ("Generador PDF Offline", "Descarga de Comprobantes", "Exportación autónoma en el navegador para cotizaciones y pedidos."),
        ("Notificaciones en Vivo", "Bandeja en Navbar", "Alertas contextuales automáticas sobre cambios de estado en pedidos y citas."),
        ("Centro de Ayuda / FAQ", "Autoservicio Guiado", "Solución a dudas frecuentes sobre garantías, despachos y pagos.")
    ]
    cx = 70
    for ctitle, csub, cdesc in contact_pts:
        draw.rounded_rectangle([cx, 705, cx + 280, 820], radius=8, outline="#E2E8F0", width=1, fill="#F8FAFC")
        draw.text((cx + 12, 715), ctitle, fill="#0F172A", font=font_box_title)
        draw.text((cx + 12, 735), csub, fill="#2563EB", font=font_badge)
        words = cdesc.split(" ")
        l1, l2 = "", ""
        for w in words:
            if len(l1 + " " + w) < 28: l1 += " " + w
            else: l2 += " " + w
        draw.text((cx + 12, 760), l1.strip(), fill="#475569", font=font_item)
        draw.text((cx + 12, 780), l2.strip(), fill="#475569", font=font_item)
        cx += 300

    img.save(DIAGRAM_PATH, "PNG", dpi=(300, 300))
    print(f"[OK] User Manual Diagram generated at: {DIAGRAM_PATH}")

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=90, bottom=90, left=120, right=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def add_header_footer(doc):
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("FOTOCOPIADORAS SyP | MANUAL DE USUARIO Y OPERACIONES")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    frun1 = fp.add_run("Confidencial - Entrega de Proyecto & Sustentación Técnica | Manual de Operación v2.0")
    frun1.font.name = "Calibri"
    frun1.font.size = Pt(8.5)
    frun1.font.color.rgb = RGBColor(100, 116, 139)

def format_row(row, bg_color=None, is_header=False):
    for cell in row.cells:
        set_cell_margins(cell, top=80, bottom=80, left=110, right=110)
        if bg_color:
            set_cell_background(cell, bg_color)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = "Calibri"
                if is_header:
                    run.font.size = Pt(8.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = RGBColor(30, 41, 59)

def build_user_manual_document():
    generate_user_diagram()
    doc = Document()
    
    section = doc.sections[0]
    section.top_margin = Inches(0.98)
    section.bottom_margin = Inches(0.98)
    section.left_margin = Inches(0.98)
    section.right_margin = Inches(0.98)
    
    add_header_footer(doc)
    
    NAVY = RGBColor(15, 76, 129)
    SLATE = RGBColor(43, 108, 176)
    CHARCOAL = RGBColor(30, 41, 59)
    MUTED = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # PORTADA FORMAL
    # -------------------------------------------------------------
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(40)
    p_pre.paragraph_format.space_after = Pt(10)
    r_pre = p_pre.add_run("MANUAL DE USUARIO Y GUÍA DE OPERACIÓN DEL SISTEMA")
    r_pre.font.name = "Calibri"
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = SLATE
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(15)
    r_title = p_title.add_run("MANUAL INTEGRAL DE USUARIO Y OPERACIONES\nPLATAFORMA E-COMMERCE Y SERVICIO TÉCNICO")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_brand = doc.add_paragraph()
    p_brand.paragraph_format.space_before = Pt(0)
    p_brand.paragraph_format.space_after = Pt(25)
    r_brand = p_brand.add_run('EMPRESA: "FOTOCOPIADORAS SyP" (NEIVA, HUILA)')
    r_brand.font.name = "Calibri"
    r_brand.font.size = Pt(14)
    r_brand.font.bold = True
    r_brand.font.color.rgb = CHARCOAL
    p_brand.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_norm = doc.add_paragraph()
    p_norm.paragraph_format.space_before = Pt(10)
    p_norm.paragraph_format.space_after = Pt(35)
    r_norm = p_norm.add_run("Parte 1: Guía de Navegación del Cliente y Tienda Virtual E-commerce\nParte 2: Manual de Administración y Operaciones del Negocio (Panel Admin)\nFormato Visual: Procedimientos Numerados, DoD y Marcadores [CAPTURA]")
    r_norm.font.name = "Calibri"
    r_norm.font.size = Pt(10.5)
    r_norm.font.italic = True
    r_norm.font.color.rgb = MUTED
    p_norm.alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_roles = doc.add_table(rows=4, cols=2)
    t_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    roles_data = [
        ("Destinatario Comercial (Cliente):", "Sra. Gladys Solano Murcia\nRepresentante Legal - Fotocopiadoras SyP"),
        ("Destinatario Académico / Evaluador:", "Instructor Técnico de Software\nEvaluación de Etapa Productiva / Formación"),
        ("Documentador Técnico & UX:", "Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\nIngeniería de Software & Soporte"),
        ("Versión y Ámbito del Documento:", "Versión 2.0 (Producción) | Clientes y Administradores")
    ]
    for idx, (lbl, val) in enumerate(roles_data):
        row = t_roles.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.8)
        cell_val.width = Inches(3.7)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "FFFFFF")
        set_cell_margins(cell_lbl, 80, 80, 100, 100)
        set_cell_margins(cell_val, 80, 80, 100, 100)
        
        p0 = cell_lbl.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.font.name = "Calibri"
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY
        
        p1 = cell_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = CHARCOAL
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # CONTROL DE VERSIONES
    # -------------------------------------------------------------
    h1 = doc.add_heading("Control de Versiones del Documento", level=1)
    h1.paragraph_format.space_before = Pt(15)
    h1.paragraph_format.space_after = Pt(10)
    
    t_vers = doc.add_table(rows=3, cols=5)
    t_vers.alignment = WD_TABLE_ALIGNMENT.CENTER
    vers_headers = ["Versión", "Fecha", "Autor", "Descripción del Cambio", "Estado"]
    for c_idx, h in enumerate(vers_headers):
        t_vers.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_vers.rows[0], bg_color="0F4C81", is_header=True)
    
    vers_rows = [
        ("1.0", "11/09/2026", "Equipo Desarrollo SyP", "Guía básica inicial de uso de la tienda para pruebas internas.", "Superado"),
        ("2.0", "04/11/2026", "Ingeniero de Software Senior", "Manual completo dividido en Parte 1 (Cliente) y Parte 2 (Administradora/Dueña), procedimientos numerados, marcadores de captura y sección FAQ/Troubleshooting.", "Aprobado")
    ]
    for r_idx, r_data in enumerate(vers_rows):
        row = t_vers.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx % 2 == 0 else "F8FAFC")

    # -------------------------------------------------------------
    # TABLA DE CONTENIDO
    # -------------------------------------------------------------
    h_toc = doc.add_heading("Contenido del Documento", level=1)
    h_toc.paragraph_format.space_before = Pt(20)
    h_toc.paragraph_format.space_after = Pt(10)
    
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.line_spacing = 1.2
    toc_items = [
        "1. INTRODUCCIÓN Y MAPA DE NAVEGACIÓN",
        "   1.1 Propósito y Audiencia del Manual",
        "   1.2 Diagrama de Flujo y Mapa de Experiencia de Usuario",
        "   1.3 Convenciones de Marcadores Visuales [CAPTURA]",
        "2. PARTE 1: GUÍA DEL CLIENTE Y TIENDA VIRTUAL",
        "   2.1 Registro de Cuenta e Inicio de Sesión de Clientes",
        "   2.2 Exploración del Catálogo, Filtros Facetados y Buscador",
        "   2.3 Ficha Técnica del Producto y Compatibilidad Ricoh",
        "   2.4 Gestión del Carrito de Compras",
        "   2.5 Módulo de Cotizaciones Formales en Línea y Descarga PDF",
        "   2.6 Proceso de Checkout y Formas de Pago Admitidas",
        "   2.7 Agendamiento de Solicitudes de Servicio Técnico",
        "   2.8 Reporte Mensual de Contadores de Fotocopiado (Renting)",
        "   2.9 Seguimiento de Pedidos y Bandeja de Notificaciones",
        "3. PARTE 2: MANUAL DE ADMINISTRACIÓN Y OPERACIONES DEL NEGOCIO",
        "   3.1 Acceso Seguro al Panel Administrativo (admin.html)",
        "   3.2 Tablero de Analítica Comercial y Métricas Financieras",
        "   3.3 Gestión de Productos, Precios e Inventario (CRUD)",
        "   3.4 Control de Pedidos, Aprobación de Pagos y Despacho",
        "   3.5 Asignación y Seguimiento de Servicios Técnicos",
        "   3.6 Auditoría de Contadores de Renting para Facturación",
        "   3.7 Emisión de Notificaciones y Avisos a Clientes",
        "   3.8 Exportación de Datos Comerciales a Formato CSV",
        "4. PREGUNTAS FRECUENTES (FAQ) Y SOLUCIÓN DE PROBLEMAS COMUNES",
        "   4.1 FAQ para Clientes y Usuarios del E-commerce",
        "   4.2 FAQ para la Administradora / Personal del Negocio",
        "5. CONTROL DE APROBACIÓN Y FIRMAS DE CONFORMIDAD"
    ]
    for item in toc_items:
        r = toc_p.add_run(item + "\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. INTRODUCCIÓN Y MAPA DE NAVEGACIÓN
    # -------------------------------------------------------------
    doc.add_heading("1. Introducción y Mapa de Navegación", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("1.1 Propósito y Audiencia del Manual\n")
    r.bold = True
    p.add_run(
        "El presente manual constituye la guía operativa oficial de la plataforma web de 'Fotocopiadoras SyP'. "
        "Ha sido redactado con un enfoque dual para servir tanto a los clientes corporativos y particulares "
        "(Parte 1: Experiencia de Compra y Servicios), como al equipo operativo liderado por la propietaria "
        "y representante legal, Sra. Gladys Solano Murcia, y el personal técnico liderado por Juan Sebastián Portela "
        "(Parte 2: Panel Administrativo y Gestión del Negocio).\n\n"
        "Su estructura paso a paso garantiza que cualquier usuario, sin importar su nivel de conocimientos tecnológicos, "
        "pueda operar la plataforma eficientemente."
    )

    p = doc.add_paragraph()
    r = p.add_run("1.2 Diagrama de Flujo y Mapa de Experiencia de Usuario\n")
    r.bold = True
    p.add_run(
        "A continuación se ilustra el mapa de navegación integral, modelando los caminos de interacción de los clientes "
        "y los procesos administrativos concurrentes:"
    )

    if os.path.exists(DIAGRAM_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(DIAGRAM_PATH, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Mapa de Navegación y Flujos Operativos - Fotocopiadoras SyP.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED

    p = doc.add_paragraph()
    r = p.add_run("1.3 Convenciones de Marcadores Visuales [CAPTURA]\n")
    r.bold = True
    p.add_run(
        "A lo largo del documento se incluyen marcadores tipográficos estandarizados con el formato '[CAPTURA: descripción detallada]' "
        "que señalan la pantalla exacta, modal o formulario que el usuario observará al ejecutar cada procedimiento."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. PARTE 1: GUÍA DEL CLIENTE Y TIENDA VIRTUAL
    # -------------------------------------------------------------
    doc.add_heading("2. Parte 1: Guía del Cliente y Tienda Virtual", level=1)

    def render_manual_section(sec_id, sec_title, obj, steps, expected, screenshot_desc):
        h2 = doc.add_heading(f"2.{sec_id} {sec_title}", level=2)
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Objetivo del Procedimiento: ")
        r.bold = True
        r.font.color.rgb = NAVY
        p.add_run(obj)

        p = doc.add_paragraph()
        r = p.add_run("Pasos Numerados de Ejecución:\n")
        r.bold = True
        r.font.color.rgb = CHARCOAL
        for s_idx, st in enumerate(steps):
            p.add_run(f"{s_idx + 1}. {st}\n")

        p = doc.add_paragraph()
        r = p.add_run("Resultado Esperado: ")
        r.bold = True
        r.font.color.rgb = RGBColor(5, 150, 105)
        p.add_run(expected)

        # Screenshot callout box
        p_box = doc.add_paragraph()
        p_box.paragraph_format.space_before = Pt(4)
        p_box.paragraph_format.space_after = Pt(8)
        t_shot = doc.add_table(rows=1, cols=1)
        t_shot.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t_shot.rows[0].cells[0]
        cell.width = Inches(6.4)
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, 70, 70, 100, 100)
        p_sh = cell.paragraphs[0]
        r_sh = p_sh.add_run(f"📷 [CAPTURA: {screenshot_desc}]")
        r_sh.bold = True
        r_sh.font.size = Pt(9)
        r_sh.font.color.rgb = RGBColor(30, 64, 175)

    # 2.1 Registro e Inicio de Sesión
    render_manual_section(
        1, "Registro de Cuenta e Inicio de Sesión de Clientes",
        "Permitir al cliente crear su cuenta corporativa o personal para realizar compras, consultar órdenes y reportar contadores.",
        [
            "En la cabecera superior de cualquier pantalla, hacer clic en el botón 'Iniciar Sesión' o en el icono de usuario.",
            "Para registrarse por primera vez, hacer clic en la pestaña 'Crear Cuenta'.",
            "Diligenciar los campos requeridos: Nombre Completo o Razón Social, Correo Electrónico, Teléfono Celular y Contraseña segura (mínimo 6 caracteres).",
            "Presionar el botón azul 'Registrarse'.",
            "Si ya dispone de cuenta, ingresar correo y contraseña en la pestaña 'Iniciar Sesión' y hacer clic en 'Entrar'."
        ],
        "El sistema valida los datos, emite un token seguro de sesión y muestra el nombre del usuario en el menú superior.",
        "Vista login.html mostrando el formulario dual con pestañas 'Iniciar Sesión' y 'Registrarse', con campos de entrada limpios."
    )

    # 2.2 Exploración del Catálogo y Filtros
    render_manual_section(
        2, "Exploración del Catálogo, Filtros Facetados y Buscador",
        "Localizar fotocopiadoras multifuncionales, repuestos o tintas Ricoh de forma rápida mediante filtros avanzados.",
        [
            "Ingresar a la sección 'Productos' desde el menú principal de navegación.",
            "Para filtrar por categoría, hacer clic en los botones de filtro rápido: 'Fotocopiadoras', 'Impresoras', 'Tintas y Tóneres', 'Repuestos' o 'Mantenimiento'.",
            "Para buscar un modelo específico (ej. 'Ricoh MP 4002' o '301'), escribir el texto en la barra de búsqueda en tiempo real.",
            "Utilizar el selector de ordenamiento para ordenar por precio (Menor a Mayor o Mayor a Menor) o relevancia."
        ],
        "El catálogo actualiza dinámicamente las tarjetas de producto en pantalla en menos de medio segundo sin recargar la página.",
        "Pantalla productos.html mostrando la barra de búsqueda superior, píldoras de categorías y cuadrícula de tarjetas de productos Ricoh."
    )

    # 2.3 Ficha Técnica del Producto
    render_manual_section(
        3, "Ficha Técnica del Producto y Compatibilidad Ricoh",
        "Consultar los datos técnicos de un equipo o verificar compatibilidad de un repuesto antes de comprar.",
        [
            "En cualquier tarjeta de producto, hacer clic en el botón 'Ver Detalles' o 'Ficha Técnica'.",
            "Examinar la ventana modal emergente con los detalles:",
            "  - Velocidad de impresión (ppm) y ciclo de trabajo mensual.",
            "  - Funciones disponibles (Copia, Impresión, Escáner dúplex, Red).",
            "  - Códigos de tóners o repuestos compatibles certificados Ricoh.",
            "  - Disponibilidad de inventario ('En Stock' o 'Pocas Unidades').",
            "Hacer clic en 'Agregar al Carrito' directamente desde la ficha o cerrar la ventana."
        ],
        "Apertura fluida de la ventana modal con la galería de fotos del equipo y especificaciones técnicas completas.",
        "Modal emergente de Ficha Técnica detallada mostrando la Ricoh MP 5054 con insignias de garantía y especificaciones."
    )

    # 2.4 Carrito de Compras
    render_manual_section(
        4, "Gestión del Carrito de Compras",
        "Controlar la lista de productos seleccionados, modificar unidades y verificar subtotales en tiempo real.",
        [
            "Hacer clic en el icono del Carrito de Compras ubicado en la esquina superior derecha del menú.",
            "Revisar el panel lateral deslizable (Drawer) con la lista de artículos.",
            "Para aumentar o disminuir unidades, presionar los botones '+' o '-'.",
            "Para quitar un artículo, presionar el icono de papelera correspondiente.",
            "Verificar el subtotal acumulado antes de impuestos."
        ],
        "El carrito recalcula instantáneamente los montos y persiste la información aunque se cierre el navegador.",
        "Panel lateral deslizable (Cart Drawer) abierto con artículos Ricoh, contador numérico y botón 'Proceder a Cotizar/Comprar'."
    )

    doc.add_page_break()

    # 2.5 Generación de Cotizaciones en PDF
    render_manual_section(
        5, "Módulo de Cotizaciones Formales en Línea y Descarga PDF",
        "Generar una cotización formal oficial con cálculo automático del IVA del 19% para aprobación presupuestal de empresas.",
        [
            "Desde el carrito de compras o menú principal, seleccionar 'Cotización'.",
            "Revisar la tabla de productos seleccionados, precios unitarios y subtotales.",
            "Diligenciar los datos del destinatario: Empresa o Nombre, Correo Electrónico y Teléfono de Contacto.",
            "Verificar la liquidación tributaria legal:",
            "  - Subtotal (Monto bruto).",
            "  - IVA 19% (Liquidado automáticamente conforme a la ley colombiana).",
            "  - Total Liquidado en Pesos Colombianos (COP).",
            "Hacer clic en el botón azul 'Guardar y Descargar Cotización en PDF'."
        ],
        "El sistema genera un código oficial 'COT-XXXXXX', guarda el registro en la base de datos y abre el diálogo de impresión/PDF.",
        "Vista cotizacion.html con la cotización formal membretada de Fotocopiadoras SyP, desglose del 19% de IVA y código único."
    )

    # 2.6 Checkout y Formas de Pago
    render_manual_section(
        6, "Proceso de Checkout y Formas de Pago Admitidas",
        "Formalizar la orden de compra suministrando datos de entrega y seleccionando la pasarela de pago preferida.",
        [
            "En la pantalla de cotización o carrito, presionar 'Confirmar Pedido / Checkout'.",
            "Ingresar los datos de facturación y despacho:",
            "  - Nombre o Razón Social completa.",
            "  - Cédula de Ciudadanía o NIT con dígito de verificación.",
            "  - Dirección exacta de entrega e instalación (ej. 'Calle 10 # 5-20').",
            "  - Ciudad de destino (predeterminado: 'Neiva, Huila').",
            "Seleccionar el método de pago:",
            "  - PSE (Pago seguro en línea para todos los bancos).",
            "  - Tarjeta de Crédito / Débito (Visa / Mastercard).",
            "  - Transferencia Bancaria Directa (Bancolombia / Nequi).",
            "  - Crédito Empresarial a 30 Días (exclusivo clientes corporativos con convenio).",
            "  - WhatsApp Directo (asistido por asesor comercial).",
            "Hacer clic en 'Finalizar Pedido'."
        ],
        "El sistema genera la orden con código 'PED-XXXXXX', confirma el pedido en pantalla y envía una notificación automática.",
        "Formulario modal de Checkout con selección de métodos de pago bancarios y campos de dirección en Neiva."
    )

    # 2.7 Agendamiento de Servicio Técnico
    render_manual_section(
        7, "Agendamiento de Solicitudes de Servicio Técnico",
        "Solicitar la visita técnica especializada de un experto Ricoh para mantenimiento preventivo o reparación correctiva.",
        [
            "Hacer clic en la opción 'Servicio Técnico' del menú principal.",
            "Diligenciar el formulario oficial de soporte:",
            "  - Modelo del equipo (ej. 'Ricoh MP 4002' o serie).",
            "  - Tipo de servicio requerido ('Mantenimiento Preventivo' o 'Mantenimiento Correctivo').",
            "  - Fecha deseada de la visita técnica (mínimo 24 horas de antelación).",
            "  - Franja horaria preferida (Mañana: 8:00 AM - 12:00 PM o Tarde: 2:00 PM - 6:00 PM).",
            "  - Descripción del síntoma o código de error en pantalla (ej. 'Código SC 542' o 'Atasco de papel frecuente').",
            "Presionar 'Solicitar Visita Técnica'."
        ],
        "Se genera un radicado técnico 'req_XXXX' con estado inicial 'Pendiente', visible de inmediato por la administración.",
        "Sección de agendamiento en servicio-tecnico.html con calendario interactivo y selector de fallas comunes Ricoh."
    )

    # 2.8 Reporte Mensual de Contadores de Renting
    render_manual_section(
        8, "Reporte Mensual de Contadores de Fotocopiado (Renting)",
        "Permitir a los clientes bajo contrato de alquiler reportar el conteo mensual de copias para liquidación de excesos.",
        [
            "Ingresar a 'Servicio Técnico' y seleccionar la pestaña 'Reporte de Contadores (Renting)'.",
            "Asegurarse de haber iniciado sesión con la cuenta de la empresa titular.",
            "Seleccionar el modelo del equipo alquilado asignado a su sede.",
            "Ingresar la lectura del contador mecánico monocromático (Blanco y Negro).",
            "Si el equipo es a color, ingresar la lectura del contador de color (o dejar en 0 si es monocromático).",
            "Seleccionar el mes correspondiente al informe (ej. 'Octubre 2026').",
            "Hacer clic en 'Enviar Reporte de Contadores'."
        ],
        "La lectura queda registrada en la base de datos 'counter_reports' vinculada al cliente, desplegando alerta verde de éxito.",
        "Formulario de lectura de contadores mecánicos Ricoh con campos de conteo monocromático y a color."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. PARTE 2: MANUAL DE ADMINISTRACIÓN Y OPERACIONES DEL NEGOCIO
    # -------------------------------------------------------------
    doc.add_heading("3. Parte 2: Manual de Administración y Operaciones del Negocio", level=1)

    p = doc.add_paragraph()
    p.add_run(
        "Esta sección está destinada exclusivamente a la Sra. Gladys Solano Murcia (Propietaria y Administradora General) "
        "y al personal de soporte técnico autorizado. El acceso se realiza a través de la interfaz protegida 'admin.html'."
    )

    def render_admin_section(sec_id, sec_title, obj, steps, expected, screenshot_desc):
        h2 = doc.add_heading(f"3.{sec_id} {sec_title}", level=2)
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Objetivo Operativo: ")
        r.bold = True
        r.font.color.rgb = RGBColor(185, 28, 28)
        p.add_run(obj)

        p = doc.add_paragraph()
        r = p.add_run("Procedimiento de Administración:\n")
        r.bold = True
        r.font.color.rgb = CHARCOAL
        for s_idx, st in enumerate(steps):
            p.add_run(f"{s_idx + 1}. {st}\n")

        p = doc.add_paragraph()
        r = p.add_run("Impacto y Resultado: ")
        r.bold = True
        r.font.color.rgb = RGBColor(5, 150, 105)
        p.add_run(expected)

        p_box = doc.add_paragraph()
        p_box.paragraph_format.space_before = Pt(4)
        p_box.paragraph_format.space_after = Pt(8)
        t_shot = doc.add_table(rows=1, cols=1)
        t_shot.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t_shot.rows[0].cells[0]
        cell.width = Inches(6.4)
        set_cell_background(cell, "FEF2F2")
        set_cell_margins(cell, 70, 70, 100, 100)
        p_sh = cell.paragraphs[0]
        r_sh = p_sh.add_run(f"🔒 [CAPTURA: {screenshot_desc}]")
        r_sh.bold = True
        r_sh.font.size = Pt(9)
        r_sh.font.color.rgb = RGBColor(185, 28, 28)

    # 3.1 Acceso Seguro al Panel Admin
    render_admin_section(
        1, "Acceso Seguro al Panel Administrativo (admin.html)",
        "Ingresar a la consola de control maestro verificando privilegios criptográficos de administrador.",
        [
            "Navegar a la URL protegida: 'http://localhost:5500/admin.html' (o dominio de producción).",
            "Si la sesión no está activa, el sistema presentará el formulario de autenticación administrativa.",
            "Ingresar el correo de administrador oficial ('admin@sypfotocopiadoras.com' o 'gladys.solano@sypfotocopiadoras.com').",
            "Digitar la contraseña maestra y presionar 'Entrar al Panel'."
        ],
        "El backend valida el rol 'admin' mediante JWT. Se habilita la consola con el menú lateral de gestión.",
        "Pantalla de autenticación y bienvenida al panel administrativo con indicadores de seguridad activa."
    )

    # 3.2 Tablero de Analítica Comercial
    render_admin_section(
        2, "Tablero de Analítica Comercial y Métricas Financieras",
        "Supervisar el volumen de ventas en Pesos Colombianos, estado de órdenes y modelos Ricoh más demandados.",
        [
            "En el menú lateral del panel, hacer clic en la pestaña 'Dashboard / Analítica'.",
            "Examinar las tarjetas de resumen ejecutivo:",
            "  - Ingresos Totales en COP recaudados por ventas de equipos y suministros.",
            "  - Cantidad total de órdenes registradas y distribución por método de pago.",
            "  - Estado logístico de pedidos (Pendientes, En camino, Entregados).",
            "  - Solicitudes de servicio técnico activas y modelos Ricoh más atendidos.",
            "  - Total de páginas impresas acumuladas reportadas por clientes de renting."
        ],
        "Carga en vivo de métricas consolidadas consumiendo el endpoint seguro 'GET /api/v1/admin/analytics'.",
        "Dashboard principal de admin.html con gráficos de barras, tarjetas de ingresos en COP y estado de pedidos."
    )

    # 3.3 Gestión de Productos e Inventario
    render_admin_section(
        3, "Gestión Integral de Productos, Precios e Inventario (CRUD)",
        "Crear nuevos productos, actualizar precios de venta, modificar stock o cambiar insignias destacadas.",
        [
            "Acceder a la pestaña 'Inventario y Productos'.",
            "Para crear un nuevo ítem, hacer clic en '+ Nuevo Producto':",
            "  - Asignar código SKU (ej. 'ricoh-im-c3000').",
            "  - Ingresar nombre comercial, categoría, marca ('Ricoh') y precio antes de IVA.",
            "  - Seleccionar estado de stock: 'ok' (Disponible), 'low' (Pocas unidades) o 'out' (Agotado).",
            "  - Diligenciar especificaciones técnicas (velocidad ppm, ciclo mensual) y ruta de imagen.",
            "  - Presionar 'Guardar Producto'.",
            "Para modificar precios o stock de un producto existente, presionar el botón 'Editar' en la tabla, actualizar valores y guardar."
        ],
        "El producto se actualiza inmediatamente en la base de datos 'products' y se refleja en el e-commerce.",
        "Tabla de gestión de inventario en admin.html con listado de equipos Ricoh, botones de edición y estado de stock."
    )

    # 3.4 Control de Pedidos y Despacho
    render_admin_section(
        4, "Control de Pedidos, Aprobación de Pagos y Despacho",
        "Verificar comprobantes bancarios, autorizar pedidos y actualizar el estado logístico de entrega.",
        [
            "Ingresar a la pestaña 'Pedidos y Ventas'.",
            "Localizar el pedido por su código (ej. 'PED-2026-XXXX') o nombre del cliente.",
            "Hacer clic en 'Ver Detalle' para inspeccionar los artículos comprados, dirección de entrega y método de pago.",
            "Si el pago es por transferencia bancaria o crédito a 30 días, verificar el soporte y cambiar el estado de pago a 'Aprobado'.",
            "Actualizar el estado de envío según el avance del despacho: 'En preparación', 'Despachado' o 'Entregado'.",
            "Presionar 'Actualizar Estado'."
        ],
        "El sistema ejecuta 'PATCH /api/v1/orders/{id}/status' y dispara una notificación en la bandeja del cliente.",
        "Bandeja de pedidos con selector desplegable de estados de pago y despacho, y visualizador de ítems de compra."
    )

    # 3.5 Asignación de Soporte Técnico
    render_admin_section(
        5, "Asignación y Seguimiento de Servicios Técnicos",
        "Gestionar las solicitudes de mantenimiento, asignar técnicos responsables y registrar bitácoras de servicio.",
        [
            "Ingresar a la pestaña 'Servicio Técnico / Soporte'.",
            "Examinar la lista de solicitudes con estado 'Pendiente'.",
            "Abrir la orden de trabajo para revisar el modelo del equipo y la falla reportada por el cliente.",
            "Asignar la visita al técnico responsable (ej. Juan Sebastián Portela) e ingresar notas en 'Bitácora Interna'.",
            "Cambiar el estado a 'Confirmada' y notificar la fecha final acordada con el cliente.",
            "Una vez realizada la visita en sitio, marcar la orden como 'Completada'."
        ],
        "Trazabilidad completa de la intervención técnica guardada en SQLite con fecha y hora de actualización.",
        "Módulo de gestión técnica con tabla de solicitudes, botón de asignación y campo de notas para el técnico."
    )

    # 3.6 Auditoría de Contadores de Renting
    render_admin_section(
        6, "Auditoría de Contadores de Renting para Facturación",
        "Revisar las lecturas reportadas por empresas para generar el cobro mensual de páginas impresas.",
        [
            "Ingresar a la pestaña 'Contadores de Renting'.",
            "Filtrar por el mes en curso (ej. '2026-10').",
            "Verificar las lecturas reportadas por cada cliente para los contadores monocromático y color.",
            "Comparar la lectura actual contra el histórico del mes previo para liquidar el excedente de copias.",
            "Utilizar estos datos para la emisión de la factura de cobro mensual del contrato de renting."
        ],
        "Consolidado claro de consumos por cliente y equipo disponible para auditoría contable.",
        "Tabla de reportes de contadores en admin.html mostrando cliente, modelo Ricoh, lectura mono, color y mes."
    )

    # 3.7 Exportación de Datos a CSV
    render_admin_section(
        7, "Exportación de Datos Comerciales a Formato CSV",
        "Descargar copias tabulares de órdenes, inventario y solicitudes para análisis contable en Excel.",
        [
            "En la parte superior del panel administrativo, ubicar el bloque 'Exportar Datos'.",
            "Hacer clic en el botón correspondiente según el reporte requerido:",
            "  - 'Exportar Pedidos a CSV': Descarga la relación completa de ventas, totales y clientes.",
            "  - 'Exportar Productos a CSV': Descarga el catálogo maestro con precios y stock.",
            "  - 'Exportar Servicios a CSV': Descarga el historial de órdenes de mantenimiento.",
            "Abrir el archivo '.csv' descargado en Microsoft Excel para cruce de cuentas o informes a gerencia."
        ],
        "Descarga inmediata del archivo con codificación UTF-8 y cabeceras delimitadas por comas.",
        "Botones de exportación en admin.html y diálogo de descarga del archivo orders.csv en el navegador."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. PREGUNTAS FRECUENTES (FAQ) Y SOLUCIÓN DE PROBLEMAS
    # -------------------------------------------------------------
    doc.add_heading("4. Preguntas Frecuentes (FAQ) y Solución de Problemas", level=1)

    p = doc.add_paragraph()
    r = p.add_run("4.1 Preguntas Frecuentes para Clientes y Usuarios del E-commerce\n")
    r.bold = True
    
    faq_client = [
        ("¿Cómo sé si un tóner o repuesto es compatible con mi fotocopiadora?",
         "Al abrir la ficha técnica del tóner o repuesto, revise la sección 'Modelos Compatibles'. Si el modelo de su equipo Ricoh (ej. MP 301, MP 4002) aparece en la lista, el producto está garantizado al 100%."),
        ("¿La cotización que descargo incluye el IVA?",
         "Sí. Todas las cotizaciones generadas en la plataforma desglosan automáticamente el subtotal neto y el Impuesto al Valor Agregado (IVA) del 19%, cumpliendo con los estándares de la legislación tributaria colombiana."),
        ("¿Cuánto tiempo de vigencia tiene una cotización?",
         "Las cotizaciones emitidas formalmente por Fotocopiadoras SyP tienen una validez comercial de quince (15) días calendario a partir de la fecha de generación."),
        ("¿Qué hago si no tengo cuenta y deseo comprar?",
         "Puede navegar por el catálogo, añadir productos al carrito y cotizar sin cuenta. Sin embargo, para agendar servicio técnico o guardar su historial de compras, le recomendamos registrarse en menos de un minuto."),
        ("¿Qué garantía tienen los equipos vendidos?",
         "Los equipos multifuncionales Ricoh nuevos cuentan con 12 meses de garantía directa. Los equipos reacondicionados certificados cuentan con 6 meses de garantía o un límite de 50.000 copias.")
    ]
    for q, a in faq_client:
        pq = doc.add_paragraph()
        rq = pq.add_run(f"P: {q}")
        rq.bold = True
        rq.font.color.rgb = NAVY
        pa = doc.add_paragraph()
        pa.add_run(f"R: {a}")
        pa.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("4.2 Preguntas Frecuentes para la Administradora / Personal del Negocio\n")
    r.bold = True

    faq_admin = [
        ("¿Cómo apruebo un pedido que fue pagado por transferencia Bancolombia o Nequi?",
         "Ingrese a la pestaña 'Pedidos y Ventas', ubique la orden, verifique el comprobante de pago enviado por el cliente a WhatsApp o correo, y en el selector de 'Estado de Pago' elija 'Aprobado' y guarde."),
        ("¿Qué debo hacer si un producto se agota en bodega?",
         "Ingrese a 'Inventario y Productos', busque el artículo, haga clic en 'Editar' y cambie el estado de stock a 'Agotado' ('out'). El producto seguirá visible en el catálogo pero los clientes no podrán comprarlo hasta que renueve existencias."),
        ("¿Cómo sé cuándo debo revisar los contadores de renting?",
         "Los clientes reportan sus contadores entre los días 25 y 30 de cada mes. En la última semana del mes, ingrese a la pestaña 'Contadores de Renting' y descargue el consolidado para liquidar la facturación de excesos."),
        ("¿Por qué el panel administrativo me pide iniciar sesión nuevamente?",
         "Por motivos de seguridad informática (estándar bancario JWT), las sesiones administrativas expiran automáticamente tras 60 minutos de inactividad para evitar accesos no autorizados si deja el equipo desatendido.")
    ]
    for q, a in faq_admin:
        pq = doc.add_paragraph()
        rq = pq.add_run(f"P: {q}")
        rq.bold = True
        rq.font.color.rgb = RGBColor(185, 28, 28)
        pa = doc.add_paragraph()
        pa.add_run(f"R: {a}")
        pa.paragraph_format.space_after = Pt(6)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. CONTROL DE APROBACIÓN Y FIRMAS
    # -------------------------------------------------------------
    doc.add_heading("5. Control de Aprobación y Firmas de Conformidad", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Las firmas a continuación certifican que el presente Manual de Usuario y Operaciones describe con fidelidad "
        "los procedimientos del sistema, ha sido revisado por la administración de Fotocopiadoras SyP y cumple con los "
        "estándares de entrega y sustentación requeridos:"
    )

    t_sig = doc.add_table(rows=3, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig_headers = ["Cliente / Representante Legal", "Documentador Técnico & UX", "Instructor / Evaluador Técnico"]
    for c_idx, h in enumerate(t_sig_headers):
        t_sig.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_sig.rows[0], bg_color="0F4C81", is_header=True)

    sig_content = [
        ("Sra. Gladys Solano Murcia\nRepresentante Legal\nFotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Kevin Portela [POR CONFIRMAR]\nLíder de Documentación & Desarrollo\nProyecto Fotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Instructor Evaluador [POR CONFIRMAR]\nEvaluador Etapa Productiva / Académica\nCentro de Formación Técnica\n\nFirma: _________________________\nFecha: _____ / _____ / 2026"),
        ("Aprobación de Manual de Operación", "Certificación Técnica de Usabilidad", "Aprobación y Validación Técnica")
    ]
    for r_idx, r_data in enumerate(sig_content):
        row = t_sig.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx == 0 else "F8FAFC")

    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] User Manual generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_user_manual_document()
