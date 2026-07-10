from django.contrib import admin
from .dealer_models import (
    Country, State, District, Dealers
)

class DistrictInline(admin.TabularInline):
    model = District
    extra = 1

class StateAdmin(admin.ModelAdmin):
    inlines = [DistrictInline]
    list_display = ['name', 'country', 'created_at']
    list_filter = ['country']
    search_fields = ['name']

class StateInline(admin.TabularInline):
    model = State
    extra = 1

class CountryAdmin(admin.ModelAdmin):
    inlines = [StateInline]
    list_display = ['name', 'created_at']
    search_fields = ['name']

class DealersInline(admin.TabularInline):
    model = Dealers
    extra = 1
    # Limiting fields so the table doesn't get excessively wide in the admin
    fields = ['dealer_name', 'dealer_type', 'dealer_email', 'dealer_phone', 'dealer_status']

class DistrictAdmin(admin.ModelAdmin):
    inlines = [DealersInline]
    list_display = ['name', 'state', 'created_at']
    list_filter = ['state__country', 'state']
    search_fields = ['name']

class DealerAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'dealer_type', 'dealer_name', 'dealer_city', 'dealer_state', 'dealer_country', 'dealer_status', 'is_main']
    list_filter = ['dealer_type', 'dealer_status', 'is_main', 'dealer_state', 'dealer_country']
    search_fields = ['dealer_name', 'dealer_city', 'dealer_state', 'dealer_country']
    ordering = ['-dealer_created_at']
    readonly_fields = ['unique_id']

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Dealers, DealerAdmin)

