"""
Fotocopiadora SyP — Database Seeding Script (Users, Products & Categories)
"""
import uuid
from database import get_db, init_db
from security import hash_password

CATEGORIES = [
    {"id": "cat_1", "slug": "fotocopiadoras", "name": "Fotocopiadoras", "sort_order": 1},
    {"id": "cat_2", "slug": "impresoras", "name": "Impresoras", "sort_order": 2},
    {"id": "cat_3", "slug": "tintas", "name": "Tintas y Tóneres", "sort_order": 3},
    {"id": "cat_4", "slug": "repuestos", "name": "Repuestos", "sort_order": 4},
    {"id": "cat_5", "slug": "accesorios", "name": "Accesorios", "sort_order": 5},
    {"id": "cat_6", "slug": "mantenimiento", "name": "Mantenimiento", "sort_order": 6},
]

PRODUCTS = [
    {
        "id": "sp-2554c",
        "name": "Multifuncional Láser Ricoh MP 2554",
        "category_slug": "fotocopiadoras",
        "brand": "Ricoh",
        "price": 3400000.0,
        "spec": "35 ppm · copia, imprime y escanea · hasta 20.000 pág/mes",
        "stock_status": "ok",
        "rating": 4.9,
        "reviews_count": 42,
        "badge": "Más Vendido",
        "discount_percent": 10,
        "speed": "35 ppm",
        "duty_cycle": "20.000 pág/mes",
        "paper_size": "Carta, Oficio, Doble Carta (A3 / A4)",
        "connectivity": "Red Gigabit Ethernet, USB 2.0, SD Card",
        "functions": "Copia, Impresión de Red, Escáner Dúplex Color",
        "toner_yield": "24.000 páginas al 5%",
        "cost_per_page": "$8 COP / página",
        "compatible_ids": "sp-ton2554, sp-cil2554, sp-correa",
        "image_url": "img/prod_copier.jpg",
    },
    {
        "id": "sp-600bn",
        "name": "Multifuncional Láser B/N Ricoh MP 301 SPF",
        "category_slug": "fotocopiadoras",
        "brand": "Ricoh",
        "price": 1850000.0,
        "spec": "31 ppm · dúplex automático · escáner a color",
        "stock_status": "ok",
        "rating": 4.8,
        "reviews_count": 36,
        "badge": "Recomendado",
        "discount_percent": 0,
        "speed": "31 ppm",
        "duty_cycle": "10.000 pág/mes",
        "paper_size": "Carta, Oficio, Legal (A4)",
        "connectivity": "Red Ethernet 10/100, USB 2.0",
        "functions": "Copia, Impresión, Escáner a Color, Dúplex",
        "toner_yield": "8.000 páginas",
        "cost_per_page": "$9 COP / página",
        "compatible_ids": "sp-ton301, sp-cil301, sp-correa",
        "image_url": "img/prod_copier.jpg",
    },
    {
        "id": "sp-c306",
        "name": "Multifuncional Color Ricoh MP C306 HD",
        "category_slug": "fotocopiadoras",
        "brand": "Ricoh",
        "price": 2600000.0,
        "spec": "30 ppm · pantalla táctil 10.1\" · red gigabit",
        "stock_status": "ok",
        "rating": 5.0,
        "reviews_count": 19,
        "badge": "Color HD",
        "discount_percent": 0,
        "speed": "30 ppm Color / B&N",
        "duty_cycle": "15.000 pág/mes",
        "paper_size": "Carta, Oficio, Folio",
        "connectivity": "Pantalla Smart 10.1\", Gigabit LAN, WiFi opcional",
        "functions": "Multifuncional Color Láser, Escáner de Alta Definición",
        "toner_yield": "17.000 pág (Negro) / 12.000 (Color)",
        "cost_per_page": "$35 COP / pág color",
        "compatible_ids": "sp-ton4501c, sp-banda",
        "image_url": "img/prod_copier.jpg",
    },
    {
        "id": "sp-5054",
        "name": "Multifuncional Láser Ricoh MP 5054 Industrial",
        "category_slug": "fotocopiadoras",
        "brand": "Ricoh",
        "price": 4900000.0,
        "spec": "50 ppm B/N · alto volumen industrial · hasta 50.000 pág/mes",
        "stock_status": "ok",
        "rating": 4.9,
        "reviews_count": 58,
        "badge": "Alto Volumen",
        "discount_percent": 5,
        "speed": "50 ppm",
        "duty_cycle": "50.000 pág/mes",
        "paper_size": "Carta, Oficio, Doble Carta (A3/A4)",
        "connectivity": "Red Gigabit, USB Host 2.0, Disco Duro 320GB",
        "functions": "Copia, Impresión de Red, Escaneo Dúplex simultáneo 180 ipm",
        "toner_yield": "37.000 páginas",
        "cost_per_page": "$6 COP / página",
        "compatible_ids": "sp-ton5054, sp-cil2554, sp-correa",
        "image_url": "img/prod_copier.jpg",
    },
    {
        "id": "sp-p501",
        "name": "Impresora Láser Monocromática Ricoh P 501",
        "category_slug": "impresoras",
        "brand": "Ricoh",
        "price": 1350000.0,
        "spec": "45 ppm · dúplex automático · red gigabit y bajo consumo",
        "stock_status": "ok",
        "rating": 4.8,
        "reviews_count": 24,
        "badge": "Alto Rendimiento",
        "discount_percent": 0,
        "speed": "45 ppm",
        "duty_cycle": "80.000 pág/mes",
        "paper_size": "Carta, Oficio, Ejecutivo",
        "connectivity": "Red Gigabit Ethernet, USB 2.0",
        "functions": "Impresora Láser Monocromática de Alta Velocidad",
        "toner_yield": "14.000 páginas",
        "cost_per_page": "$8 COP / página",
        "compatible_ids": "sp-recarga1000",
        "image_url": "img/prod_printer.jpg",
    },
    {
        "id": "sp-ton301",
        "name": "Tóner Ricoh MP 301 (Tipo 301 / 1270D)",
        "category_slug": "tintas",
        "brand": "Ricoh",
        "price": 34000.0,
        "spec": "Rendimiento aprox. 8.000 páginas al 5%",
        "stock_status": "ok",
        "rating": 4.9,
        "reviews_count": 95,
        "badge": "Top Ventas",
        "discount_percent": 0,
        "image_url": "img/prod_toner.jpg",
    },
    {
        "id": "sp-ton2554",
        "name": "Tóner Negro Ricoh MP 2554 / 3054 / 3554",
        "category_slug": "tintas",
        "brand": "Ricoh",
        "price": 78000.0,
        "spec": "Rendimiento aprox. 24.000 páginas",
        "stock_status": "ok",
        "rating": 5.0,
        "reviews_count": 73,
        "badge": "Original / Homologado",
        "discount_percent": 0,
        "image_url": "img/prod_toner.jpg",
    },
    {
        "id": "sp-cil2554",
        "name": "Cilindro Tambor OPC Ricoh MP 2554 / 3554 / 5054",
        "category_slug": "repuestos",
        "brand": "Ricoh",
        "price": 61000.0,
        "spec": "Duración certificada 60.000 páginas",
        "stock_status": "ok",
        "rating": 4.9,
        "reviews_count": 38,
        "badge": "Alta Duración",
        "discount_percent": 0,
        "image_url": "img/prod_supplies.jpg",
    },
    {
        "id": "sp-correa",
        "name": "Gomas de Alimentación de Papel Ricoh (Pick Up Rollers)",
        "category_slug": "repuestos",
        "brand": "Ricoh",
        "price": 28000.0,
        "spec": "Set x3 unidades antideslizantes originales Ricoh",
        "stock_status": "ok",
        "rating": 4.7,
        "reviews_count": 41,
        "badge": "",
        "discount_percent": 0,
        "image_url": "img/prod_supplies.jpg",
    },
    {
        "id": "sp-kitstd",
        "name": "Mantenimiento Preventivo Completo Ricoh en Taller",
        "category_slug": "mantenimiento",
        "brand": "Ricoh",
        "price": 120000.0,
        "spec": "Desarme, soplado, lubricación y calibración óptica para equipos Ricoh",
        "stock_status": "ok",
        "rating": 5.0,
        "reviews_count": 83,
        "badge": "Garantizado",
        "discount_percent": 0,
        "image_url": "img/service_workshop.jpg",
    },
    {
        "id": "sp-visita",
        "name": "Visita Técnica de Emergencia / Diagnóstico Ricoh",
        "category_slug": "mantenimiento",
        "brand": "Ricoh",
        "price": 45000.0,
        "spec": "Atención prioritaria en sitio para equipos Ricoh · Neiva y perímetro",
        "stock_status": "ok",
        "rating": 4.9,
        "reviews_count": 97,
        "badge": "Express < 24h",
        "discount_percent": 0,
        "image_url": "img/hero_service.jpg",
    },
]

def seed_database():
    init_db()
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Insertar Categorías
        for c in CATEGORIES:
            cursor.execute("""
            INSERT OR REPLACE INTO categories (id, slug, name, sort_order)
            VALUES (?, ?, ?, ?)
            """, (c["id"], c["slug"], c["name"], c["sort_order"]))

        # 2. Insertar Productos
        for p in PRODUCTS:
            cursor.execute("""
            INSERT OR REPLACE INTO products (
                id, name, category_slug, brand, price, spec, stock_status, rating,
                reviews_count, badge, discount_percent, speed, duty_cycle, paper_size,
                connectivity, functions, toner_yield, cost_per_page, compatible_ids, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"], p["name"], p["category_slug"], p.get("brand", "Ricoh"), p["price"],
                p["spec"], p.get("stock_status", "ok"), p.get("rating", 4.9), p.get("reviews_count", 25),
                p.get("badge", ""), p.get("discount_percent", 0), p.get("speed"), p.get("duty_cycle"),
                p.get("paper_size"), p.get("connectivity"), p.get("functions"), p.get("toner_yield"),
                p.get("cost_per_page"), p.get("compatible_ids"), p.get("image_url")
            ))

        # 3. Insertar Usuarios Administrativos y Técnicos
        admin_hash = hash_password("admin123")
        gladys_hash = hash_password("gladys2026")
        juan_hash = hash_password("juan2026")
        demo_client_hash = hash_password("cliente123")

        cursor.execute("""
        INSERT OR REPLACE INTO users (id, email, password_hash, name, phone, role, is_active)
        VALUES 
        ('usr_admin', 'admin@sypfotocopiadoras.com', ?, 'Administración SyP Central', '+57 314 380 4967', 'admin', 1),
        ('usr_gladys', 'gladys.solano@sypfotocopiadoras.com', ?, 'Gladys Solano Murcia', '+57 314 380 4967', 'admin', 1),
        ('usr_juan', 'juan.portela@sypfotocopiadoras.com', ?, 'Juan Sebastián Portela', '+57 317 820 4193', 'admin', 1),
        ('usr_cliente_demo', 'cliente@notaria2neiva.com', ?, 'Dra. Carmen Cecilia Andrade', '+57 310 555 1234', 'cliente', 1)
        """, (admin_hash, gladys_hash, juan_hash, demo_client_hash))

        # 4. Solicitudes de servicio técnico de demostración
        cursor.execute("""
        INSERT OR REPLACE INTO maintenance_requests (
            id, client_id, client_name, client_email, client_phone, equipment, service_type, desired_date, desired_time, description, status, admin_notes
        ) VALUES
        ('req_101', 'usr_cliente_demo', 'Dra. Carmen Cecilia Andrade', 'cliente@notaria2neiva.com', '+57 310 555 1234', 'Ricoh MP 2554', 'Mantenimiento preventivo', '2026-10-15', '09:00', 'Mantenimiento preventivo semestral de 20.000 copias.', 'Confirmada', 'Técnico asignado: Juan Sebastián Portela'),
        ('req_102', NULL, 'Miller González', 'miller.gonzalez@colegiocampestre.edu.co', '+57 312 444 8899', 'Ricoh MP 5054 Industrial', 'Mantenimiento correctivo', '2026-10-16', '14:30', 'Error SC 542 en pantalla tras corte de luz en el colegio.', 'En proceso', 'Revisión de termistores de fusión en sitio programada.'),
        ('req_103', NULL, 'Sandra Milena Rojas', 'sandra.rojas@papeleriatoma.com', '+57 315 999 0011', 'Ricoh MP 301 SPF', 'Diagnóstico', '2026-10-18', '10:00', 'Atascos continuos en bandeja 1 al tomar papel bond de 75g.', 'Pendiente', '')
        """)

        print(f"[SyP Seed] Successfully seeded {len(CATEGORIES)} categories, {len(PRODUCTS)} products, 4 users and 3 service requests.")

if __name__ == "__main__":
    seed_database()
