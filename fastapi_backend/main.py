"""
Fotocopiadora SyP — REST API Server (FastAPI + JWT Authentication + SQLite)
"""
import uuid
import json
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status, Query
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
    current_user: Optional[dict] = Depends(lambda: None) # Flexible para cliente logueado o invitado
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
        cursor.execute("SELECT id FROM maintenance_requests WHERE id = ?", (request_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Solicitud no encontrada.")
        
        cursor.execute("""
        UPDATE maintenance_requests 
        SET status = ?, admin_notes = COALESCE(?, admin_notes), updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (payload.status, payload.admin_notes, request_id))
        
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
        cursor.execute("SELECT id FROM orders WHERE id = ? OR order_code = ?", (order_id, order_id))
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

