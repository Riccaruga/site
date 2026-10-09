from django import forms

from .models import ContactMessage

INPUT_CLS = ("w-full border rounded-lg px-4 py-3 outline-none "
             "focus:ring-2 focus:ring-stone-900 focus:border-stone-900")


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLS,
                "placeholder": "Ваше имя",
            }),
            "email": forms.EmailInput(attrs={
                "class": INPUT_CLS,
                "placeholder": "Email для ответа",
            }),
            "message": forms.Textarea(attrs={
                "class": INPUT_CLS,
                "rows": 6,
                "placeholder": "Расскажите, какая картина интересует...",
            }),
        }
        labels = {
            "name": "Имя",
            "email": "Email",
            "message": "Сообщение",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Красная рамка на полях с ошибками
        for name, field in self.fields.items():
            if self.errors.get(name):
                field.widget.attrs["class"] += " border-red-500"
