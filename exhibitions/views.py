from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView

from .models import Exhibition


class ExhibitionListView(ListView):
    model = Exhibition
    template_name = "exhibitions/list.html"
    context_object_name = "exhibitions"

    def get_queryset(self):
        return Exhibition.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.now().date()
        qs = self.get_queryset()
        ctx["current"] = qs.filter(
            date_start__lte=today
        ).filter(Q(date_end__isnull=True) | Q(date_end__gte=today))
        ctx["upcoming"] = qs.filter(date_start__gt=today)
        ctx["past"] = qs.filter(
            Q(date_end__lt=today) |
            Q(date_end__isnull=True, date_start__lt=today)
        )
        return ctx
