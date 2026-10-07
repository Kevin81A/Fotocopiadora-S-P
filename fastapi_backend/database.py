"""
Fotocopiadora SyP — Database Layer (SQLite + Thread-safe Connection Pool)
"""
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syp.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Tabla de Usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'cliente',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

        # 2. Tabla de Categorías
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            icon_svg TEXT,
            sort_order INTEGER DEFAULT 0
        )
        """)

        # 3. Tabla de Productos y Repuestos Ricoh
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category_slug TEXT NOT NULL,
            brand TEXT NOT NULL DEFAULT 'Ricoh',
            price REAL NOT NULL,
            spec TEXT NOT NULL,
            stock_status TEXT NOT NULL DEFAULT 'ok',
            is_active INTEGER NOT NULL DEFAULT 1,
            rating REAL DEFAULT 4.9,
            reviews_count INTEGER DEFAULT 25,
            badge TEXT,
            discount_percent INTEGER DEFAULT 0,
            speed TEXT,
            duty_cycle TEXT,
            paper_size TEXT,
            connectivity TEXT,
            functions TEXT,
            toner_yield TEXT,
            cost_per_page TEXT,
            compatible_ids TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_slug) REFERENCES categories(slug)
        )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_cat ON products(category_slug)")

        # 4. Tabla de Solicitudes de Servicio Técnico
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id TEXT PRIMARY KEY,
            client_id TEXT,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            client_phone TEXT,
            equipment TEXT NOT NULL,
            service_type TEXT NOT NULL,
            desired_date TEXT NOT NULL,
            desired_time TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Pendiente',
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users(id)
        )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_requests_email ON maintenance_requests(client_email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_requests_status ON maintenance_requests(status)")

        # 5. Tabla de Mensajes de Contacto
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 6. Tabla de Cotizaciones Guardadas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id TEXT PRIMARY KEY,
            quote_code TEXT UNIQUE NOT NULL,
            client_name TEXT,
            client_email TEXT,
            client_phone TEXT,
            items_json TEXT NOT NULL,
            subtotal REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_quotes_code ON quotes(quote_code)")

        # 7. Tabla de Reporte de Contadores de Copias (Renting)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter_reports (
            id TEXT PRIMARY KEY,
            client_id TEXT,
            client_name TEXT NOT NULL,
            equipment_model TEXT NOT NULL,
            mono_counter INTEGER NOT NULL,
            color_counter INTEGER DEFAULT 0,
            report_month TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users(id)
        )
        """)

        # 8. Tabla de Pedidos y Transacciones de E-commerce
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            order_code TEXT UNIQUE NOT NULL,
            client_id TEXT,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            client_nit TEXT,
            delivery_address TEXT NOT NULL,
            delivery_city TEXT NOT NULL DEFAULT 'Neiva, Huila',
            items_json TEXT NOT NULL,
            subtotal REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_status TEXT NOT NULL DEFAULT 'Aprobado',
            shipping_status TEXT NOT NULL DEFAULT 'En preparación',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users(id)
        )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_code ON orders(order_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_email ON orders(client_email)")

        # 9. Tabla de Notificaciones en Tiempo Real
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            user_email TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'info',
            link_url TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_email, is_read)")

        print("[SyP DB] Database initialized successfully at:", DB_PATH)

if __name__ == "__main__":
    init_db()
