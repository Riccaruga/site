from django.views.generic import DetailView, ListView

from .models import Artwork


class ArtworkListView(ListView):
    model = Artwork
    template_name = "gallery/list.html"
    context_object_name = "artworks"
    paginate_by = 24

    def get_queryset(self):
        return Artwork.objects.filter(is_published=True)


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = "gallery/detail.html"
    context_object_name = "artwork"
    slug_field = "slug"

    def get_queryset(self):
        return Artwork.objects.filter(is_published=True).prefetch_related("extra_images")

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
