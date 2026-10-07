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
        ctx["upcoming"] = qs.filter(date_start__gte=today)
        ctx["past"] = qs.filter(date_start__lt=today)
        return ctx
