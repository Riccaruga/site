from django.db import models
from django.urls import reverse

from gallery.models import unique_slugify


class Exhibition(models.Model):
    title = models.CharField("Название", max_length=220)
    slug = models.SlugField("Slug", max_length=240, unique=True, blank=True)
    venue = models.CharField("Площадка", max_length=220)
    city = models.CharField("Город", max_length=120, blank=True)
    date_start = models.DateField("Дата начала")
    date_end = models.DateField("Дата окончания", null=True, blank=True)
    description = models.TextField("Описание", blank=True)
    link = models.URLField("Ссылка", blank=True)
    is_published = models.BooleanField("Опубликовано", default=True)

    class Meta:
        verbose_name = "Выставка"
        verbose_name_plural = "Выставки"
        ordering = ["-date_start"]

    def __str__(self):
        return f"{self.title} — {self.venue}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)
