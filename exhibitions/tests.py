from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Exhibition


class ExhibitionSectionsTests(TestCase):
    def setUp(self):
        today = timezone.now().date()
        self.current_long = Exhibition.objects.create(
            title="Текущая длинная", venue="Галерея",
            date_start=today - timedelta(days=5),
            date_end=today + timedelta(days=5),
        )
        self.current_one_day = Exhibition.objects.create(
            title="Текущая сегодня", venue="Галерея",
            date_start=today, date_end=None,
        )
        self.upcoming = Exhibition.objects.create(
            title="Будущая", venue="Галерея",
            date_start=today + timedelta(days=10),
            date_end=today + timedelta(days=20),
        )
        self.past = Exhibition.objects.create(
            title="Прошедшая", venue="Галерея",
            date_start=today - timedelta(days=20),
            date_end=today - timedelta(days=1),
        )
        self.past_no_end = Exhibition.objects.create(
            title="Прошедшая без даты конца", venue="Галерея",
            date_start=today - timedelta(days=3), date_end=None,
        )

    def test_sections_split(self):
        resp = self.client.get(reverse("exhibitions:list"))
        self.assertEqual(resp.status_code, 200)
        current = list(resp.context["current"])
        upcoming = list(resp.context["upcoming"])
        past = list(resp.context["past"])
        self.assertIn(self.current_long, current)
        self.assertIn(self.current_one_day, current)
        self.assertIn(self.upcoming, upcoming)
        self.assertNotIn(self.upcoming, current)
        self.assertIn(self.past, past)
        self.assertIn(self.past_no_end, past)
        self.assertNotIn(self.past, current)
        self.assertContains(resp, "Текущие")

    def test_model_helpers(self):
        self.assertTrue(self.current_long.is_current())
        self.assertFalse(self.current_long.is_finished())
        self.assertTrue(self.upcoming.is_finished() is False)
        self.assertFalse(self.upcoming.is_current())
        self.assertTrue(self.past.is_finished())
