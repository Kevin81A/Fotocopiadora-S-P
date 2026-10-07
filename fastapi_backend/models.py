"""
Fotocopiadora SyP — Pydantic Schemas & Data Validation Models
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# --- Auth Schemas ---
class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    role: str
    is_active: bool
    created_at: Optional[str] = None

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    category_slug: str
    brand: str = "Ricoh"
    price: float = Field(..., gt=0)
    spec: str
    stock_status: str = "ok" # 'ok', 'low', 'out'
    rating: float = 4.9
    reviews_count: int = 25
    badge: Optional[str] = None
    discount_percent: int = 0
    speed: Optional[str] = None
    duty_cycle: Optional[str] = None
    paper_size: Optional[str] = None
    connectivity: Optional[str] = None
    functions: Optional[str] = None
    toner_yield: Optional[str] = None
    cost_per_page: Optional[str] = None
    compatible_ids: Optional[str] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    id: str = Field(..., min_length=3, max_length=50)

class ProductResponse(ProductBase):
    id: str
    is_active: bool = True
    created_at: Optional[str] = None

# --- Maintenance Request Schemas ---
class MaintenanceRequestCreate(BaseModel):
    equipment: str = Field(..., min_length=2)
    service_type: str = Field(..., min_length=2)
    desired_date: str
    desired_time: str
    description: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None

class MaintenanceStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(Pendiente|Confirmada|En proceso|Completada|Cancelada)$")
    admin_notes: Optional[str] = None

class MaintenanceRequestResponse(BaseModel):
    id: str
    client_id: Optional[str]
    client_name: str
    client_email: str
    client_phone: Optional[str]
    equipment: str
    service_type: str
    desired_date: str
    desired_time: str
    description: Optional[str]
    status: str
    admin_notes: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

# --- Contact & Quotes ---
class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., min_length=7)
    subject: str
    message: str = Field(..., min_length=10)

class QuoteCreate(BaseModel):
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None
    items_json: str
    subtotal: float
    iva: float
    total: float
    notes: Optional[str] = None

class QuoteResponse(BaseModel):
    id: str
    quote_code: str
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    items_json: str
    subtotal: float
    iva: float
    total: float
    notes: Optional[str] = None
    created_at: Optional[str] = None

# --- Orders & E-Commerce Schemas ---
class OrderCreate(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=150)
    client_email: EmailStr
    client_phone: str = Field(..., min_length=7, max_length=25)
    client_nit: Optional[str] = None
    delivery_address: str = Field(..., min_length=5, max_length=250)
    delivery_city: str = "Neiva, Huila"
    items_json: str
    subtotal: float = Field(..., gt=0)
    iva: float = Field(..., ge=0)
    total: float = Field(..., gt=0)
    payment_method: str = Field(..., pattern="^(PSE|Tarjeta de Crédito / Débito|Transferencia Bancolombia / Nequi|Crédito Empresarial 30 Días|WhatsApp Directo)$")
    payment_status: Optional[str] = "Aprobado"
    notes: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    payment_status: Optional[str] = Field(None, pattern="^(Aprobado|Pendiente|Rechazado|En Verificación)$")
    shipping_status: Optional[str] = Field(None, pattern="^(En preparación|Despachado|En camino|Entregado|Cancelado)$")
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: str
    order_code: str
    client_id: Optional[str] = None
    client_name: str
    client_email: str
    client_phone: str
    client_nit: Optional[str] = None
    delivery_address: str
    delivery_city: str
    items_json: str
    subtotal: float
    iva: float
    total: float
    payment_method: str
    payment_status: str
    shipping_status: str
    notes: Optional[str] = None
    created_at: Optional[str] = None

class CounterReportCreate(BaseModel):
    equipment_model: str
    mono_counter: int = Field(..., ge=0)
    color_counter: int = Field(0, ge=0)
    report_month: str
    notes: Optional[str] = None

# --- Notifications Schemas ---
class NotificationCreate(BaseModel):
    user_id: Optional[str] = None
    user_email: EmailStr
    title: str = Field(..., min_length=2, max_length=150)
    message: str = Field(..., min_length=2)
    type: str = "info" # 'order', 'maintenance', 'system', 'promo', 'renting'
    link_url: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    user_email: str
    title: str
    message: str
    type: str
    link_url: Optional[str] = None
    is_read: bool = False
    created_at: Optional[str] = None

# --- Analytics Overview Schemas ---
class AnalyticsOverviewResponse(BaseModel):
    total_sales_cop: float
    orders_count: int
    payment_methods_breakdown: dict
    shipping_status_breakdown: dict
    maintenance_count: int
    maintenance_by_status: dict
    ricoh_models_serviced: dict
    renting_pages_printed: int
    quotes_count: int
    recent_activity: List[dict]


