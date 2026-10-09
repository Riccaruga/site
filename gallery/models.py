from django.db import models
from django.urls import reverse
from django.utils.text import slugify as django_slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

try:
    from pytils.translit import slugify as translit_slugify
except ImportError:  # fallback если pytils нет
    translit_slugify = django_slugify


def unique_slugify(instance, value, slug_field_name="slug"):
    """Транслитерация кириллицы в латиницу + уникальность."""
    base = translit_slugify(value) or django_slugify(value) or "work"
    slug = base
    Model = instance.__class__
    i = 2
    while Model.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


class Series(models.Model):
    name = models.CharField("Название серии", max_length=200, unique=True)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    description = models.TextField("Описание", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Серия"
        verbose_name_plural = "Серии"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Artwork(models.Model):
    title = models.CharField("Название", max_length=220)
    slug = models.SlugField("Slug", max_length=240, unique=True, blank=True)
    series = models.ForeignKey(
        Series, verbose_name="Серия", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="artworks",
    )
    year = models.PositiveIntegerField("Год", null=True, blank=True)
    technique = models.CharField("Техника", max_length=220, blank=True,
                                 help_text="Например: холст, масло")
    width_cm = models.DecimalField("Ширина, см", max_digits=6, decimal_places=1,
                                   null=True, blank=True)
    height_cm = models.DecimalField("Высота, см", max_digits=6, decimal_places=1,
                                    null=True, blank=True)
    description = models.TextField("История картины", blank=True)
    image = models.ImageField("Изображение", upload_to="artworks/%Y/")
    # Превью для списка: ровная рамка 4:3, картину не обрезаем (Fit, не Fill)
    list_thumb = ImageSpecField(source="image",
                                processors=[ResizeToFit(600, 600)],
                                format="WEBP", options={"quality": 75})
    list_thumb_2x = ImageSpecField(source="image",
                                   processors=[ResizeToFit(1200, 1200)],
                                   format="WEBP", options={"quality": 70})
    detail_medium = ImageSpecField(source="image",
                                   processors=[ResizeToFit(1200, 1200)],
                                   format="WEBP", options={"quality": 78})
    detail_large = ImageSpecField(source="image",
                                  processors=[ResizeToFit(1800, 1800)],
                                  format="WEBP", options={"quality": 75})
    is_featured = models.BooleanField("На главную", default=False)
    is_published = models.BooleanField("Опубликовано", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    # Зарезервировано под будущий магазин, в v1 скрыто:
    is_for_sale = models.BooleanField("В продаже (будущее)", default=False)
    price = models.DecimalField("Цена (будущее)", max_digits=10, decimal_places=2,
                                null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Картина"
        verbose_name_plural = "Картины"
        ordering = ["order", "-year", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gallery:detail", kwargs={"slug": self.slug})

    @property
    def dimensions_display(self):
        if self.width_cm and self.height_cm:
            # убираем .0 для целых
            def fmt(v):
                s = f"{v}".rstrip("0").rstrip(".")
                return s
            return f"{fmt(self.width_cm)} × {fmt(self.height_cm)} см"
        return ""


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(
        Artwork, verbose_name="Картина",
        on_delete=models.CASCADE, related_name="extra_images",
    )
    image = models.ImageField("Изображение", upload_to="artworks/details/%Y/")
    caption = models.CharField("Подпись", max_length=220, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    thumb = ImageSpecField(source="image",
                           processors=[ResizeToFill(400, 400)],
                           format="WEBP", options={"quality": 70})

    class Meta:
        verbose_name = "Доп. фото картины"
        verbose_name_plural = "Доп. фото картин"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.artwork.title} — фото {self.pk}"
