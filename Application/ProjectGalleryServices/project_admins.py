from django.contrib import admin

from .project_models import (
    Gallery,
    Project,
    ProjectImages
)


class ProjectImagesStackedInline(admin.TabularInline):
    model = ProjectImages
    extra = 1


class ProjecAdmin(admin.ModelAdmin):
    inlines = [ProjectImagesStackedInline]
    list_display = ('title', 'location')
    list_filter = ('location',)
    search_fields = ('title', 'location')
    ordering = ('created_at',)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    list_filter = ('title',)
    search_fields = ('title',)


admin.site.register(Project, ProjecAdmin)
admin.site.register(Gallery, GalleryAdmin)