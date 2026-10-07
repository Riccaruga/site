from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Artwork, Series

# 1x1 gif для тестов без Pillow-зависимостей на реальных фото
TEST_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff"
    b"\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00"
    b"\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
)


def test_image(name="test.gif"):
    return SimpleUploadedFile(name, TEST_GIF, content_type="image/gif")


class GalleryTests(TestCase):
    def setUp(self):
        self.series = Series.objects.create(name="Пейзажи")
        self.art = Artwork.objects.create(
            title="Вечер у реки",
            series=self.series,
            year=2024,
            technique="холст, масло",
            image=test_image(),
        )

    def test_slug_transliterated(self):
        # gallery/models.py: unique_slugify через pytils
        self.assertTrue(self.art.slug)
        self.assertNotIn(" ", self.art.slug)
        # кириллицы в слаге быть не должно
        self.assertEqual(self.art.slug, "vecher-u-reki")

    def test_list_url(self):
        url = reverse("gallery:list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Вечер у реки")

    def test_detail_url(self):
        resp = self.client.get(self.art.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "холст, масло")

    def test_filter_by_series(self):
        url = reverse("gallery:list") + f"?series={self.series.slug}"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
