from django.contrib import admin

from .ui_models import *


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_2', 'description')
    list_filter = ('title', 'title_2', 'description')
    search_fields = ('title', 'title_2', 'description')
    ordering = ('created_at', 'updated_at')

admin.site.register(HomeSlider, HomeSliderAdmin)
    