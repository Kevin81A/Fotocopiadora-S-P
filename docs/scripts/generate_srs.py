import os
import sys
from PIL import Image, ImageDraw, ImageFont
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Docs")
os.makedirs(DOCS_DIR, exist_ok=True)
OUTPUT_DOCX = os.path.join(DOCS_DIR, "01_SRS_Fotocopiadoras_SyP.docx")
DIAGRAM_PATH = os.path.join(DOCS_DIR, "srs_use_case_diagram.png")

def generate_diagram():
    """Generates a high-resolution Use Case & Architecture Diagram using Pillow."""
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Try default fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_box = ImageFont.truetype("arialbd.ttf", 15)
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_actor = ImageFont.truetype("arialbd.ttf", 14)
    except Exception:
        font_title = font_box = font_sub = font_actor = ImageFont.load_default()

    # Draw header banner
    draw.rectangle([0, 0, width, 65], fill="#0F4C81")
    draw.text((30, 20), "PLATAFORMA FOTOCOPIADORAS SyP - DIAGRAMA GENERAL DE CASOS DE USO (IEEE 830)", fill="#FFFFFF", font=font_title)

    # Boundary Box: Sistema SyP Web & FastAPI
    draw.rounded_rectangle([250, 90, 950, 710], radius=15, outline="#0F4C81", width=3, fill="#FFFFFF")
    draw.text((270, 105), "LÍMITE DEL SISTEMA: Plataforma E-commerce & Servicio Técnico SyP", fill="#0F4C81", font=font_box)

    # Actor 1: Visitante (Left Top)
    draw.rounded_rectangle([20, 130, 200, 200], radius=10, outline="#64748B", width=2, fill="#E2E8F0")
    draw.text((45, 145), "ACTOR: Visitante", fill="#1E293B", font=font_actor)
    draw.text((35, 168), "(Usuario no autenticado)", fill="#475569", font=font_sub)

    # Actor 2: Cliente Registrado (Left Bottom)
    draw.rounded_rectangle([20, 360, 200, 440], radius=10, outline="#2563EB", width=2, fill="#DBEAFE")
    draw.text((35, 375), "ACTOR: Cliente SyP", fill="#1E40AF", font=font_actor)
    draw.text((35, 398), "(Registrado con JWT)", fill="#3B82F6", font=font_sub)

    # Actor 3: Dueña / Admin (Right Top)
    draw.rounded_rectangle([990, 160, 1180, 240], radius=10, outline="#DC2626", width=2, fill="#FEE2E2")
    draw.text((1005, 175), "ACTOR: Administrador", fill="#991B1B", font=font_actor)
    draw.text((1015, 198), "(Gladys Solano Murcia)", fill="#B91C1C", font=font_sub)

    # Actor 4: Técnico de Soporte (Right Bottom)
    draw.rounded_rectangle([990, 430, 1180, 510], radius=10, outline="#D97706", width=2, fill="#FEF3C7")
    draw.text((1005, 445), "ACTOR: Técnico Ricoh", fill="#92400E", font=font_actor)
    draw.text((1015, 468), "(Juan Sebastián Portela)", fill="#B45309", font=font_sub)

    # Use cases inside system boundary
    use_cases = [
        # (x, y, text1, text2, color, fill_color, border_color)
        (280, 150, "CU-01: Explorar Catálogo Ricoh", "Filtros facetados, búsqueda y specs", "#1E293B", "#F1F5F9", "#94A3B8"),
        (610, 150, "CU-02: Generar Cotización", "Cálculo de IVA y exportación PDF", "#1E293B", "#F1F5F9", "#94A3B8"),
        (280, 250, "CU-03: Realizar Checkout y Pedido", "PSE, Bancolombia, Nequi, Crédito", "#1E293B", "#EFF6FF", "#60A5FA"),
        (610, 250, "CU-04: Gestión de Cuenta y JWT", "Registro, Login, Sesión segura", "#1E293B", "#EFF6FF", "#60A5FA"),
        (280, 360, "CU-05: Solicitar Servicio Técnico", "Mantenimiento preventivo/correctivo", "#1E293B", "#EFF6FF", "#60A5FA"),
        (610, 360, "CU-06: Reportar Contadores (Renting)", "Lectura mensual de copias mono/color", "#1E293B", "#EFF6FF", "#60A5FA"),
        (280, 480, "CU-07: Gestión CRUD Productos", "Precios, stock, categorías e imágenes", "#7F1D1D", "#FEF2F2", "#F87171"),
        (610, 480, "CU-08: Control de Pedidos y Despacho", "Aprobación de pagos y seguimiento", "#7F1D1D", "#FEF2F2", "#F87171"),
        (280, 590, "CU-09: Dashboard & Analítica SyP", "Ingresos COP, métricas y exportación CSV", "#7F1D1D", "#FEF2F2", "#F87171"),
        (610, 590, "CU-10: Asignación Técnica de Visitas", "Actualización de estado y notas", "#78350F", "#FFFBEB", "#FBBF24"),
    ]

    for (ux, uy, utxt1, utxt2, txtcol, bgcol, bdrcol) in use_cases:
        draw.rounded_rectangle([ux, uy, ux + 290, uy + 70], radius=8, outline=bdrcol, width=2, fill=bgcol)
        draw.text((ux + 15, uy + 14), utxt1, fill=txtcol, font=font_box)
        draw.text((ux + 15, uy + 38), utxt2, fill="#64748B", font=font_sub)

    # Draw connection lines (arrows / relations)
    # Visitante -> CU-01, CU-02
    draw.line([(200, 165), (280, 180)], fill="#64748B", width=2)
    draw.line([(200, 165), (610, 180)], fill="#64748B", width=1)
    
    # Cliente -> CU-03, CU-04, CU-05, CU-06
    draw.line([(200, 390), (280, 285)], fill="#2563EB", width=2)
    draw.line([(200, 400), (610, 285)], fill="#2563EB", width=2)
    draw.line([(200, 410), (280, 395)], fill="#2563EB", width=2)
    draw.line([(200, 420), (610, 395)], fill="#2563EB", width=2)

    # Admin -> CU-07, CU-08, CU-09
    draw.line([(990, 200), (570, 515)], fill="#DC2626", width=2)
    draw.line([(990, 210), (900, 515)], fill="#DC2626", width=2)
    draw.line([(990, 220), (570, 625)], fill="#DC2626", width=2)

    # Tecnico -> CU-06, CU-10
    draw.line([(990, 470), (900, 395)], fill="#D97706", width=1)
    draw.line([(990, 480), (900, 625)], fill="#D97706", width=2)

    img.save(DIAGRAM_PATH, "PNG", dpi=(300, 300))
    print(f"[OK] Diagram generated at: {DIAGRAM_PATH}")

def set_cell_background(cell, hex_color):
    """Sets background shading of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding."""
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
    """Configures professional header and footer."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    
    # Header for later pages
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("FOTOCOPIADORAS SyP | ESPECIFICACIÓN DE REQUISITOS DE SOFTWARE (IEEE 830)")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    # Footer for later pages
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    frun1 = fp.add_run("Confidencial - Entrega de Proyecto & Sustentación Técnica | Versión 2.0")
    frun1.font.name = "Calibri"
    frun1.font.size = Pt(8.5)
    frun1.font.color.rgb = RGBColor(100, 116, 139)

def format_row(row, bg_color=None, is_header=False):
    for cell in row.cells:
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        if bg_color:
            set_cell_background(cell, bg_color)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = "Calibri"
                if is_header:
                    run.font.size = Pt(9.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(30, 41, 59)

def build_srs_document():
    generate_diagram()
    doc = Document()
    
    # Page setup: Margins 2.5 cm (approx 0.984 inches)
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
    r_pre = p_pre.add_run("PROYECTO DE DESARROLLO E INTEGRACIÓN TECNOLÓGICA")
    r_pre.font.name = "Calibri"
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = SLATE
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(15)
    r_title = p_title.add_run("ESPECIFICACIÓN DE REQUISITOS DE SOFTWARE (SRS)\nSISTEMA E-COMMERCE Y GESTIÓN DE SERVICIO TÉCNICO")
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
    r_norm = p_norm.add_run("Estándar de Conformidad: IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018\nSeguridad y Mitigación: Estándar OWASP Top 10 API & Framework Strix")
    r_norm.font.name = "Calibri"
    r_norm.font.size = Pt(10.5)
    r_norm.font.italic = True
    r_norm.font.color.rgb = MUTED
    p_norm.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Box for Project Roles
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(25)
    p_box.paragraph_format.space_after = Pt(20)
    
    t_roles = doc.add_table(rows=4, cols=2)
    t_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    roles_data = [
        ("Destinatario Comercial (Cliente):", "Sra. Gladys Solano Murcia\nRepresentante Legal - Fotocopiadoras SyP"),
        ("Destinatario Académico / Evaluador:", "Instructor Técnico de Software\nEvaluación de Etapa Productiva / Formación"),
        ("Desarrollador / Documentador:", "Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\nIngeniería de Software & Arquitectura"),
        ("Fecha de Publicación y Versión:", "Noviembre de 2026 | Versión 2.0 (Alineada al Código en Producción)")
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
        ("1.0", "16/08/2026", "Equipo Desarrollo SyP", "Borrador inicial preliminar de requisitos basado en el estudio de mercado del sector de fotocopiado (referencia Copy Caess).", "Obsoleto"),
        ("2.0", "04/11/2026", "Ingeniero de Software Senior", "Actualización integral IEEE 830 basada en el 100% del código real (FastAPI, SQLite WAL, PWA, JWT, Strix). Incorporación de cotizaciones formales, contadores de copias y trazabilidad.", "Aprobado")
    ]
    for r_idx, r_data in enumerate(vers_rows):
        row = t_vers.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx % 2 == 0 else "F8FAFC")

    # -------------------------------------------------------------
    # TABLA DE CONTENIDO (ESTRUCTURA FORMAL)
    # -------------------------------------------------------------
    h_toc = doc.add_heading("Contenido del Documento", level=1)
    h_toc.paragraph_format.space_before = Pt(20)
    h_toc.paragraph_format.space_after = Pt(10)
    
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.line_spacing = 1.2
    toc_items = [
        "1. INTRODUCCIÓN",
        "   1.1 Propósito del Documento",
        "   1.2 Alcance del Producto de Software (SyP Web & REST API)",
        "   1.3 Definiciones, Acrónimos y Abreviaturas",
        "   1.4 Referencias Normativas y Técnicas",
        "   1.5 Visión General del Documento",
        "2. DESCRIPCIÓN GENERAL DEL PRODUCTO",
        "   2.1 Contexto Empresarial y Comercial (Neiva, Huila)",
        "   2.2 Perspectiva del Producto y Arquitectura de Alto Nivel",
        "   2.3 Funciones Principales del Sistema",
        "   2.4 Características y Perfiles de Usuarios",
        "   2.5 Restricciones Generales del Proyecto",
        "   2.6 Suposiciones y Dependencias Críticas",
        "3. ACTORES DEL SISTEMA Y MATRIZ DE PERMISOS",
        "4. DIAGRAMA GENERAL DE CASOS DE USO (IEEE 830)",
        "5. REQUISITOS FUNCIONALES DETALLADOS (RF-01 A RF-15)",
        "6. REQUISITOS NO FUNCIONALES (ISO/IEC 25010)",
        "7. REGLAS DE NEGOCIO TÉCNICAS Y COMERCIALES (RN-01 A RN-08)",
        "8. ESPECIFICACIÓN DE CASOS DE USO PRINCIPALES",
        "9. MATRIZ DE TRAZABILIDAD (REQUISITOS <-> CÓDIGO <-> BASE DE DATOS)",
        "10. CONTROL DE APROBACIÓN Y FIRMAS DE CONFORMIDAD"
    ]
    for item in toc_items:
        r = toc_p.add_run(item + "\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. INTRODUCCIÓN
    # -------------------------------------------------------------
    doc.add_heading("1. Introducción", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("1.1 Propósito del Documento\n")
    r.bold = True
    p.add_run(
        "El presente documento define la Especificación de Requisitos de Software (SRS) formal para la plataforma digital "
        "de comercio electrónico y soporte técnico de la empresa Fotocopiadoras SyP, ubicada en Neiva, Huila. "
        "Este artefacto de ingeniería cumple un doble objetivo: en primer lugar, actúa como contrato formal de alcance "
        "y especificación funcional con la propietaria y representante legal de la empresa, Sra. Gladys Solano Murcia; "
        "en segundo lugar, proporciona al Instructor y evaluador técnico el sustento metodológico riguroso bajo los estándares "
        "IEEE Std 830-1998 e ISO/IEC/IEEE 29148:2018, demostrando que la solución desarrollada satisface las necesidades del negocio, "
        "garantizando mantenibilidad, trazabilidad y seguridad de la información."
    )
    
    p = doc.add_paragraph()
    r = p.add_run("1.2 Alcance del Producto de Software (SyP Web & REST API)\n")
    r.bold = True
    p.add_run("? Acceso Web en Vivo: https://kevin81a.github.io/Fotocopiadora-S-P/\n? Repositorio GitHub: https://github.com/Kevin81A/Fotocopiadora-S-P\n\n")
    p.add_run(
        'El sistema informático denominado "Plataforma Digital Fotocopiadoras SyP" comprende dos subsistemas interconectados: '
        'un cliente frontend interactivo multipágina estructurado como Progressive Web App (PWA) con almacenamiento local y capacidades offline, '
        'y un servidor backend desacoplado que expone servicios web RESTful mediante el microframework FastAPI, persistencia transaccional '
        'en SQLite con modo WAL y control de acceso robusto mediante tokens JWT.\n\n'
        'El alcance funcional incluye:\n'
        '• Catálogo electrónico especializado en tecnología Ricoh: fotocopiadoras multifuncionales, impresoras, tóners/tintas, repuestos certificados y suministros.\n'
        '• Sistema de búsqueda facetada y filtros dinámicos por categoría, rango de precio, velocidad de impresión (ppm) y disponibilidad de inventario.\n'
        '• Carrito de compras persistente con sincronización reactiva en cliente y validación de precios en servidor.\n'
        '• Módulo generador de cotizaciones formales para clientes corporativos con cálculo legal de IVA del 19% y exportación para impresión/PDF.\n'
        '• Flujo de checkout con soporte para múltiples métodos de pago (PSE, transferencias bancarias, crédito empresarial a 30 días y pasarela asistida por WhatsApp).\n'
        '• Módulo de agendamiento y seguimiento de solicitudes de servicio técnico correctivo y preventivo.\n'
        '• Módulo de captura mensual de contadores de copias (monocromático y color) para clientes bajo modalidad de alquiler (renting).\n'
        '• Panel administrativo integral (CMS/Dashboard) con autenticación basada en roles (RBAC), control de inventario, cambio de estados de pedidos, '
        'gestión de órdenes de servicio, bandeja de notificaciones y exportación de datos en formato CSV.\n\n'
        'Límites y exclusiones explícitas (Fuera de Alcance v1):\n'
        '• Integración con facturación electrónica DIAN directa (se reserva para la versión 3.0 mediante proveedor tecnológico autorizado).\n'
        '• Aplicación móvil nativa en tiendas Play Store/App Store (se suple eficientemente con la tecnología PWA responsiva).\n'
        '• Módulo contable o de liquidación de nómina de la empresa.'
    )

    p = doc.add_paragraph()
    r = p.add_run("1.3 Definiciones, Acrónimos y Abreviaturas\n")
    r.bold = True
    
    t_def = doc.add_table(rows=8, cols=2)
    t_def.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_def.rows[0].cells[0].paragraphs[0].add_run("Término / Acrónimo")
    t_def.rows[0].cells[1].paragraphs[0].add_run("Definición Técnica en el Contexto del Proyecto")
    format_row(t_def.rows[0], bg_color="0F4C81", is_header=True)
    
    defs_data = [
        ("IEEE 830", "Estándar de la IEEE para la redacción estructurada de especificaciones de requisitos de software."),
        ("PWA", "Progressive Web App; aplicación web capaz de instalarse en dispositivos, trabajar offline mediante Service Worker y brindar experiencia nativa."),
        ("JWT", "JSON Web Token (RFC 7519); estándar abierto para la transmisión segura de afirmaciones de identidad entre cliente y servidor."),
        ("Bcrypt", "Función de hashing criptográfico adaptativo para almacenamiento de contraseñas resistentes a ataques de fuerza bruta."),
        ("WAL Mode", "Write-Ahead Logging; modo de concurrencia de SQLite que permite múltiples lectores concurrentes mientras un escritor opera sin bloqueos."),
        ("IDOR / BOLA", "Insecure Direct Object Reference / Broken Object-Level Authorization; fallo donde un usuario accede a recursos de otro manipulando identificadores."),
        ("Renting Ricoh", "Modelo de negocio donde se alquilan fotocopiadoras a empresas y se factura periódicamente por páginas impresas reportadas en contadores.")
    ]
    for idx, (t, d) in enumerate(defs_data):
        row = t_def.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(t)
        row.cells[1].paragraphs[0].add_run(d)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("1.4 Referencias Normativas y Técnicas\n")
    r.bold = True
    p.add_run(
        "1. IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications.\n"
        "2. ISO/IEC/IEEE 29148:2018: Systems and software engineering — Life cycle processes — Requirements engineering.\n"
        "3. OWASP Top 10 API Security Risks (2023): Estándar de mitigación de vulnerabilidades en APIs REST.\n"
        "4. Playbooks de Seguridad de la Información del Framework Strix (UseStrix/Strix).\n"
        "5. Código fuente y modelos relacionales del repositorio oficial del proyecto Fotocopiadoras SyP (Noviembre 2026)."
    )

    # -------------------------------------------------------------
    # 2. DESCRIPCIÓN GENERAL DEL PRODUCTO
    # -------------------------------------------------------------
    doc.add_heading("2. Descripción General del Producto", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("2.1 Contexto Empresarial y Comercial (Neiva, Huila)\n")
    r.bold = True
    p.add_run(
        "Fotocopiadoras SyP es una empresa comercial y de servicios técnicos radicada en la ciudad de Neiva (Huila, Colombia), "
        "con una amplia trayectoria en la provisión de soluciones integrales de impresión y copiado corporativo. "
        "Su modelo de operación contempla la venta de fotocopiadoras multifuncionales nuevas y reacondicionadas (con foco principal "
        "en la marca Ricoh, de alta demanda por notarías, constructoras, juzgados y entidades educativas), comercialización de consumibles "
        "(tóner negro y color, cartuchos, tintas), repuestos originales (cilindros, cuchillas de limpieza, rodillos de calor, bandas de transferencia), "
        "mantenimiento técnico especializado preventivo y correctivo en sitio, y esquemas de alquiler de equipos (renting) mediante cobro por volumen de copias."
    )

    p = doc.add_paragraph()
    r = p.add_run("2.2 Perspectiva del Producto y Arquitectura de Alto Nivel\n")
    r.bold = True
    p.add_run(
        "SyP Web se concibe como una solución desacoplada y orientada a servicios. El subsistema Frontend se ejecuta en el navegador del cliente "
        "aprovechando APIs nativas del estándar HTML5, estilos CSS3 modulares y controladores JavaScript Vanilla que consumen asíncronamente "
        "los endpoints del Backend expuestos bajo la URI base `/api/v1/`. El subsistema Backend opera sobre Python 3.12 y el servidor ASGI Uvicorn, "
        "interactuando con una base de datos relacional SQLite protegida mediante llaves foráneas e índices B-Tree."
    )

    p = doc.add_paragraph()
    r = p.add_run("2.3 Funciones Principales del Sistema\n")
    r.bold = True
    p.add_run(
        "1. Catálogo interactivo con filtrado dinámico por categorías, marcas, rangos de precio y búsqueda por texto libre.\n"
        "2. Ficha de producto con variantes, especificaciones técnicas (ppm, ciclo mensual, conectividad) y compatibilidades.\n"
        "3. Carrito de compras con persistencia reactiva en cliente y validación de totales en servidor.\n"
        "4. Generación de cotizaciones formales en formato PDF con vigencia predeterminada de 15 días.\n"
        "5. Checkout con validación de datos de entrega y selección de canales de pago PSE, transferencia o crédito a 30 días.\n"
        "6. Portal de autenticación y registro de clientes con sesiones seguras JWT (HS256).\n"
        "7. Agendamiento de servicios técnicos indicando fecha, franja horaria y descripción de la falla del equipo.\n"
        "8. Reporte mensual de contadores de copias para clientes corporativos de renting.\n"
        "9. Panel de control administrativo (Admin CMS) con tablero de indicadores financieros, inventario y exportación CSV."
    )

    p = doc.add_paragraph()
    r = p.add_run("2.4 Características y Perfiles de Usuarios\n")
    r.bold = True
    
    t_usr = doc.add_table(rows=5, cols=3)
    t_usr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_usr.rows[0].cells[0].paragraphs[0].add_run("Perfil de Usuario")
    t_usr.rows[0].cells[1].paragraphs[0].add_run("Descripción / Responsabilidad en el Negocio")
    t_usr.rows[0].cells[2].paragraphs[0].add_run("Habilidades Técnicas")
    format_row(t_usr.rows[0], bg_color="0F4C81", is_header=True)
    
    usr_data = [
        ("Visitante Anónimo", "Persona o empresa que explora el catálogo, cotiza productos y revisa canales de atención sin iniciar sesión.", "Básicas (Navegación web)"),
        ("Cliente Registrado", "Cliente corporativo o particular con cuenta activa; realiza pedidos, agenda visitas técnicas y consulta historiales.", "Básicas (Gestión de cuenta)"),
        ("Dueña / Administradora General (Gladys Solano Murcia)", "Responsable del negocio; gestiona precios, stock, aprueba pedidos, supervisa facturación y analiza métricas de ventas.", "Medias (Uso de paneles web intuitivos)"),
        ("Técnico de Soporte (Juan Sebastián Portela)", "Especialista técnico; revisa solicitudes de mantenimiento, atiende visitas en campo y registra novedades y estados técnicos.", "Medias-Técnicas (Operación de equipos Ricoh)")
    ]
    for idx, (p1, p2, p3) in enumerate(usr_data):
        row = t_usr.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(p1)
        row.cells[1].paragraphs[0].add_run(p2)
        row.cells[2].paragraphs[0].add_run(p3)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("2.5 Restricciones Generales del Proyecto\n")
    r.bold = True
    p.add_run(
        "• Lenguaje y Moneda: Operación 100% en idioma español (Colombia) y visualización monetaria en Pesos Colombianos (COP).\n"
        "• Impuestos: Desglose obligatorio de IVA del 19% en cotizaciones y órdenes de compra, conforme a la legislación tributaria colombiana.\n"
        "• Dependencias Tecnológicas: Backend en Python 3.12 y FastAPI, base de datos SQLite con conexión en modo WAL, frontend Vanilla JS sin frameworks pesados.\n"
        "• Seguridad: Cumplimiento estricto de las directivas OWASP Top 10 API y subsanación de vulnerabilidades Strix (Rate Limiting, JWT de alta entropía, CORS controlado y protección de rutas sensibles)."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. ACTORES DEL SISTEMA Y MATRIZ DE PERMISOS
    # -------------------------------------------------------------
    doc.add_heading("3. Actores del Sistema y Matriz de Permisos (RBAC)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "El sistema implementa un modelo de Control de Acceso Basado en Roles (RBAC) validado tanto en el cliente como en el backend "
        "a través de las dependencias `get_current_user` y `require_admin`. A continuación se detalla la matriz de privilegios:"
    )
    
    t_rbac = doc.add_table(rows=8, cols=4)
    t_rbac.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_rbac_headers = ["Módulo / Funcionalidad", "Visitante Anónimo", "Cliente Autenticado", "Administrador (Dueña/Técnico)"]
    for c_idx, h in enumerate(t_rbac_headers):
        t_rbac.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_rbac.rows[0], bg_color="0F4C81", is_header=True)
    
    rbac_rows = [
        ("Navegar Catálogo y Ficha de Productos", "Permitido (Lectura)", "Permitido (Lectura)", "Permitido (Lectura y Gestión)"),
        ("Generar Cotizaciones Formales", "Permitido (Rate Limited)", "Permitido (Asociada a cuenta)", "Permitido (Auditoría global)"),
        ("Crear Pedidos y Realizar Checkout", "Permitido (Como invitado)", "Permitido (Historial propio)", "Permitido (Gestión y Despacho)"),
        ("Solicitar Servicio Técnico", "Permitido (Con datos contacto)", "Permitido (Historial propio)", "Permitido (Asignación y Notas)"),
        ("Reportar Lectura de Contadores (Renting)", "Restringido (Requiere cuenta)", "Permitido (Sus equipos)", "Permitido (Auditoría contable)"),
        ("Crear y Editar Productos / Precios", "Denegado (401/403)", "Denegado (403)", "Permitido (Control total)"),
        ("Visualizar Analítica y Exportar CSV", "Denegado (401/403)", "Denegado (403)", "Permitido (Exclusivo Admin)")
    ]
    for r_idx, r_data in enumerate(rbac_rows):
        row = t_rbac.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx % 2 == 0 else "F8FAFC")

    # -------------------------------------------------------------
    # 4. DIAGRAMA GENERAL DE CASOS DE USO
    # -------------------------------------------------------------
    doc.add_heading("4. Diagrama General de Casos de Uso (IEEE 830)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "A continuación se presenta el diagrama general de casos de uso del sistema Fotocopiadoras SyP, modelando los cuatro "
        "actores clave y su interacción con los módulos del sistema dentro del límite de la plataforma tecnológica:"
    )
    
    if os.path.exists(DIAGRAM_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(DIAGRAM_PATH, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Diagrama de Casos de Uso y Límites del Sistema Fotocopiadoras SyP.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. REQUISITOS FUNCIONALES DETALLADOS (RF-01 A RF-15)
    # -------------------------------------------------------------
    doc.add_heading("5. Requisitos Funcionales Detallados (RF-01 a RF-15)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Los requisitos funcionales han sido definidos bajo el estándar IEEE 830 y verificados contra el código fuente "
        "en producción. Cada requisito incluye su identificador único, actor asociado, prioridad según MoSCoW "
        "(Must have, Should have, Could have) y su criterio de aceptación técnico comprobable:"
    )

    rf_list = [
        ("RF-01", "Catálogo Interactivo y Búsqueda Facetada Ricoh",
         "El sistema debe presentar el catálogo de productos permitiendo filtrado reactivo por categoría (Fotocopiadoras, Impresoras, Tintas y Tóneres, Repuestos, Accesorios, Mantenimiento), búsqueda por texto libre y ordenamiento por precio y relevancia.",
         "Alta (Must Have)", "Visitante / Cliente",
         "Al ingresar una búsqueda o filtro, el endpoint 'GET /api/v1/products' debe retornar los registros coincidentes en menos de 500 ms y la interfaz debe renderizar las tarjetas de producto sin recargar la página."),
         
        ("RF-02", "Ficha Técnica y Compatibilidad de Repuestos",
         "El sistema debe desplegar la ficha técnica detallada del producto seleccionado, mostrando imágenes, especificaciones técnicas (velocidad ppm, ciclo de trabajo, compatibilidad de códigos de repuestos, rendimiento de tóner) y estado de inventario.",
         "Alta (Must Have)", "Visitante / Cliente",
         "El endpoint 'GET /api/v1/products/{id}' debe entregar el objeto JSON completo con las especificaciones técnicas Ricoh y mostrar badge de stock ('ok', 'low', 'out')."),

        ("RF-03", "Carrito de Compras Persistente en Cliente",
         "El sistema debe permitir agregar, actualizar cantidades y eliminar productos en el carrito de compras, persistiendo la selección en el navegador mediante 'localStorage' y reflejando el contador en el menú superior.",
         "Alta (Must Have)", "Visitante / Cliente",
         "Los artículos agregados deben permanecer en el carrito tras recargar la página o navegar entre secciones, recalculando subtotales inmediatamente."),

        ("RF-04", "Generación Formal de Cotizaciones en Línea",
         "El sistema debe permitir a cualquier usuario generar una cotización formal a partir del carrito o productos seleccionados, calculando el subtotal, el IVA legal del 19% y el valor total, asignando un código único alfanumérico (ej. 'COT-XXXXXX').",
         "Alta (Must Have)", "Visitante / Cliente",
         "La cotización se registra en la base de datos vía 'POST /api/v1/quotes' y se habilita la visualización formateada con opción de impresión directa o guardado en PDF."),

        ("RF-05", "Procesamiento de Órdenes de Compra (Checkout)",
         "El sistema debe permitir concretar la compra capturando datos fiscales del comprador (Nombre/Razón Social, NIT/Cédula, Dirección, Teléfono, Ciudad) y método de pago (PSE, Tarjeta de Crédito/Débito, Transferencia Bancolombia/Nequi, Crédito Empresarial 30 Días).",
         "Alta (Must Have)", "Cliente / Visitante",
         "La orden se genera mediante 'POST /api/v1/orders' retornando un código de pedido ('PED-XXXXXX') con estado de pago 'Pendiente' o 'Aprobado' y notificación automática al panel administrativo."),

        ("RF-06", "Autenticación Segura y Gestión de Sesiones JWT",
         "El sistema debe permitir el registro de clientes y el inicio de sesión validando credenciales mediante contraseñas cifradas en Bcrypt y emitiendo un token Bearer JWT con tiempo de expiración configurable.",
         "Alta (Must Have)", "Todos los Usuarios",
         "El endpoint 'POST /api/v1/auth/login' debe retornar un token JWT válido y los endpoints protegidos deben validar dicho token en la cabecera 'Authorization: Bearer <token>'."),

        ("RF-07", "Solicitud y Agendamiento de Servicio Técnico",
         "El sistema debe proveer un módulo donde los clientes puedan registrar solicitudes de mantenimiento preventivo o correctivo, indicando marca/modelo del equipo Ricoh, falla observada, fecha deseada y franja horaria.",
         "Alta (Must Have)", "Cliente / Visitante",
         "La solicitud debe almacenarse en la tabla 'maintenance_requests' mediante 'POST /api/v1/requests' con estado inicial 'Pendiente', visible de inmediato en el panel del técnico."),

        ("RF-08", "Módulo de Reporte de Contadores de Copias (Renting)",
         "El sistema debe permitir a los clientes corporativos reportar mensualmente el número de impresiones monocromáticas y a color de sus equipos alquilados para el proceso de liquidación y facturación periódica.",
         "Alta (Must Have)", "Cliente Registrado",
         "El reporte se envía vía 'POST /api/v1/counters' asociando el usuario autenticado, modelo del equipo, mes lectivo y lecturas numéricas no negativas."),

        ("RF-09", "Panel Administrativo y Dashboard Analítico",
         "El sistema debe proveer una interfaz de administración segura exclusiva para roles con privilegio 'admin' (Dueña y Técnicos), mostrando estadísticas de ventas en COP, cantidad de pedidos por estado y distribución de servicios técnicos.",
         "Alta (Must Have)", "Administrador",
         "El endpoint 'GET /api/v1/admin/analytics' debe ser inaccesible sin token de administrador (HTTP 403 Forbidden) y debe suministrar datos agregados en tiempo real."),

        ("RF-10", "Gestión Integral del Catálogo (CRUD Productos)",
         "El panel administrativo debe permitir crear, actualizar y desactivar productos, repuestos y consumibles, modificando precios, inventario y fichas técnicas.",
         "Alta (Must Have)", "Administrador",
         "Las peticiones 'POST /api/v1/products' y 'PUT /api/v1/products/{id}' deben actualizar de manera inmediata los registros en SQLite previa validación de esquemas Pydantic."),

        ("RF-11", "Control y Despacho de Pedidos",
         "El administrador debe poder auditar todos los pedidos registrados, verificar comprobantes de pago y actualizar los estados de pago ('Aprobado', 'Rechazado') y envío ('En preparación', 'Despachado', 'Entregado').",
         "Alta (Must Have)", "Administrador",
         "La actualización mediante 'PATCH /api/v1/orders/{id}/status' debe disparar automáticamente una notificación interna para el cliente."),

        ("RF-12", "Gestión y Asignación de Solicitudes Técnicas",
         "El personal administrativo debe poder revisar las solicitudes de servicio técnico pendientes, asignar técnicos responsables (ej. Juan Sebastián Portela), registrar notas internas y cambiar su estado a 'Confirmada' o 'Completada'.",
         "Alta (Must Have)", "Administrador / Técnico",
         "La acción 'PATCH /api/v1/requests/{id}/status' actualiza el registro e inserta notas técnicas en la base de datos."),

        ("RF-13", "Bandeja de Notificaciones en Tiempo Real",
         "El sistema debe almacenar y entregar notificaciones al cliente relativas a cambios en sus pedidos o citas de servicio técnico, permitiendo marcarlas como leídas.",
         "Media (Should Have)", "Cliente / Admin",
         "El cliente consulta sus notificaciones vía 'GET /api/v1/notifications/my' y puede marcarlas con 'PATCH /api/v1/notifications/{id}/read'."),

        ("RF-14", "Exportación de Datos Comerciales a CSV",
         "El sistema debe permitir a la administración descargar en formato delimitado por comas (CSV) los datos históricos de pedidos, productos, solicitudes técnicas y reportes de contadores.",
         "Media (Should Have)", "Administrador",
         "El endpoint 'GET /api/v1/admin/export/{dataset}' debe retornar una respuesta con cabecera 'Content-Type: text/csv' y descarga inmediata."),

        ("RF-15", "Canal de Contacto y Redirección a WhatsApp Business",
         "El sistema debe integrar canales directos de atención al cliente mediante enlaces interactivos preconfigurados hacia la línea oficial de WhatsApp Business de Fotocopiadoras SyP y formulario PQR.",
         "Alta (Must Have)", "Visitante / Cliente",
         "Al hacer clic en el botón de WhatsApp se debe abrir la app o web con un mensaje contextual estructurado (referencia del equipo o solicitud).")
    ]

    for rf_id, rf_name, rf_desc, rf_prio, rf_actor, rf_crit in rf_list:
        t_rf = doc.add_table(rows=5, cols=2)
        t_rf.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        cell_h = t_rf.rows[0].cells[0]
        cell_h.merge(t_rf.rows[0].cells[1])
        cell_h.paragraphs[0].add_run(f"{rf_id}: {rf_name}")
        format_row(t_rf.rows[0], bg_color="0F4C81", is_header=True)
        
        fields = [
            ("Descripción Funcional:", rf_desc),
            ("Prioridad MoSCoW:", rf_prio),
            ("Actor Principal:", rf_actor),
            ("Criterio de Aceptación (DoD):", rf_crit)
        ]
        for f_idx, (f_lbl, f_val) in enumerate(fields):
            row = t_rf.rows[f_idx + 1]
            c0, c1 = row.cells[0], row.cells[1]
            c0.width = Inches(2.2)
            c1.width = Inches(4.3)
            set_cell_background(c0, "F1F5F9")
            set_cell_background(c1, "FFFFFF")
            set_cell_margins(c0, 60, 60, 90, 90)
            set_cell_margins(c1, 60, 60, 90, 90)
            
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(f_lbl)
            r0.bold = True
            r0.font.size = Pt(9)
            r0.font.color.rgb = NAVY
            
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(f_val)
            r1.font.size = Pt(9)
            r1.font.color.rgb = CHARCOAL
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. REQUISITOS NO FUNCIONALES (ISO/IEC 25010)
    # -------------------------------------------------------------
    doc.add_heading("6. Requisitos No Funcionales (ISO/IEC 25010)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Los requisitos no funcionales definen las restricciones arquitecturales, criterios de calidad y estándares de seguridad "
        "clasificados según la norma internacional de calidad de software ISO/IEC 25010:"
    )

    t_rnf = doc.add_table(rows=12, cols=4)
    t_rnf.alignment = WD_TABLE_ALIGNMENT.CENTER
    rnf_headers = ["ID", "Categoría ISO 25010", "Especificación Técnica", "Métrica de Verificación"]
    for c_idx, h in enumerate(rnf_headers):
        t_rnf.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_rnf.rows[0], bg_color="0F4C81", is_header=True)

    rnf_data = [
        ("RNF-01", "Rendimiento y Tiempo de Respuesta", "El backend FastAPI debe responder las peticiones de lectura del catálogo en menos de 1.5 segundos bajo condiciones normales.", "Latencia < 1500 ms medida en endpoint /health y /products."),
        ("RNF-02", "Seguridad en Autenticación", "Las contraseñas de los usuarios deben encriptarse obligatoriamente mediante algoritmo Bcrypt con factor de costo de 12 rondas.", "Ninguna contraseña se almacena en texto plano; tokens firmados con HS256."),
        ("RNF-03", "Mitigación OWASP Top 10", "Protección contra BOLA/IDOR, inyección SQL mediante consultas parametrizadas SQLite y Rate Limiting en endpoints sensibles.", "Zero vulnerabilidades críticas confirmadas en auditoría de seguridad Strix."),
        ("RNF-04", "Disponibilidad y Resiliencia", "La plataforma debe ofrecer un uptime mínimo del 99.5%, permitiendo operación continua de consulta de catálogo.", "Arquitectura desacoplada en VPS Linux y hosting estático de alta disponibilidad."),
        ("RNF-05", "Usabilidad y Accesibilidad", "Diseño totalmente responsivo con navegación fluida y jerarquía tipográfica legible en pantallas de 360px hasta 1920px.", "Conformidad con directivas WCAG 2.1 nivel AA."),
        ("RNF-06", "Compatibilidad de Navegadores", "Soporte nativo y sin distorsión visual en Google Chrome, Mozilla Firefox, Apple Safari y Microsoft Edge.", "Validación en navegadores evergreen de escritorio y móviles."),
        ("RNF-07", "Mantenibilidad del Código", "Estructura modular dividida en capas (datos, seguridad, esquemas, rutas) siguiendo buenas prácticas PEP 8.", "Validación estática con linters y tipado estricto con Pydantic v2."),
        ("RNF-08", "Concurrencia de Base de Datos", "SQLite configurado con 'PRAGMA journal_mode = WAL' y pool con 'check_same_thread=False' para alta concurrencia.", "Soporte de múltiples lectores simultáneos sin bloqueo de escritor."),
        ("RNF-09", "Localización e Impuestos", "Presentación de moneda en Pesos Colombianos (COP), fechas en formato DD/MM/AAAA y desglose legal de IVA del 19%.", "Cálculo exacto de IVA conforme al estatuto tributario colombiano."),
        ("RNF-10", "Copias de Seguridad", "Política de respaldo programado de la base de datos 'syp.db' y archivo '.jwt_secret' para contingencias operativas.", "Generación de backups periódicos en almacenamiento seguro independiente."),
        ("RNF-11", "Capacidades Offline (PWA)", "El frontend debe soportar almacenamiento en caché de assets estáticos y pantalla de fallback ante desconexión.", "Service Worker 'sw.js' registrado y pantalla 'offline.html' funcional.")
    ]
    for idx, (c1, c2, c3, c4) in enumerate(rnf_data):
        row = t_rnf.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        row.cells[3].paragraphs[0].add_run(c4)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    # -------------------------------------------------------------
    # 7. REGLAS DE NEGOCIO (RN-01 A RN-08)
    # -------------------------------------------------------------
    doc.add_heading("7. Reglas de Negocio Técnicas y Comerciales (RN-01 a RN-08)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Las reglas de negocio corresponden a las políticas operativas, comerciales y tributarias inmutables que "
        "rigen la lógica transaccional de Fotocopiadoras SyP:"
    )

    t_rn = doc.add_table(rows=9, cols=3)
    t_rn.alignment = WD_TABLE_ALIGNMENT.CENTER
    rn_headers = ["Regla", "Nombre de la Regla", "Descripción Operativa y Lógica de Negocio"]
    for c_idx, h in enumerate(rn_headers):
        t_rn.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_rn.rows[0], bg_color="0F4C81", is_header=True)

    rn_data = [
        ("RN-01", "Cálculo Obligatorio de IVA 19%", "Todo producto comercializado (equipos, suministros y repuestos) está gravado con el Impuesto al Valor Agregado (IVA) del 19% en Colombia. El sistema debe calcular: Total = Subtotal + (Subtotal * 0.19)."),
        ("RN-02", "Control de Stock y Disponibilidad", "Los productos con 'stock_status' = 'out' (agotado) se exhiben en el catálogo pero no pueden agregarse al carrito de compras ni emitir pedidos directos."),
        ("RN-03", "Aprobación de Órdenes y Pagos", "Las órdenes con pago PSE o tarjeta se marcan inicialmente en estado de verificación hasta la confirmación de la pasarela o comprobante bancario; las órdenes con 'Crédito 30 Días' requieren aprobación manual de la dueña."),
        ("RN-04", "Políticas de Garantía Ricoh", "Los equipos multifuncionales nuevos gozan de 12 meses de garantía directa; los equipos reacondicionados cuentan con 6 meses de garantía o límite de 50.000 copias (lo que ocurra primero)."),
        ("RN-05", "Liquidación de Renting por Contador", "Los clientes en alquiler de fotocopiadoras deben reportar su contador entre los días 25 y 30 de cada mes; el valor a facturar corresponde a las copias excedentes del cupo base pactado en contrato."),
        ("RN-06", "Agendamiento Técnico Anticipado", "Las solicitudes de servicio técnico deben programarse con un mínimo de 24 horas de anticipación para garantizar la disponibilidad del personal en campo en el área metropolitana de Neiva."),
        ("RN-07", "Vigencia de Cotizaciones", "Las cotizaciones emitidas formalmente por el sistema tienen una vigencia comercial garantizada de quince (15) días calendario a partir de su fecha de emisión."),
        ("RN-08", "Control de Acceso y Caducidad JWT", "Las sesiones administrativas y de cliente expiran automáticamente tras el tiempo de expiración fijado en la variable 'ACCESS_TOKEN_EXPIRE_MINUTES' (60 minutos por defecto), forzando re-autenticación.")
    ]
    for idx, (c1, c2, c3) in enumerate(rn_data):
        row = t_rn.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. ESPECIFICACIÓN DE CASOS DE USO PRINCIPALES
    # -------------------------------------------------------------
    doc.add_heading("8. Especificación de Casos de Uso Principales", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "A continuación se documentan formalmente los casos de uso nucleares que sustentan la operación "
        "de la plataforma e-commerce y el servicio técnico de Fotocopiadoras SyP:"
    )

    cu_list = [
        ("CU-01", "Realizar Pedido y Checkout E-commerce",
         "Visitante o Cliente Registrado",
         "El usuario cuenta con artículos seleccionados en su carrito de compras.",
         "1. El usuario accede a la vista de checkout.\n2. Ingresa sus datos de entrega y fiscales (Nombre, NIT/Cédula, Dirección, Teléfono).\n3. Selecciona el método de pago deseado (PSE, Transferencia, Crédito empresarial).\n4. El sistema valida los datos y envía la petición a 'POST /api/v1/orders'.\n5. El backend registra la orden en SQLite, descuenta el stock preventivamente y emite un código de orden 'PED-XXXXXX'.\n6. El sistema despliega la pantalla de confirmación y ofrece enlace de notificación a WhatsApp.",
         "Si falla la conexión con el servidor o los datos fiscales son incompletos, el sistema marca los campos en rojo y no procesa la orden.",
         "El pedido queda registrado con estado 'Pendiente' y se genera una notificación para la administración."),

        ("CU-02", "Solicitar Mantenimiento Técnico de Equipos",
         "Cliente Registrado o Visitante Corporativo",
         "El cliente tiene un equipo Ricoh que requiere revisión o soporte.",
         "1. El usuario ingresa a la sección 'Servicio Técnico'.\n2. Completa el formulario indicando modelo del equipo, tipo de servicio (preventivo/correctivo), fecha sugerida y descripción del fallo.\n3. Presiona 'Solicitar Servicio'.\n4. El sistema envía 'POST /api/v1/requests'.\n5. El servidor genera un identificador de solicitud 'req_XXXXXX' con estado 'Pendiente'.\n6. El sistema muestra mensaje de confirmación en pantalla.",
         "Si la fecha seleccionada corresponde a un día no hábil o pasado, el validador frontend solicita corregir la fecha.",
         "La solicitud queda disponible en la bandeja administrativa para asignación de visita técnica."),

        ("CU-03", "Gestión y Cambio de Estados de Pedidos",
         "Dueña / Administradora General (Gladys Solano Murcia)",
         "El administrador ha iniciado sesión con credenciales válidas en 'admin.html'.",
         "1. El administrador ingresa a la pestaña 'Pedidos y Ventas'.\n2. El sistema lista las órdenes registradas desde 'GET /api/v1/orders'.\n3. Selecciona una orden y verifica el comprobante bancario.\n4. Modifica el estado de pago a 'Aprobado' y el despacho a 'En preparación' o 'Despachado'.\n5. Envía la actualización mediante 'PATCH /api/v1/orders/{id}/status'.\n6. El sistema persiste los cambios y emite notificación interna.",
         "Si el token de sesión ha expirado, el sistema redirige automáticamente al login protegiendo la transacción.",
         "La orden queda actualizada con trazabilidad completa de cambios."),

        ("CU-04", "Reporte Mensual de Contadores de Fotocopiado",
         "Cliente Corporativo en Modalidad Renting",
         "El cliente dispone de equipos en alquiler y ha iniciado sesión en la plataforma.",
         "1. El cliente accede a la vista de contadores dentro de 'Servicio Técnico'.\n2. Selecciona el modelo de equipo asignado.\n3. Digita la lectura actual del contador monocromático y del contador a color.\n4. Selecciona el mes a reportar.\n5. Envía el reporte mediante 'POST /api/v1/counters'.\n6. El sistema valida que los contadores sean números enteros no negativos y registra la entrada en SQLite.",
         "Si el contador ingresado es menor al registrado en el mes anterior, el sistema alerta sobre posible inconsistencia de lectura.",
         "La lectura queda registrada en 'counter_reports' para auditoría y facturación de excesos de copias.")
    ]

    for cu_id, cu_name, cu_actor, cu_pre, cu_flow, cu_alt, cu_post in cu_list:
        t_cu = doc.add_table(rows=7, cols=2)
        t_cu.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        cell_h = t_cu.rows[0].cells[0]
        cell_h.merge(t_cu.rows[0].cells[1])
        cell_h.paragraphs[0].add_run(f"CASO DE USO: {cu_id} - {cu_name}")
        format_row(t_cu.rows[0], bg_color="0F4C81", is_header=True)
        
        cu_fields = [
            ("Actor Principal:", cu_actor),
            ("Precondición:", cu_pre),
            ("Flujo Normal (Paso a Paso):", cu_flow),
            ("Flujos Alternativos / Excepciones:", cu_alt),
            ("Postcondición:", cu_post)
        ]
        for f_idx, (f_lbl, f_val) in enumerate(cu_fields):
            row = t_cu.rows[f_idx + 1]
            c0, c1 = row.cells[0], row.cells[1]
            c0.width = Inches(2.2)
            c1.width = Inches(4.3)
            set_cell_background(c0, "F1F5F9")
            set_cell_background(c1, "FFFFFF")
            set_cell_margins(c0, 60, 60, 90, 90)
            set_cell_margins(c1, 60, 60, 90, 90)
            
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(f_lbl)
            r0.bold = True
            r0.font.size = Pt(9)
            r0.font.color.rgb = NAVY
            
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(f_val)
            r1.font.size = Pt(9)
            r1.font.color.rgb = CHARCOAL
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. MATRIZ DE TRAZABILIDAD (REQUISITOS <-> CÓDIGO <-> BD)
    # -------------------------------------------------------------
    doc.add_heading("9. Matriz de Trazabilidad (Requisitos <-> Código <-> BD)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Para dar pleno cumplimiento a los criterios de evaluación del estándar ISO/IEC 12207 e IEEE 830, la siguiente matriz "
        "establece la trazabilidad bidireccional entre los Requisitos Funcionales, las vistas del Frontend, los Endpoints de la API "
        "y las tablas de la base de datos relacional:"
    )

    t_traz = doc.add_table(rows=16, cols=5)
    t_traz.alignment = WD_TABLE_ALIGNMENT.CENTER
    traz_headers = ["Req. ID", "Nombre Funcional", "Componente / Vista UI", "Endpoint Backend (FastAPI)", "Tabla SQLite"]
    for c_idx, h in enumerate(traz_headers):
        t_traz.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_traz.rows[0], bg_color="0F4C81", is_header=True)

    traz_data = [
        ("RF-01", "Catálogo y Búsqueda", "productos.html / js/products.js", "GET /api/v1/products", "products, categories"),
        ("RF-02", "Ficha Técnica Ricoh", "productos.html (Modal detalle)", "GET /api/v1/products/{id}", "products"),
        ("RF-03", "Carrito de Compras", "index.html, productos.html (Drawer)", "Gestión Local / Storage", "Almacenamiento Local"),
        ("RF-04", "Cotizaciones en Línea", "cotizacion.html / js/main.js", "POST /api/v1/quotes", "quotes"),
        ("RF-05", "Checkout y Pedidos", "cotizacion.html (Checkout modal)", "POST /api/v1/orders", "orders, users"),
        ("RF-06", "Autenticación JWT", "login.html / js/auth.js", "POST /api/v1/auth/login, register", "users"),
        ("RF-07", "Servicio Técnico", "servicio-tecnico.html / js/main.js", "POST /api/v1/requests", "maintenance_requests"),
        ("RF-08", "Reporte Contadores", "servicio-tecnico.html", "POST /api/v1/counters", "counter_reports"),
        ("RF-09", "Dashboard Analítico", "admin.html / js/main.js", "GET /api/v1/admin/analytics", "orders, requests, quotes"),
        ("RF-10", "CRUD de Productos", "admin.html (Pestaña inventario)", "POST, PUT /api/v1/products", "products, categories"),
        ("RF-11", "Gestión de Pedidos", "admin.html (Pestaña órdenes)", "GET, PATCH /api/v1/orders", "orders"),
        ("RF-12", "Asignación Técnica", "admin.html (Pestaña soporte)", "GET, PATCH /api/v1/requests", "maintenance_requests"),
        ("RF-13", "Notificaciones", "admin.html, navbar widget", "GET, PATCH /api/v1/notifications", "notifications"),
        ("RF-14", "Exportación CSV", "admin.html (Botones exportar)", "GET /api/v1/admin/export/{set}", "Todas las entidades"),
        ("RF-15", "Canal de Contacto", "contacto.html / WhatsApp float", "POST /api/v1/contact", "contact_messages")
    ]
    for idx, (c1, c2, c3, c4, c5) in enumerate(traz_data):
        row = t_traz.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        row.cells[3].paragraphs[0].add_run(c4)
        row.cells[4].paragraphs[0].add_run(c5)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    # -------------------------------------------------------------
    # 10. CONTROL DE APROBACIÓN Y FIRMAS
    # -------------------------------------------------------------
    doc.add_heading("10. Control de Aprobación y Firmas de Conformidad", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "La firma del presente documento certifica que los requisitos aquí especificados corresponden fielmente a los "
        "acuerdos de alcance, necesidades comerciales de Fotocopiadoras SyP y estándares técnicos exigidos para la entrega formal del software:"
    )

    t_sig = doc.add_table(rows=3, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig_headers = ["Cliente / Representante Legal", "Desarrollador / Documentador", "Instructor / Evaluador Técnico"]
    for c_idx, h in enumerate(t_sig_headers):
        t_sig.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_sig.rows[0], bg_color="0F4C81", is_header=True)

    sig_content = [
        ("Sra. Gladys Solano Murcia\nRepresentante Legal\nFotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Kevin Portela [POR CONFIRMAR]\nLíder de Desarrollo de Software\nProyecto Fotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Instructor Evaluador [POR CONFIRMAR]\nEvaluador Etapa Productiva / Académica\nCentro de Formación Técnica\n\nFirma: _________________________\nFecha: _____ / _____ / 2026"),
        ("Conformidad Comercial y Operativa", "Conformidad Arquitectural y Funcional", "Aprobación y Validación Técnica")
    ]
    for r_idx, r_data in enumerate(sig_content):
        row = t_sig.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx == 0 else "F8FAFC")

    # Save final document
    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] SRS Document generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_srs_document()
