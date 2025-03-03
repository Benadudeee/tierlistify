from django import forms
from .models import TierListEntry
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

