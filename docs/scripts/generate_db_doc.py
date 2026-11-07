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
OUTPUT_DOCX = os.path.join(DOCS_DIR, "04_Diccionario_y_Modelo_Base_Datos.docx")
DIAGRAM_PATH = os.path.join(DOCS_DIR, "er_diagram_syp.png")

def generate_er_diagram():
    """Generates an Entity-Relationship (ERD) diagram image using Pillow."""
    width, height = 1350, 950
    img = Image.new("RGB", (width, height), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 22)
        font_tbl_hdr = ImageFont.truetype("arialbd.ttf", 15)
        font_col_pk = ImageFont.truetype("arialbd.ttf", 11)
        font_col = ImageFont.truetype("arial.ttf", 11)
        font_badge = ImageFont.truetype("arialbd.ttf", 10)
    except Exception:
        font_title = font_tbl_hdr = font_col_pk = font_col = font_badge = ImageFont.load_default()

    # Header Banner
    draw.rectangle([0, 0, width, 65], fill="#0F4C81")
    draw.text((30, 20), "MODELO ENTIDAD-RELACIÓN (ER) - BASE DE DATOS FOTOCOPIADORAS SyP (SQLITE WAL)", fill="#FFFFFF", font=font_title)

    # Helper function to draw a table box
    def draw_entity(x, y, w, title, columns, header_bg="#0F4C81"):
        h = 32 + len(columns) * 22 + 8
        # Shadow / Border
        draw.rounded_rectangle([x, y, x + w, y + h], radius=6, outline="#CBD5E1", width=2, fill="#FFFFFF")
        # Header
        draw.rounded_rectangle([x, y, x + w, y + 30], radius=6, outline=header_bg, width=1, fill=header_bg)
        draw.rectangle([x, y + 20, x + w, y + 30], fill=header_bg)
        draw.text((x + 12, y + 7), title, fill="#FFFFFF", font=font_tbl_hdr)
        
        # Columns
        curr_y = y + 36
        for col_name, col_type, is_pk, is_fk in columns:
            if is_pk:
                draw.text((x + 10, curr_y), "PK", fill="#D97706", font=font_badge)
                draw.text((x + 35, curr_y), col_name, fill="#0F172A", font=font_col_pk)
            elif is_fk:
                draw.text((x + 10, curr_y), "FK", fill="#2563EB", font=font_badge)
                draw.text((x + 35, curr_y), col_name, fill="#1E293B", font=font_col)
            else:
                draw.text((x + 35, curr_y), col_name, fill="#475569", font=font_col)
                
            draw.text((x + w - 85, curr_y), col_type, fill="#94A3B8", font=font_col)
            curr_y += 22
        return (x, y, w, h)

    # Define entities
    # 1. users (Center Anchor)
    u_cols = [
        ("id", "TEXT", True, False),
        ("email", "TEXT UNIQUE", False, False),
        ("password_hash", "TEXT", False, False),
        ("name", "TEXT", False, False),
        ("phone", "TEXT", False, False),
        ("role", "TEXT ('cliente'|'admin')", False, False),
        ("is_active", "INTEGER (0|1)", False, False),
        ("created_at", "TIMESTAMP", False, False),
        ("last_login", "TIMESTAMP", False, False)
    ]
    u_box = draw_entity(530, 100, 290, "users (Usuarios)", u_cols, header_bg="#0F4C81")

    # 2. categories (Left Top)
    c_cols = [
        ("id", "TEXT", True, False),
        ("slug", "TEXT UNIQUE", False, False),
        ("name", "TEXT", False, False),
        ("icon_svg", "TEXT", False, False),
        ("sort_order", "INTEGER", False, False)
    ]
    c_box = draw_entity(40, 100, 260, "categories (Categorías)", c_cols, header_bg="#1E293B")

    # 3. products (Left Center)
    p_cols = [
        ("id", "TEXT", True, False),
        ("name", "TEXT", False, False),
        ("category_slug", "TEXT", False, True),
        ("brand", "TEXT ('Ricoh')", False, False),
        ("price", "REAL", False, False),
        ("spec", "TEXT", False, False),
        ("stock_status", "TEXT ('ok'|'low'|'out')", False, False),
        ("is_active", "INTEGER", False, False),
        ("speed, duty_cycle", "TEXT (Ricoh specs)", False, False),
        ("compatible_ids", "TEXT", False, False),
        ("image_url", "TEXT", False, False),
        ("created_at", "TIMESTAMP", False, False)
    ]
    p_box = draw_entity(40, 270, 290, "products (Equipos y Repuestos)", p_cols, header_bg="#0369A1")

    # 4. orders (Center Bottom)
    o_cols = [
        ("id", "TEXT", True, False),
        ("order_code", "TEXT UNIQUE", False, False),
        ("client_id", "TEXT", False, True),
        ("client_name, email, phone", "TEXT", False, False),
        ("delivery_address, city", "TEXT", False, False),
        ("items_json", "TEXT (JSON)", False, False),
        ("subtotal, iva (19%), total", "REAL", False, False),
        ("payment_method, status", "TEXT", False, False),
        ("shipping_status", "TEXT", False, False),
        ("created_at", "TIMESTAMP", False, False)
    ]
    o_box = draw_entity(510, 480, 330, "orders (Pedidos E-commerce)", o_cols, header_bg="#059669")

    # 5. maintenance_requests (Right Top)
    m_cols = [
        ("id", "TEXT", True, False),
        ("client_id", "TEXT", False, True),
        ("client_name, email, phone", "TEXT", False, False),
        ("equipment", "TEXT (Modelo Ricoh)", False, False),
        ("service_type", "TEXT (Prev|Corr)", False, False),
        ("desired_date, time", "TEXT", False, False),
        ("description, admin_notes", "TEXT", False, False),
        ("status", "TEXT (Pend|Conf|Proc|Comp)", False, False),
        ("created_at, updated_at", "TIMESTAMP", False, False)
    ]
    m_box = draw_entity(960, 100, 340, "maintenance_requests (Soporte)", m_cols, header_bg="#B45309")

    # 6. counter_reports (Right Bottom)
    cr_cols = [
        ("id", "TEXT", True, False),
        ("client_id", "TEXT", False, True),
        ("client_name", "TEXT", False, False),
        ("equipment_model", "TEXT", False, False),
        ("mono_counter", "INTEGER", False, False),
        ("color_counter", "INTEGER", False, False),
        ("report_month", "TEXT", False, False),
        ("notes", "TEXT", False, False),
        ("created_at", "TIMESTAMP", False, False)
    ]
    cr_box = draw_entity(960, 480, 340, "counter_reports (Renting Copias)", cr_cols, header_bg="#D97706")

    # 7. notifications (Center Far Bottom)
    n_cols = [
        ("id", "TEXT", True, False),
        ("user_id", "TEXT", False, True),
        ("user_email", "TEXT", False, False),
        ("title, message", "TEXT", False, False),
        ("type", "TEXT ('info'|'order'|'maint')", False, False),
        ("is_read", "INTEGER (0|1)", False, False),
        ("created_at", "TIMESTAMP", False, False)
    ]
    n_box = draw_entity(510, 750, 330, "notifications (Alertas en Vivo)", n_cols, header_bg="#4F46E5")

    # 8. quotes (Left Far Bottom)
    q_cols = [
        ("id", "TEXT", True, False),
        ("quote_code", "TEXT UNIQUE", False, False),
        ("client_name, email, phone", "TEXT", False, False),
        ("items_json", "TEXT (JSON)", False, False),
        ("subtotal, iva (19%), total", "REAL", False, False),
        ("notes", "TEXT", False, False),
        ("created_at", "TIMESTAMP", False, False)
    ]
    q_box = draw_entity(40, 620, 290, "quotes (Cotizaciones Formales)", q_cols, header_bg="#0284C7")

    # 9. contact_messages (Right Far Bottom)
    cm_cols = [
        ("id", "TEXT", True, False),
        ("name, email, phone", "TEXT", False, False),
        ("subject, message", "TEXT", False, False),
        ("is_read", "INTEGER (0|1)", False, False),
        ("created_at", "TIMESTAMP", False, False)
    ]
    cm_box = draw_entity(960, 750, 340, "contact_messages (PQR y Mensajes)", cm_cols, header_bg="#64748B")

    # Draw Relation Lines (Crow's Foot / ER arrows)
    # 1. categories -> products (FK: category_slug -> slug)
    draw.line([(170, 230), (170, 270)], fill="#0284C7", width=2)
    draw.polygon([(165, 265), (175, 265), (170, 275)], fill="#0284C7")
    draw.text((180, 245), "1 : N", fill="#0369A1", font=font_badge)

    # 2. users -> maintenance_requests (FK: client_id -> id)
    draw.line([(820, 160), (960, 160)], fill="#B45309", width=2)
    draw.polygon([(955, 155), (955, 165), (965, 160)], fill="#B45309")
    draw.text((865, 142), "1 : N (client_id)", fill="#92400E", font=font_badge)

    # 3. users -> orders (FK: client_id -> id)
    draw.line([(675, 335), (675, 480)], fill="#059669", width=2)
    draw.polygon([(670, 475), (680, 475), (675, 485)], fill="#059669")
    draw.text((685, 395), "1 : N (client_id)", fill="#047857", font=font_badge)

    # 4. users -> counter_reports (FK: client_id -> id)
    draw.line([(820, 280), (890, 280), (890, 550), (960, 550)], fill="#D97706", width=2)
    draw.polygon([(955, 545), (955, 555), (965, 550)], fill="#D97706")
    draw.text((900, 532), "1 : N", fill="#B45309", font=font_badge)

    # 5. users -> notifications (FK: user_id -> id)
    draw.line([(640, 725), (640, 750)], fill="#4F46E5", width=2)
    draw.polygon([(635, 745), (645, 745), (640, 755)], fill="#4F46E5")
    draw.text((650, 730), "1 : N", fill="#4338CA", font=font_badge)

    img.save(DIAGRAM_PATH, "PNG", dpi=(300, 300))
    print(f"[OK] ER Diagram generated at: {DIAGRAM_PATH}")

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
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
    hrun = hp.add_run("FOTOCOPIADORAS SyP | DICCIONARIO DE DATOS Y MODELO RELACIONAL")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    frun1 = fp.add_run("Confidencial - Entrega de Proyecto & Sustentación Técnica | Base de Datos v2.0")
    frun1.font.name = "Calibri"
    frun1.font.size = Pt(8.5)
    frun1.font.color.rgb = RGBColor(100, 116, 139)

def format_row(row, bg_color=None, is_header=False):
    for cell in row.cells:
        set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
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

def build_database_document():
    generate_er_diagram()
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
    r_pre = p_pre.add_run("INGENIERÍA DE SOFTWARE & PERSISTENCIA TRANSACCIONAL")
    r_pre.font.name = "Calibri"
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = SLATE
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(15)
    r_title = p_title.add_run("DICCIONARIO DE DATOS Y MODELO DE BASE DE DATOS\nSISTEMA E-COMMERCE Y SERVICIO TÉCNICO")
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
    r_norm = p_norm.add_run("Motor de Datos: SQLite 3 Modo WAL (Write-Ahead Logging)\nEstándar de Modelado: Diagrama Entidad-Relación y Normalización 3FN\nIntegridad Referencial: PRAGMA foreign_keys = ON & Índices B-Tree")
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
        ("Desarrollador / Administrador DB:", "Kevin Portela [POR CONFIRMAR: Datos Completos y Ficha]\nIngeniería de Software & Arquitectura de Datos"),
        ("Versión y Entorno de Persistencia:", "Versión 2.0 (Producción) | SQLite 3 WAL (syp.db)")
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
        ("1.0", "07/10/2026", "Equipo Desarrollo SyP", "Diseño inicial del esquema relacional (7 tablas básicas: users, categories, products, maintenance_requests, contact_messages, quotes, counter_reports).", "Superado"),
        ("2.0", "04/11/2026", "Ingeniero de Software Senior", "Ampliación a 9 tablas en producción (inclusión formal de orders y notifications), optimización de índices B-Tree, soporte WAL y diccionario exhaustivo de columnas.", "Aprobado")
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
        "1. INTRODUCCIÓN Y ARQUITECTURA DE PERSISTENCIA",
        "   1.1 Propósito y Justificación Tecnológica (SQLite 3 WAL)",
        "   1.2 Modo de Concurrencia y Configuración de Pragmas",
        "   1.3 Capa de Acceso a Datos y Manejo de Conexiones en Python",
        "2. MODELO ENTIDAD-RELACIÓN (ER) Y CARDINALIDADES",
        "   2.1 Diagrama Entidad-Relación Global",
        "   2.2 Matriz de Relaciones y Llaves Foráneas (FK)",
        "   2.3 Reglas de Integridad Referencial y Acciones Cascada",
        "3. DICCIONARIO DE DATOS DETALLADO (9 TABLAS EN PRODUCCIÓN)",
        "   3.1 Tabla: users (Cuentas de Acceso y Roles)",
        "   3.2 Tabla: categories (Categorías del Catálogo Ricoh)",
        "   3.3 Tabla: products (Equipos Multifuncionales, Suministros y Repuestos)",
        "   3.4 Tabla: maintenance_requests (Solicitudes de Servicio Técnico)",
        "   3.5 Tabla: contact_messages (Mensajes y PQRs del Portal)",
        "   3.6 Tabla: quotes (Cotizaciones Formales con IVA)",
        "   3.7 Tabla: counter_reports (Lecturas Mensuales de Copias / Renting)",
        "   3.8 Tabla: orders (Pedidos, Checkout y Transacciones Comerciales)",
        "   3.9 Tabla: notifications (Bandeja de Alertas en Tiempo Real)",
        "4. ESTRATEGIA DE INDEXACIÓN Y RENDIMIENTO B-TREE",
        "   4.1 Análisis de Índices Creados y Optimización de Consultas",
        "5. POLÍTICAS DE MANTENIMIENTO, RESPALDOS (BACKUP) Y RECUPERACIÓN",
        "   5.1 Procedimiento de Respaldo en Caliente (Hot Backup)",
        "   5.2 Rutinas de Mantenimiento (VACUUM, Integrity Check y Checkpoint)",
        "6. CONTROL DE APROBACIÓN Y FIRMAS DE CONFORMIDAD"
    ]
    for item in toc_items:
        r = toc_p.add_run(item + "\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. INTRODUCCIÓN Y ARQUITECTURA DE PERSISTENCIA
    # -------------------------------------------------------------
    doc.add_heading("1. Introducción y Arquitectura de Persistencia", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("1.1 Propósito y Justificación Tecnológica (SQLite 3 WAL)\n")
    r.bold = True
    p.add_run(
        "El presente documento técnico constituye el Diccionario de Datos y Modelo de Persistencia Relacional oficial "
        "de la plataforma digital 'Fotocopiadoras SyP'. Su objetivo es proveer la especificación exacta de las estructuras "
        "de datos, restricciones de integridad referencial, tipos de columnas, índices y políticas de mantenimiento que rigen "
        "el almacenamiento de la información comercial, pedidos, cotizaciones, soporte técnico y contadores de fotocopiado.\n\n"
        "La persistencia del sistema está implementada sobre el motor relacional SQLite 3. Esta decisión de ingeniería responde "
        "a los siguientes criterios de arquitectura:\n"
        "• Latencia Cero en Servidor: Al operar como motor embebido en proceso (in-process), se eliminan los saltos de red TCP/IP "
        "asociados a gestores cliente-servidor externos (ej. PostgreSQL o MySQL remotos), permitiendo lecturas de catálogo en menos de 5 ms.\n"
        "• Portabilidad Absoluta y Facilidad de Backup: Toda la base de datos se consolida en un único archivo binario autocontenido ('syp.db'), "
        "facilitando esquemas de respaldo atómico, clonación para pruebas y migración inmediata entre servidores sin configurar demonios externos.\n"
        "• Cumplimiento Estricto ACID: Garantiza transacciones atómicas, consistentes, aisladas y durables."
    )

    p = doc.add_paragraph()
    r = p.add_run("1.2 Modo de Concurrencia y Configuración de Pragmas\n")
    r.bold = True
    p.add_run(
        "Para superar la limitación clásica de bloqueos de archivo en SQLite tradicional, el backend de Fotocopiadoras SyP "
        "inicializa la conexión ejecutando directivas Pragma avanzadas al momento de apertura:\n"
        "1. PRAGMA journal_mode = WAL: Activa el modo Write-Ahead Logging. Bajo este esquema, las modificaciones se escriben en un archivo "
        "de registro separado ('syp.db-wal') sin bloquear a los lectores. Esto permite concurrencia masiva donde cientos de clientes "
        "pueden consultar el catálogo simultáneamente mientras se registra un pedido o una solicitud técnica.\n"
        "2. PRAGMA foreign_keys = ON: Activa la obligatoriedad de llaves foráneas a nivel de motor, rechazando cualquier inserción o borrado "
        "que viole la integridad de datos entre entidades.\n"
        "3. Timeout de Bloqueo a 20.0 Segundos: Si ocurre contención de escritura, la conexión espera hasta 20 segundos antes de emitir un fallo."
    )

    p = doc.add_paragraph()
    r = p.add_run("1.3 Capa de Acceso a Datos y Manejo de Conexiones en Python\n")
    r.bold = True
    p.add_run(
        "En el archivo 'syp-backend/database.py', el acceso se gestiona mediante un generador contextual de transacciones seguro:\n"
        "```python\n"
        "@contextmanager\n"
        "def get_db():\n"
        "    conn = get_db_connection()\n"
        "    try:\n"
        "        yield conn\n"
        "        conn.commit()\n"
        "    except Exception:\n"
        "        conn.rollback()\n"
        "        raise\n"
        "    finally:\n"
        "        conn.close()\n"
        "```\n"
        "Este patrón garantiza que si una operación falla a mitad de ejecución, se emite un 'rollback' automático, evitando registros huérfanos "
        "y cerrando siempre los descriptores de archivo para evitar fugas de memoria o bloqueos de base de datos."
    )

    # -------------------------------------------------------------
    # 2. MODELO ENTIDAD-RELACIÓN (ER) Y CARDINALIDADES
    # -------------------------------------------------------------
    doc.add_heading("2. Modelo Entidad-Relación (ER) y Cardinalidades", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("2.1 Diagrama Entidad-Relación Global\n")
    r.bold = True
    p.add_run(
        "A continuación se presenta el Diagrama Entidad-Relación que ilustra las 9 entidades de la base de datos "
        "de Fotocopiadoras SyP, sus llaves primarias, llaves foráneas y cardinalidades de asociación:"
    )

    if os.path.exists(DIAGRAM_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(DIAGRAM_PATH, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Diagrama Entidad-Relación (ERD) Normalizado - Base de Datos syp.db.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED

    p = doc.add_paragraph()
    r = p.add_run("2.2 Matriz de Relaciones y Llaves Foráneas (FK)\n")
    r.bold = True
    
    t_rel = doc.add_table(rows=6, cols=5)
    t_rel.alignment = WD_TABLE_ALIGNMENT.CENTER
    rel_headers = ["Tabla Origen", "Columna FK", "Tabla Destino (Referenciada)", "Columna PK", "Cardinalidad y Semántica"]
    for c_idx, h in enumerate(rel_headers):
        t_rel.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_rel.rows[0], bg_color="0F4C81", is_header=True)

    rel_data = [
        ("products", "category_slug", "categories", "slug", "N : 1 (Todo producto pertenece a una categoría válida)."),
        ("maintenance_requests", "client_id", "users", "id", "N : 1 Opcional (Asocia la orden técnica al cliente registrado)."),
        ("orders", "client_id", "users", "id", "N : 1 Opcional (Permite checkout registrado o compra como invitado)."),
        ("counter_reports", "client_id", "users", "id", "N : 1 Obligatorio (Asocia la lectura mensual al cliente de renting)."),
        ("notifications", "user_id", "users", "id", "N : 1 Opcional (Entrega la notificación al perfil del usuario).")
    ]
    for idx, (c1, c2, c3, c4, c5) in enumerate(rel_data):
        row = t_rel.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        row.cells[3].paragraphs[0].add_run(c4)
        row.cells[4].paragraphs[0].add_run(c5)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("2.3 Reglas de Integridad Referencial y Acciones Cascada\n")
    r.bold = True
    p.add_run(
        "• Restricción de Borrado (ON DELETE RESTRICT): No se permite eliminar una categoría en 'categories' si existen productos "
        "asociados a su slug en 'products'. Esto previene la existencia de productos huérfanos en el catálogo.\n"
        "• Preservación Histórica de Clientes: Al registrarse un pedido o solicitud de servicio técnico, los datos fiscales (nombre, email, teléfono, nit) "
        "se congelan en las columnas de la tabla de la orden. Si el usuario modifica su perfil en 'users', el registro histórico de la orden permanece intacto "
        "para fines contables y tributarios.\n"
        "• Desnormalización Controlada en 'items_json': Las líneas de productos de un pedido o cotización se almacenan como cadenas JSON serializadas "
        "en las tablas 'orders' y 'quotes'. Esta estrategia garantiza una fotografía inmutable del producto, precio unitario y cantidad al momento exacto "
        "de la transacción, blindando el sistema contra variaciones posteriores en el catálogo de precios."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. DICCIONARIO DE DATOS DETALLADO (9 TABLAS EN PRODUCCIÓN)
    # -------------------------------------------------------------
    doc.add_heading("3. Diccionario de Datos Detallado (9 Tablas en Producción)", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "A continuación se presenta la especificación exhaustiva de cada una de las 9 tablas del sistema, "
        "detallando nombres de columnas, tipos de datos físicos en SQLite, nulabilidad, llaves, valores por defecto, "
        "restricciones e índices asociados:"
    )

    # Helper function for rendering table dictionaries
    def render_dict_table(table_name, table_desc, columns_info):
        h2 = doc.add_heading(f"3.{table_idx} Tabla: {table_name}", level=2)
        h2.paragraph_format.space_before = Pt(12)
        h2.paragraph_format.space_after = Pt(4)
        
        pd = doc.add_paragraph()
        rd = pd.add_run(f"Propósito y Descripción: {table_desc}")
        rd.font.size = Pt(9.5)
        rd.font.italic = True
        rd.font.color.rgb = CHARCOAL
        
        t = doc.add_table(rows=len(columns_info) + 1, cols=8)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_hdrs = ["Columna", "Tipo Dato", "Nulo", "Llave", "Default", "Restricciones", "Índice", "Descripción"]
        for c_idx, ch in enumerate(col_hdrs):
            t.rows[0].cells[c_idx].paragraphs[0].add_run(ch)
        format_row(t.rows[0], bg_color="0F4C81", is_header=True)
        
        # Set specific widths
        widths = [Inches(1.1), Inches(0.8), Inches(0.5), Inches(0.5), Inches(0.8), Inches(0.8), Inches(0.9), Inches(1.8)]
        for r_idx, col_data in enumerate(columns_info):
            row = t.rows[r_idx + 1]
            for c_idx, val in enumerate(col_data):
                cell = row.cells[c_idx]
                cell.width = widths[c_idx]
                cell.paragraphs[0].add_run(val)
            format_row(row, bg_color="FFFFFF" if r_idx % 2 == 0 else "F8FAFC")
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 3.1 users
    table_idx = 1
    users_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador único alfanumérico (ej. 'usr_admin', 'usr_gladys')."),
        ("email", "TEXT", "NO", "-", "None", "UNIQUE", "idx_users_email", "Correo electrónico institucional o de cliente; credencial de acceso."),
        ("password_hash", "TEXT", "NO", "-", "None", "Bcrypt 12 rounds", "-", "Hash criptográfico de la contraseña del usuario."),
        ("name", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Nombre completo del usuario o razón social de la empresa."),
        ("phone", "TEXT", "NO", "-", "None", "Min 7 chars", "-", "Número de teléfono de contacto o línea celular para WhatsApp."),
        ("role", "TEXT", "NO", "-", "'cliente'", "'cliente' | 'admin'", "-", "Rol en el sistema para control de acceso basado en roles (RBAC)."),
        ("is_active", "INTEGER", "NO", "-", "1", "0 = Inactivo, 1 = Activo", "-", "Bandera de estado; permite revocar acceso sin eliminar histórico."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora del registro del usuario en la plataforma."),
        ("last_login", "TIMESTAMP", "SÍ", "-", "None", "ISO-8601 UTC", "-", "Fecha y hora de la última autenticación exitosa.")
    ]
    render_dict_table("users", "Almacena los perfiles de usuarios registrados, roles de administración y credenciales de acceso.", users_cols)

    # 3.2 categories
    table_idx = 2
    cat_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador único de la categoría (ej. 'cat_fotocopiadoras')."),
        ("slug", "TEXT", "NO", "-", "None", "UNIQUE", "slug_auto", "Cadena amigable para URL (ej. 'fotocopiadoras', 'repuestos')."),
        ("name", "TEXT", "NO", "-", "None", "None", "-", "Nombre visual descriptivo de la categoría para el menú y catálogo."),
        ("icon_svg", "TEXT", "SÍ", "-", "None", "SVG markup", "-", "Código SVG vectorial del icono para renderizado en el frontend."),
        ("sort_order", "INTEGER", "SÍ", "-", "0", "Orden ascendente", "-", "Prioridad de visualización en el menú y filtros de navegación.")
    ]
    render_dict_table("categories", "Define la taxonomía del catálogo comercial de Fotocopiadoras SyP (Equipos, Insumos, Repuestos).", cat_cols)

    # 3.3 products
    table_idx = 3
    prod_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Código de producto o SKU comercial (ej. 'ricoh-mp-301', 'toner-mp-4002')."),
        ("name", "TEXT", "NO", "-", "None", "Min 3 chars", "-", "Nombre comercial completo del equipo o consumible."),
        ("category_slug", "TEXT", "NO", "FK", "None", "categories(slug)", "idx_products_cat", "Clave foránea que enlaza el producto con su categoría correspondiente."),
        ("brand", "TEXT", "NO", "-", "'Ricoh'", "None", "-", "Marca del fabricante del equipo o insumo (por defecto 'Ricoh')."),
        ("price", "REAL", "NO", "-", "None", "gt 0 COP", "-", "Precio de venta en Pesos Colombianos (COP) antes de IVA."),
        ("spec", "TEXT", "NO", "-", "None", "None", "-", "Descripción técnica general o resumen de características operativas."),
        ("stock_status", "TEXT", "NO", "-", "'ok'", "'ok' | 'low' | 'out'", "-", "Estado de disponibilidad de inventario."),
        ("is_active", "INTEGER", "NO", "-", "1", "0 = Oculto, 1 = Activo", "-", "Visibilidad en el catálogo público del e-commerce."),
        ("rating", "REAL", "SÍ", "-", "4.9", "Rango 1.0 - 5.0", "-", "Calificación promedio asignada por clientes."),
        ("reviews_count", "INTEGER", "SÍ", "-", "25", "ge 0", "-", "Número de reseñas registradas para el producto."),
        ("badge", "TEXT", "SÍ", "-", "None", "'MÁS VENDIDO'|'NUEVO'", "-", "Etiqueta visual destacada para tarjetas de producto."),
        ("discount_percent", "INTEGER", "SÍ", "-", "0", "0 a 100", "-", "Porcentaje de descuento comercial aplicado sobre el precio base."),
        ("speed", "TEXT", "SÍ", "-", "None", "ej. '31 ppm'", "-", "Velocidad de impresión en páginas por minuto (específica de fotocopiadoras)."),
        ("duty_cycle", "TEXT", "SÍ", "-", "None", "ej. '50.000 pág/mes'", "-", "Ciclo de trabajo mensual recomendado por el fabricante."),
        ("paper_size", "TEXT", "SÍ", "-", "None", "ej. 'Carta / Oficio / A4'", "-", "Formatos de papel soportados por las bandejas del equipo."),
        ("connectivity", "TEXT", "SÍ", "-", "None", "ej. 'Ethernet Gigabit, USB'", "-", "Interfaces de conexión y red soportadas."),
        ("functions", "TEXT", "SÍ", "-", "None", "ej. 'Copia, Impresión, Escáner'", "-", "Funcionalidades multifuncionales del equipo."),
        ("toner_yield", "TEXT", "SÍ", "-", "None", "ej. '8.000 páginas'", "-", "Rendimiento estimado del cartucho de tóner asociado."),
        ("cost_per_page", "TEXT", "SÍ", "-", "None", "ej. '$18 COP/página'", "-", "Cálculo técnico estimado del costo por página impresa."),
        ("compatible_ids", "TEXT", "SÍ", "-", "None", "Lista CSV de modelos", "-", "Modelos de fotocopiadoras compatibles con el repuesto o tóner."),
        ("image_url", "TEXT", "SÍ", "-", "None", "Ruta local o URL", "-", "Ruta del recurso gráfico del producto (ej. 'img/ricoh-mp301.png')."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha de creación del registro en la base de datos.")
    ]
    render_dict_table("products", "Catálogo principal de fotocopiadoras, impresoras, tóners y repuestos certificados Ricoh.", prod_cols)

    doc.add_page_break()

    # 3.4 maintenance_requests
    table_idx = 4
    maint_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador único de la solicitud de servicio técnico (ej. 'req_XXXX')."),
        ("client_id", "TEXT", "SÍ", "FK", "None", "users(id)", "-", "Llave foránea opcional hacia el usuario que generó la solicitud."),
        ("client_name", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Nombre del cliente o encargado que reporta el mantenimiento."),
        ("client_email", "TEXT", "NO", "-", "None", "Formato Email", "idx_requests_email", "Correo electrónico de contacto para notificaciones de servicio."),
        ("client_phone", "TEXT", "SÍ", "-", "None", "Min 7 chars", "-", "Línea telefónica para coordinación de la visita del técnico."),
        ("equipment", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Modelo o número de serie del equipo a intervenir (ej. 'Ricoh MP 4002')."),
        ("service_type", "TEXT", "NO", "-", "None", "Preventivo|Correctivo", "-", "Tipo de intervención técnica requerida."),
        ("desired_date", "TEXT", "NO", "-", "None", "YYYY-MM-DD", "-", "Fecha tentativa requerida por el cliente para la visita técnica."),
        ("desired_time", "TEXT", "NO", "-", "None", "HH:MM", "-", "Franja horaria solicitada para la visita (mañana o tarde)."),
        ("description", "TEXT", "SÍ", "-", "None", "None", "-", "Descripción detallada de la falla observada, ruidos o código de error SC."),
        ("status", "TEXT", "NO", "-", "'Pendiente'", "Pend|Conf|Proc|Comp|Canc", "idx_requests_status", "Estado administrativo del ciclo de vida de la orden técnica."),
        ("admin_notes", "TEXT", "SÍ", "-", "None", "None", "-", "Bitácora interna y notas técnicas registradas por el personal de soporte."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora del reporte de la solicitud."),
        ("updated_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora de la última actualización de estado.")
    ]
    render_dict_table("maintenance_requests", "Registro y seguimiento de servicios técnicos preventivos y correctivos para equipos de fotocopiado.", maint_cols)

    # 3.5 contact_messages
    table_idx = 5
    contact_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador único del mensaje recibido."),
        ("name", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Nombre de la persona o contacto corporativo remitente."),
        ("email", "TEXT", "NO", "-", "None", "Formato Email", "-", "Correo electrónico para envío de respuesta comercial."),
        ("phone", "TEXT", "NO", "-", "None", "Min 7 chars", "-", "Teléfono de contacto del remitente."),
        ("subject", "TEXT", "NO", "-", "None", "None", "-", "Asunto del mensaje o clasificación de la consulta."),
        ("message", "TEXT", "NO", "-", "None", "Min 10 chars", "-", "Cuerpo detallado del mensaje, solicitud de asesoría o PQR."),
        ("is_read", "INTEGER", "SÍ", "-", "0", "0 = No leído, 1 = Leído", "-", "Estado de visualización en la bandeja del panel administrativo."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora de radicación del mensaje.")
    ]
    render_dict_table("contact_messages", "Recepción de mensajes de contacto general, consultas corporativas y peticiones de clientes.", contact_cols)

    # 3.6 quotes
    table_idx = 6
    quotes_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador único de la cotización generada."),
        ("quote_code", "TEXT", "NO", "-", "None", "UNIQUE", "idx_quotes_code", "Código alfanumérico público de cotización (ej. 'COT-1A2B3C')."),
        ("client_name", "TEXT", "SÍ", "-", "None", "None", "-", "Nombre o empresa destinataria de la cotización."),
        ("client_email", "TEXT", "SÍ", "-", "None", "Formato Email", "-", "Correo del cliente para envío de la cotización formal."),
        ("client_phone", "TEXT", "SÍ", "-", "None", "None", "-", "Teléfono del contacto comercial."),
        ("items_json", "TEXT", "NO", "-", "None", "JSON Array", "-", "Estructura serializada con la lista de productos, precios y cantidades."),
        ("subtotal", "REAL", "NO", "-", "None", "gt 0 COP", "-", "Suma de los precios de los productos antes de impuestos."),
        ("iva", "REAL", "NO", "-", "None", "ge 0 COP (19%)", "-", "Valor liquidado del Impuesto al Valor Agregado (IVA 19%)."),
        ("total", "REAL", "NO", "-", "None", "gt 0 COP", "-", "Monto final liquidado en Pesos Colombianos."),
        ("notes", "TEXT", "SÍ", "-", "None", "None", "-", "Observaciones comerciales o condiciones de entrega pactadas."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha de generación; base para el cómputo de 15 días de vigencia.")
    ]
    render_dict_table("quotes", "Almacena las cotizaciones formales emitidas con liquidación tributaria legal del 19% de IVA.", quotes_cols)

    doc.add_page_break()

    # 3.7 counter_reports
    table_idx = 7
    counter_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador del reporte mensual de contadores."),
        ("client_id", "TEXT", "SÍ", "FK", "None", "users(id)", "-", "Llave foránea hacia el usuario corporativo bajo contrato de renting."),
        ("client_name", "TEXT", "NO", "-", "None", "None", "-", "Nombre de la empresa o cliente titular del equipo alquilado."),
        ("equipment_model", "TEXT", "NO", "-", "None", "None", "-", "Modelo del equipo Ricoh reportado (ej. 'Ricoh MP 5002')."),
        ("mono_counter", "INTEGER", "NO", "-", "None", "ge 0", "-", "Lectura del contador mecánico de impresiones blanco y negro."),
        ("color_counter", "INTEGER", "SÍ", "-", "0", "ge 0", "-", "Lectura del contador mecánico de impresiones full color."),
        ("report_month", "TEXT", "NO", "-", "None", "YYYY-MM", "-", "Mes y año correspondiente a la lectura reportada (ej. '2026-10')."),
        ("notes", "TEXT", "SÍ", "-", "None", "None", "-", "Observaciones sobre el estado del contador o cambio de tóner."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora exacta del envío del reporte.")
    ]
    render_dict_table("counter_reports", "Captura de lecturas mensuales de contadores para liquidación periódica del servicio de renting.", counter_cols)

    # 3.8 orders
    table_idx = 8
    orders_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador interno de la orden de compra."),
        ("order_code", "TEXT", "NO", "-", "None", "UNIQUE", "idx_orders_code", "Código público de seguimiento del pedido (ej. 'PED-2026-XXXX')."),
        ("client_id", "TEXT", "SÍ", "FK", "None", "users(id)", "-", "Llave foránea hacia el usuario si la compra fue autenticada."),
        ("client_name", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Nombre o razón social del comprador para despacho y facturación."),
        ("client_email", "TEXT", "NO", "-", "None", "Formato Email", "idx_orders_email", "Correo electrónico del cliente para envío de comprobantes."),
        ("client_phone", "TEXT", "NO", "-", "None", "Min 7 chars", "-", "Número de teléfono celular para coordinación de la entrega."),
        ("client_nit", "TEXT", "SÍ", "-", "None", "None", "-", "Número de Identificación Tributaria (NIT) o Cédula de Ciudadanía."),
        ("delivery_address", "TEXT", "NO", "-", "None", "Min 5 chars", "-", "Dirección física de entrega o instalación del equipo/suministro."),
        ("delivery_city", "TEXT", "NO", "-", "'Neiva, Huila'", "None", "-", "Ciudad y departamento de destino del despacho."),
        ("items_json", "TEXT", "NO", "-", "None", "JSON Array", "-", "Detalle serializado inmutable de los ítems adquiridos con precio histórico."),
        ("subtotal", "REAL", "NO", "-", "None", "gt 0 COP", "-", "Suma de los valores de los productos antes de impuestos."),
        ("iva", "REAL", "NO", "-", "None", "ge 0 COP", "-", "Valor liquidado del Impuesto al Valor Agregado (19%)."),
        ("total", "REAL", "NO", "-", "None", "gt 0 COP", "-", "Monto total a cancelar en Pesos Colombianos."),
        ("payment_method", "TEXT", "NO", "-", "None", "PSE|Tarjeta|Transf|Crédito", "-", "Canal de pago seleccionado por el cliente durante el checkout."),
        ("payment_status", "TEXT", "NO", "-", "'Aprobado'", "Aprobado|Pendiente|Rechazado", "-", "Estado de validación financiera de la transacción."),
        ("shipping_status", "TEXT", "NO", "-", "'En preparación'", "Prep|Desp|Camino|Entreg|Canc", "-", "Estado logístico de preparación y despacho del pedido."),
        ("notes", "TEXT", "SÍ", "-", "None", "None", "-", "Instrucciones especiales de entrega o datos de guía de transporte."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora de creación de la orden.")
    ]
    render_dict_table("orders", "Gestión de transacciones comerciales, pagos y seguimiento logístico del e-commerce.", orders_cols)

    # 3.9 notifications
    table_idx = 9
    notif_cols = [
        ("id", "TEXT", "NO", "PK", "None", "None", "PK_auto", "Identificador único de la notificación emitida."),
        ("user_id", "TEXT", "SÍ", "FK", "None", "users(id)", "-", "Llave foránea hacia el usuario destinatario de la alerta."),
        ("user_email", "TEXT", "NO", "-", "None", "Formato Email", "idx_notifications_user", "Correo del destinatario (permite entrega por cuenta o email)."),
        ("title", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Título corto y descriptivo del evento notificado."),
        ("message", "TEXT", "NO", "-", "None", "Min 2 chars", "-", "Mensaje detallado con la novedad o actualización."),
        ("type", "TEXT", "NO", "-", "'info'", "'info'|'order'|'maint'|'promo'", "-", "Categoría del evento para filtrado e icono visual."),
        ("link_url", "TEXT", "SÍ", "-", "None", "URL relativa", "-", "Ruta de navegación dentro de la plataforma al hacer clic en la alerta."),
        ("is_read", "INTEGER", "SÍ", "-", "0", "0 = No leída, 1 = Leída", "idx_notifications_user", "Estado de lectura por parte del usuario receptor."),
        ("created_at", "TIMESTAMP", "SÍ", "-", "CURRENT_TIMESTAMP", "ISO-8601 UTC", "-", "Fecha y hora de generación de la alerta.")
    ]
    render_dict_table("notifications", "Bandeja de notificaciones internas del sistema para pedidos, citas técnicas y avisos administrativos.", notif_cols)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ESTRATEGIA DE INDEXACIÓN Y RENDIMIENTO B-TREE
    # -------------------------------------------------------------
    doc.add_heading("4. Estrategia de Indexación y Rendimiento B-Tree", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Para garantizar tiempos de respuesta inferiores a 50 milisegundos en búsquedas complejas y prevenir escaneos completos "
        "de tabla (Full Table Scans), el esquema de SQLite incluye 8 índices B-Tree secundarios diseñados sobre las columnas "
        "de mayor selectividad y cardinalidad de filtro:"
    )

    t_idx = doc.add_table(rows=9, cols=5)
    t_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    idx_headers = ["Nombre del Índice", "Tabla", "Columnas Indexadas", "Tipo de Índice", "Propósito y Consulta Optimizada"]
    for c_idx, h in enumerate(idx_headers):
        t_idx.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_idx.rows[0], bg_color="0F4C81", is_header=True)

    idx_data = [
        ("idx_users_email", "users", "email", "B-Tree Secundario", "Optimiza la autenticación en 'POST /api/v1/auth/login' (búsqueda de usuario por email)."),
        ("idx_products_cat", "products", "category_slug", "B-Tree Secundario", "Acelera el filtrado del catálogo en 'GET /api/v1/products?category=fotocopiadoras'."),
        ("idx_requests_email", "maintenance_requests", "client_email", "B-Tree Secundario", "Permite auditoría rápida de solicitudes de servicio por cliente."),
        ("idx_requests_status", "maintenance_requests", "status", "B-Tree Secundario", "Optimiza la bandeja del panel administrativo para filtrar órdenes 'Pendientes'."),
        ("idx_quotes_code", "quotes", "quote_code", "B-Tree Secundario", "Permite la recuperación instantánea de una cotización mediante su código alfanumérico."),
        ("idx_orders_code", "orders", "order_code", "B-Tree Secundario", "Acelera el rastreo público del pedido en 'GET /api/v1/orders/{order_code}'."),
        ("idx_orders_email", "orders", "client_email", "B-Tree Secundario", "Agiliza la consulta del historial de compras del cliente autenticado."),
        ("idx_notifications_user", "notifications", "user_email, is_read", "B-Tree Compuesto", "Optimiza la consulta de alertas no leídas en el navbar: WHERE user_email = ? AND is_read = 0.")
    ]
    for idx, (c1, c2, c3, c4, c5) in enumerate(idx_data):
        row = t_idx.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(c1)
        row.cells[1].paragraphs[0].add_run(c2)
        row.cells[2].paragraphs[0].add_run(c3)
        row.cells[3].paragraphs[0].add_run(c4)
        row.cells[4].paragraphs[0].add_run(c5)
        format_row(row, bg_color="FFFFFF" if idx % 2 == 0 else "F8FAFC")

    # -------------------------------------------------------------
    # 5. POLÍTICAS DE MANTENIMIENTO, RESPALDOS Y RECUPERACIÓN
    # -------------------------------------------------------------
    doc.add_heading("5. Políticas de Mantenimiento, Respaldos y Recuperación", level=1)
    
    p = doc.add_paragraph()
    r = p.add_run("5.1 Procedimiento de Respaldo en Caliente (Hot Backup)\n")
    r.bold = True
    p.add_run(
        "Al operar en modo WAL, no es seguro realizar una copia directa mediante el explorador de archivos mientras el servidor Uvicorn "
        "esté en ejecución, debido a que parte de las transacciones pueden residir en memoria o en el archivo temporal 'syp.db-wal'. "
        "El estándar técnico definido para Fotocopiadoras SyP implementa la API de copia de seguridad en caliente nativa de SQLite:\n\n"
        "```python\n"
        "import sqlite3, shutil, datetime\n"
        "def backup_syp_database(source_path='syp.db', backup_dir='backups/'):\n"
        "    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')\n"
        "    dest_path = f'{backup_dir}/syp_backup_{timestamp}.db'\n"
        "    src_conn = sqlite3.connect(source_path)\n"
        "    dst_conn = sqlite3.connect(dest_path)\n"
        "    with dst_conn:\n"
        "        src_conn.backup(dst_conn, pages=100) # Copia atómica sin bloquear lectores\n"
        "    dst_conn.close()\n"
        "    src_conn.close()\n"
        "    print(f'[BACKUP OK] Respaldo generado en: {dest_path}')\n"
        "```\n"
        "Este procedimiento puede programarse diariamente mediante Cron (en Linux) o Tareas Programadas (en Windows) sin necesidad "
        "de desconectar el servidor ni interrumpir la navegación de los clientes."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.2 Rutinas de Mantenimiento (VACUUM, Integrity Check y Checkpoint)\n")
    r.bold = True
    p.add_run(
        "Para mantener el rendimiento óptimo del archivo 'syp.db' a lo largo del tiempo, se establecen tres rutinas obligatorias:\n"
        "1. Verificación de Integridad Física (Semanal): Ejecución del comando 'PRAGMA integrity_check;' y 'PRAGMA foreign_key_check;'. "
        "Debe retornar 'ok' garantizando que ningún puntero B-Tree esté corrupto.\n"
        "2. Vaciado del WAL a Disco Principal (Checkpoint Diario): Ejecución de 'PRAGMA wal_checkpoint(TRUNCATE);' para transferir todas "
        "las transacciones del archivo WAL hacia el archivo principal 'syp.db', reduciendo el tamaño del archivo de log a cero bytes.\n"
        "3. Desfragmentación y Compactación (Mensual): Ejecución de 'VACUUM;' para reorganizar el espacio en disco liberado tras la eliminación "
        "o actualización de registros, disminuyendo el tamaño físico del archivo en el almacenamiento del servidor."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. CONTROL DE APROBACIÓN Y FIRMAS
    # -------------------------------------------------------------
    doc.add_heading("6. Control de Aprobación y Firmas de Conformidad", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "Las firmas a continuación certifican que el modelo relacional, tipos de datos, restricciones e índices especificados "
        "en este documento corresponden fielmente a la implementación física de la base de datos de Fotocopiadoras SyP y satisfacen "
        "los requisitos de persistencia del proyecto:"
    )

    t_sig = doc.add_table(rows=3, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig_headers = ["Cliente / Representante Legal", "Desarrollador / Administrador DB", "Instructor / Evaluador Técnico"]
    for c_idx, h in enumerate(t_sig_headers):
        t_sig.rows[0].cells[c_idx].paragraphs[0].add_run(h)
    format_row(t_sig.rows[0], bg_color="0F4C81", is_header=True)

    sig_content = [
        ("Sra. Gladys Solano Murcia\nRepresentante Legal\nFotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Kevin Portela [POR CONFIRMAR]\nLíder de Persistencia & Backend\nProyecto Fotocopiadoras SyP\n\nFirma: _________________________\nFecha: _____ / _____ / 2026",
         "Instructor Evaluador [POR CONFIRMAR]\nEvaluador Etapa Productiva / Académica\nCentro de Formación Técnica\n\nFirma: _________________________\nFecha: _____ / _____ / 2026"),
        ("Conformidad de Datos de Negocio", "Conformidad Técnica y Modelo ER", "Aprobación y Validación Técnica")
    ]
    for r_idx, r_data in enumerate(sig_content):
        row = t_sig.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].add_run(val)
        format_row(row, bg_color="FFFFFF" if r_idx == 0 else "F8FAFC")

    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] Database Document generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_database_document()
