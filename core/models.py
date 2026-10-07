from django.db import models


class ArtistProfile(models.Model):
    """Профиль художника — предполагается одна запись (singleton)."""
    name = models.CharField("Имя художника", max_length=200, default="Имя Художника")
    bio = models.TextField("Биография", blank=True)
    statement = models.TextField("Artist statement", blank=True)
    photo = models.ImageField("Фото художника", upload_to="artist/", null=True, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    telegram = models.URLField("Telegram", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    whatsapp = models.URLField("WhatsApp", blank=True)
    cv_file = models.FileField("CV (PDF)", upload_to="artist/", null=True, blank=True)
    meta_title = models.CharField("Meta title", max_length=200, blank=True)
    meta_description = models.TextField("Meta description", blank=True)

    class Meta:
        verbose_name = "Профиль художника"
        verbose_name_plural = "Профиль художника"

    def __str__(self):
        return self.name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"name": "Имя Художника"})
        return obj


class ContactMessage(models.Model):
    name = models.CharField("Имя", max_length=120)
    email = models.EmailField("Email")
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    is_read = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения с формы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.created_at:%d.%m.%Y}"
