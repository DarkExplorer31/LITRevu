from django import forms
from . import models


class CreateTicket(forms.ModelForm):
    ticket_creation = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class CreateReview(forms.ModelForm):
    review_creation = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
    )

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]


class UserSearching(forms.Form):
    query = forms.CharField(label="Recherche d'utilisateurs", max_length=100)
