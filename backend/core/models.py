from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de Categoría")
    slug = models.SlugField(max_length=100, unique=True)
    icon_svg = models.TextField(blank=True, verbose_name="SVG del Icono")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Marca")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STOCK_CHOICES = [
        ('ok', 'Disponible'),
        ('low', 'Pocas unidades'),
        ('out', 'Agotado'),
    ]

    id_code = models.CharField(max_length=50, unique=True, verbose_name="Código de Producto / ID")
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Categoría")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Marca")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Precio (COP)")
    spec = models.CharField(max_length=300, verbose_name="Especificaciones / Descripción corta")
    stock_status = models.CharField(max_length=10, choices=STOCK_CHOICES, default='ok', verbose_name="Disponibilidad")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Descuento (%)")
    is_featured = models.BooleanField(default=False, verbose_name="¿Producto Destacado en Inicio?")
    compatible_models = models.TextField(blank=True, help_text="Modelos compatibles separados por comas. Ej: Aficio MP 301, MP 2554", verbose_name="Modelos Compatibles")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Foto del Producto")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Producto / Insumo"
        verbose_name_plural = "Productos e Insumos"
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return f"{self.name} - ${self.price:,.0f} COP"


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('En proceso', 'En proceso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('Mantenimiento preventivo', 'Mantenimiento preventivo'),
        ('Mantenimiento correctivo', 'Mantenimiento correctivo'),
        ('Diagnóstico', 'Diagnóstico'),
        ('Instalación de equipo', 'Instalación de equipo'),
        ('Recarga / Insumos', 'Recarga / Insumos'),
    ]

    client_name = models.CharField(max_length=150, verbose_name="Nombre del Cliente")
    client_email = models.EmailField(verbose_name="Correo Electrónico")
    client_phone = models.CharField(max_length=25, verbose_name="Teléfono / WhatsApp")
    equipment = models.CharField(max_length=150, verbose_name="Marca y Modelo del Equipo")
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, default='Diagnóstico', verbose_name="Tipo de Servicio")
    scheduled_date = models.DateField(verbose_name="Fecha Deseada")
    scheduled_time = models.TimeField(verbose_name="Hora Deseada")
    description = models.TextField(verbose_name="Descripción de la Falla o Necesidad")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente', verbose_name="Estado de la Solicitud")
    admin_notes = models.TextField(blank=True, verbose_name="Notas Internas de Administración")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Solicitud de Servicio Técnico"
        verbose_name_plural = "Solicitudes de Servicio Técnico"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.status}] {self.client_name} - {self.equipment} ({self.service_type})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo")
    phone = models.CharField(max_length=25, verbose_name="Teléfono")
    subject = models.CharField(max_length=150, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    is_read = models.BooleanField(default=False, verbose_name="¿Leído?")

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%d/%m/%Y')})"
