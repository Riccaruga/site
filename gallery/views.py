from django.views.generic import DetailView, ListView

from .models import Artwork, Series


class ArtworkListView(ListView):
    model = Artwork
    template_name = "gallery/list.html"
    context_object_name = "artworks"
    paginate_by = 24

    def get_queryset(self):
        qs = Artwork.objects.filter(is_published=True).select_related("series")
        series_slug = self.request.GET.get("series")
        year = self.request.GET.get("year")
        if series_slug:
            qs = qs.filter(series__slug=series_slug)
        if year and year.isdigit():
            qs = qs.filter(year=int(year))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["series_list"] = Series.objects.all()
        ctx["years"] = (
            Artwork.objects.filter(is_published=True, year__isnull=False)
            .values_list("year", flat=True).distinct().order_by("-year")
        )
        ctx["active_series"] = self.request.GET.get("series", "")
        ctx["active_year"] = self.request.GET.get("year", "")
        return ctx


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = "gallery/detail.html"
    context_object_name = "artwork"
    slug_field = "slug"

    def get_queryset(self):
        return Artwork.objects.filter(is_published=True).select_related("series").prefetch_related("extra_images")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # prev / next по order
        current = self.object
        ctx["prev_artwork"] = (
            Artwork.objects.filter(is_published=True, order__lt=current.order)
            .order_by("-order").first()
        )
        ctx["next_artwork"] = (
            Artwork.objects.filter(is_published=True, order__gt=current.order)
            .order_by("order").first()
        )
        return ctx
