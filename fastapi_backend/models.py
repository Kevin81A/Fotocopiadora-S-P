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

class CounterReportCreate(BaseModel):
    equipment_model: str
    mono_counter: int = Field(..., ge=0)
    color_counter: int = Field(0, ge=0)
    report_month: str
    notes: Optional[str] = None
