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
