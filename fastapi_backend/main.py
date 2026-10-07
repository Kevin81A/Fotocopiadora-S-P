"""
Fotocopiadora SyP — REST API Server (FastAPI + JWT Authentication + SQLite)
"""
import uuid
import json
import csv
import io
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from database import get_db, init_db
from security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_optional_current_user,
    require_admin,
)
from models import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    AuthTokenResponse,
    ProductResponse,
    ProductCreate,
    ProductBase,
    MaintenanceRequestCreate,
    MaintenanceRequestResponse,
    MaintenanceStatusUpdate,
    ContactMessageCreate,
    QuoteCreate,
    QuoteResponse,
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse,
    CounterReportCreate,
    NotificationCreate,
    NotificationResponse,
    AnalyticsOverviewResponse,
)

# Inicializar Base de Datos al arrancar
init_db()

app = FastAPI(
    title="Fotocopiadora SyP — API REST Oficial",
    description="Servidor API seguro para E-commerce, Catálogo Ricoh, Mantenimiento Técnico y Autenticación JWT.",
    version="1.0.0",
)

# Habilitar CORS para peticiones desde el frontend web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 0. NOTIFICATION HELPERS (Disparadores automáticos)
# ============================================================
SHIPPING_EMOJI = {
    "En preparación": "📦", "Despachado": "🚚", "En camino": "🛵",
    "Entregado": "✅", "Cancelado": "❌",
}
MAINT_EMOJI = {
    "Pendiente": "⏳", "Confirmada": "📅", "En proceso": "🔧",
    "Completada": "✅", "Cancelada": "❌",
}

def ricoh_label(equipment: str) -> str:
    """Evita duplicar la marca ('Ricoh Ricoh MP 2554')."""
    eq = (equipment or "").strip()
    return eq if eq.lower().startswith("ricoh") else f"Ricoh {eq}"

def create_notification(cursor, user_email: str, title: str, message: str,
                        notif_type: str = "info", link_url: Optional[str] = None,
                        user_id: Optional[str] = None) -> Optional[str]:
    """Inserta una notificación usando el cursor de la transacción en curso."""
    if not user_email:
        return None
    email_norm = user_email.lower().strip()
    if not user_id:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email_norm,))
        u = cursor.fetchone()
        user_id = u["id"] if u else None
    notif_id = f"ntf_{uuid.uuid4().hex[:12]}"
    cursor.execute("""
    INSERT INTO notifications (id, user_id, user_email, title, message, type, link_url, is_read)
    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
    """, (notif_id, user_id, email_norm, title[:150], message, notif_type, link_url))
    return notif_id

def notify_admins(cursor, title: str, message: str, notif_type: str = "system",
                  link_url: Optional[str] = None) -> None:
    """Envía la misma notificación a todos los usuarios con rol administrativo."""
    cursor.execute("SELECT id, email FROM users WHERE role IN ('admin', 'tecnico', 'ventas') AND is_active = 1")
    for a in cursor.fetchall():
        create_notification(cursor, a["email"], title, message, notif_type, link_url, a["id"])

# ============================================================
# 1. HEALTH & METRICS ENDPOINTS
# ============================================================
@app.get("/api/v1/health")
def health_check():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM products WHERE is_active = 1")
        products_cnt = cursor.fetchone()["cnt"]
        cursor.execute("SELECT COUNT(*) as cnt FROM maintenance_requests")
        requests_cnt = cursor.fetchone()["cnt"]
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        users_cnt = cursor.fetchone()["cnt"]
        cursor.execute("SELECT COUNT(*) as cnt FROM orders")
        orders_cnt = cursor.fetchone()["cnt"]
        cursor.execute("SELECT COUNT(*) as cnt FROM quotes")
        quotes_cnt = cursor.fetchone()["cnt"]
    
    return {
        "status": "online",
        "service": "Fotocopiadora SyP Backend API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": "connected (SQLite WAL)",
        "stats": {
            "active_products": products_cnt,
            "maintenance_requests": requests_cnt,
            "registered_users": users_cnt,
            "orders": orders_cnt,
            "quotes": quotes_cnt,
        }
    }

# ============================================================
# 2. AUTHENTICATION & USERS ENDPOINTS (JWT)
# ============================================================
@app.post("/api/v1/auth/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest):
    email_norm = payload.email.lower().strip()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email_norm,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta registrada con este correo electrónico.",
            )
        
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        pwd_hash = hash_password(payload.password)
        
        cursor.execute("""
        INSERT INTO users (id, email, password_hash, name, phone, role, is_active)
        VALUES (?, ?, ?, ?, ?, 'cliente', 1)
        """, (user_id, email_norm, pwd_hash, payload.name.strip(), payload.phone.strip()))
        
        # Generar token JWT
        token_data = {"sub": email_norm, "id": user_id, "name": payload.name, "role": "cliente"}
        access_token = create_access_token(token_data)
        
        user_res = UserResponse(
            id=user_id,
            name=payload.name,
            email=email_norm,
            phone=payload.phone,
            role="cliente",
            is_active=True,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        
        return AuthTokenResponse(access_token=access_token, user=user_res)

@app.post("/api/v1/auth/login", response_model=AuthTokenResponse)
def login_user(payload: UserLoginRequest):
    email_norm = payload.email.lower().strip()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, email, password_hash, name, phone, role, is_active, created_at 
        FROM users WHERE email = ?
        """, (email_norm,))
        user = cursor.fetchone()
        
        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo electrónico o contraseña incorrectos.",
            )
        
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta cuenta ha sido inhabilitada. Contacta a soporte.",
            )
        
        # Actualizar last_login
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user["id"],))
        
        token_data = {
            "sub": user["email"],
            "id": user["id"],
            "name": user["name"],
            "role": user["role"],
        }
        access_token = create_access_token(token_data)
        
        user_res = UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            phone=user["phone"],
            role=user["role"],
            is_active=bool(user["is_active"]),
            created_at=str(user["created_at"]) if user["created_at"] else None,
        )
        
        return AuthTokenResponse(access_token=access_token, user=user_res)

@app.get("/api/v1/auth/me", response_model=UserResponse)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

# ============================================================
# 3. PRODUCTS & CATALOG ENDPOINTS (Ricoh)
# ============================================================
@app.get("/api/v1/products", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    include_inactive: bool = False,
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if not include_inactive:
            query += " AND is_active = 1"
        
        if category and category != "all":
            query += " AND category_slug = ?"
            params.append(category)
        
        if search:
            query += " AND (name LIKE ? OR spec LIKE ? OR compatible_ids LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
        
        query += " ORDER BY price DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for r in rows:
            results.append(ProductResponse(
                id=r["id"],
                name=r["name"],
                category_slug=r["category_slug"],
                brand=r["brand"] or "Ricoh",
                price=float(r["price"]),
                spec=r["spec"],
                stock_status=r["stock_status"] or "ok",
                is_active=bool(r["is_active"]),
                rating=float(r["rating"] or 4.9),
                reviews_count=int(r["reviews_count"] or 25),
                badge=r["badge"] or "",
                discount_percent=int(r["discount_percent"] or 0),
                speed=r["speed"],
                duty_cycle=r["duty_cycle"],
                paper_size=r["paper_size"],
                connectivity=r["connectivity"],
                functions=r["functions"],
                toner_yield=r["toner_yield"],
                cost_per_page=r["cost_per_page"],
                compatible_ids=r["compatible_ids"],
                image_url=r["image_url"],
                created_at=str(r["created_at"]) if r["created_at"] else None,
            ))
        return results

@app.get("/api/v1/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        r = cursor.fetchone()
        if not r:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        
        return ProductResponse(
            id=r["id"],
            name=r["name"],
            category_slug=r["category_slug"],
            brand=r["brand"] or "Ricoh",
            price=float(r["price"]),
            spec=r["spec"],
            stock_status=r["stock_status"] or "ok",
            is_active=bool(r["is_active"]),
            rating=float(r["rating"] or 4.9),
            reviews_count=int(r["reviews_count"] or 25),
            badge=r["badge"] or "",
            discount_percent=int(r["discount_percent"] or 0),
            speed=r["speed"],
            duty_cycle=r["duty_cycle"],
            paper_size=r["paper_size"],
            connectivity=r["connectivity"],
            functions=r["functions"],
            toner_yield=r["toner_yield"],
            cost_per_page=r["cost_per_page"],
            compatible_ids=r["compatible_ids"],
            image_url=r["image_url"],
            created_at=str(r["created_at"]) if r["created_at"] else None,
        )

@app.post("/api/v1/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, admin_user: dict = Depends(require_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (payload.id,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese ID.")
        
        cursor.execute("""
        INSERT INTO products (
            id, name, category_slug, brand, price, spec, stock_status, is_active,
            rating, reviews_count, badge, discount_percent, speed, duty_cycle,
            paper_size, connectivity, functions, toner_yield, cost_per_page,
            compatible_ids, image_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payload.id, payload.name, payload.category_slug, payload.brand, payload.price,
            payload.spec, payload.stock_status, payload.rating, payload.reviews_count,
            payload.badge, payload.discount_percent, payload.speed, payload.duty_cycle,
            payload.paper_size, payload.connectivity, payload.functions, payload.toner_yield,
            payload.cost_per_page, payload.compatible_ids, payload.image_url
        ))
        
        return ProductResponse(id=payload.id, is_active=True, **payload.model_dump())

@app.put("/api/v1/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, payload: ProductBase, admin_user: dict = Depends(require_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        
        cursor.execute("""
        UPDATE products SET
            name = ?, category_slug = ?, brand = ?, price = ?, spec = ?,
            stock_status = ?, rating = ?, reviews_count = ?, badge = ?,
            discount_percent = ?, speed = ?, duty_cycle = ?, paper_size = ?,
            connectivity = ?, functions = ?, toner_yield = ?, cost_per_page = ?,
            compatible_ids = ?, image_url = ?
        WHERE id = ?
        """, (
            payload.name, payload.category_slug, payload.brand, payload.price, payload.spec,
            payload.stock_status, payload.rating, payload.reviews_count, payload.badge,
            payload.discount_percent, payload.speed, payload.duty_cycle, payload.paper_size,
            payload.connectivity, payload.functions, payload.toner_yield, payload.cost_per_page,
            payload.compatible_ids, payload.image_url, product_id
        ))
        
        return ProductResponse(id=product_id, is_active=True, **payload.model_dump())

# ============================================================
# 4. MAINTENANCE REQUESTS ENDPOINTS (Servicio Técnico)
# ============================================================
@app.post("/api/v1/requests", response_model=MaintenanceRequestResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_request(
    payload: MaintenanceRequestCreate,
    current_user: Optional[dict] = Depends(get_optional_current_user) # Flexible para cliente logueado o invitado
):
    req_id = f"req_{uuid.uuid4().hex[:8]}"
    
    client_name = payload.client_name or (current_user.get("name") if current_user else "Cliente Web")
    client_email = payload.client_email or (current_user.get("email") if current_user else "contacto@cliente.com")
    client_phone = payload.client_phone or (current_user.get("phone") if current_user else "")
    client_id = current_user.get("id") if current_user else None
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO maintenance_requests (
            id, client_id, client_name, client_email, client_phone, equipment,
            service_type, desired_date, desired_time, description, status, admin_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pendiente', '')
        """, (
            req_id, client_id, client_name, client_email, client_phone,
            payload.equipment, payload.service_type, payload.desired_date,
            payload.desired_time, payload.description or ""
        ))

        # Disparadores automáticos
        create_notification(
            cursor, client_email,
            f"🔧 Solicitud {req_id} recibida",
            f"Agendamos tu {payload.service_type} para el {ricoh_label(payload.equipment)} el "
            f"{payload.desired_date} ({payload.desired_time}). Un técnico confirmará pronto.",
            "maintenance", "/cuenta.html#solicitudes", client_id
        )
        notify_admins(
            cursor, f"🛠️ Nueva solicitud técnica {req_id}",
            f"{client_name} · {ricoh_label(payload.equipment)} · {payload.service_type} · {payload.desired_date}",
            "maintenance", "/admin.html#requests"
        )
        
        return MaintenanceRequestResponse(
            id=req_id,
            client_id=client_id,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            equipment=payload.equipment,
            service_type=payload.service_type,
            desired_date=payload.desired_date,
            desired_time=payload.desired_time,
            description=payload.description,
            status="Pendiente",
            admin_notes="",
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

@app.get("/api/v1/requests/my", response_model=List[MaintenanceRequestResponse])
def get_my_requests(current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM maintenance_requests 
        WHERE client_id = ? OR client_email = ? 
        ORDER BY created_at DESC
        """, (current_user["id"], current_user["email"]))
        rows = cursor.fetchall()
        
        return [
            MaintenanceRequestResponse(
                id=r["id"],
                client_id=r["client_id"],
                client_name=r["client_name"],
                client_email=r["client_email"],
                client_phone=r["client_phone"],
                equipment=r["equipment"],
                service_type=r["service_type"],
                desired_date=r["desired_date"],
                desired_time=r["desired_time"],
                description=r["description"],
                status=r["status"],
                admin_notes=r["admin_notes"],
                created_at=str(r["created_at"]) if r["created_at"] else None,
                updated_at=str(r["updated_at"]) if r["updated_at"] else None,
            ) for r in rows
        ]

@app.get("/api/v1/requests", response_model=List[MaintenanceRequestResponse])
def list_all_requests(
    status_filter: Optional[str] = None,
    admin_user: dict = Depends(require_admin)
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM maintenance_requests WHERE 1=1"
        params = []
        if status_filter and status_filter != "all":
            query += " AND status = ?"
            params.append(status_filter)
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [
            MaintenanceRequestResponse(
                id=r["id"],
                client_id=r["client_id"],
                client_name=r["client_name"],
                client_email=r["client_email"],
                client_phone=r["client_phone"],
                equipment=r["equipment"],
                service_type=r["service_type"],
                desired_date=r["desired_date"],
                desired_time=r["desired_time"],
                description=r["description"],
                status=r["status"],
                admin_notes=r["admin_notes"],
                created_at=str(r["created_at"]) if r["created_at"] else None,
                updated_at=str(r["updated_at"]) if r["updated_at"] else None,
            ) for r in rows
        ]

@app.patch("/api/v1/requests/{request_id}/status")
def update_request_status(
    request_id: str,
    payload: MaintenanceStatusUpdate,
    admin_user: dict = Depends(require_admin)
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_id, client_email, equipment FROM maintenance_requests WHERE id = ?", (request_id,))
        req_row = cursor.fetchone()
        if not req_row:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada.")
        
        cursor.execute("""
        UPDATE maintenance_requests 
        SET status = ?, admin_notes = COALESCE(?, admin_notes), updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (payload.status, payload.admin_notes, request_id))

        # Disparador automático: avisar al cliente del avance del servicio técnico
        msg = f"Tu servicio para el equipo {ricoh_label(req_row['equipment'])} ahora está: {MAINT_EMOJI.get(payload.status, '🔧')} {payload.status}."
        if payload.admin_notes:
            msg += f" Nota del técnico: {payload.admin_notes}"
        create_notification(
            cursor, req_row["client_email"],
            f"Servicio técnico {request_id}: {payload.status}",
            msg, "maintenance", "/cuenta.html#solicitudes", req_row["client_id"]
        )
        
        return {"ok": True, "id": request_id, "status": payload.status}

# ============================================================
# 5. QUOTES, CONTACT & COUNTER REPORTING ENDPOINTS
# ============================================================
@app.post("/api/v1/contact")
def create_contact_message(payload: ContactMessageCreate):
    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO contact_messages (id, name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (msg_id, payload.name, payload.email, payload.phone, payload.subject, payload.message))
        return {"ok": True, "id": msg_id, "message": "Mensaje recibido correctamente. Te contactaremos pronto."}

@app.post("/api/v1/quotes")
def save_quotation(payload: QuoteCreate):
    quote_code = f"COT-2026-{uuid.uuid4().hex[:6].upper()}"
    quote_id = f"q_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO quotes (id, quote_code, client_name, client_email, client_phone, items_json, subtotal, iva, total, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            quote_id, quote_code, payload.client_name or "", payload.client_email or "",
            payload.client_phone or "", payload.items_json, payload.subtotal, payload.iva,
            payload.total, payload.notes or ""
        ))
        return {
            "ok": True,
            "quote_code": quote_code,
            "id": quote_id,
            "permalink_url": f"/cotizacion.html?code={quote_code}"
        }

@app.get("/api/v1/quotes/{quote_code}")
def get_quotation_by_code(quote_code: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes WHERE quote_code = ?", (quote_code,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Cotización no encontrada.")
        
        return {
            "quote_code": row["quote_code"],
            "client_name": row["client_name"],
            "client_email": row["client_email"],
            "client_phone": row["client_phone"],
            "items": json.loads(row["items_json"]),
            "subtotal": row["subtotal"],
            "iva": row["iva"],
            "total": row["total"],
            "notes": row["notes"],
            "created_at": str(row["created_at"]),
        }

@app.get("/api/v1/quotes", response_model=List[QuoteResponse])
def list_all_quotes(admin_user: dict = Depends(require_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [
            QuoteResponse(
                id=r["id"],
                quote_code=r["quote_code"],
                client_name=r["client_name"],
                client_email=r["client_email"],
                client_phone=r["client_phone"],
                items_json=r["items_json"],
                subtotal=r["subtotal"],
                iva=r["iva"],
                total=r["total"],
                notes=r["notes"],
                created_at=str(r["created_at"])
            ) for r in rows
        ]

# ============================================================
# 8. ORDERS & E-COMMERCE ENDPOINTS
# ============================================================
@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    current_user: Optional[dict] = Depends(get_optional_current_user)
):
    order_code = f"ORD-2026-{uuid.uuid4().hex[:6].upper()}"
    order_id = f"ord_{uuid.uuid4().hex[:10]}"
    client_id = current_user["id"] if current_user else None
    
    # Validar formato items_json
    try:
        items = json.loads(payload.items_json)
        if not isinstance(items, list) or len(items) == 0:
            raise ValueError("Items must be a non-empty list.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato inválido de productos en el pedido: {str(e)}"
        )

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO orders (
            id, order_code, client_id, client_name, client_email, client_phone, client_nit,
            delivery_address, delivery_city, items_json, subtotal, iva, total,
            payment_method, payment_status, shipping_status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'En preparación', ?)
        """, (
            order_id, order_code, client_id, payload.client_name.strip(), payload.client_email.lower().strip(),
            payload.client_phone.strip(), payload.client_nit.strip() if payload.client_nit else None,
            payload.delivery_address.strip(), payload.delivery_city.strip(), payload.items_json,
            payload.subtotal, payload.iva, payload.total, payload.payment_method,
            payload.payment_status or "Aprobado", payload.notes.strip() if payload.notes else None
        ))

        # Disparadores automáticos: cliente + equipo administrativo
        create_notification(
            cursor, payload.client_email.lower().strip(),
            f"✅ Pedido {order_code} recibido",
            f"Registramos tu pedido por ${payload.total:,.0f} COP ({payload.payment_method}). "
            "Te avisaremos cuando sea despachado en Neiva.".replace(",", "."),
            "order", f"/cotizacion.html?order={order_code}", client_id
        )
        notify_admins(
            cursor, f"🛒 Nuevo pedido {order_code}",
            f"{payload.client_name.strip()} · ${payload.total:,.0f} COP · {payload.payment_method}".replace(",", "."),
            "order", "/admin.html#orders"
        )
        
        return {
            "ok": True,
            "order_code": order_code,
            "id": order_id,
            "payment_status": payload.payment_status or "Aprobado",
            "shipping_status": "En preparación",
            "receipt_url": f"/cotizacion.html?order={order_code}",
            "message": "¡Pedido registrado exitosamente en el sistema de Fotocopiadora SyP!"
        }

@app.get("/api/v1/orders/{order_code}")
def get_order_by_code(order_code: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_code = ? OR id = ?", (order_code, order_code))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        
        return {
            "id": row["id"],
            "order_code": row["order_code"],
            "client_name": row["client_name"],
            "client_email": row["client_email"],
            "client_phone": row["client_phone"],
            "client_nit": row["client_nit"],
            "delivery_address": row["delivery_address"],
            "delivery_city": row["delivery_city"],
            "items": json.loads(row["items_json"]),
            "subtotal": row["subtotal"],
            "iva": row["iva"],
            "total": row["total"],
            "payment_method": row["payment_method"],
            "payment_status": row["payment_status"],
            "shipping_status": row["shipping_status"],
            "notes": row["notes"],
            "created_at": str(row["created_at"]),
        }

@app.get("/api/v1/orders/user/my")
def get_my_orders(current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM orders 
        WHERE client_id = ? OR client_email = ?
        ORDER BY created_at DESC
        """, (current_user["id"], current_user["email"]))
        rows = cursor.fetchall()
        
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "order_code": r["order_code"],
                "client_name": r["client_name"],
                "total": r["total"],
                "payment_method": r["payment_method"],
                "payment_status": r["payment_status"],
                "shipping_status": r["shipping_status"],
                "created_at": str(r["created_at"]),
                "items_count": len(json.loads(r["items_json"]))
            })
        return result

@app.get("/api/v1/orders", response_model=List[OrderResponse])
def list_all_orders(admin_user: dict = Depends(require_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [
            OrderResponse(
                id=r["id"],
                order_code=r["order_code"],
                client_id=r["client_id"],
                client_name=r["client_name"],
                client_email=r["client_email"],
                client_phone=r["client_phone"],
                client_nit=r["client_nit"],
                delivery_address=r["delivery_address"],
                delivery_city=r["delivery_city"],
                items_json=r["items_json"],
                subtotal=r["subtotal"],
                iva=r["iva"],
                total=r["total"],
                payment_method=r["payment_method"],
                payment_status=r["payment_status"],
                shipping_status=r["shipping_status"],
                notes=r["notes"],
                created_at=str(r["created_at"])
            ) for r in rows
        ]

@app.patch("/api/v1/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    payload: OrderStatusUpdate,
    admin_user: dict = Depends(require_admin)
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, order_code, client_id, client_email FROM orders WHERE id = ? OR order_code = ?", (order_id, order_id))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        
        target_id = row["id"]
        
        if payload.payment_status and payload.shipping_status:
            cursor.execute("UPDATE orders SET payment_status = ?, shipping_status = ? WHERE id = ?", (payload.payment_status, payload.shipping_status, target_id))
        elif payload.payment_status:
            cursor.execute("UPDATE orders SET payment_status = ? WHERE id = ?", (payload.payment_status, target_id))
        elif payload.shipping_status:
            cursor.execute("UPDATE orders SET shipping_status = ? WHERE id = ?", (payload.shipping_status, target_id))
            
        if payload.notes:
            cursor.execute("UPDATE orders SET notes = ? WHERE id = ?", (payload.notes, target_id))

        # Disparador automático: notificar al cliente del cambio
        if payload.payment_status or payload.shipping_status:
            parts = []
            if payload.shipping_status:
                parts.append(f"Envío: {SHIPPING_EMOJI.get(payload.shipping_status, '📦')} {payload.shipping_status}")
            if payload.payment_status:
                parts.append(f"Pago: {payload.payment_status}")
            msg = " · ".join(parts)
            if payload.notes:
                msg += f" — {payload.notes}"
            create_notification(
                cursor, row["client_email"],
                f"Actualización de tu pedido {row['order_code']}",
                msg, "order", f"/cotizacion.html?order={row['order_code']}", row["client_id"]
            )
            
        return {"ok": True, "message": "Estado del pedido actualizado con éxito."}

@app.post("/api/v1/counters")
def submit_counter_report(payload: CounterReportCreate, current_user: dict = Depends(get_current_user)):
    rep_id = f"cnt_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO counter_reports (
            id, client_id, client_name, equipment_model, mono_counter, color_counter, report_month, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rep_id, current_user["id"], current_user["name"], payload.equipment_model,
            payload.mono_counter, payload.color_counter, payload.report_month, payload.notes or ""
        ))
        return {"ok": True, "id": rep_id, "message": "Reporte de contador registrado con éxito."}

@app.get("/api/v1/counters")
def list_all_counter_reports(admin_user: dict = Depends(require_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM counter_reports ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "client_id": r["client_id"],
                "client_name": r["client_name"],
                "equipment_model": r["equipment_model"],
                "mono_counter": r["mono_counter"],
                "color_counter": r["color_counter"],
                "report_month": r["report_month"],
                "notes": r["notes"],
                "created_at": str(r["created_at"])
            }
            for r in rows
        ]

# ============================================================
# 9. NOTIFICATIONS ENDPOINTS (Centro de Notificaciones)
# ============================================================
def _row_to_notification(r) -> NotificationResponse:
    return NotificationResponse(
        id=r["id"],
        user_id=r["user_id"],
        user_email=r["user_email"],
        title=r["title"],
        message=r["message"],
        type=r["type"],
        link_url=r["link_url"],
        is_read=bool(r["is_read"]),
        created_at=str(r["created_at"]) if r["created_at"] else None,
    )

@app.get("/api/v1/notifications/my")
def get_my_notifications(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM notifications
        WHERE user_id = ? OR user_email = ?
        ORDER BY created_at DESC, rowid DESC
        LIMIT ?
        """, (current_user["id"], current_user["email"], limit))
        rows = cursor.fetchall()
        cursor.execute("""
        SELECT COUNT(*) AS cnt FROM notifications
        WHERE (user_id = ? OR user_email = ?) AND is_read = 0
        """, (current_user["id"], current_user["email"]))
        unread = cursor.fetchone()["cnt"]
        return {
            "unread_count": unread,
            "items": [_row_to_notification(r).model_dump() for r in rows],
        }

@app.patch("/api/v1/notifications/{notif_id}/read")
def mark_notification_read(notif_id: str, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE notifications SET is_read = 1
        WHERE id = ? AND (user_id = ? OR user_email = ?)
        """, (notif_id, current_user["id"], current_user["email"]))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Notificación no encontrada.")
        return {"ok": True, "id": notif_id}

@app.post("/api/v1/notifications/mark-all-read")
def mark_all_notifications_read(current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE notifications SET is_read = 1
        WHERE (user_id = ? OR user_email = ?) AND is_read = 0
        """, (current_user["id"], current_user["email"]))
        return {"ok": True, "updated": cursor.rowcount}

@app.post("/api/v1/notifications", status_code=status.HTTP_201_CREATED)
def admin_send_notification(payload: NotificationCreate, admin_user: dict = Depends(require_admin)):
    """Permite al administrador enviar una notificación manual (promo, recordatorio de contadores, etc.)."""
    with get_db() as conn:
        cursor = conn.cursor()
        notif_id = create_notification(
            cursor, payload.user_email, payload.title, payload.message,
            payload.type, payload.link_url, payload.user_id
        )
        return {"ok": True, "id": notif_id}

# ============================================================
# 10. ADMIN ANALYTICS & CSV EXPORTS
# ============================================================
@app.get("/api/v1/admin/analytics", response_model=AnalyticsOverviewResponse)
def get_admin_analytics(
    month: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}$", description="Filtrar ventas por mes YYYY-MM"),
    admin_user: dict = Depends(require_admin)
):
    with get_db() as conn:
        cursor = conn.cursor()

        # --- Ventas (excluye pedidos rechazados / cancelados) ---
        sales_query = """
        SELECT payment_method, shipping_status, payment_status, total FROM orders
        WHERE payment_status != 'Rechazado' AND shipping_status != 'Cancelado'
        """
        params: list = []
        if month:
            sales_query += " AND strftime('%Y-%m', created_at) = ?"
            params.append(month)
        cursor.execute(sales_query, params)
        order_rows = cursor.fetchall()

        total_sales = 0.0
        payment_breakdown: dict = {}
        for r in order_rows:
            total_sales += float(r["total"] or 0)
            pm = r["payment_method"]
            entry = payment_breakdown.setdefault(pm, {"count": 0, "total": 0.0})
            entry["count"] += 1
            entry["total"] += float(r["total"] or 0)

        cursor.execute("SELECT shipping_status, COUNT(*) AS cnt FROM orders GROUP BY shipping_status")
        shipping_breakdown = {r["shipping_status"]: r["cnt"] for r in cursor.fetchall()}

        # --- Mantenimiento ---
        cursor.execute("SELECT status, COUNT(*) AS cnt FROM maintenance_requests GROUP BY status")
        maint_by_status = {r["status"]: r["cnt"] for r in cursor.fetchall()}
        maint_total = sum(maint_by_status.values())

        cursor.execute("""
        SELECT equipment, COUNT(*) AS cnt FROM maintenance_requests
        GROUP BY equipment ORDER BY cnt DESC LIMIT 8
        """)
        models_serviced = {r["equipment"]: r["cnt"] for r in cursor.fetchall()}

        # --- Renting: páginas impresas (suma de contadores reportados) ---
        cursor.execute("SELECT COALESCE(SUM(mono_counter + color_counter), 0) AS pages FROM counter_reports")
        renting_pages = int(cursor.fetchone()["pages"] or 0)

        cursor.execute("SELECT COUNT(*) AS cnt FROM quotes")
        quotes_cnt = cursor.fetchone()["cnt"]

        # --- Actividad reciente combinada ---
        cursor.execute("""
        SELECT 'order' AS kind, order_code AS ref, client_name, total AS amount, shipping_status AS status, created_at FROM orders
        UNION ALL
        SELECT 'maintenance', id, client_name, NULL, status, created_at FROM maintenance_requests
        UNION ALL
        SELECT 'counter', id, client_name, (mono_counter + color_counter), report_month, created_at FROM counter_reports
        ORDER BY created_at DESC LIMIT 10
        """)
        recent = [
            {
                "kind": r["kind"], "ref": r["ref"], "client_name": r["client_name"],
                "amount": r["amount"], "status": r["status"], "created_at": str(r["created_at"]),
            }
            for r in cursor.fetchall()
        ]

        return AnalyticsOverviewResponse(
            total_sales_cop=round(total_sales, 2),
            orders_count=len(order_rows),
            payment_methods_breakdown=payment_breakdown,
            shipping_status_breakdown=shipping_breakdown,
            maintenance_count=maint_total,
            maintenance_by_status=maint_by_status,
            ricoh_models_serviced=models_serviced,
            renting_pages_printed=renting_pages,
            quotes_count=quotes_cnt,
            recent_activity=recent,
        )

_EXPORT_TABLES = {
    "orders": ("orders", ["order_code", "client_name", "client_email", "client_phone", "client_nit",
                          "delivery_address", "delivery_city", "subtotal", "iva", "total",
                          "payment_method", "payment_status", "shipping_status", "notes", "created_at"]),
    "requests": ("maintenance_requests", ["id", "client_name", "client_email", "client_phone", "equipment",
                                          "service_type", "desired_date", "desired_time", "description",
                                          "status", "admin_notes", "created_at", "updated_at"]),
    "counters": ("counter_reports", ["id", "client_name", "equipment_model", "mono_counter",
                                     "color_counter", "report_month", "notes", "created_at"]),
    "quotes": ("quotes", ["quote_code", "client_name", "client_email", "client_phone",
                          "subtotal", "iva", "total", "notes", "created_at"]),
}

@app.get("/api/v1/admin/export/{dataset}")
def export_dataset_csv(dataset: str, admin_user: dict = Depends(require_admin)):
    if dataset not in _EXPORT_TABLES:
        raise HTTPException(status_code=404, detail="Dataset no válido. Usa: orders, requests, counters, quotes.")
    table, columns = _EXPORT_TABLES[dataset]
    buf = io.StringIO()
    buf.write("\ufeff")  # BOM para que Excel abra tildes correctamente
    writer = csv.writer(buf, delimiter=";")
    writer.writerow(columns)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {', '.join(columns)} FROM {table} ORDER BY created_at DESC")
        for r in cursor.fetchall():
            writer.writerow(["" if r[c] is None else r[c] for c in columns])
    filename = f"syp_{dataset}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return Response(
        content=buf.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

