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
OUTPUT_DOCX = os.path.join(DOCS_DIR, "05_Manual_de_Instalacion_y_Despliegue.docx")
DIAGRAM_PATH = os.path.join(DOCS_DIR, "deployment_diagram.png")

def generate_deploy_diagram():
    """Generates a high-resolution Deployment Topology Diagram using Pillow."""
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
    draw.text((30, 20), "TOPOLOGÍA DE DESPLIEGUE EN PRODUCCIÓN & DEV - FOTOCOPIADORAS SyP", fill="#FFFFFF", font=font_title)

    # Helper function for container boxes
    def draw_node(x, y, w, h, title, subtitle, items, bg_color="#FFFFFF", border_color="#0F4C81", header_color="#0F4C81"):
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

    # 1. CLIENT NODE (Mobile / Desktop Browsers)
    client_items = [
        "Navegador Chrome, Firefox, Safari, Edge",
        "Dispositivo Móvil (Android / iOS) / Desktop",
        "PWA Cache Storage & IndexedDB",
        "Almacenamiento Local (JWT & Carrito SyP)",
        "Service Worker (sw.js - Control de Conexión)",
        "Peticiones HTTPS seguras hacia CDN y VPS"
    ]
    draw_node(40, 100, 360, 230, "1. NODO CLIENTE (USUARIOS)", "Dispositivos Móviles, Tablets & PCs", client_items, border_color="#2563EB", header_color="#1E40AF")

    # 2. FRONTEND PRODUCTION CLOUD (Vercel Edge Network)
    vercel_items = [
        "Vercel Global Edge Network (CDN Global)",
        "Hosting de Archivos Estáticos (syp-web/)",
        "vercel.json (cleanUrls: true)",
        "Cabeceras: X-Content-Type, X-Frame, X-XSS",
        "Certificado SSL Automático (Let's Encrypt TLS 1.3)",
        "Redirección y Rutas Limpias sin extensión .html"
    ]
    draw_node(480, 100, 390, 230, "2. NODO FRONTEND (VERCEL CDN)", "Producción Cloud - Entrega de Contenido", vercel_items, border_color="#0D9488", header_color="#0F766E")

    # 3. BACKEND VPS SERVER (Ubuntu Linux 22.04 / 24.04 LTS)
    vps_items = [
        "Servidor Virtual Dedicado / VPS (Ubuntu Server)",
        "Reverse Proxy Nginx (Puerto 80 / 443)",
        "Certbot SSL Let's Encrypt (HTTPS Automático)",
        "Servicio Systemd (syp-backend.service)",
        "Uvicorn Worker ASGI (127.0.0.1:8000)",
        "Python 3.12 Virtual Environment (venv)",
        "Base de Datos SQLite WAL (syp.db)",
        "Firewall UFW (Puertos 22, 80, 443 abiertos)"
    ]
    draw_node(930, 100, 380, 270, "3. NODO BACKEND (VPS LINUX)", "Servidor de Aplicación & Base de Datos", vps_items, border_color="#DC2626", header_color="#B91C1C")

    # 4. LOCAL DEVELOPMENT ENVIRONMENT (Windows 11 / PowerShell)
    dev_items = [
        "Entorno Local de Pruebas & Desarrollo",
        "Windows 11 + PowerShell 5.1 / 7+",
        "iniciar_servidores.ps1 (Orquestador dual)",
        "servidor.ps1 / serve_frontend.py (Puerto 5500)",
        "Bloqueo de Archivos Sensibles (.db, .py, .env)",
        "FastAPI Uvicorn Reload (http://127.0.0.1:8000)",
        "Entorno Virtual Local venv (Python 3.12.10)",
        "Documentación Interactiva (/docs y /redoc)"
    ]
    draw_node(40, 420, 600, 270, "4. ENTORNO DE DESARROLLO LOCAL (DEV)", "Windows PowerShell + Uvicorn Local Dual", dev_items, border_color="#D97706", header_color="#B45309")

    # 5. BACKUP & RECOVERY STORAGE
    backup_items = [
        "Directorio Local Protegido /backups/",
        "Snapshots Diarios con sqlite3_backup API",
        "Respaldo Atómico de syp.db y .jwt_secret",
        "Rotación Automática de Backups (30 días)",
        "Copia Externa Fuera de Sitio (Off-site GDrive/S3)",
        "Plan de Recuperación RPO < 24h, RTO < 30min"
    ]
    draw_node(710, 420, 600, 270, "5. SUBSISTEMA DE RESPALDO (BACKUP)", "Políticas de Retención y Recuperación", backup_items, border_color="#059669", header_color="#047857")

    # 6. EXTERNAL FLOW BANNER
    draw.rounded_rectangle([40, 730, 1270, 860], radius=10, outline="#64748B", width=2, fill="#FFFFFF")
    draw.rounded_rectangle([40, 730, 1270, 770], radius=10, outline="#475569", width=1, fill="#475569")
    draw.rectangle([40, 755, 1270, 770], fill="#475569")
    draw.text((60, 740), "6. FLUJO DE INTEGRACIÓN CONTINUA, SEGURIDAD PERIMETRAL Y TRÁFICO", fill="#FFFFFF", font=font_box_title)

    flow_boxes = [
        (60, 785, 270, 65, "Git Push -> Vercel Deploy", "Pipeline Frontend", "Actualización automática del frontend con cada push a la rama main de GitHub."),
        (370, 785, 270, 65, "CORS Whitelist", "Protección de API", "El VPS solo acepta peticiones procedentes del dominio de Vercel y localhost."),
        (680, 785, 270, 65, "Nginx Security Rules", "Bloqueo de Exploits", "Bloqueo perimetral a descargas de código fuente .py y base de datos SQLite."),
        (990, 785, 270, 65, "Systemd Watchdog", "Alta Disponibilidad", "Reinicio automático del backend FastAPI ante fallos imprevistos del proceso.")
    ]
    for bx, by, bw, bh, btit, bsub, bdesc in flow_boxes:
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6, outline="#CBD5E1", width=1, fill="#F8FAFC")
        draw.text((bx + 10, by + 6), btit, fill="#0F172A", font=font_badge)
        draw.text((bx + 10, by + 22), bsub, fill="#64748B", font=font_badge)
        draw.text((bx + 10, by + 40), bdesc[:45] + "...", fill="#334155", font=font_item)

    # Connections
    # Client -> Vercel
    draw.line([(400, 215), (480, 215)], fill="#2563EB", width=2)
    draw.polygon([(475, 210), (475, 220), (482, 215)], fill="#2563EB")
    draw.text((410, 195), "GET HTML", fill="#1E40AF", font=font_badge)

    # Client -> VPS
    draw.line([(220, 100), (220, 80), (1120, 80), (1120, 100)], fill="#DC2626", width=2)
    draw.polygon([(1115, 95), (1125, 95), (1120, 102)], fill="#DC2626")
    draw.text((640, 65), "HTTPS /api/v1/ (Bearer JWT)", fill="#B91C1C", font=font_badge)

    # VPS -> Backup
    draw.line([(1120, 370), (1120, 420)], fill="#059669", width=2)
    draw.polygon([(1115, 415), (1125, 415), (1120, 422)], fill="#059669")
    draw.text((1130, 390), "sqlite3_backup", fill="#047857", font=font_badge)

    img.save(DIAGRAM_PATH, "PNG", dpi=(300, 300))
    print(f"[OK] Deployment Diagram generated at: {DIAGRAM_PATH}")

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
    hrun = hp.add_run("FOTOCOPIADORAS SyP | MANUAL DE INSTALACIÓN Y DESPLIEGUE")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    frun1 = fp.add_run("Confidencial - Entrega de Proyecto & Sustentación Técnica | Guía de Operaciones v2.0")
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

def build_deployment_document():
    generate_deploy_diagram()
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
    r_pre = p_pre.add_run("GUÍA DE OPERACIONES, INFRAESTRUCTURA Y DEVOPS")
    r_pre.font.name = "Calibri"
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = SLATE
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(15)
    r_title = p_title.add_run("MANUAL DE INSTALACIÓN, CONFIGURACIÓN Y DESPLIEGUE\nPLATAFORMA E-COMMERCE Y SERVICIO TÉCNICO")
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
    r_norm = p_norm.add_run("Entornos Cubiertos: Desarrollo Local (PowerShell) & Producción (Vercel CDN + Linux VPS)\nServidor ASGI: FastAPI / Uvicorn | Reverse Proxy: Nginx con SSL Let's Encrypt\nSeguridad en Despliegue: Hardening Perimetral, CORS Estricto y Backups en Caliente")
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
        ("Líder de Despliegue & DevOps:", "Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\nIngeniería de Software & Infraestructura"),
        ("Versión y Entorno de Despliegue:", "Versión 2.0 (Producción) | Vercel (Frontend) + VPS Linux (API)")
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
        ("1.0", "06/10/2026", "Equipo Desarrollo SyP", "Instrucciones iniciales de ejecución local mediante scripts PowerShell de prueba.", "Superado"),
        ("2.0", "04/11/2026", "Ingeniero de Software Senior", "Manual completo de puesta en marcha: entorno local dual PowerShell, despliegue desacoplado en producción (Vercel + VPS Linux Nginx), Systemd, SSL y hardening de seguridad.", "Aprobado")
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
        "1. REQUISITOS PREVIOS DEL SISTEMA",
        "   1.1 Matriz de Hardware Mínimo y Recomendado (Local y Servidor)",
        "   1.2 Software Base y Versiones Oficiales Requeridas",
        "   1.3 Dependencias de Red y Puertos de Comunicación",
        "2. TOPOLOGÍA DE DESPLIEGUE EN PRODUCCIÓN Y DESARROLLO",
        "   2.1 Diagrama de Arquitectura de Despliegue",
        "   2.2 Componentes de la Infraestructura en la Nube",
        "3. GUÍA DE INSTALACIÓN Y EJECUCIÓN EN ENTORNO LOCAL (DEV)",
        "   3.1 Clonación del Repositorio de Código Fuente",
        "   3.2 Preparación del Entorno Virtual Python 3.12",
        "   3.3 Instalación de Dependencias (requirements.txt)",
        "   3.4 Configuración de Variables de Entorno (.env)",
        "   3.5 Análisis y Ejecución de Scripts PowerShell (iniciar_servidores.ps1)",
        "   3.6 Servidor Estático Seguro (servidor.ps1 / serve_frontend.py)",
        "4. GUÍA DE DESPLIEGUE EN PRODUCCIÓN (FRONTEND EN VERCEL)",
        "   4.1 Configuración de vercel.json (Cabeceras y Rutas Limpias)",
        "   4.2 Despliegue Mediante Vercel CLI y GitHub Continuous Deployment",
        "   4.3 Enlace con Dominio Comercial y Configuración DNS",
        "5. GUÍA DE DESPLIEGUE EN PRODUCCIÓN (BACKEND EN VPS LINUX)",
        "   5.1 Aprovisionamiento del Sistema Operativo (Ubuntu Server LTS)",
        "   5.2 Configuración del Servicio Systemd (syp-backend.service)",
        "   5.3 Configuración de Proxy Inverso Nginx y Hardening (nginx_security.conf)",
        "   5.4 Instalación de Certificado SSL Gratuito con Let's Encrypt (Certbot)",
        "   5.5 Configuración de Firewall Perimetral (UFW)",
        "6. POLÍTICA DE SEGURIDAD Y CONFIGURACIÓN DE CORS",
        "7. VERIFICACIÓN POST-DESPLIEGUE Y SOLUCIÓN DE PROBLEMAS (TROUBLESHOOTING)",
        "   7.1 Batería de Pruebas de Humo (Smoke Testing) con /health",
        "   7.2 Inspección de Registros y Logs en Tiempo Real",
        "   7.3 Matriz de Solución de Errores Comunes",
        "8. CONTROL DE APROBACIÓN Y FIRMAS DE CONFORMIDAD"
    ]
    for item in toc_items:
        r = toc_p.add_run(item + "\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. REQUISITOS PREVIOS DEL SISTEMA
    # -------------------------------------------------------------
    doc.add_heading("1. Requisitos Previos del Sistema", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("1.1 Matriz de Hardware Mínimo y Recomendado (Local y Servidor)\n")
    r.bold = True
    p.add_run(
        "Para garantizar una ejecución fluida tanto en estaciones de trabajo de desarrollo como en servidores virtuales de producción (VPS), "
        "se especifican los siguientes requerimientos de hardware:"
    )

    t_hw = doc.add_table(rows=5, cols=4)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    hw_headers = ["Componente Hardware", "Entorno Local (Mínimo)", "Servidor VPS (Mínimo Producción)", "Servidor VPS (Recomendado)"]
    for c_idx, h in enumerate(hw_headers):
        t_hw.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_hw.rows[0], bg_color="0F4C81", is_header=True)

    hw_data = [
        ("Procesador (CPU)", "2 Núcleos x86_64 @ 2.0 GHz", "1 vCPU @ 2.0 GHz (KVM/Virtual)", "2 vCPU @ 2.4 GHz o superior"),
        ("Memoria RAM", "4 GB RAM física", "1 GB RAM (con 1 GB Swap)", "2 GB RAM DDR4 / DDR5"),
        ("Almacenamiento (Disco)", "2 GB de espacio libre (HDD/SSD)", "15 GB SSD / NVMe", "25 GB SSD NVMe de alta velocidad"),
        ("Conectividad de Red", "Conexión a internet banda ancha", "100 Mbps simétricos (IP pública fija)", "1 Gbps simétrico con protección DDoS")
    ]
    for idx, (c1, c2, c3, c4) in enumerate(hw_data):
        row = t_hw.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        row.cells[3].paragraphs[0].add_run(c4)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("1.2 Software Base y Versiones Oficiales Requeridas\n")
    r.bold = True
    p.add_run(
        "• Intérprete Python: Versión oficial Python 3.12.x (64 bits). Debe incluir 'pip' y el módulo estándar 'venv'.\n"
        "• Sistema Operativo Local: Windows 10/11 (con PowerShell 5.1 o PowerShell 7+) o macOS / Linux con shell Bash.\n"
        "• Sistema Operativo Servidor: Ubuntu Server 22.04 LTS o Ubuntu Server 24.04 LTS (recomendado).\n"
        "• Servidor Web / Proxy: Nginx versión 1.18.0 o superior.\n"
        "• Gestor de Certificados: Certbot con plugin python3-certbot-nginx.\n"
        "• Navegadores de Prueba: Google Chrome 120+, Mozilla Firefox 120+, Apple Safari 16+, Microsoft Edge 120+."
    )

    p = doc.add_paragraph()
    r = p.add_run("1.3 Dependencias de Red y Puertos de Comunicación\n")
    r.bold = True
    p.add_run(
        "• Puerto 80 (HTTP): Entrada pública web para redirección obligatoria a HTTPS en Nginx.\n"
        "• Puerto 443 (HTTPS): Entrada pública cifrada TLS para la entrega de la API REST.\n"
        "• Puerto 8000: Puerto interno de escucha del servidor ASGI Uvicorn (restringido a 127.0.0.1, nunca expuesto a internet).\n"
        "• Puerto 5500: Puerto local de desarrollo para el servidor estático del frontend.\n"
        "• Puerto 22 (SSH): Gestión remota de la consola del servidor (restringida mediante clave pública RSA/ED25519)."
    )

    # -------------------------------------------------------------
    # 2. TOPOLOGÍA DE DESPLIEGUE EN PRODUCCIÓN Y DESARROLLO
    # -------------------------------------------------------------
    doc.add_heading("2. Topología de Despliegue en Producción y Desarrollo", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("2.1 Diagrama de Arquitectura de Despliegue\n")
    r.bold = True
    p.add_run(
        "A continuación se presenta la topología física y lógica de la infraestructura de Fotocopiadoras SyP, "
        "ilustrando los nodos de cliente, la red de entrega Vercel CDN, el servidor VPS Linux con Nginx y SQLite WAL, "
        "y el entorno local de desarrollo orquestado por PowerShell:"
    )

    if os.path.exists(DIAGRAM_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(DIAGRAM_PATH, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Topología de Infraestructura de Despliegue - Fotocopiadoras SyP.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. GUÍA DE INSTALACIÓN Y EJECUCIÓN EN ENTORNO LOCAL (DEV)
    # -------------------------------------------------------------
    doc.add_heading("3. Guía de Instalación y Ejecución en Entorno Local (DEV)", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("3.1 Clonación del Repositorio de Código Fuente\n")
    r.bold = True
    p.add_run(
        "Abrir una terminal de PowerShell y clonar el repositorio del proyecto en la estación de trabajo:\n"
        "```powershell\n"
        "cd \"C:\\Users\\<TuUsuario>\\Proyectos\"\n"
        "git clone https://github.com/Kevin81A/Fotocopiadora-S-P.git SYP\n"
        "cd SYP\n"
        "```"
    )

    p = doc.add_paragraph()
    r = p.add_run("3.2 Preparación del Entorno Virtual Python 3.12\n")
    r.bold = True
    p.add_run(
        "Es obligatorio crear un entorno virtual aislado para evitar colisiones de paquetes con el sistema operativo:\n"
        "```powershell\n"
        "# 1. Ubicarse en el directorio del backend\n"
        "cd .\\syp-backend\n\n"
        "# 2. Crear el entorno virtual con Python 3.12\n"
        "python -m venv venv\n\n"
        "# 3. Activar el entorno virtual en PowerShell\n"
        ".\\venv\\Scripts\\Activate.ps1\n"
        "```\n"
        "Nota: Si PowerShell arroja error de directivas de ejecución de scripts, ejecutar una única vez:\n"
        "'Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser'."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.3 Instalación de Dependencias (requirements.txt)\n")
    r.bold = True
    p.add_run(
        "Con el entorno virtual activado, instalar las dependencias exactas del proyecto:\n"
        "```powershell\n"
        "pip install --upgrade pip\n"
        "pip install -r requirements.txt\n"
        "```\n"
        "Las dependencias instaladas corresponden a:\n"
        "• fastapi>=0.115.0: Framework asíncrono para la construcción de las APIs REST.\n"
        "• uvicorn>=0.30.0: Servidor ASGI de ultra alto rendimiento.\n"
        "• pydantic>=2.8.0: Validación de tipos y esquemas de datos.\n"
        "• email-validator>=2.2.0: Validación de sintaxis de correos electrónicos.\n"
        "• pyjwt>=2.9.0: Codificación y verificación criptográfica de tokens JWT.\n"
        "• bcrypt>=4.2.0: Algoritmo de salting y hashing seguro de contraseñas.\n"
        "• python-multipart>=0.0.9: Soporte para procesar formularios multipart/form-data."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.4 Configuración de Variables de Entorno (.env)\n")
    r.bold = True
    p.add_run(
        "Crear un archivo '.env' en la raíz de 'syp-backend/' o establecer las variables de sesión en PowerShell:\n"
        "```ini\n"
        "# Archivo: syp-backend/.env\n"
        "ENVIRONMENT=development\n"
        "SYP_JWT_SECRET=syp_dev_secret_key_neiva_huila_2026_ricoh_specialist_local\n"
        "ACCESS_TOKEN_EXPIRE_MINUTES=60\n"
        "ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000\n"
        "```"
    )

    p = doc.add_paragraph()
    r = p.add_run("3.5 Análisis y Ejecución de Scripts PowerShell (iniciar_servidores.ps1)\n")
    r.bold = True
    p.add_run(
        "El repositorio incluye el orquestador automático 'syp-web/iniciar_servidores.ps1' que levanta el entorno de trabajo dual "
        "con un solo comando:\n"
        "```powershell\n"
        "cd .\\syp-web\n"
        "powershell -ExecutionPolicy Bypass -File .\\iniciar_servidores.ps1\n"
        "```\n\n"
        "Explicación técnica línea por línea de lo que hace el script:\n"
        "1. 'Write-Host ...': Despliega encabezados en consola identificando el proyecto Fotocopiadoras SyP.\n"
        "2. '$backendDir = Join-Path $PSScriptRoot \"fastapi_backend\"': Resuelve dinámicamente la ruta física del backend.\n"
        "3. 'Start-Process -FilePath $pythonExe -ArgumentList \"-m uvicorn main:app --host 127.0.0.1 --port 8000 --reload\"': "
        "Inicia el backend FastAPI en segundo plano en el puerto 8000 con recarga en caliente activa ante cambios de código.\n"
        "4. 'Start-Process \"http://localhost:5500/index.html\"': Abre automáticamente el navegador predeterminado en la tienda.\n"
        "5. 'powershell -File servidor.ps1': Inicia el servidor estático seguro en el puerto 5500, manteniéndose en escucha."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.6 Servidor Estático Seguro (servidor.ps1 / serve_frontend.py)\n")
    r.bold = True
    p.add_run(
        "Para subsanar de raíz la vulnerabilidad VULN-01 (exposición de base de datos en web root), el script 'serve_frontend.py' "
        "(o su homólogo 'servidor.ps1') implementa un filtro de seguridad HTTP de doble barrera:\n"
        "• Bloqueo de Extensiones: Cualquier petición finalizada en '.db', '.sqlite', '.sqlite3', '.py', '.env', '.md', '.log' "
        "o '.key' es interceptada inmediatamente, respondiendo un error 'HTTP 403 Forbidden: Tipo de archivo restringido'.\n"
        "• Bloqueo de Directorios Protegidos: Se niega el acceso a prefijos como '/.git', '/fastapi_backend', '/backend' o '/.vscode'.\n"
        "• Inyección Automática de Cabeceras: Envía 'X-Content-Type-Options: nosniff', 'X-Frame-Options: SAMEORIGIN' "
        "y 'X-XSS-Protection: 1; mode=block' en cada respuesta."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. GUÍA DE DESPLIEGUE EN PRODUCCIÓN (FRONTEND EN VERCEL)
    # -------------------------------------------------------------
    doc.add_heading("4. Guía de Despliegue en Producción (Frontend en Vercel)", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("4.1 Configuración de vercel.json (Cabeceras y Rutas Limpias)\n")
    r.bold = True
    p.add_run(
        "El archivo 'syp-web/vercel.json' define las directivas de entrega para la red global de Vercel:\n"
        "```json\n"
        "{\n"
        "  \"version\": 2,\n"
        "  \"cleanUrls\": true,\n"
        "  \"headers\": [\n"
        "    {\n"
        "      \"source\": \"/(.*)\",\n"
        "      \"headers\": [\n"
        "        { \"key\": \"X-Content-Type-Options\", \"value\": \"nosniff\" },\n"
        "        { \"key\": \"X-Frame-Options\", \"value\": \"SAMEORIGIN\" },\n"
        "        { \"key\": \"X-XSS-Protection\", \"value\": \"1; mode=block\" }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "```\n"
        "La directiva 'cleanUrls: true' permite a los usuarios navegar hacia URLs elegantes (ej. '/productos' en lugar de '/productos.html'), "
        "optimizando el posicionamiento en buscadores (SEO) y la experiencia de usuario."
    )

    p = doc.add_paragraph()
    r = p.add_run("4.2 Despliegue Mediante Vercel CLI y GitHub Continuous Deployment\n")
    r.bold = True
    p.add_run(
        "Método 1: Despliegue Automatizado por GitHub (Recomendado):\n"
        "1. Conectar el repositorio de GitHub con el panel de control de Vercel (https://vercel.com).\n"
        "2. En la configuración del proyecto, seleccionar 'Root Directory' como 'syp-web/'.\n"
        "3. En 'Framework Preset', seleccionar 'Other' (HTML/JS Estático puro).\n"
        "4. Cada commit a la rama 'main' disparará un despliegue y validación automática en menos de 30 segundos.\n\n"
        "Método 2: Despliegue Directo por CLI:\n"
        "```bash\n"
        "npm install -g vercel\n"
        "cd syp-web/\n"
        "vercel login\n"
        "vercel --prod\n"
        "```"
    )

    p = doc.add_paragraph()
    r = p.add_run("4.3 Enlace con Dominio Comercial y Configuración DNS\n")
    r.bold = True
    p.add_run(
        "Para vincular el dominio oficial de la empresa (ej. 'sypfotocopiadoras.com'):\n"
        "1. En Vercel: Settings -> Domains -> Añadir 'sypfotocopiadoras.com' y 'www.sypfotocopiadoras.com'.\n"
        "2. En el proveedor de DNS (GoDaddy, Namecheap o Cloudflare): Configurar los registros:\n"
        "   - Tipo A | Nombre: @ | Valor: 76.76.21.21\n"
        "   - Tipo CNAME | Nombre: www | Valor: cname.vercel-dns.com."
    )

    # -------------------------------------------------------------
    p = doc.add_paragraph()
    r = p.add_run("4.4 Despliegue Oficial en Produccion en GitHub Pages (Acceso Directo)\n")
    r.bold = True
    p.add_run(
        "Como entorno de produccion en vivo y demostracion publica para el evaluador e instructor, el frontend "
        "se encuentra desplegado y activo en la infraestructura de GitHub Pages:\n"
        "\xe2\x80\xa2 URL Oficial de la Aplicacion en Produccion: https://kevin81a.github.io/Fotocopiadora-S-P/\n"
        "\xe2\x80\xa2 Repositorio Oficial del Proyecto: https://github.com/Kevin81A/Fotocopiadora-S-P\n"
        "\xe2\x80\xa2 Rama de Produccion: main\n"
        "\xe2\x80\xa2 Modo de Entrega: HTTPS con cifrado TLS 1.3 y CDN de alta disponibilidad.\n"
        "El evaluador puede acceder directamente al enlace anterior desde cualquier navegador de escritorio o movil para validar el funcionamiento integral de la tienda virtual, cotizador, buscador Ricoh SC y agendamiento tecnico.\n\n"
    )

    # 5. GUÍA DE DESPLIEGUE EN PRODUCCIÓN (BACKEND EN VPS LINUX)
    # -------------------------------------------------------------
    doc.add_heading("5. Guía de Despliegue en Producción (Backend en VPS Linux)", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("5.1 Aprovisionamiento del Sistema Operativo (Ubuntu Server LTS)\n")
    r.bold = True
    p.add_run(
        "Conectarse al servidor mediante SSH y actualizar los paquetes base:\n"
        "```bash\n"
        "sudo apt update && sudo apt upgrade -y\n"
        "sudo apt install -y python3.12 python3.12-venv python3-pip nginx certbot python3-certbot-nginx git ufw\n\n"
        "# Crear usuario de servicio sin privilegios de root para ejecutar la app\n"
        "sudo adduser --system --group --no-create-home sypapp\n"
        "sudo mkdir -p /var/www/syp-backend\n"
        "sudo chown -R sypapp:sypapp /var/www/syp-backend\n"
        "```"
    )

    p = doc.add_paragraph()
    r = p.add_run("5.2 Configuración del Servicio Systemd (syp-backend.service)\n")
    r.bold = True
    p.add_run(
        "Crear el archivo de servicio '/etc/systemd/system/syp-backend.service' para garantizar que FastAPI se ejecute "
        "como demonio en segundo plano con reinicio automático ante caídas:\n"
        "```ini\n"
        "[Unit]\n"
        "Description=FastAPI Server - Fotocopiadoras SyP API\n"
        "After=network.target\n\n"
        "[Service]\n"
        "User=sypapp\n"
        "Group=sypapp\n"
        "WorkingDirectory=/var/www/syp-backend\n"
        "Environment=\"PATH=/var/www/syp-backend/venv/bin\"\n"
        "Environment=\"ENVIRONMENT=production\"\n"
        "Environment=\"SYP_JWT_SECRET=TU_CLAVE_DE_ALTA_ENTROPIA_DE_64_CARACTERES_AQUI\"\n"
        "Environment=\"ALLOWED_ORIGINS=https://sypfotocopiadoras.com,https://www.sypfotocopiadoras.com\"\n"
        "ExecStart=/var/www/syp-backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2\n"
        "Restart=always\n"
        "RestartSec=5s\n\n"
        "[Install]\n"
        "WantedBy=multi-user.target\n"
        "```\n\n"
        "Activar y arrancar el servicio:\n"
        "```bash\n"
        "sudo systemctl daemon-reload\n"
        "sudo systemctl enable syp-backend\n"
        "sudo systemctl start syp-backend\n"
        "sudo systemctl status syp-backend\n"
        "```"
    )

    p = doc.add_paragraph()
    r = p.add_run("5.3 Configuración de Proxy Inverso Nginx y Hardening (nginx_security.conf)\n")
    r.bold = True
    p.add_run(
        "Copiar el archivo de hardening 'syp-web/nginx_security.conf' hacia '/etc/nginx/snippets/syp_security.conf'.\n"
        "Luego, configurar el virtual host en '/etc/nginx/sites-available/api.sypfotocopiadoras.com':\n"
        "```nginx\n"
        "server {\n"
        "    listen 80;\n"
        "    server_name api.sypfotocopiadoras.com;\n\n"
        "    include /etc/nginx/snippets/syp_security.conf;\n\n"
        "    location / {\n"
        "        proxy_pass http://127.0.0.1:8000;\n"
        "        proxy_http_version 1.1;\n"
        "        proxy_set_header Upgrade $http_upgrade;\n"
        "        proxy_set_header Connection 'upgrade';\n"
        "        proxy_set_header Host $host;\n"
        "        proxy_set_header X-Real-IP $remote_addr;\n"
        "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
        "        proxy_set_header X-Forwarded-Proto $scheme;\n"
        "        proxy_read_timeout 60s;\n"
        "        proxy_connect_timeout 60s;\n"
        "    }\n"
        "}\n"
        "```\n"
        "Activar el sitio: 'sudo ln -s /etc/nginx/sites-available/api.sypfotocopiadoras.com /etc/nginx/sites-enabled/' y probar con 'sudo nginx -t'."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.4 Instalación de Certificado SSL Gratuito con Let's Encrypt (Certbot)\n")
    r.bold = True
    p.add_run(
        "Ejecutar Certbot para obtener y configurar automáticamente el certificado SSL TLS 1.3:\n"
        "```bash\n"
        "sudo certbot --nginx -d api.sypfotocopiadoras.com\n"
        "```\n"
        "Seleccionar la opción de redirección obligatoria de HTTP a HTTPS. Certbot configurará un temporizador systemd para "
        "renovación automática cada 90 días sin intervención humana."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. POLÍTICA DE SEGURIDAD Y CONFIGURACIÓN DE CORS
    # -------------------------------------------------------------
    doc.add_heading("6. Política de Seguridad y Configuración de CORS", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "El intercambio de recursos de origen cruzado (CORS) es el mecanismo mediante el cual el navegador permite o rechaza que el frontend "
        "(alojado en el dominio de Vercel) consuma los endpoints de la API (alojados en el VPS). "
        "Para cumplir con el estándar OWASP y mitigar la vulnerabilidad VULN-06:\n\n"
        "1. En Desarrollo: Se admiten orígenes locales estrictos ('http://localhost:5500', 'http://127.0.0.1:5500').\n"
        "2. En Producción: Se prohíbe el uso de comodines ('*') en presencia de credenciales ('allow_credentials=True'). "
        "La lista blanca se restringe exclusivamente al dominio comercial del cliente mediante la variable:\n"
        "'ALLOWED_ORIGINS=https://sypfotocopiadoras.com,https://www.sypfotocopiadoras.com'.\n\n"
        "Cualquier petición originada desde un dominio no autorizado será bloqueada por el navegador antes de procesarse."
    )

    # -------------------------------------------------------------
    # 7. VERIFICACIÓN POST-DESPLIEGUE Y SOLUCIÓN DE PROBLEMAS
    # -------------------------------------------------------------
    doc.add_heading("7. Verificación Post-Despliegue y Solución de Problemas (Troubleshooting)", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("7.1 Batería de Pruebas de Humo (Smoke Testing) con /health\n")
    r.bold = True
    p.add_run(
        "Inmediatamente después de desplegar, ejecutar la siguiente verificación mediante cURL:\n"
        "```bash\n"
        "curl -i https://api.sypfotocopiadoras.com/api/v1/health\n"
        "```\n"
        "Respuesta esperada (HTTP 200 OK):\n"
        "```json\n"
        "{\n"
        "  \"status\": \"ok\",\n"
        "  \"environment\": \"production\",\n"
        "  \"app\": \"Fotocopiadora SyP Official REST API\",\n"
        "  \"stats\": {\n"
        "    \"products\": 11,\n"
        "    \"categories\": 6,\n"
        "    \"users\": 5,\n"
        "    \"orders\": 4,\n"
        "    \"maintenance_requests\": 8\n"
        "  }\n"
        "}\n"
        "```"
    )

    p = doc.add_paragraph()
    r = p.add_run("7.2 Inspección de Registros y Logs en Tiempo Real\n")
    r.bold = True
    p.add_run(
        "• Ver logs en vivo del backend FastAPI: 'sudo journalctl -u syp-backend -f'\n"
        "• Ver logs de acceso de Nginx: 'sudo tail -f /var/log/nginx/access.log'\n"
        "• Ver logs de errores y bloqueos de seguridad de Nginx: 'sudo tail -f /var/log/nginx/error.log'"
    )

    p = doc.add_paragraph()
    r = p.add_run("7.3 Matriz de Solución de Errores Comunes\n")
    r.bold = True
    
    t_trouble = doc.add_table(rows=6, cols=3)
    t_trouble.alignment = WD_TABLE_ALIGNMENT.CENTER
    tr_headers = ["Síntoma / Mensaje de Error", "Causa Raíz Probable", "Acción de Remediación Inmediata"]
    for c_idx, h in enumerate(tr_headers):
        t_trouble.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_trouble.rows[0], bg_color="0F4C81", is_header=True)

    tr_data = [
        ("Error: 'Address already in use' (Puerto 8000 o 5500 ocupado)", "Existe una instancia previa de Uvicorn o Python corriendo en segundo plano.", "En PowerShell: 'Get-Process python | Stop-Process -Force'. En Linux: 'sudo fuser -k 8000/tcp'."),
        ("Error de CORS: 'No Access-Control-Allow-Origin header'", "El dominio del frontend no está registrado en la variable 'ALLOWED_ORIGINS'.", "Agregar el dominio exacto en el archivo .env o en el servicio systemd y reiniciar."),
        ("HTTP 502 Bad Gateway en Nginx", "El proceso Uvicorn está detenido o falló al arrancar.", "Verificar 'sudo systemctl status syp-backend' y corregir errores sintácticos en logs."),
        ("SQLite: 'attempt to write a readonly database'", "Permisos insuficientes en el archivo syp.db o en la carpeta que lo contiene.", "Ejecutar 'sudo chown -R sypapp:sypapp /var/www/syp-backend' y verificar permisos de escritura."),
        ("HTTP 429 Too Many Requests", "Se superó el límite de peticiones de login (5/min) o registro (3/hora).", "Esperar que expire la ventana de tiempo del rate limiter o reiniciar el proceso en desarrollo.")
    ]
    for idx, (c1, c2, c3) in enumerate(tr_data):
        row = t_trouble.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. CONTROL DE APROBACIÓN Y FIRMAS
    # -------------------------------------------------------------
    doc.add_heading("8. Control de Aprobación y Firmas de Conformidad", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Las firmas a continuación certifican que los procedimientos de instalación, topología de despliegue, "
        "variables de entorno y medidas de seguridad perimetral detalladas en este manual han sido verificadas "
        "y puestas a prueba satisfactoriamente:"
    )

    t_sig = doc.add_table(rows=3, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig_headers = ["Cliente / Representante Legal", "Líder de Despliegue & DevOps", "Instructor / Evaluador Técnico"]
    for c_idx, h in enumerate(t_sig_headers):
        t_sig.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_sig.rows[0], bg_color="0F4C81", is_header=True)

    sig_content = [
        ("Sra. Gladys Solano Murcia\nRepresentante Legal\nFotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Kevin Portela [POR CONFIRMAR]\nLíder de Despliegue & DevOps\nProyecto Fotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Instructor Evaluador [POR CONFIRMAR]\nEvaluador Etapa Productiva / Académica\nCentro de Formación Técnica\n\nFirma: _________________________\nFecha: _____ / _____ / 2026"),
        ("Conformidad Operativa y Puesta en Marcha", "Conformidad de Infraestructura y Despliegue", "Aprobación y Validación Técnica")
    ]
    for r_idx, r_data in enumerate(sig_content):
        row = t_sig.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx == 0 else "F8FAFC")

    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] Deployment Manual generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_deployment_document()
