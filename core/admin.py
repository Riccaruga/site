from django.contrib import admin

from .models import ArtistProfile, ContactMessage


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Только одна запись профиля
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "short_message", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message")
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")

    @admin.display(description="Сообщение")
    def short_message(self, obj):
        return (obj.message[:60] + "…") if len(obj.message) > 60 else obj.message

    def has_add_permission(self, request):
        return False
