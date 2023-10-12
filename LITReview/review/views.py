from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import models


class HomePage(LoginRequiredMixin, View):
    template_name = "review/home.html"
    user = None

    def get(self, request):
        self.user = request.user
        tickets = models.Ticket.objects.all()
        reviews = models.Review.objects.all()
        return render(
            request,
            self.template_name,
            context={"tickets": tickets, "reviews": reviews},
        )


# Ticket views
class TicketCreation(LoginRequiredMixin, FormView):
    model = models.Ticket
    template_name = "review/ticket_creation.html"
    form_class = forms.CreateTicket
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user_id = self.request.user.id
        ticket.save()
        return super().form_valid(form)


class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    template_name = "review/ticket_creation.html"
    form_class = forms.CreateTicket
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user_id = self.request.user.id
        ticket.save()
        return super().form_valid(form)


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = models.Ticket
    success_url = reverse_lazy("home")
    template_name = "review/ticket_delete_confirm.html"


# Review views
class ReviewWithTicketCreation(LoginRequiredMixin, View):
    template_name = "review/review_creation.html"
    review_form = forms.CreateReview
    ticket_form = forms.CreateTicket

    def get(self, request):
        ticket_form = self.ticket_form()
        review_form = self.review_form()
        return render(
            request,
            self.template_name,
            context={
                "ticket_form": ticket_form,
                "review_form": review_form,
            },
        )

    def post(self, request):
        ticket_form = self.ticket_form()
        review_form = self.review_form()
        if all(review_form.is_valid(), ticket_form.is_valid()):
            ticket_valid = ticket_form.save(commit=False)
            review_valid = review_form.save(commit=False)
            ticket_valid.user_id = self.request.user.id
            review_valid.user_id = self.request.user.id
            ticket_valid.save()
            review_valid.save()
            return redirect("home")
        return render(
            request,
            self.template_name,
            context={
                "ticket_form": ticket_form,
                "review_form": review_form,
            },
        )


class ReviewOnlyCreation(LoginRequiredMixin, View):
    template_name = "review/review_creation.html"
    review_form = forms.CreateReview

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        review_form = self.review_form()
        return render(
            request,
            self.template_name,
            context={
                "ticket_id": ticket_id,
                "ticket": ticket,
                "review_form": review_form,
            },
        )

    def post(self, request, ticket_id):
        review_form = self.review_form()
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if review_form.is_valid():
            review_valid = review_form.save(commit=False)
            review_valid.user_id = self.request.user.id
            review_valid.ticket = ticket
            review_valid.save()
            return redirect("home")
        return render(
            request,
            self.template_name,
            context={
                "ticket_id": ticket_id,
                "ticket": ticket,
                "review_form": review_form,
            },
        )


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = models.Review
    template_name = "review/review_creation.html"
    form_class = forms.CreateReview
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        Review = form.save(commit=False)
        Review.user_id = self.request.user.id
        Review.save()
        return super().form_valid(form)


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = models.Review
    success_url = reverse_lazy("home")
    template_name = "review/review_delete_confirm.html"


# Response error
def error_404(request, exception):
    return render(request, "review/error_404.html")


def error_500(request):
    return render(request, "review/error_500.html")
