from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "contact-input",
                "placeholder": "Your name",
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        max_length=254,
        error_messages={
            "invalid": "Enter a valid email address (for example: name@example.com).",
        },
        widget=forms.EmailInput(
            attrs={
                "class": "contact-input",
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "inputmode": "email",
                "pattern": r"[^@\s]+@[^@\s]+\.[^@\s]+",
                "title": "Enter a valid email address, e.g. name@example.com",
            }
        ),
    )
    message = forms.CharField(
        max_length=3000,
        strip=True,
        widget=forms.Textarea(
            attrs={
                "class": "contact-textarea",
                "placeholder": "Your message",
                "rows": 6,
            }
        ),
    )
