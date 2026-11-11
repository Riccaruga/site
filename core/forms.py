from django import forms

from .models import ContactMessage

INPUT_CLS = (
    "w-full border border-stone-300 rounded-xl px-3.5 py-2.5 bg-white outline-none "
    "placeholder:text-stone-400 transition "
    "focus:border-stone-700 focus:ring-2 focus:ring-stone-900/10"
)
SELECT_CLS = f"{INPUT_CLS} appearance-none pr-10 cursor-pointer"
MESSAGE_MAX_LENGTH = 2000
SUBJECT_CHOICES = [("", "Выберите тему"), *ContactMessage.Subject.choices]


class ContactForm(forms.ModelForm):
    subject = forms.ChoiceField(
        label="Тема обращения",
        required=False,
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            "class": SELECT_CLS,
            "aria-describedby": "subject-hint",
        }),
    )
    message = forms.CharField(
        label="Сообщение",
        max_length=MESSAGE_MAX_LENGTH,
        widget=forms.Textarea(attrs={
            "class": INPUT_CLS,
            "rows": 5,
            "placeholder": "Расскажите, что вас заинтересовало...",
        }),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
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

            described_by = attrs.get("aria-describedby", "").split()
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
