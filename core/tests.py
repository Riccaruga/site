from django.test import TestCase
from django.urls import reverse

from .models import ArtistProfile


class CorePagesTests(TestCase):
    def test_home_about_contacts_exhibitions(self):
        for name in ["core:home", "core:about", "core:contacts",
                     "gallery:list", "exhibitions:list"]:
            with self.subTest(name=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 200)

    def test_contact_post(self):
        resp = self.client.post(reverse("core:contacts"), {
            "name": "Гость",
            "email": "guest@example.com",
            "message": "Интересует картина",
        })
        # редирект после успеха
        self.assertEqual(resp.status_code, 302)

    def test_contact_post_redirects_with_sent_flag(self):
        resp = self.client.post(reverse("core:contacts"), {
            "name": "Гость",
            "email": "guest@example.com",
            "message": "Интересует картина",
        })
        self.assertTrue(resp.url.endswith("?sent=1#contact-form"))

    def test_contact_artwork_context(self):
        resp = self.client.get(reverse("core:contacts"), {"artwork": "Тишина"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "О картине")
        self.assertContains(resp, "Тишина")
        self.assertContains(resp, 'name="artwork"')

    def test_contact_sent_panel(self):
        resp = self.client.get(reverse("core:contacts") + "?sent=1")
        self.assertContains(resp, "Сообщение отправлено")

    def test_contact_invalid_shows_errors(self):
        resp = self.client.post(reverse("core:contacts"), {
            "name": "",
            "email": "bad",
            "message": "",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Проверьте выделенные поля")
        self.assertContains(resp, 'aria-invalid="true"')

    def test_contact_message_max_length(self):
        resp = self.client.post(reverse("core:contacts"), {
            "name": "Гость",
            "email": "guest@example.com",
            "message": "x" * 2001,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Проверьте выделенные поля")

    def test_profile_singleton(self):
        p = ArtistProfile.get_solo()
        self.assertEqual(p.pk, 1)

    def test_nav_active_state(self):
        # Текущий раздел подсвечен тёмной кнопкой
        for name in ["gallery:list", "core:about",
                     "exhibitions:list", "core:contacts"]:
            with self.subTest(name=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, "bg-stone-900 text-white")
