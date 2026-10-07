from django.urls import path

from .views import ExhibitionListView

app_name = "exhibitions"

urlpatterns = [
    path("exhibitions/", ExhibitionListView.as_view(), name="list"),
]
