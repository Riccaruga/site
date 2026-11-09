from django import forms

from .models import ContactMessage

INPUT_CLS = (
    "w-full border border-stone-300 rounded-lg px-4 py-3 bg-white outline-none "
    "placeholder:text-stone-400 transition "
    "focus:ring-2 focus:ring-stone-900/15 focus:border-stone-900"
)
MESSAGE_MAX_LENGTH = 2000


class ContactForm(forms.ModelForm):
    message = forms.CharField(
        label="Сообщение",
        max_length=MESSAGE_MAX_LENGTH,
        widget=forms.Textarea(attrs={
            "class": INPUT_CLS,
            "rows": 6,
            "placeholder": "Расскажите, какая картина интересует...",
        }),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLS,
                "placeholder": "Ваше имя",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": INPUT_CLS,
                "placeholder": "Email для ответа",
                "autocomplete": "email",
                "inputmode": "email",
            }),
        }
        labels = {
            "name": "Имя",
            "email": "Email",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = field.widget.attrs
            if field.required:
                attrs["required"] = True
                attrs["aria-required"] = "true"

            described_by = []
            if name == "message":
                described_by.append("message-counter")

            # Красная рамка и доступные подсказки для полей с ошибками
            if self.errors.get(name):
                cls = attrs.get("class", "")
                if "border-stone-300" in cls:
                    cls = cls.replace("border-stone-300", "border-red-500")
                else:
                    cls = f"{cls} border-red-500"
                attrs["class"] = cls
                attrs["aria-invalid"] = "true"
                described_by.append(f"{self[name].id_for_label}-error")

            if described_by:
                attrs["aria-describedby"] = " ".join(described_by)
