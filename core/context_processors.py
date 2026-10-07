from .models import ArtistProfile


def artist_profile(request):
    try:
        profile = ArtistProfile.objects.first()
    except Exception:
        profile = None
    return {"artist_profile": profile}
