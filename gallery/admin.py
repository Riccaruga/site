from django.contrib import admin
from django.utils.html import format_html

from .models import Artwork, ArtworkImage, Series


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 0
    fields = ("image", "preview", "caption", "order")
    readonly_fields = ("preview",)

    @admin.display(description="Превью")
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px"/>', obj.image.url)
        return "—"


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "series", "year", "is_featured",
                    "is_published", "order")
    list_filter = ("series", "year", "is_published", "is_featured")
    search_fields = ("title", "technique", "description")
    list_editable = ("is_featured", "is_published", "order")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ArtworkImageInline]
    readonly_fields = ("preview", "created_at", "updated_at")
    fieldsets = (
        ("Основное", {"fields": ("title", "slug", "series", "year",
                                 "technique", "width_cm", "height_cm",
                                 "description")}),
        ("Изображение", {"fields": ("image", "preview")}),
        ("Публикация", {"fields": ("is_published", "is_featured", "order")}),
        ("Будущий магазин (скрыто)", {
            "fields": ("is_for_sale", "price"),
            "classes": ("collapse",),
        }),
        ("Служебное", {"fields": ("created_at", "updated_at"),
                       "classes": ("collapse",)}),
    )

    @admin.display(description="Фото")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px"/>', obj.image.url)
        return "—"

    @admin.display(description="Превью")
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:300px"/>', obj.image.url)
        return "—"
