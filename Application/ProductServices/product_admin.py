from django.contrib import admin
from .product_models import *


class ProductFamilyInline(admin.TabularInline):
    model = ProductFamily
    extra = 1


class ProductDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    inlines = [ProductFamilyInline]

admin.site.register(ProductDepartment, ProductDepartmentAdmin)


class ProductFamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active', 'created_at', 'updated_at')
    list_filter = ('department', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

admin.site.register(ProductFamily, ProductFamilyAdmin)


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'price', 'discount_percentage', 'discount_price', 'is_available', 'created_at', 'updated_at')
    list_filter = ('family', 'is_available', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'additional_info', 'technical_spec')
    ordering = ('-created_at',)
    inlines = [ProductImagesInline]

admin.site.register(Product, ProductAdmin)


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('product__name',)
