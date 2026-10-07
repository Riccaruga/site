from django.contrib import admin

from .models import Exhibition


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ("title", "venue", "city", "date_start", "date_end", "is_published")
    list_filter = ("is_published", "city")
    search_fields = ("title", "venue", "city")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date_start"
