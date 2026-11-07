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
OUTPUT_DOCX = os.path.join(DOCS_DIR, "07_Acta_de_Entrega_y_Cierre.docx")
DIAGRAM_PATH = os.path.join(DOCS_DIR, "delivery_seal_diagram.png")

def generate_handover_seal():
    """Generates an Official Handover & Acceptance Certificate Graphic using Pillow."""
    width, height = 1350, 750
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
    draw.text((30, 20), "CERTIFICACIÓN DE ENTREGA FORMAL Y CIERRE DE PROYECTO - FOTOCOPIADORAS SyP", fill="#FFFFFF", font=font_title)

    # Big Verification Card (Center)
    draw.rounded_rectangle([50, 95, 1300, 710], radius=12, outline="#059669", width=3, fill="#FFFFFF")
    draw.rounded_rectangle([50, 95, 1300, 150], radius=12, outline="#059669", width=1, fill="#059669")
    draw.rectangle([50, 130, 1300, 150], fill="#059669")
    draw.text((75, 110), "ACTA DE RECIBO A SATISFACCIÓN Y CONFORMIDAD TÉCNICO-COMERCIAL", fill="#FFFFFF", font=font_box_title)

    # 3 Summary Pillars
    pillars = [
        ("1. ENTREGABLE SOFTWARE", "Código Fuente & Base de Datos", [
            "Frontend PWA Vanilla JS (syp-web/)",
            "Backend REST API FastAPI 0.115+ (syp-backend/)",
            "Base de datos relacional syp.db (SQLite WAL)",
            "9 Tablas normalizadas con datos semilla Ricoh",
            "Scripts de automatización PowerShell y Python"
        ], "#2563EB", "#1E40AF"),
        ("2. ENTREGABLE DOCUMENTAL", "Paquete Técnico en Docs/", [
            "01_SRS_Fotocopiadoras_SyP.docx (IEEE 830)",
            "02_Manual_de_Usuario_SyP.docx (Cliente & Admin)",
            "03_Manual_Tecnico_y_Arquitectura.docx (C4 / OWASP)",
            "04_Diccionario_y_Modelo_Base_Datos.docx (ERD / WAL)",
            "05_Manual_de_Instalacion_y_Despliegue.docx (Vercel / VPS)",
            "06_Plan_y_Matriz_de_Pruebas.docx (QA / test_api.py)",
            "07_Acta_de_Entrega_y_Cierre.docx (Cierre Formal)"
        ], "#0F4C81", "#0A355C"),
        ("3. CONFORMIDAD & GARANTÍA", "Términos de Soporte y SLA", [
            "Recepción formal por Sra. Gladys Solano Murcia",
            "Aprobación técnica por Instructor Evaluador",
            "Garantía técnica de software por 90 días",
            "Alineación 100% con directivas OWASP Top 10",
            "Soporte contra defectos y guía de operación"
        ], "#059669", "#047857")
    ]

    px = 75
    for ptitle, psub, pitems, pbdr, phdr in pillars:
        draw.rounded_rectangle([px, 175, px + 380, 520], radius=8, outline=pbdr, width=2, fill="#F8FAFC")
        draw.rounded_rectangle([px, 175, px + 380, 225], radius=8, outline=phdr, width=1, fill=phdr)
        draw.rectangle([px, 205, px + 380, 225], fill=phdr)
        draw.text((px + 15, 185), ptitle, fill="#FFFFFF", font=font_box_title)
        draw.text((px + 15, 235), psub, fill="#64748B", font=font_badge)
        
        iy = 265
        for itm in pitems:
            draw.text((px + 15, iy), "✔ " + itm, fill="#1E293B", font=font_item)
            iy += 28
        px += 410

    # Signatures Seal Banner (Bottom)
    draw.rounded_rectangle([75, 545, 1275, 685], radius=8, outline="#E2E8F0", width=1, fill="#F1F5F9")
    draw.text((95, 560), "TRIPLE AVAL DE CIERRE FORMAL DEL PROYECTO:", fill="#0F172A", font=font_box_title)

    sigs = [
        ("Sra. Gladys Solano Murcia", "Representante Legal - Fotocopiadoras SyP", "Cliente Receptor a Satisfacción"),
        ("Kevin Portela [POR CONFIRMAR]", "Líder de Desarrollo y Arquitectura", "Entrega Técnica y Garantía"),
        ("Instructor Evaluador [POR CONFIRMAR]", "Evaluador de Etapa Productiva / Académica", "Aprobación y Validación Institucional")
    ]
    sx = 95
    for sname, scargo, srol in sigs:
        draw.rounded_rectangle([sx, 590, sx + 370, 670], radius=6, outline="#CBD5E1", width=1, fill="#FFFFFF")
        draw.text((sx + 12, 600), sname, fill="#0F4C81", font=font_box_title)
        draw.text((sx + 12, 624), scargo, fill="#475569", font=font_badge)
        draw.text((sx + 12, 644), "Rol: " + srol, fill="#059669", font=font_badge)
        sx += 400

    img.save(DIAGRAM_PATH, "PNG", dpi=(300, 300))
    print(f"[OK] Handover Diagram generated at: {DIAGRAM_PATH}")

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
    hrun = hp.add_run("FOTOCOPIADORAS SyP | ACTA FORMAL DE ENTREGA Y CIERRE DE PROYECTO")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    frun1 = fp.add_run("Confidencial - Entrega de Proyecto & Sustentación Técnica | Acta de Cierre v2.0")
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

def build_handover_document():
    generate_handover_seal()
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
    r_pre = p_pre.add_run("GESTIÓN DE PROYECTOS DE SOFTWARE & ENTREGA FORMAL")
    r_pre.font.name = "Calibri"
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = SLATE
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(15)
    r_title = p_title.add_run("ACTA DE ENTREGA FORMAL Y CIERRE DE PROYECTO\nPLATAFORMA E-COMMERCE Y SERVICIO TÉCNICO")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_brand = doc.add_paragraph()
    p_brand.paragraph_format.space_before = Pt(0)
    p_brand.paragraph_format.space_after = Pt(25)
    r_brand = p_brand.add_run('EMPRESA CLIENTE: "FOTOCOPIADORAS SyP" (NEIVA, HUILA)')
    r_brand.font.name = "Calibri"
    r_brand.font.size = Pt(14)
    r_brand.font.bold = True
    r_brand.font.color.rgb = CHARCOAL
    p_brand.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_norm = doc.add_paragraph()
    p_norm.paragraph_format.space_before = Pt(10)
    p_norm.paragraph_format.space_after = Pt(35)
    r_norm = p_norm.add_run("Declaración de Recepción a Satisfacción & Certificación Técnica\nEntrega de Código Fuente, Base de Datos, Credenciales y Paquete Documental (7/7 Documentos)\nTérminos de Garantía de Software, Acuerdos de Nivel de Servicio (SLA) y Soporte")
    r_norm.font.name = "Calibri"
    r_norm.font.size = Pt(10.5)
    r_norm.font.italic = True
    r_norm.font.color.rgb = MUTED
    p_norm.alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_roles = doc.add_table(rows=4, cols=2)
    t_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    roles_data = [
        ("Cliente Receptor (Representante Legal):", "Sra. Gladys Solano Murcia\nRepresentante Legal - Fotocopiadoras SyP (Neiva, Huila)"),
        ("Evaluador Académico / Institucional:", "Instructor Técnico de Software\nEvaluación de Etapa Productiva / Formación"),
        ("Líder de Desarrollo & Entrega:", "Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\nIngeniería de Software & Arquitectura"),
        ("Fecha de Suscripción del Acta:", "04 de Noviembre de 2026 | Neiva, Huila, Colombia")
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
    
    t_vers = doc.add_table(rows=2, cols=5)
    t_vers.alignment = WD_TABLE_ALIGNMENT.CENTER
    vers_headers = ["Versión", "Fecha", "Autor", "Descripción del Cambio", "Estado"]
    for c_idx, h in enumerate(vers_headers):
        t_vers.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_vers.rows[0], bg_color="0F4C81", is_header=True)
    
    vers_rows = [
        ("1.0", "04/11/2026", "Ingeniero de Software Senior", "Emisión formal del Acta de Entrega y Cierre del Proyecto Fotocopiadoras SyP con inventario total de entregables, checklist 7/7, garantías y firmas.", "Aprobado para Suscripción")
    ]
    for r_idx, r_data in enumerate(vers_rows):
        row = t_vers.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF")

    # -------------------------------------------------------------
    # TABLA DE CONTENIDO
    # -------------------------------------------------------------
    h_toc = doc.add_heading("Contenido del Documento", level=1)
    h_toc.paragraph_format.space_before = Pt(20)
    h_toc.paragraph_format.space_after = Pt(10)
    
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.line_spacing = 1.2
    toc_items = [
        "1. DATOS GENERALES DEL PROYECTO Y PARTES INTERVINIENTES",
        "   1.1 Información Corporativa e Institucional",
        "   1.2 Diagrama de Certificación de Entrega y Cierre Formal",
        "2. RESUMEN EJECUTIVO Y OBJETIVOS ALCANZADOS",
        "3. CHECKLIST EXHAUSTIVO DE ENTREGABLES DEL SISTEMA",
        "   3.1 Software Ejecutable y Código Fuente",
        "   3.2 Base de Datos Relacional y Esquema en Producción",
        "   3.3 Paquete Completo de Documentación Técnica Formal (7 Documentos)",
        "   3.4 Credenciales y Cuentas de Acceso Administrativo",
        "4. DECLARACIÓN DE RECEPCIÓN A SATISFACCIÓN",
        "5. TÉRMINOS DE GARANTÍA, SOPORTE TÉCNICO Y MANTENIMIENTO",
        "   5.1 Vigencia de la Garantía de Software (90 Días Calendario)",
        "   5.2 Acuerdos de Nivel de Servicio (SLA) y Cobertura de Incidencias",
        "   5.3 Exclusiones y Limitaciones de Responsabilidad",
        "6. PROTOCOLO DE CIERRE Y FIRMAS DE CONFORMIDAD"
    ]
    for item in toc_items:
        r = toc_p.add_run(item + "\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. DATOS GENERALES DEL PROYECTO
    # -------------------------------------------------------------
    doc.add_heading("1. Datos Generales del Proyecto y Partes Intervinientes", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("1.1 Información Corporativa e Institucional\n")
    r.bold = True
    p.add_run(
        "En la ciudad de Neiva, Departamento del Huila, República de Colombia, a los cuatro (04) días del mes de noviembre de 2026, "
        "se reúnen de manera formal las partes intervinientes con el propósito de protocolizar la entrega, recibo a satisfacción "
        "y cierre definitivo del proyecto de desarrollo de software denominado:\n\n"
        "\"PLATAFORMA WEB E-COMMERCE Y GESTIÓN DE SERVICIO TÉCNICO ESPECIALIZADO RICOH — FOTOCOPIADORAS SyP\"\n\n"
        "Partes que intervienen en el presente acto:\n"
        "1. PARTE RECEPTORA (EL CLIENTE):\n"
        "   • Entidad: FOTOCOPIADORAS SyP\n"
        "   • Representante Legal: Sra. Gladys Solano Murcia\n"
        "   • Domicilio Comercial: Neiva, Huila, Colombia\n"
        "   • Rol: Beneficiario comercial, receptor del sistema y titular de los derechos de explotación operativa.\n\n"
        "2. PARTE ENTREGADORA (EL DESARROLLADOR):\n"
        "   • Responsable Técnico: Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\n"
        "   • Rol: Ingeniero de Software, Arquitecto de Persistencia y Líder de Desarrollo del Proyecto.\n\n"
        "3. PARTE EVALUADORA INSTITUCIONAL:\n"
        "   • Funcionario: Instructor Evaluador Técnico [POR CONFIRMAR]\n"
        "   • Centro: Centro de Formación Técnica y Tecnológica / Formación Profesional\n"
        "   • Rol: Supervisor académico, garante de conformidad técnica y metodológica de la etapa de formación."
    )

    p = doc.add_paragraph()
    r = p.add_run("1.2 Diagrama de Certificación de Entrega y Cierre Formal\n")
    r.bold = True
    p.add_run(
        "A continuación se presenta el certificado visual de cierre que sintetiza los tres pilares de entrega acordados:"
    )

    if os.path.exists(DIAGRAM_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(DIAGRAM_PATH, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Certificación Gráfica de Entrega Formal y Cierre del Proyecto SyP.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. RESUMEN EJECUTIVO Y OBJETIVOS ALCANZADOS
    # -------------------------------------------------------------
    doc.add_heading("2. Resumen Ejecutivo y Objetivos Alcanzados", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "El proyecto consistió en el diseño, desarrollo, aseguramiento de calidad e implementación de un ecosistema digital "
        "robusto para Fotocopiadoras SyP, resolviendo integralmente la necesidad de digitalizar las ventas de equipos Ricoh, "
        "facilitar la cotización formal con liquidación legal de impuestos en Colombia (IVA 19%), coordinar mantenimientos en campo "
        "y capturar mensualmente las lecturas mecánicas de fotocopiado en clientes corporativos bajo modalidad de alquiler (renting).\n\n"
        "Metas técnicas y de negocio cumplidas al 100%:\n"
        "✔ Arquitectura desacoplada de alto rendimiento: Frontend PWA responsivo en Vanilla JS sin dependencias pesadas y Backend en FastAPI (Python 3.12).\n"
        "✔ Catálogo facetado y buscador en tiempo real con 11 equipos y consumibles Ricoh iniciales con especificaciones técnicas completas.\n"
        "✔ Motor de cotizaciones formales con generación de código 'COT-XXXXXX' y exportación directa en formato PDF descargable.\n"
        "✔ Pasarela de checkout adaptable a métodos de pago nacionales (PSE, transferencias Bancolombia/Nequi, crédito empresarial a 30 días y WhatsApp).\n"
        "✔ Módulo de agendamiento de servicio técnico preventivo/correctivo con franjas horarias y asignación interna a técnicos.\n"
        "✔ Módulo de captura mensual de contadores de copias blanco/negro y color para facturación de renting.\n"
        "✔ Panel de control administrativo integral (admin.html) con analítica financiera en Pesos Colombianos y exportación masiva en CSV.\n"
        "✔ Blindaje de seguridad conforme a OWASP Top 10 API y framework Strix (Bcrypt 12 rondas, tokens JWT HS256, Rate Limiting y CORS estricto)."
    )

    # -------------------------------------------------------------
    # 3. CHECKLIST EXHAUSTIVO DE ENTREGABLES
    # -------------------------------------------------------------
    doc.add_heading("3. Checklist Exhaustivo de Entregables del Sistema", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "A continuación se relaciona detalladamente la totalidad de los entregables tangibles suministrados y verificados "
        "en presencia de las partes:"
    )

    def render_checklist_table(headers, rows_data):
        t = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for c_idx, h in enumerate(headers):
            t.rows[0].cells[c_idx].paragraphs[0].add_run(h)
        format_row(t.rows[0], bg_color="0F4C81", is_header=True)
        for r_idx, r_data in enumerate(rows_data):
            row = t.rows[r_idx + 1]
            for c_idx, val in enumerate(r_data):
                cell = row.cells[c_idx]
                p = cell.paragraphs[0]
                r = p.add_run(val)
                if c_idx == len(r_data) - 1:
                    r.bold = True
                    r.font.color.rgb = RGBColor(5, 150, 105)
            format_row(row, bg_color="FFFFFF" if r_idx % 2 == 0 else "F8FAFC")
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 3.1 Software y Código Fuente
    doc.add_heading("3.0 Enlaces Oficiales de Acceso y Repositorio de Codigo", level=2)
    p_links = doc.add_paragraph()
    p_links.add_run(
        "Para efectos de revision, auditoria tecnica y prueba funcional por parte del Instructor Evaluador y la Direccion del Negocio, se certifican los siguientes accesos directos:\n"
        "\xe2\x80\xa2 Aplicacion Web Funcional en Vivo (Produccion): https://kevin81a.github.io/Fotocopiadora-S-P/\n"
        "\xe2\x80\xa2 Repositorio Oficial en GitHub: https://github.com/Kevin81A/Fotocopiadora-S-P\n"
        "\xe2\x80\xa2 Rama Principal Consolidada: main\n"
        "\xe2\x80\xa2 Estado del Despliegue: Operativo 100% con protocolo seguro HTTPS y compatibilidad multiplataforma.\n\n"
    )

    doc.add_heading("3.1 Componentes de Software y Código Fuente", level=2)
    sw_headers = ["Componente", "Ubicación en Repositorio", "Tecnología / Framework", "Estado de Entrega"]
    sw_data = [
        ("Frontend Tienda PWA", "syp-web/", "HTML5, CSS3 Modular, Vanilla JS, Service Worker", "Entregado y Operativo"),
        ("Backend REST API", "syp-backend/", "Python 3.12, FastAPI 0.115+, Uvicorn, Pydantic v2", "Entregado y Operativo"),
        ("Persistencia Relacional", "syp-backend/syp.db", "SQLite 3 Modo WAL (Write-Ahead Logging)", "Entregado y Poblado"),
        ("Orquestador PowerShell", "syp-web/iniciar_servidores.ps1", "PowerShell 5.1 / 7+ (Arranque dual)", "Entregado y Verificado"),
        ("Servidor Estático Seguro", "syp-web/serve_frontend.py", "Python ThreadingHTTPServer con bloqueo perimetral", "Entregado y Verificado"),
        ("Suite de Integración API", "syp-backend/test_api.py", "Script de pruebas automatizadas E2E", "Entregado y Aprobado")
    ]
    render_checklist_table(sw_headers, sw_data)

    # 3.2 Paquete de Documentación en Docs/
    doc.add_heading("3.2 Paquete Completo de Documentación Técnica Formal (Carpeta Docs/)", level=2)
    p_docs = doc.add_paragraph()
    p_docs.add_run("Se certifica la entrega del paquete documental íntegro en formato Microsoft Word (.docx):")
    
    doc_headers = ["#", "Nombre del Archivo Word", "Estándar / Marco Aplicable", "Descripción Clave", "Estado"]
    doc_data = [
        ("01", "01_SRS_Fotocopiadoras_SyP.docx", "IEEE Std 830-1998 / ISO 29148", "Especificación de Requisitos de Software (15 RF, 11 RNF, 8 RN, Casos de Uso)", "Verificado y Aprobado"),
        ("02", "02_Manual_de_Usuario_SyP.docx", "Guía UX / ISO/IEC 25010", "Manual de Usuario Cliente y Manual de Operaciones Administradora con marcadores [CAPTURA]", "Verificado y Aprobado"),
        ("03", "03_Manual_Tecnico_y_Arquitectura.docx", "C4 Model / OWASP Top 10", "Arquitectura Desacoplada, Catálogo de 29 Endpoints y Mitigaciones Strix VULN-01 a 08", "Verificado y Aprobado"),
        ("04", "04_Diccionario_y_Modelo_Base_Datos.docx", "Normalización 3FN / Relacional", "Diccionario de las 9 Tablas SQLite WAL, Modelo ERD, Índices B-Tree y Backups", "Verificado y Aprobado"),
        ("05", "05_Manual_de_Instalacion_y_Despliegue.docx", "Guía DevOps / Nginx / Vercel", "Instalación Local dual, Despliegue en Vercel (Front) y VPS Ubuntu (Back), Systemd, SSL", "Verificado y Aprobado"),
        ("06", "06_Plan_y_Matriz_de_Pruebas.docx", "IEEE Std 829-2008 / ISO 29119", "Plan QA, Matriz de 20 Casos Funcionales, Ejecución test_api.py y Seguridad OWASP", "Verificado y Aprobado"),
        ("07", "07_Acta_de_Entrega_y_Cierre.docx", "Gestión Formal de Proyectos", "Acta formal de cierre, checklist de entregables, SLA, garantía de 90 días y firmas", "Verificado y Aprobado")
    ]
    render_checklist_table(doc_headers, doc_data)

    # 3.3 Credenciales Iniciales
    doc.add_heading("3.3 Cuentas y Credenciales de Acceso al Sistema", level=2)
    cred_headers = ["Identificador", "Correo de Acceso", "Contraseña Inicial", "Rol / Privilegio", "Uso Recomendado"]
    cred_data = [
        ("usr_admin", "admin@sypfotocopiadoras.com", "admin123", "admin", "Cuenta de administración técnica y mantenimiento del servidor."),
        ("usr_gladys", "gladys.solano@sypfotocopiadoras.com", "gladys2026*", "admin", "Cuenta maestra de la propietaria (Gladys Solano Murcia) para control comercial."),
        ("usr_juan", "juan.portela@sypfotocopiadoras.com", "tecnico2026*", "admin", "Cuenta para soporte técnico en campo y asignación de órdenes."),
        ("usr_cliente_demo", "cliente@notaria2neiva.com", "notaria123", "cliente", "Cuenta demo corporativa para verificación del flujo de cliente.")
    ]
    render_checklist_table(cred_headers, cred_data)

    p_warn = doc.add_paragraph()
    r_w = p_warn.add_run("IMPORTANTE: ")
    r_w.bold = True
    r_w.font.color.rgb = RGBColor(185, 28, 28)
    p_warn.add_run(
        "Por estrictas normas de seguridad de la información, se recomienda a la Sra. Gladys Solano Murcia y a su equipo técnico "
        "actualizar las contraseñas iniciales inmediatamente después del despliegue en producción."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. DECLARACIÓN DE RECEPCIÓN A SATISFACCIÓN
    # -------------------------------------------------------------
    doc.add_heading("4. Declaración de Recepción a Satisfacción", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "La Sra. Gladys Solano Murcia, en su calidad de Representante Legal de Fotocopiadoras SyP, manifiesta expresamente que:\n\n"
        "1. Ha presenciado las demostraciones operativas de la plataforma web en sus módulos de Catálogo Ricoh, Cotizaciones formales con IVA, "
        "Checkout, Solicitud de Servicio Técnico, Reporte de Contadores y Panel Administrativo.\n"
        "2. Ha recibido a entera conformidad la totalidad del código fuente, base de datos poblada y los siete (7) documentos formales en formato Word (.docx).\n"
        "3. Constata que el software cumple cabalmente con los requerimientos pactados para la etapa actual, resolviendo las necesidades comerciales de la empresa.\n\n"
        "Por su parte, el Instructor Evaluador certifica que el proyecto cumple con los lineamientos curriculares, técnicos, arquitecturales "
        "y metodológicos exigidos en la formación profesional del área de desarrollo de software."
    )

    # -------------------------------------------------------------
    # 5. TÉRMINOS DE GARANTÍA, SOPORTE Y MANTENIMIENTO
    # -------------------------------------------------------------
    doc.add_heading("5. Términos de Garantía, Soporte Técnico y Mantenimiento", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("5.1 Vigencia de la Garantía de Software (90 Días Calendario)\n")
    r.bold = True
    p.add_run(
        "El desarrollador otorga un período de garantía técnica gratuita por un término de noventa (90) días calendario, "
        "contados a partir de la firma de la presente acta. Esta garantía cubre exclusivamente:\n"
        "• Corrección de defectos de programación (bugs) o errores imprevistos en los endpoints FastAPI o vistas web.\n"
        "• Fallos en el recálculo tributario de cotizaciones o en la persistencia de transacciones en SQLite.\n"
        "• Asistencia para la restauración de copias de seguridad de la base de datos ante contingencias técnicas imputables al código."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.2 Acuerdos de Nivel de Servicio (SLA) para Soporte\n")
    r.bold = True
    p.add_run(
        "Durante el período de garantía, las solicitudes de soporte se clasificarán según su nivel de criticidad:\n"
        "• Incidencia Crítica (Sistema fuera de línea o caída de base de datos): Tiempo máximo de respuesta de 4 horas; resolución en menos de 24 horas.\n"
        "• Incidencia Media (Fallo en un filtro o error cosmético visual): Tiempo de respuesta de 12 horas; resolución en menos de 48 horas.\n"
        "• Consultas Operativas: Atención en horario hábil a través de WhatsApp o correo electrónico."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.3 Exclusiones y Limitaciones de Responsabilidad\n")
    r.bold = True
    p.add_run(
        "Quedan explícitamente excluidos de la garantía:\n"
        "1. Modificaciones o alteraciones no autorizadas en el código fuente o en la base de datos realizadas por terceros ajenos al desarrollador.\n"
        "2. Caídas del servicio originadas por falta de pago del dominio, vencimiento del hosting VPS, o fallas masivas en proveedores externos (Vercel, Let's Encrypt).\n"
        "3. Solicitud de nuevas funcionalidades, módulos adicionales o rediseños visuales que no formen parte del alcance definido en el SRS v2.0."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. PROTOCOLO DE CIERRE Y FIRMAS
    # -------------------------------------------------------------
    doc.add_heading("6. Protocolo de Cierre y Firmas de Conformidad", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "En constancia de lo acordado y como manifestación formal de aceptación, las partes firman el presente documento en tres (3) "
        "ejemplares del mismo tenor y valor probatorio en la ciudad de Neiva (Huila), a los 04 días del mes de noviembre de 2026:"
    )

    t_sig = doc.add_table(rows=3, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig_headers = ["POR LA EMPRESA (CLIENTE)", "POR EL EQUIPO DESARROLLADOR", "POR LA INSTITUCIÓN EVALUADORA"]
    for c_idx, h in enumerate(t_sig_headers):
        t_sig.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_sig.rows[0], bg_color="0F4C81", is_header=True)

    sig_content = [
        ("Sra. Gladys Solano Murcia\nRepresentante Legal\nFotocopiadoras SyP - Neiva, Huila\nC.C. No. _____________________\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Kevin Portela [POR CONFIRMAR]\nLíder de Desarrollo y Arquitectura\nC.C. No. _____________________\nFicha No. _____________________\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Instructor Evaluador [POR CONFIRMAR]\nEvaluador Etapa Productiva / Académica\nCentro de Formación Técnica\nC.C. No. _____________________\n\nFirma: _________________________\nFecha: _____ / _____ / 2026"),
        ("Recibido a Satisfacción Comercial", "Entrega Formal y Garantía", "Aprobación y Validación Técnica")
    ]
    for r_idx, r_data in enumerate(sig_content):
        row = t_sig.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx == 0 else "F8FAFC")

    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] Handover Document generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_handover_document()
