from django import forms
from django.contrib.auth.models import User

RATE_VALUES = [
    (6, "S-Tier"),
    (5, "A-Tier"),
    (4, "B-Tier"),
    (3, "C-Tier"),
    (2, "D-Tier"),
    (1, "F-Tier"),
]

class RateEntryForm(forms.Form):
    rating = forms.ChoiceField(choices=RATE_VALUES)

class PostCreationForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=550)
    is_private = forms.BooleanField(
            label="Keep tierlist private?",
            required=False,
            initial=False,
    )

class CreateEntryForm(forms.Form):
    name = forms.CharField(max_length=200)
    image = forms.ImageField()
    