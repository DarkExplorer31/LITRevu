from django import forms
from . import models


class CreateTicket(forms.ModelForm):
    ticket_creation = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
    )
    title = forms.CharField(
        label="Titre", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class CreateReview(forms.ModelForm):
    review_creation = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
    )

    rating = forms.ChoiceField(
        label="Note",
        choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )

    headline = forms.CharField(
        label="Titre de la critique",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    body = forms.CharField(
        label="Description de la critique",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]


class CreateTicketReviewForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Titre du ticket",
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        label="Description du ticket",
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Image du ticket",
    )

    rating = forms.ChoiceField(
        choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        widget=forms.Select(attrs={"class": "custom-select"}),
        label="Note de la critique",
    )

    headline = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Titre de la critique",
    )

    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        label="Contenu de la critique",
    )


class UserSearching(forms.Form):
    query = forms.CharField(
        label="Recherche d'utilisateur",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
