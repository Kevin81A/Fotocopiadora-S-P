import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import urllib.parse
from .models import Category, Brand, Product, ServiceRequest, ContactMessage

# Personalización del Panel Django Admin
admin.site.site_header = "Fotocopiadora SyP — Administración Central"
admin.site.site_title = "SyP Fotocopiadora Portal"
admin.site.index_title = "Gestión de Catálogo, Solicitudes Técnicas y Clientes"


def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural.lower().replace(" ", "_")}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Exportar seleccionados a archivo CSV (Excel)"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_code', 'category', 'brand', 'formatted_price', 'stock_status_badge', 'is_featured')
    list_filter = ('category', 'brand', 'stock_status', 'is_featured')
    search_fields = ('name', 'id_code', 'spec', 'compatible_models')
    list_editable = ('is_featured',)
    actions = [export_as_csv]

    def formatted_price(self, obj):
        return f"${obj.price:,.0f} COP"
    formatted_price.short_description = "Precio"

    def stock_status_badge(self, obj):
        colors = {
            'ok': '#2e7d32',
            'low': '#e65100',
            'out': '#c62828',
        }
        color = colors.get(obj.stock_status, '#333')
        return format_html(
            '<span style="background-color:{}; color:#fff; padding:3px 8px; border-radius:3px; font-weight:600; font-size:11px;">{}</span>',
            color,
            obj.get_stock_status_display()
        )
    stock_status_badge.short_description = "Estado Stock"


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_phone', 'equipment', 'service_type', 'scheduled_date', 'scheduled_time', 'status_badge', 'whatsapp_action')
    list_filter = ('status', 'service_type', 'scheduled_date')
    search_fields = ('client_name', 'client_email', 'client_phone', 'equipment', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = [export_as_csv, 'mark_as_completed', 'mark_as_in_progress', 'mark_as_confirmed']

    def status_badge(self, obj):
        colors = {
            'Pendiente': '#f57c00',
            'Confirmada': '#0288d1',
            'En proceso': '#7b1fa2',
            'Completada': '#2e7d32',
            'Cancelada': '#d32f2f',
        }
        color = colors.get(obj.status, '#555')
        return format_html(
            '<span style="background-color:{}; color:#fff; padding:4px 9px; border-radius:3px; font-weight:700; font-size:11px;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = "Estado"

    def whatsapp_action(self, obj):
        clean_phone = ''.join(filter(str.isdigit, str(obj.client_phone)))
        if not clean_phone.startswith('57') and len(clean_phone) == 10:
            clean_phone = '57' + clean_phone

        msg = (
            f"Hola {obj.client_name}, le escribimos de Fotocopiadora SyP en Neiva. "
            f"Confirmamos su solicitud de {obj.service_type} para su equipo {obj.equipment} "
            f"programada para el {obj.scheduled_date} a las {obj.scheduled_time}."
        )
        url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"

        return format_html(
            '<a href="{}" target="_blank" style="background:#25D366; color:#fff; padding:4px 8px; border-radius:3px; text-decoration:none; font-weight:bold; font-size:11px;">💬 WhatsApp</a>',
            url
        )
    whatsapp_action.short_description = "Notificar Cliente"

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='Confirmada')
    mark_as_confirmed.short_description = "Marcar como Confirmada"

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='En proceso')
    mark_as_in_progress.short_description = "Marcar como En Proceso"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completada')
    mark_as_completed.short_description = "Marcar como Completada"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    actions = [export_as_csv, 'mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marcar como leído"
