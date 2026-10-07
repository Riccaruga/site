from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "placeholder": "Ваше имя",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "placeholder": "Email для ответа",
            }),
            "message": forms.Textarea(attrs={
                "class": "w-full border rounded px-3 py-2",
                "rows": 5,
                "placeholder": "Расскажите, какая картина интересует...",
            }),
        }
        labels = {
            "name": "Имя",
            "email": "Email",
            "message": "Сообщение",
        }
