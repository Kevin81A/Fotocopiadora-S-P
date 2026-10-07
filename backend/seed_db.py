import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syp_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Category, Brand, Product, ServiceRequest

User = get_user_model()

def seed():
    print("[INFO] Iniciando migracion y poblado de base de datos para Fotocopiadora SyP...")

    # 1. Crear Superusuario Administrador
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@fotocopiadorasyp.com', 'admin123')
        print("[OK] Superusuario creado: admin / admin123")
    else:
        print("[INFO] Superusuario ya existia.")

    # 2. Categorías
    categories_data = [
        ('fotocopiadoras', 'Fotocopiadoras'),
        ('impresoras', 'Impresoras'),
        ('tintas', 'Tintas y Tóneres'),
        ('repuestos', 'Repuestos'),
        ('accesorios', 'Accesorios'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    cat_map = {}
    for slug, name in categories_data:
        cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
        cat_map[slug] = cat

    print(f"[OK] {len(cat_map)} Categorias sincronizadas.")

    # 3. Marcas
    brands_data = ['Ricoh', 'Kyocera', 'Canon', 'HP', 'Konica Minolta', 'Epson']
    brand_map = {}
    for bname in brands_data:
        brand, _ = Brand.objects.get_or_create(name=bname, defaults={'slug': bname.lower().replace(' ', '-')})
        brand_map[bname] = brand

    print(f"[OK] {len(brand_map)} Marcas registradas.")

    # 4. Productos
    products_data = [
        {
            'id_code': 'sp-2554c',
            'name': 'Multifuncional Láser Ricoh MP 2554',
            'cat': 'fotocopiadoras',
            'brand': 'Ricoh',
            'price': 3400000,
            'spec': '35 ppm · copia, imprime y escanea · hasta 20.000 pág/mes',
            'stock': 'ok',
            'models': 'MP 2554 / 3054 / 3554',
            'featured': True,
        },
        {
            'id_code': 'sp-600bn',
            'name': 'Multifuncional Láser B/N MP 301',
            'cat': 'fotocopiadoras',
            'brand': 'Ricoh',
            'price': 1850000,
            'spec': '31 ppm · dúplex automático · escáner a color',
            'stock': 'ok',
            'models': 'Aficio MP 301',
            'featured': True,
        },
        {
            'id_code': 'sp-c306',
            'name': 'Multifuncional Color Compacta C306',
            'cat': 'fotocopiadoras',
            'brand': 'Ricoh',
            'price': 2600000,
            'spec': '30 ppm · pantalla táctil 10.1" · red gigabit',
            'stock': 'ok',
            'models': 'MP C306 / C406 Color',
            'featured': True,
        },
        {
            'id_code': 'sp-m2040',
            'name': 'Kyocera Ecosys M2040dn Multifuncional',
            'cat': 'fotocopiadoras',
            'brand': 'Kyocera',
            'price': 2100000,
            'spec': '40 ppm B/N · tambor de larga duración (100.000 pág)',
            'stock': 'ok',
            'models': 'Ecosys M2040dn',
            'featured': True,
        },
        {
            'id_code': 'sp-p400',
            'name': 'Impresora Láser Monocromática HP M404',
            'cat': 'impresoras',
            'brand': 'HP',
            'price': 980000,
            'spec': '40 ppm · dúplex automático · bajo consumo',
            'stock': 'ok',
            'models': 'LaserJet Pro M404 / M428',
            'featured': False,
        },
        {
            'id_code': 'sp-p220c',
            'name': 'Impresora Color Ricoh SP C250',
            'cat': 'impresoras',
            'brand': 'Ricoh',
            'price': 1450000,
            'spec': '22 ppm color · WiFi y Ethernet integrados',
            'stock': 'ok',
            'models': 'MP C2003 / C2503 Color',
            'featured': False,
        },
        {
            'id_code': 'sp-ton301',
            'name': 'Tóner Compatible Ricoh MP 301 (Tipo 301)',
            'cat': 'tintas',
            'brand': 'Ricoh',
            'price': 34000,
            'spec': 'Rendimiento aprox. 8.000 páginas al 5%',
            'stock': 'ok',
            'models': 'Aficio MP 301',
            'featured': True,
        },
        {
            'id_code': 'sp-ton2554',
            'name': 'Tóner Negro Ricoh MP 2554 / 3054 / 3554',
            'cat': 'tintas',
            'brand': 'Ricoh',
            'price': 78000,
            'spec': 'Rendimiento aprox. 24.000 páginas',
            'stock': 'ok',
            'models': 'MP 2554 / 3054 / 3554',
            'featured': True,
        },
        {
            'id_code': 'sp-ton2040',
            'name': 'Tóner Kyocera TK-1175 Compatible',
            'cat': 'tintas',
            'brand': 'Kyocera',
            'price': 65000,
            'spec': 'Rendimiento aprox. 12.000 páginas',
            'stock': 'ok',
            'models': 'Ecosys M2040dn, Ecosys M2135dn',
            'featured': False,
        },
        {
            'id_code': 'sp-ton4501c',
            'name': 'Kit Tóner Color Ricoh MP C306 / C406 (CMYK)',
            'cat': 'tintas',
            'brand': 'Ricoh',
            'price': 216000,
            'spec': '17.000 pág. negro / 12.000 pág. colores',
            'stock': 'ok',
            'models': 'MP C306 / C406 Color',
            'featured': False,
        },
        {
            'id_code': 'sp-recarga1000',
            'name': 'Polvo de Tóner Universal 1000gr Premium',
            'cat': 'tintas',
            'brand': 'Ricoh',
            'price': 95000,
            'spec': 'Micro-filtrado de alta densidad · negro profundo',
            'stock': 'ok',
            'models': 'Aficio MP 301, MP 2554 / 3054 / 3554, Ecosys M2040dn, imageRUNNER 2206 / 2520',
            'featured': False,
        },
        {
            'id_code': 'sp-cil2554',
            'name': 'Cilindro Tambor OPC Ricoh MP 2554 / 3554',
            'cat': 'repuestos',
            'brand': 'Ricoh',
            'price': 61000,
            'spec': 'Duración certificada 60.000 páginas',
            'stock': 'ok',
            'models': 'MP 2554 / 3054 / 3554',
            'featured': False,
        },
        {
            'id_code': 'sp-cil301',
            'name': 'Cilindro OPC + Cuchilla Ricoh MP 301',
            'cat': 'repuestos',
            'brand': 'Ricoh',
            'price': 48000,
            'spec': 'Kit completo de revelado y limpieza',
            'stock': 'ok',
            'models': 'Aficio MP 301',
            'featured': False,
        },
        {
            'id_code': 'sp-banda',
            'name': 'Banda de Transferencia Ricoh MP C2503 / C306',
            'cat': 'repuestos',
            'brand': 'Ricoh',
            'price': 280000,
            'spec': 'Vida útil 120.000–150.000 copias',
            'stock': 'ok',
            'models': 'MP C306 / C406 Color, MP C2003 / C2503 Color',
            'featured': False,
        },
        {
            'id_code': 'sp-correa',
            'name': 'Gomas de Alimentación de Papel (Pick Up Rollers)',
            'cat': 'repuestos',
            'brand': 'Ricoh',
            'price': 28000,
            'spec': 'Set x3 unidades antideslizantes',
            'stock': 'ok',
            'models': 'Aficio MP 301, MP 2554 / 3054 / 3554, Ecosys M2040dn',
            'featured': False,
        },
        {
            'id_code': 'sp-kitstd',
            'name': 'Mantenimiento Preventivo Completo en Taller',
            'cat': 'mantenimiento',
            'brand': 'Ricoh',
            'price': 120000,
            'spec': 'Desarme, soplado, lubricación y calibración óptica',
            'stock': 'ok',
            'models': 'Aficio MP 301, MP 2554 / 3054 / 3554, Ecosys M2040dn',
            'featured': True,
        },
        {
            'id_code': 'sp-visita',
            'name': 'Visita Técnica de Emergencia / Diagnóstico',
            'cat': 'mantenimiento',
            'brand': 'Ricoh',
            'price': 45000,
            'spec': 'Atención prioritaria en sitio · Neiva y perímetro',
            'stock': 'ok',
            'models': 'Aficio MP 301, MP 2554 / 3054 / 3554, Ecosys M2040dn, imageRUNNER 2206 / 2520',
            'featured': True,
        },
    ]

    for p in products_data:
        Product.objects.update_or_create(
            id_code=p['id_code'],
            defaults={
                'name': p['name'],
                'category': cat_map[p['cat']],
                'brand': brand_map.get(p['brand']),
                'price': p['price'],
                'spec': p['spec'],
                'stock_status': p['stock'],
                'compatible_models': p['models'],
                'is_featured': p['featured'],
            }
        )

    print(f"[OK] {len(products_data)} Productos e insumos cargados en la Base de Datos.")

    # 5. Solicitud de prueba inicial
    if ServiceRequest.objects.count() == 0:
        ServiceRequest.objects.create(
            client_name='Carlos Mendoza (Empresa Huila)',
            client_email='cmendoza@empresa.com',
            client_phone='3154879652',
            equipment='Ricoh MP 2554',
            service_type='Mantenimiento preventivo',
            scheduled_date='2026-10-15',
            scheduled_time='09:00',
            description='Mantenimiento preventivo semestral y cambio de tóner negro.',
            status='Confirmada',
            admin_notes='Asignado técnico Juan Sebastián Portela.'
        )
        print("[OK] Solicitud tecnica de prueba creada.")

    print("\n[LISTO] Base de datos de Fotocopiadora SyP lista y poblada con exito!")

if __name__ == '__main__':
    seed()
