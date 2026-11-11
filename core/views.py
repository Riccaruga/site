from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm
from .models import ArtistProfile


def home(request):
    profile = ArtistProfile.objects.first()
    return render(request, "core/home.html", {
        "profile": profile,
    })


def about(request):
    profile = ArtistProfile.get_solo()
    return render(request, "core/about.html", {"profile": profile})


def contacts(request):
    profile = ArtistProfile.objects.first()

    raw_artwork = (
        request.POST.get("artwork") if request.method == "POST"
        else request.GET.get("artwork")
    )
    artwork_title = (raw_artwork or "").strip()
    is_json = (
        request.headers.get("Accept", "") == "application/json"
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
    )

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Уведомление на почту (в dev уходит в консоль)
            recipient = getattr(profile, "email", "") or settings.CONTACT_EMAIL
            body = f"От: {msg.name} <{msg.email}>"
            topic = msg.get_subject_display()
            if topic:
                body += f"\nТема: {topic}"
            if artwork_title:
                body += f"\nКартина: «{artwork_title}»"
            body += f"\n\n{msg.message}"
            try:
                send_mail(
                    subject=f"Сообщение с сайта от {msg.name}",
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient] if recipient else [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            if is_json:
                return JsonResponse({"ok": True})
            # Успех показываем внутри карточки формы
            return redirect(f"{reverse('core:contacts')}?sent=1#contact-form")
        else:
            if is_json:
                return JsonResponse(
                    {"ok": False, "errors": form.errors.get_json_data()},
                    status=400,
                )
    else:
        # Предзаполнение если пришли с картины ?artwork=...
        initial = {}
        if artwork_title:
            initial["message"] = f"Здравствуйте! Интересует картина «{artwork_title}». "
        form = ContactForm(initial=initial)

    return render(request, "core/contacts.html", {
        "form": form,
        "profile": profile,
        "artwork_title": artwork_title,
        "sent": request.GET.get("sent") == "1",
    })
