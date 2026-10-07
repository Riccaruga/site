from django.urls import path

from .views import ArtworkDetailView, ArtworkListView

app_name = "gallery"

urlpatterns = [
    path("gallery/", ArtworkListView.as_view(), name="list"),
    path("gallery/<slug:slug>/", ArtworkDetailView.as_view(), name="detail"),
]
