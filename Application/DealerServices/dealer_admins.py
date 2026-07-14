import nested_admin
from django.contrib import admin
from .dealer_models import *

class DistrictInline(nested_admin.NestedTabularInline):
    model = District
    extra = 1

class StateInline(nested_admin.NestedTabularInline):
    model = State
    extra = 1
    inlines = [DistrictInline]

class CountryAdmin(nested_admin.NestedModelAdmin):
    inlines = [StateInline]
    list_display = ['name', 'created_at']
    search_fields = ['name']

class StateAdmin(admin.ModelAdmin):
    inlines = [DistrictInline]
    list_display = ['name', 'country', 'created_at']
    list_filter = ['country']
    search_fields = ['name']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'created_at']
    list_filter = ['state__country', 'state']
    search_fields = ['name']


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)


class SubFranchaseInline(admin.StackedInline):
    model = SubFranchaseModel
    extra = 1

class MainFranchaseAdmin(admin.ModelAdmin):
    inlines = [SubFranchaseInline]
    list_display = ['name', 'phone', 'email', 'state', 'district', 'is_available', 'created_at']
    list_filter = ['is_available', 'state', 'district']
    search_fields = ['name', 'email', 'phone', 'pincode']

class SubFranchaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_franchase', 'phone', 'email', 'state', 'district', 'is_available', 'created_at']
    list_filter = ['is_available', 'main_franchase', 'state', 'district']
    search_fields = ['name', 'email', 'phone', 'pincode', 'main_franchase__name']

admin.site.register(MainFranchaseModel, MainFranchaseAdmin)
admin.site.register(SubFranchaseModel, SubFranchaseAdmin)

class WarrentyRegisterAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'franchise', 'product_name', 'model_number', 'serial_number', 'purchased_date', 'created_at']
    list_filter = ['franchise', 'state', 'district', 'purchased_date']
    search_fields = ['fullname', 'email', 'phone', 'serial_number', 'model_number', 'franchise', 'product_name']

admin.site.register(WarrantyRegisterModel, WarrentyRegisterAdmin)
