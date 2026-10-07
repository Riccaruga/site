from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from exhibitions.models import Exhibition

from .forms import ContactForm
from .models import ArtistProfile


def home(request):
    upcoming = Exhibition.objects.filter(
        is_published=True, date_start__gte=timezone.now().date()
    ).order_by("date_start")[:3]
    profile = ArtistProfile.objects.first()
    return render(request, "core/home.html", {
        "upcoming": upcoming,
        "profile": profile,
    })


def about(request):
    profile = ArtistProfile.get_solo()
    return render(request, "core/about.html", {"profile": profile})


def contacts(request):
    profile = ArtistProfile.objects.first()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Уведомление на почту (в dev уходит в консоль)
            recipient = getattr(profile, "email", "") or settings.CONTACT_EMAIL
            try:
                send_mail(
                    subject=f"Сообщение с сайта от {msg.name}",
                    message=f"От: {msg.name} <{msg.email}>\n\n{msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient] if recipient else [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Спасибо! Сообщение отправлено. Я отвечу в ближайшее время.")
            return redirect("core:contacts")
    else:
        # Предзаполнение если пришли с картины ?artwork=...
        initial = {}
        artwork_title = request.GET.get("artwork")
        if artwork_title:
            initial["message"] = f"Здравствуйте! Интересует картина «{artwork_title}». "
        form = ContactForm(initial=initial)
    return render(request, "core/contacts.html", {"form": form, "profile": profile})
