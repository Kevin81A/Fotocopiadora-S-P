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
OUTPUT_DOCX = os.path.join(DOCS_DIR, "03_Manual_Tecnico_y_Arquitectura.docx")
DIAGRAM_PATH = os.path.join(DOCS_DIR, "tech_architecture_diagram.png")

def generate_arch_diagram():
    """Generates an Architecture & Component Diagram using Pillow."""
    width, height = 1350, 900
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
    draw.text((30, 20), "ARQUITECTURA DE SOFTWARE C4 & COMPONENTES - FOTOCOPIADORAS SyP", fill="#FFFFFF", font=font_title)

    # Helper function for container boxes
    def draw_container(x, y, w, h, title, subtitle, items, bg_color="#FFFFFF", border_color="#0F4C81", header_color="#0F4C81"):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=10, outline=border_color, width=2, fill=bg_color)
        draw.rounded_rectangle([x, y, x + w, y + 42], radius=10, outline=header_color, width=1, fill=header_color)
        draw.rectangle([x, y + 25, x + w, y + 42], fill=header_color)
        draw.text((x + 15, y + 10), title, fill="#FFFFFF", font=font_box_title)
        draw.text((x + 15, y + 48), subtitle, fill="#64748B", font=font_box_sub)
        
        curr_y = y + 72
        for itm in items:
            draw.text((x + 15, curr_y), "• " + itm, fill="#1E293B", font=font_item)
            curr_y += 20
        return (x, y, w, h)

    # 1. CLIENT LAYER (Browsers & PWA)
    client_items = [
        "Single-Page & Multi-view Responsive UI",
        "HTML5 Semántico + CSS3 Modular (Variables)",
        "Vanilla JS (State & Reactive DOM)",
        "PWA Service Worker (sw.js - Cache First Assets)",
        "Web App Manifest (PWA instalable)",
        "LocalStorage (Carrito & Tokens JWT)"
    ]
    draw_container(40, 100, 360, 230, "1. CAPA CLIENTE (FRONTEND PWA)", "Navegadores Evergreen (Móvil, Tablet, Desktop)", client_items, border_color="#2563EB", header_color="#1E40AF")

    # 2. PROXY & REVERSE PROXY (Vercel / Nginx)
    gateway_items = [
        "Vercel Edge Network (Hosting Estático)",
        "Servidor Estático Seguro (Puerto 5500)",
        "Bloqueo de Extensiones (.db, .py, .env, .git)",
        "Cabeceras de Seguridad (X-Frame, CSP, nosniff)",
        "Terminación TLS/SSL (HTTPS Puerto 443)",
        "CORS Filter (Orígenes Permitidos Controlados)"
    ]
    draw_container(40, 370, 360, 230, "2. ENTRADA Y SEGURIDAD PERIMETRAL", "Nginx / Vercel Edge / Static Server", gateway_items, border_color="#0D9488", header_color="#0F766E")

    # 3. BACKEND REST API (FastAPI)
    backend_items = [
        "FastAPI 0.115+ (Asynchronous ASGI)",
        "Uvicorn Server (Puerto 8000 en 127.0.0.1)",
        "Enrutamiento /api/v1 (29 Endpoints Reales)",
        "Inyección de Dependencias (Depends)",
        "Pydantic v2 (Esquemas y Validación Estricta)",
        "InMemoryRateLimiter (Protección Brute Force)"
    ]
    draw_container(480, 100, 390, 230, "3. CAPA DE APLICACIÓN (FASTAPI)", "Python 3.12 Asynchronous Core", backend_items, border_color="#0F4C81", header_color="#0F4C81")

    # 4. SECURITY & AUTHENTICATION SUBSYSTEM
    sec_items = [
        "Autenticación JWT (RFC 7519, Algoritmo HS256)",
        "Hashing Bcrypt con 12 Rondas de Salting",
        "Control de Acceso RBAC (cliente vs admin)",
        "Gestión Segura de Clave Secreta (.jwt_secret)",
        "Expiración Parametrizable (ACCESS_TOKEN_EXPIRE)",
        "Protección BOLA / IDOR en Órdenes y Cotizaciones"
    ]
    draw_container(480, 370, 390, 230, "4. SUBSISTEMA DE SEGURIDAD (JWT)", "Capa de Protección y Autenticación", sec_items, border_color="#DC2626", header_color="#B91C1C")

    # 5. DATA ACCESS & TRANSACTION LAYER
    dal_items = [
        "Context Manager get_db() con Commit / Rollback",
        "Connection Pool Thread-safe (check_same_thread=False)",
        "Timeout de Bloqueo a 20.0 Segundos",
        "Serialización JSON para Órdenes y Cotizaciones",
        "Exportador Nativo de Reportes CSV",
        "Disparadores de Notificaciones Internas"
    ]
    draw_container(930, 100, 380, 230, "5. CAPA DE ACCESO A DATOS (DAL)", "database.py & Transacciones Atómicas", dal_items, border_color="#D97706", header_color="#B45309")

    # 6. PERSISTENCE ENGINE (SQLite WAL)
    db_items = [
        "Base de Datos syp.db (SQLite 3 Normalizada)",
        "Modo Concurrente WAL (Write-Ahead Logging)",
        "PRAGMA foreign_keys = ON (Integridad Dura)",
        "8 Índices B-Tree Secundarios Optimizados",
        "9 Tablas Relacionales (users, orders, etc.)",
        "Backups en Caliente (sqlite3_backup API)"
    ]
    draw_container(930, 370, 380, 230, "6. MOTOR DE PERSISTENCIA (SQLITE WAL)", "Almacenamiento Local de Alto Rendimiento", db_items, border_color="#059669", header_color="#047857")

    # 7. EXTERNAL INTEGRATIONS (Bottom Banner)
    draw.rounded_rectangle([40, 640, 1270, 850], radius=10, outline="#64748B", width=2, fill="#FFFFFF")
    draw.rounded_rectangle([40, 640, 1270, 680], radius=10, outline="#475569", width=1, fill="#475569")
    draw.rectangle([40, 665, 1270, 680], fill="#475569")
    draw.text((60, 650), "7. SERVICIOS EXTERNOS Y CANALES DE INTEGRACIÓN", fill="#FFFFFF", font=font_box_title)
    
    ext_boxes = [
        (70, 700, 260, 120, "WhatsApp Business API", "wa.me Protocol", "Enlace directo con mensajes contextuales predefinidos para soporte y cotizaciones."),
        (370, 700, 260, 120, "Pasarelas Locales (PSE / Bancos)", "Checkout E-commerce", "Soporte de pagos por PSE, Bancolombia, Nequi y transferencias directas."),
        (670, 700, 260, 120, "Google Maps Platform", "Ubicación Georreferenciada", "Mapa embebido con la sede física de Fotocopiadoras SyP en Neiva."),
        (970, 700, 260, 120, "Generador PDF Cliente", "Impresión de Cotizaciones", "Conversión de órdenes y cotizaciones en comprobantes PDF descargables.")
    ]
    for ex, ey, ew, eh, etit, esub, edesc in ext_boxes:
        draw.rounded_rectangle([ex, ey, ex + ew, ey + eh], radius=6, outline="#CBD5E1", width=1, fill="#F8FAFC")
        draw.text((ex + 10, ey + 8), etit, fill="#0F172A", font=font_badge)
        draw.text((ex + 10, ey + 26), esub, fill="#64748B", font=font_badge)
        # Word wrap desc
        words = edesc.split(" ")
        line1, line2 = "", ""
        for w in words:
            if len(line1 + " " + w) < 32:
                line1 += " " + w
            else:
                line2 += " " + w
        draw.text((ex + 10, ey + 48), line1.strip(), fill="#334155", font=font_item)
        draw.text((ex + 10, ey + 68), line2.strip(), fill="#334155", font=font_item)

    # Connection lines between main layers
    # Frontend -> Gateway
    draw.line([(220, 330), (220, 370)], fill="#2563EB", width=2)
    draw.polygon([(215, 365), (225, 365), (220, 372)], fill="#2563EB")
    draw.text((230, 345), "HTTPS / WSS", fill="#1E40AF", font=font_badge)

    # Gateway -> Backend
    draw.line([(400, 485), (440, 485), (440, 215), (480, 215)], fill="#0D9488", width=2)
    draw.polygon([(475, 210), (475, 220), (482, 215)], fill="#0D9488")
    draw.text((410, 345), "CORS / Proxy", fill="#0F766E", font=font_badge)

    # Backend <-> Security
    draw.line([(675, 330), (675, 370)], fill="#DC2626", width=2)
    draw.polygon([(670, 365), (680, 365), (675, 372)], fill="#DC2626")
    draw.text((685, 345), "Depends(JWT)", fill="#B91C1C", font=font_badge)

    # Backend <-> DAL
    draw.line([(870, 215), (930, 215)], fill="#D97706", width=2)
    draw.polygon([(925, 210), (925, 220), (932, 215)], fill="#D97706")
    draw.text((880, 195), "get_db()", fill="#B45309", font=font_badge)

    # DAL <-> SQLite WAL
    draw.line([(1120, 330), (1120, 370)], fill="#059669", width=2)
    draw.polygon([(1115, 365), (1125, 365), (1120, 372)], fill="#059669")
    draw.text((1130, 345), "SQL / WAL", fill="#047857", font=font_badge)

    img.save(DIAGRAM_PATH, "PNG", dpi=(300, 300))
    print(f"[OK] Tech Architecture Diagram generated at: {DIAGRAM_PATH}")

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
    hrun = hp.add_run("FOTOCOPIADORAS SyP | MANUAL TÉCNICO Y DE ARQUITECTURA DE SOFTWARE")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    frun1 = fp.add_run("Confidencial - Entrega de Proyecto & Sustentación Técnica | Arquitectura v2.0")
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

def build_tech_manual_document():
    generate_arch_diagram()
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
    r_pre = p_pre.add_run("INGENIERÍA DE SOFTWARE & ARQUITECTURA DE SISTEMAS")
    r_pre.font.name = "Calibri"
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = SLATE
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(15)
    r_title = p_title.add_run("MANUAL TÉCNICO Y DE ARQUITECTURA DE SOFTWARE\nPLATAFORMA E-COMMERCE Y SERVICIO TÉCNICO")
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
    r_norm = p_norm.add_run("Modelo de Arquitectura: Patrón Desacoplado Cliente-API (C4 Model)\nBackend: FastAPI 0.115+ (Python 3.12) | Persistencia: SQLite 3 Modo WAL\nSeguridad: JWT HS256, Bcrypt 12 Rounds, Rate Limiting y Mitigaciones OWASP/Strix")
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
        ("Líder de Arquitectura & Desarrollo:", "Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\nIngeniero de Software & Arquitecto Técnico"),
        ("Versión y Entorno de Ejecución:", "Versión 2.0 (Producción) | FastAPI + PWA Vanilla JS")
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
        ("1.0", "11/09/2026", "Equipo Desarrollo SyP", "Documentación técnica preliminar de prototipos frontend y servicios legacy.", "Superado"),
        ("2.0", "04/11/2026", "Ingeniero de Software Senior", "Manual técnico exhaustivo basado en el 100% del código real (FastAPI, catálogo de 29 endpoints, seguridad JWT, PWA, mitigación OWASP Strix).", "Aprobado")
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
        "1. ARQUITECTURA GENERAL DEL SISTEMA",
        "   1.1 Patrón Arquitectural: Desacoplado Cliente-API",
        "   1.2 Diagrama de Arquitectura y Componentes C4 (Contenedores)",
        "   1.3 Flujo de Datos y Comunicación entre Subsistemas",
        "2. SUBSISTEMA FRONTEND Y PROGRESSIVE WEB APP (PWA)",
        "   2.1 Estructura del Árbol de Directorios del Cliente",
        "   2.2 Arquitectura de Componentes en JavaScript Vanilla",
        "   2.3 Configuración PWA, Service Worker y Modo Offline",
        "   2.4 Sistema de Estilos y Diseño Responsivo CSS3",
        "3. SUBSISTEMA BACKEND Y API REST (FASTAPI)",
        "   3.1 Estructura Modular y Ciclo de Vida de la Aplicación",
        "   3.2 Inyección de Dependencias y Manejo Transaccional",
        "   3.3 Esquemas de Datos y Validación Estricta con Pydantic v2",
        "4. ESPECIFICACIÓN Y CATÁLOGO COMPLETO DE ENDPOINTS (29 APIS)",
        "   4.1 Módulo 1: Health y Diagnóstico del Servidor (1 Endpoint)",
        "   4.2 Módulo 2: Autenticación, Usuarios y Perfil (3 Endpoints)",
        "   4.3 Módulo 3: Catálogo de Productos y Repuestos Ricoh (4 Endpoints)",
        "   4.4 Módulo 4: Solicitudes de Servicio Técnico (4 Endpoints)",
        "   4.5 Módulo 5: Cotizaciones Formales y Contacto PQR (4 Endpoints)",
        "   4.6 Módulo 6: Pedidos, Checkout y Despacho (5 Endpoints)",
        "   4.7 Módulo 7: Reportes Mensuales de Contadores - Renting (2 Endpoints)",
        "   4.8 Módulo 8: Sistema de Notificaciones en Vivo (4 Endpoints)",
        "   4.9 Módulo 9: Analítica Administrativa y Exportación CSV (2 Endpoints)",
        "5. CAPA DE SEGURIDAD, DIRECTIVAS OWASP Y AUDITORÍA STRIX",
        "   5.1 Flujo Criptográfico y Gestión de Tokens JWT (HS256)",
        "   5.2 Hashing de Contraseñas con Bcrypt (12 Rondas)",
        "   5.3 Control de Acceso Basado en Roles (RBAC)",
        "   5.4 Política de Orígenes Cruzados (CORS) y Restricción de Cabeceras",
        "   5.5 Mecanismo de Rate Limiting en Memoria",
        "   5.6 Matriz de Remediación de Vulnerabilidades Strix (VULN-01 a VULN-08)",
        "6. CONTROL DE APROBACIÓN Y FIRMAS DE CONFORMIDAD"
    ]
    for item in toc_items:
        r = toc_p.add_run(item + "\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. ARQUITECTURA GENERAL DEL SISTEMA
    # -------------------------------------------------------------
    doc.add_heading("1. Arquitectura General del Sistema", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("1.1 Patrón Arquitectural: Desacoplado Cliente-API\n")
    r.bold = True
    p.add_run(
        "La solución tecnológica de 'Fotocopiadoras SyP' ha sido diseñada bajo el patrón arquitectural de Cliente-API Desacoplado "
        "(Decoupled Client-API Architecture). Este enfoque separa de manera estricta la interfaz de usuario y la lógica de presentación "
        "(Frontend) de las reglas de negocio, persistencia y seguridad transaccional (Backend).\n\n"
        "Ventajas estratégicas del modelo implementado:\n"
        "• Escalabilidad Independiente: El frontend se sirve como un conjunto de recursos estáticos altamente optimizados que pueden "
        "desplegarse en redes globales de distribución de contenido (CDN / Edge Networks como Vercel), mientras que el backend "
        "FastAPI opera sobre un servidor ASGI enfocado exclusivamente en procesar peticiones JSON concurrentes.\n"
        "• Mantenibilidad y Trazabilidad: Los cambios en la interfaz visual no alteran la lógica de negocio ni comprometen la base de datos. "
        "Asimismo, el catálogo de APIs REST puede ser consumido por futuros clientes (como aplicaciones móviles nativas o sistemas de facturación).\n"
        "• Resiliencia y Rendimiento: El frontend aprovecha capacidades de Progressive Web App (PWA) para operar en modo desconectado "
        "o con conectividad intermitente, apoyándose en la base de datos local SQLite configurada con modo WAL en el backend."
    )

    p = doc.add_paragraph()
    r = p.add_run("1.2 Diagrama de Arquitectura y Componentes C4 (Contenedores)\n")
    r.bold = True
    p.add_run(
        "A continuación se presenta el diagrama de componentes y arquitectura global de la plataforma, modelando los 7 subsistemas "
        "principales, sus protocolos de enlace y sus mecanismos de contención perimetral:"
    )

    if os.path.exists(DIAGRAM_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(DIAGRAM_PATH, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Diagrama de Arquitectura C4 y Flujo de Componentes - Fotocopiadoras SyP.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED

    p = doc.add_paragraph()
    r = p.add_run("1.3 Flujo de Datos y Comunicación entre Subsistemas\n")
    r.bold = True
    p.add_run(
        "1. Interacción del Usuario: El cliente accede al sitio mediante HTTPS. Los recursos estáticos (HTML5, CSS3, JS) son entregados "
        "por el servidor estático o la CDN de Vercel.\n"
        "2. Registro y Autenticación: El cliente envía sus credenciales mediante 'POST /api/v1/auth/login'. El backend verifica el hash Bcrypt "
        "en SQLite y emite un token JWT firmado con HS256. El cliente almacena el token en su 'localStorage' seguro.\n"
        "3. Peticiones Autorizadas: Para endpoints protegidos (checkout, servicio técnico, reporte de contadores, analítica), el cliente "
        "inyecta la cabecera HTTP 'Authorization: Bearer <token>'. La dependencia 'get_current_user' valida la firma, extrae el identificador "
        "y comprueba que la cuenta esté activa ('is_active = 1').\n"
        "4. Persistencia Transaccional: Las operaciones de escritura invocan el context manager 'get_db()', ejecutando transacciones ACID "
        "en el archivo WAL de SQLite ('syp.db-wal') sin interferir con las lecturas concurrentes del catálogo."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. SUBSISTEMA FRONTEND Y PROGRESSIVE WEB APP (PWA)
    # -------------------------------------------------------------
    doc.add_heading("2. Subsistema Frontend y Progressive Web App (PWA)", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("2.1 Estructura del Árbol de Directorios del Cliente\n")
    r.bold = True
    p.add_run(
        "El código fuente del frontend reside en el directorio 'syp-web/' y se organiza bajo una estructura modular:\n"
        "• syp-web/\n"
        "  ├── css/\n"
        "  │   └── style.css                 # Hoja de estilos unificada y modular (110 KB)\n"
        "  ├── js/\n"
        "  │   ├── auth.js                   # Módulo de sesión, login, registro y decodificación JWT\n"
        "  │   ├── main.js                   # Núcleo de la aplicación: carrito, checkout, órdenes y UI reactiva\n"
        "  │   └── products.js               # Catálogo de datos, buscador facetado y filtros de repuestos\n"
        "  ├── img/                          # Recursos gráficos vectoriales, logos y fotografías Ricoh\n"
        "  ├── index.html                    # Página de aterrizaje (Landing) y equipos destacados\n"
        "  ├── productos.html                # Catálogo interactivo con filtros dinámicos\n"
        "  ├── cotizacion.html               # Generador de cotizaciones en PDF con desglose de IVA 19%\n"
        "  ├── servicio-tecnico.html         # Módulo de agendamiento y reporte mensual de contadores\n"
        "  ├── contacto.html                 # Canales de atención PQR, horarios y Google Maps\n"
        "  ├── nosotros.html                 # Trayectoria institucional y especialización Ricoh\n"
        "  ├── login.html                    # Portal unificado de autenticación y registro\n"
        "  ├── admin.html                    # Panel administrativo integral (Dashboard y CRUD)\n"
        "  ├── offline.html                  # Pantalla de respaldo ante desconexión de red\n"
        "  ├── manifest.json                 # Metadatos de la PWA para instalación en dispositivos\n"
        "  ├── sw.js                         # Service Worker con caché 'Network-First'\n"
        "  └── vercel.json                   # Configuración de despliegue y cabeceras de seguridad"
    )

    p = doc.add_paragraph()
    r = p.add_run("2.2 Arquitectura de Componentes en JavaScript Vanilla\n")
    r.bold = True
    p.add_run(
        "A diferencia de aplicaciones basadas en frameworks pesados (como React o Angular) que introducen una sobrecarga de bundles "
        "de varios megabytes, Fotocopiadoras SyP utiliza JavaScript Vanilla estructurado con patrones de módulos limpios:\n"
        "• Objeto Global 'SyP': Encapsula el estado de la aplicación, el carrito de compras, el cálculo de totales y los helpers de formato monetario COP.\n"
        "• Módulo 'Auth': Maneja el ciclo de vida del token JWT, refresco de sesión en memoria, verificación de expiración y persistencia "
        "en 'localStorage'. Provee la función 'Auth.getAuthHeaders()' para adjuntar automáticamente el token en peticiones 'fetch()'.\n"
        "• Renderizado Declarativo del DOM: El renderizado de tarjetas de producto, líneas de cotización y pedidos se ejecuta mediante template literals "
        "sanitizados, asegurando fluidez a 60 cuadros por segundo (FPS)."
    )

    p = doc.add_paragraph()
    r = p.add_run("2.3 Configuración PWA, Service Worker y Modo Offline\n")
    r.bold = True
    p.add_run(
        "La plataforma cumple con los estándares modernos de Progressive Web Apps (PWA), permitiendo su instalación como aplicación "
        "independiente tanto en Android (mediante WebAPK) como en Windows y macOS:\n"
        "• manifest.json: Define el nombre 'Fotocopiadoras SyP', colores corporativos ('theme_color: #0F4C81', 'background_color: #F8FAFC'), "
        "modo de visualización 'standalone' e iconos adaptativos de 192x192 y 512x512 píxeles.\n"
        "• Service Worker (sw.js): Implementa una estrategia de caché dual:\n"
        "  - Estrategia Cache-First para recursos estáticos inmutables (CSS, imágenes de equipos Ricoh, fuentes tipográficas).\n"
        "  - Estrategia Network-First con fallback para vistas HTML; si la conexión a internet falla, el Service Worker intercepta la solicitud "
        "y despliega inmediatamente la vista 'offline.html', garantizando que el usuario nunca vea la pantalla de error genérica del navegador."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. SUBSISTEMA BACKEND Y API REST (FASTAPI)
    # -------------------------------------------------------------
    doc.add_heading("3. Subsistema Backend y API REST (FastAPI)", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("3.1 Estructura Modular y Ciclo de Vida de la Aplicación\n")
    r.bold = True
    p.add_run(
        "El servidor backend está implementado en Python 3.12 utilizando el microframework asíncrono FastAPI. Su arquitectura "
        "se organiza en 4 módulos nucleares de alta cohesión y bajo acoplamiento:\n"
        "1. main.py: Punto de entrada de la aplicación; inicializa el servidor FastAPI, registra middlewares (CORS, Rate Limiting), "
        "define los manejadores de excepciones globales y expone los 29 endpoints del sistema.\n"
        "2. security.py: Capa criptográfica; contiene los algoritmos de hashing Bcrypt, generación y validación de tokens JWT, "
        "gestión de la clave secreta y las dependencias de control de acceso 'get_current_user' y 'require_admin'.\n"
        "3. models.py: Capa de esquemas Pydantic v2; define los contratos de entrada y salida, asegurando validación tipada estricta, "
        "expresiones regulares y límites de longitud antes de que los datos alcancen la base de datos.\n"
        "4. database.py: Capa de persistencia y conexión SQLite WAL; administra la inicialización de tablas, índices B-Tree y "
        "el context manager transaccional 'get_db()'."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.2 Inyección de Dependencias y Manejo Transaccional\n")
    r.bold = True
    p.add_run(
        "FastAPI proporciona un sistema nativo de inyección de dependencias ('Depends') que se aprovecha transversalmente en el backend:\n"
        "• Dependencia de Autenticación: Cualquier ruta que requiera usuario autenticado declara 'current_user: dict = Depends(get_current_user)'. "
        "Si la petición carece de cabecera Bearer o el token es inválido, el sistema corta la ejecución y responde 'HTTP 401 Unauthorized'.\n"
        "• Dependencia de Privilegios Administrativos: Las rutas de gestión declaran 'admin_user: dict = Depends(require_admin)'. "
        "Si el usuario está autenticado pero su rol es 'cliente', el sistema deniega el acceso con 'HTTP 403 Forbidden'.\n"
        "• Dependencias de Protección Anti-Abuso: Endpoints como login, registro y cotizaciones inyectan dependencias de Rate Limiting "
        "('Depends(rate_limit_login)'), mitigando ataques de fuerza bruta."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.3 Esquemas de Datos y Validación Estricta con Pydantic v2\n")
    r.bold = True
    p.add_run(
        "El archivo 'models.py' define esquemas inmutables basados en Pydantic BaseModel, asegurando que ninguna entrada maliciosa "
        "comprometa la lógica del sistema. Entre los esquemas principales destacan:\n"
        "• UserRegisterRequest: Valida nombre (min 2, max 100 caracteres), email (EmailStr normalizado), teléfono (min 7 caracteres) "
        "y contraseña (min 6 caracteres).\n"
        "• OrderCreate: Exige validación de precio estrictamente positivo ('gt=0'), IVA no negativo ('ge=0'), dirección de entrega física "
        "y valida el método de pago mediante expresión regular estricta contra la lista permitida ('^(PSE|Tarjeta|Transferencia|Crédito|WhatsApp)$').\n"
        "• CounterReportCreate: Restringe las lecturas de contadores mecánicos Ricoh a números enteros mayores o iguales a cero ('ge=0'), "
        "evitando valores negativos o inconsistencias de facturación."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ESPECIFICACIÓN Y CATÁLOGO COMPLETO DE ENDPOINTS (29 APIS)
    # -------------------------------------------------------------
    doc.add_heading("4. Especificación y Catálogo Completo de Endpoints (29 APIs)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "A continuación se presenta el catálogo técnico exhaustivo de los 29 endpoints reales que componen la API REST "
        "de Fotocopiadoras SyP bajo la ruta base '/api/v1', documentando método HTTP, ruta, autenticación requerida, "
        "parámetros de entrada, respuesta y códigos de estado estándar:"
    )

    endpoints_data = [
        # (Modulo, Metodo, Ruta, Descripcion, Auth, Request/Params, Response Model, Status Codes)
        ("1. Health", "GET", "/api/v1/health", "Diagnóstico de salud del backend, modo de entorno y estadísticas de la base de datos.", "Pública", "Ninguno", "{status: 'ok', environment: str, stats: dict}", "200"),
        ("2. Auth", "POST", "/api/v1/auth/register", "Registro de nuevos clientes comerciales con hashing Bcrypt automático.", "Pública (Rate Limit)", "UserRegisterRequest (JSON)", "AuthTokenResponse (Token + User)", "201, 400, 429"),
        ("2. Auth", "POST", "/api/v1/auth/login", "Autenticación de clientes y administradores; emisión de token Bearer JWT.", "Pública (Rate Limit)", "UserLoginRequest (JSON)", "AuthTokenResponse (Token + User)", "200, 401, 429"),
        ("2. Auth", "GET", "/api/v1/auth/me", "Consulta del perfil y privilegios del usuario autenticado en la sesión actual.", "Bearer JWT (Cliente/Admin)", "Cabecera Authorization", "UserResponse (Datos de perfil)", "200, 401"),
        ("3. Catálogo", "GET", "/api/v1/products", "Catálogo público de productos con filtros por categoría, búsqueda, precio y orden.", "Pública", "Query: category, search, min/max_price, sort", "List[ProductResponse]", "200"),
        ("3. Catálogo", "GET", "/api/v1/products/{id}", "Ficha técnica detallada, especificaciones Ricoh y stock de un producto.", "Pública", "Path: product_id (SKU)", "ProductResponse", "200, 404"),
        ("3. Catálogo", "POST", "/api/v1/products", "Creación de un nuevo producto, repuesto o consumible en el catálogo.", "Requiere Admin", "ProductCreate (JSON)", "ProductResponse", "201, 400, 401, 403"),
        ("3. Catálogo", "PUT", "/api/v1/products/{id}", "Actualización integral de precios, stock, especificaciones y ficha técnica.", "Requiere Admin", "Path: product_id, Body: ProductBase", "ProductResponse", "200, 401, 403, 404"),
        ("4. Soporte", "POST", "/api/v1/requests", "Radicación de solicitud de mantenimiento técnico preventivo o correctivo.", "Pública / Opcional JWT", "MaintenanceRequestCreate (JSON)", "MaintenanceRequestResponse", "201, 400"),
        ("4. Soporte", "GET", "/api/v1/requests/my", "Historial de solicitudes de servicio técnico del cliente autenticado.", "Bearer JWT (Cliente)", "Cabecera Authorization", "List[MaintenanceRequestResponse]", "200, 401"),
        ("4. Soporte", "GET", "/api/v1/requests", "Bandeja administrativa de todas las órdenes de servicio técnico registradas.", "Requiere Admin", "Query: status (opcional)", "List[MaintenanceRequestResponse]", "200, 401, 403"),
        ("4. Soporte", "PATCH", "/api/v1/requests/{id}/status", "Actualización del estado técnico (Confirmada, Completada) y notas de bitácora.", "Requiere Admin", "Path: request_id, Body: MaintenanceStatusUpdate", "{status: 'ok', request: dict}", "200, 400, 401, 403"),
        ("5. Cotización", "POST", "/api/v1/contact", "Recepción de mensajes del formulario de contacto general y PQRs.", "Pública (Rate Limit)", "ContactMessageCreate (JSON)", "{status: 'ok', message_id: str}", "201, 400, 429"),
        ("5. Cotización", "POST", "/api/v1/quotes", "Generación y almacenamiento de cotización formal con IVA del 19%.", "Pública / Opcional JWT", "QuoteCreate (JSON)", "{status: 'ok', quote: QuoteResponse}", "201, 400, 429"),
        ("5. Cotización", "GET", "/api/v1/quotes/{code}", "Consulta y recuperación de cotización formal mediante código COT-XXXXXX.", "Pública / Opcional JWT", "Path: quote_code", "QuoteResponse", "200, 404"),
        ("5. Cotización", "GET", "/api/v1/quotes", "Bandeja de auditoría de todas las cotizaciones emitidas por la empresa.", "Requiere Admin", "Ninguno", "List[QuoteResponse]", "200, 401, 403"),
        ("6. Pedidos", "POST", "/api/v1/orders", "Creación y confirmación de orden de compra / checkout en el e-commerce.", "Pública / Opcional JWT", "OrderCreate (JSON)", "{status: 'ok', order_code: str, ...}", "201, 400"),
        ("6. Pedidos", "GET", "/api/v1/orders/{code}", "Consulta pública del estado de un pedido mediante código PED-XXXXXX.", "Pública", "Path: order_code", "OrderResponse", "200, 404"),
        ("6. Pedidos", "GET", "/api/v1/orders/user/my", "Historial de compras y pedidos registrados del usuario autenticado.", "Bearer JWT (Cliente)", "Cabecera Authorization", "List[OrderResponse]", "200, 401"),
        ("6. Pedidos", "GET", "/api/v1/orders", "Listado y control de todos los pedidos y transacciones para despacho.", "Requiere Admin", "Query: payment_status, shipping_status", "List[OrderResponse]", "200, 401, 403"),
        ("6. Pedidos", "PATCH", "/api/v1/orders/{id}/status", "Actualización administrativa del estado de pago y guía de despacho logístico.", "Requiere Admin", "Path: order_id, Body: OrderStatusUpdate", "{status: 'ok', order: dict}", "200, 400, 401, 403"),
        ("7. Renting", "POST", "/api/v1/counters", "Envío del reporte mensual de contadores de fotocopiado (mono y color).", "Bearer JWT (Cliente)", "CounterReportCreate (JSON)", "{status: 'ok', counter_id: str}", "201, 400, 401"),
        ("7. Renting", "GET", "/api/v1/counters", "Auditoría de lecturas de contadores reportadas por clientes en renting.", "Requiere Admin", "Query: month (opcional)", "List[dict]", "200, 401, 403"),
        ("8. Notificaciones", "GET", "/api/v1/notifications/my", "Bandeja de notificaciones en vivo del usuario autenticado.", "Bearer JWT (Cliente/Admin)", "Query: unread_only (bool)", "List[NotificationResponse]", "200, 401"),
        ("8. Notificaciones", "PATCH", "/api/v1/notifications/{id}/read", "Marca una notificación específica como leída.", "Bearer JWT (Cliente/Admin)", "Path: notif_id", "{status: 'ok', is_read: True}", "200, 401, 404"),
        ("8. Notificaciones", "POST", "/api/v1/notifications/mark-all-read", "Marca todas las notificaciones pendientes del usuario como leídas.", "Bearer JWT (Cliente/Admin)", "Ninguno", "{status: 'ok', updated_count: int}", "200, 401"),
        ("8. Notificaciones", "POST", "/api/v1/notifications", "Emisión manual de avisos o notificaciones desde el panel administrativo.", "Requiere Admin", "NotificationCreate (JSON)", "NotificationResponse", "201, 400, 401, 403"),
        ("9. Analítica", "GET", "/api/v1/admin/analytics", "Métricas financieras en COP, distribución de estados y modelos más solicitados.", "Requiere Admin", "Ninguno", "AnalyticsOverviewResponse", "200, 401, 403"),
        ("9. Analítica", "GET", "/api/v1/admin/export/{dataset}", "Descarga de dataset histórico en archivo CSV (orders, products, requests).", "Requiere Admin", "Path: dataset ('orders'|'products'|'requests')", "Archivo CSV con cabeceras text/csv", "200, 400, 401, 403")
    ]

    t_api = doc.add_table(rows=len(endpoints_data) + 1, cols=7)
    t_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    api_hdrs = ["Módulo", "Método", "Ruta del Endpoint", "Descripción Técnica", "Seguridad / Auth", "Esquema / Payload", "HTTP"]
    for c_idx, ch in enumerate(api_hdrs):
        t_api.rows[0].cells[c_idx].paragraphs[0].add_run(ch)
    format_row(t_api.rows[0], bg_color="0F4C81", is_header=True)

    widths = [Inches(0.9), Inches(0.6), Inches(1.5), Inches(1.6), Inches(1.0), Inches(1.3), Inches(0.5)]
    for r_idx, ep in enumerate(endpoints_data):
        row = t_api.rows[r_idx + 1]
        mod, meth, route, desc, auth, req_pay, resp_pay, st = ep
        payload_summary = f"Req: {req_pay}\nResp: {resp_pay}"
        vals = [mod, meth, route, desc, auth, payload_summary, st]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            cell.width = widths[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            if c_idx == 1:
                r.bold = True
                if val == "GET": r.font.color.rgb = RGBColor(5, 150, 105)
                elif val == "POST": r.font.color.rgb = RGBColor(37, 99, 235)
                elif val == "PUT": r.font.color.rgb = RGBColor(217, 119, 6)
                elif val == "PATCH": r.font.color.rgb = RGBColor(124, 58, 237)
        format_row(row, bg_color="FFFFFF" if r_idx % 2 == 0 else "F8FAFC")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. CAPA DE SEGURIDAD, DIRECTIVAS OWASP Y AUDITORÍA STRIX
    # -------------------------------------------------------------
    doc.add_heading("5. Capa de Seguridad, Directivas OWASP y Auditoría Strix", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("5.1 Flujo Criptográfico y Gestión de Tokens JWT (HS256)\n")
    r.bold = True
    p.add_run(
        "El subsistema de autenticación de Fotocopiadoras SyP implementa tokens JSON Web Token (RFC 7519) utilizando el algoritmo simétrico "
        "HMAC con SHA-256 (HS256). La firma criptográfica garantiza que el payload no pueda ser alterado en el cliente sin invalidar el token.\n\n"
        "Estructura del Payload JWT generado en 'security.py':\n"
        "• sub: Dirección de correo electrónico del usuario autenticado.\n"
        "• id: Identificador único del usuario ('id' en tabla 'users').\n"
        "• role: Rol de autorización ('cliente' o 'admin').\n"
        "• iat: Timestamp UTC de emisión del token (Issued At).\n"
        "• exp: Timestamp UTC de expiración obligatoria (calculado según 'ACCESS_TOKEN_EXPIRE_MINUTES', 60 minutos por defecto).\n\n"
        "Gestión de Alta Entropía de la Clave Secreta:\n"
        "Para subsanar vulnerabilidades de claves predeterminadas, el servidor evalúa la variable de entorno 'SYP_JWT_SECRET'. "
        "Si no está fijada en desarrollo, genera una clave criptográfica de 64 caracteres de alta entropía mediante 'secrets.token_urlsafe(64)' "
        "y la persiste en un archivo protegido local ('.jwt_secret'). En entornos de producción ('ENVIRONMENT=production'), el sistema rechaza "
        "arrancar si la clave de entorno no está explícitamente configurada, impidiendo despliegues vulnerables."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.2 Hashing de Contraseñas con Bcrypt (12 Rondas)\n")
    r.bold = True
    p.add_run(
        "Ninguna contraseña se almacena jamás en texto plano. En el registro o actualización, el backend invoca:\n"
        "```python\n"
        "def hash_password(password: str) -> str:\n"
        "    salt = bcrypt.gensalt(rounds=12)\n"
        "    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')\n"
        "```\n"
        "El costo computacional de 12 rondas de salting proporciona una barrera robusta contra ataques de diccionario y ataques "
        "con tablas Rainbow o hardware especializado (ASIC/GPU), asegurando total conformidad con el estándar OWASP ASVS v4.0."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.3 Control de Acceso Basado en Roles (RBAC)\n")
    r.bold = True
    p.add_run(
        "El control de privilegios se valida en cada llamada a la API mediante dos niveles de inspección:\n"
        "1. get_current_user: Inspecciona la cabecera 'Authorization: Bearer', decodifica el JWT, comprueba la validez temporal "
        "y consulta la tabla 'users' para verificar que el usuario exista y mantenga su estado activo ('is_active = 1').\n"
        "2. require_admin: Verifica explícitamente que 'current_user.get('role') == 'admin''. De no ser así, emite 'HTTP 403 Forbidden', "
        "protegiendo las rutas de administración, inventario, analítica financiera y exportación CSV."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.4 Política de Orígenes Cruzados (CORS) y Restricción de Cabeceras\n")
    r.bold = True
    p.add_run(
        "Para corregir configuraciones inseguras de CORS que anteriormente permitían cualquier origen con credenciales activas, "
        "el middleware en 'main.py' implementa una lista blanca controlada:\n"
        "• Orígenes Permitidos: 'http://localhost:5500', 'http://127.0.0.1:5500', 'http://localhost:8000', 'http://127.0.0.1:8000' "
        "y los dominios definidos en la variable de entorno 'ALLOWED_ORIGINS' (ej. dominio oficial de producción en Vercel).\n"
        "• Cabeceras de Seguridad Perimetral: Servidas tanto por el servidor local ('serve_frontend.py') como por Nginx/Vercel:\n"
        "  - X-Content-Type-Options: nosniff (previene ataques de confusión de tipos MIME).\n"
        "  - X-Frame-Options: SAMEORIGIN (mitiga ataques de Clickjacking).\n"
        "  - X-XSS-Protection: 1; mode=block (activa filtros anti-XSS del navegador)."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.5 Mecanismo de Rate Limiting en Memoria\n")
    r.bold = True
    p.add_run(
        "Para blindar la plataforma contra ataques de denegación de servicio (DoS) y fuerza bruta en contraseñas, se implementó "
        "la clase 'InMemoryRateLimiter' protegida mediante hilos ('threading.Lock'):\n"
        "• Login: Límite estricto de 5 intentos por minuto por dirección IP.\n"
        "• Registro de Cuentas: Límite de 3 registros por hora por IP.\n"
        "• Guardado de Cotizaciones: Límite de 10 cotizaciones por minuto por IP.\n"
        "• Formulario de Contacto: Límite de 5 envíos por minuto por IP.\n"
        "Al superarse el umbral permitido, la API responde inmediatamente con código 'HTTP 429 Too Many Requests'."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.6 Matriz de Remediación de Vulnerabilidades Strix (VULN-01 a VULN-08)\n")
    r.bold = True
    p.add_run(
        "La siguiente matriz sintetiza los hallazgos identificados durante la auditoría de seguridad automatizada bajo el framework "
        "Strix y el estado de mitigación definitivo verificado en el código fuente actual:"
    )

    t_strix = doc.add_table(rows=9, cols=5)
    t_strix.alignment = WD_TABLE_ALIGNMENT.CENTER
    strix_headers = ["ID", "Vulnerabilidad Auditada", "Severidad", "Causa Raíz Identificada", "Remediación Implementada en Código"]
    for c_idx, h in enumerate(strix_headers):
        t_strix.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_strix.rows[0], bg_color="0F4C81", is_header=True)

    strix_data = [
        ("VULN-01", "Exposición de Base de Datos en Web Root", "Crítica", "Carpetas de backend y base de datos 'syp.db' ubicadas dentro de la carpeta estática.", "Filtros en 'serve_frontend.py' y Nginx bloqueando descargas de .db, .py, .env y .git con HTTP 403."),
        ("VULN-02", "Secreto JWT Hardcodeado", "Crítica", "Clave por defecto conocida en código fuente permitía falsificación de tokens admin.", "Generación dinámica con 'secrets.token_urlsafe(64)' y bloqueo de arranque en producción sin clave de entorno."),
        ("VULN-03", "Fuga PII e IDOR en Órdenes", "Alta", "Consulta de órdenes permitía ver datos de clientes arbitrarios mediante ID.", "Aislamiento de historial con 'client_id' obligatorio y consulta pública restringida solo por código alfanumérico."),
        ("VULN-04", "Manipulación de Precios en Checkout", "Alta", "El backend aceptaba subtotales y estados enviados por el cliente.", "Recálculo estricto de precios e impuestos en backend y forzado de estado inicial a 'Pendiente'."),
        ("VULN-05", "Credenciales en Código Cliente", "Alta", "Contraseñas admin de prueba presentes en scripts JS.", "Eliminación total de credenciales en cliente; autenticación delegada al endpoint /api/v1/auth/login."),
        ("VULN-06", "CORS Inseguro (Wildcard)", "Media", "CORS configurado con allow_origins=['*'] con allow_credentials=True.", "Restricción a dominios específicos mediante lista blanca parametrizada en 'ALLOWED_ORIGINS'."),
        ("VULN-07", "Ausencia de Rate Limiting", "Media", "Endpoints de login y contacto vulnerables a ataques de fuerza bruta masiva.", "Implementación de 'InMemoryRateLimiter' con ventana de tiempo y bloqueo con HTTP 429."),
        ("VULN-08", "Exposición de Swagger en Producción", "Media", "Documentación interactiva OpenAPI accesible públicamente en producción.", "Condicional en FastAPI: 'docs_url=None' si 'ENVIRONMENT=production', activo solo en desarrollo.")
    ]
    for idx, (c1, c2, c3, c4, c5) in enumerate(strix_data):
        row = t_strix.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        row.cells[3].paragraphs[0].add_run(c4)
        row.cells[4].paragraphs[0].add_run(c5)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. CONTROL DE APROBACIÓN Y FIRMAS
    # -------------------------------------------------------------
    doc.add_heading("6. Control de Aprobación y Firmas de Conformidad", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Las firmas a continuación certifican que la arquitectura técnica, catálogo de APIs, mecanismos de seguridad "
        "y componentes aquí especificados corresponden fielmente al sistema implementado y puesto a disposición para la entrega formal:"
    )

    t_sig = doc.add_table(rows=3, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig_headers = ["Cliente / Representante Legal", "Líder de Arquitectura & Desarrollo", "Instructor / Evaluador Técnico"]
    for c_idx, h in enumerate(t_sig_headers):
        t_sig.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_sig.rows[0], bg_color="0F4C81", is_header=True)

    sig_content = [
        ("Sra. Gladys Solano Murcia\nRepresentante Legal\nFotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Kevin Portela [POR CONFIRMAR]\nLíder de Arquitectura de Software\nProyecto Fotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Instructor Evaluador [POR CONFIRMAR]\nEvaluador Etapa Productiva / Académica\nCentro de Formación Técnica\n\nFirma: _________________________\nFecha: _____ / _____ / 2026"),
        ("Conformidad Funcional y de Negocio", "Conformidad Arquitectural y de Seguridad", "Aprobación y Validación Técnica")
    ]
    for r_idx, r_data in enumerate(sig_content):
        row = t_sig.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx == 0 else "F8FAFC")

    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] Technical Architecture Manual generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_tech_manual_document()
