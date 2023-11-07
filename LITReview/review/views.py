from itertools import chain
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
from django.db import models
from django.db.models import Value


from . import forms
from . import models as review_models


class HomePage(LoginRequiredMixin, View):
    template_name = "review/home.html"
    user = None

    def get(self, request):
        self.user = request.user
        user_tickets = review_models.Ticket.objects.filter(user=self.user)
        followers = review_models.UserFollows.objects.filter(user=self.user)
        # make the flux with reviews/tickets from user and all followed users
        for follower in followers:
            follower_tickets = review_models.Ticket.objects.filter(
                user=follower.followed_user
            )
            user_tickets = user_tickets | follower_tickets
        user_reviews = review_models.Review.objects.filter(
            ticket__in=user_tickets
        )
        user_reviews = user_reviews.annotate(
            content_type=Value("REVIEW", models.CharField())
        )
        # finally, exclude potentially duplicated tickets
        user_tickets = user_tickets.annotate(
            content_type=Value("TICKET", models.CharField())
        ).exclude(id__in=[review.ticket.id for review in user_reviews])
        posts = sorted(
            chain(user_reviews, user_tickets),
            key=lambda post: post.time_created,
            reverse=True,
        )
        return render(
            request,
            self.template_name,
            context={
                "posts": posts,
                "stars": [1, 2, 3, 4, 5],
            },
        )


# Ticket views
class TicketCreation(LoginRequiredMixin, FormView):
    model = review_models.Ticket
    template_name = "review/ticket_creation.html"
    form_class = forms.CreateTicket
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user_id = self.request.user.id
        ticket.save()
        return super().form_valid(form)


class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = review_models.Ticket
    template_name = "review/ticket_creation.html"
    form_class = forms.CreateTicket
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.user:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        if self.request.user == self.object.user:
            ticket = form.save(commit=False)
            ticket.user_id = self.request.user.id
            ticket.save()
            return super().form_valid(form)
        else:
            raise PermissionDenied()


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = review_models.Ticket
    success_url = reverse_lazy("home")
    template_name = "review/ticket_delete_confirm.html"

    def get(self, request, *args, **kwargs):
        review = self.get_object()
        if request.user == review.user:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()


# Review views
class ReviewWithTicketCreation(LoginRequiredMixin, View):
    template_name = "review/review_creation.html"
    form = forms.CreateTicketReviewForm

    def get(self, request):
        review_with_ticket_form = self.form()
        return render(
            request,
            self.template_name,
            context={"review_with_ticket_form": review_with_ticket_form},
        )

    def post(self, request):
        review_with_ticket_form = self.form(request.POST, request.FILES)
        if review_with_ticket_form.is_valid():
            title = review_with_ticket_form.cleaned_data["title"]
            description = review_with_ticket_form.cleaned_data["description"]
            image = review_with_ticket_form.cleaned_data["image"]
            rating = review_with_ticket_form.cleaned_data["rating"]
            headline = review_with_ticket_form.cleaned_data["headline"]
            body = review_with_ticket_form.cleaned_data["body"]

            ticket = review_models.Ticket(
                title=title,
                description=description,
                image=image,
                user=request.user,
            )
            ticket.save()

            review = review_models.Review(
                rating=rating,
                headline=headline,
                body=body,
                user=request.user,
                ticket=ticket,
            )
            review.save()

            return redirect("home")
        else:
            return render(
                request,
                self.template_name,
                context={"review_with_ticket_form": review_with_ticket_form},
            )


class ReviewOnlyCreation(LoginRequiredMixin, View):
    template_name = "review/review_creation.html"
    review_form = forms.CreateReview

    def get(self, request, ticket_id):
        ticket = get_object_or_404(review_models.Ticket, id=ticket_id)
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
        review_form = self.review_form(request.POST)
        ticket = get_object_or_404(review_models.Ticket, id=ticket_id)
        if review_form.is_valid():
            review_valid = review_form.save(commit=False)
            review_valid.user_id = self.request.user.id
            review_valid.ticket = ticket
            review_valid.save()
            return redirect("home")
        else:
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
    model = review_models.Review
    template_name = "review/review_creation.html"
    form_class = forms.CreateReview
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.user:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        if self.request.user == self.object.user:
            review = form.save(commit=False)
            review.user_id = self.request.user.id
            review.save()
            return super().form_valid(form)
        else:
            raise PermissionDenied()


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = review_models.Review
    success_url = reverse_lazy("home")
    template_name = "review/review_delete_confirm.html"

    def get(self, request, *args, **kwargs):
        review = self.get_object()
        if request.user == review.user:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()


# User and his followers
class SearchUser(LoginRequiredMixin, FormView):
    template_name = "review/searching_user.html"
    form_class = forms.UserSearching
    success_url = reverse_lazy("searching_user")

    def form_valid(self, form):
        query = form.cleaned_data.get("query")
        users = User.objects.filter(username__icontains=query).exclude(
            id=self.request.user.id
        )
        if users:
            for searched_user in users:
                is_following = review_models.UserFollows.objects.filter(
                    user=self.request.user, followed_user=searched_user
                )
            context = {
                "form": form,
                "users": users,
                "is_following": is_following,
            }
        return render(self.request, self.template_name, context)


class FollowUser(LoginRequiredMixin, View):
    def post(self, request, user_id_to_follow):
        user_to_follow = get_object_or_404(User, id=user_id_to_follow)
        try:
            review_models.UserFollows.objects.get(
                user=request.user, followed_user=user_to_follow
            )
        except review_models.UserFollows.DoesNotExist:
            user_following = review_models.UserFollows(
                user=request.user, followed_user=user_to_follow
            )
            user_following.save()
        return redirect("home")


class UnfollowUser(LoginRequiredMixin, View):
    def post(self, request, user_id_to_unfollow):
        user_to_unfollow = User.objects.get(id=user_id_to_unfollow)
        user_follow = review_models.UserFollows.objects.get(
            user=request.user, followed_user=user_to_unfollow
        )
        user_follow.delete()
        return redirect("follows_management")


class FollowersManagement(LoginRequiredMixin, View):
    model = review_models.UserFollows
    template_name = "review/follow_management.html"

    def get(self, request):
        following = self.model.objects.filter(user=request.user)
        followers = self.model.objects.filter(followed_user=request.user)
        return render(
            request,
            self.template_name,
            context={
                "following": following,
                "followers": followers,
            },
        )


# Response error
def error_404(request, exception):
    return render(request, "review/error_404.html", status=404)


def error_500(request):
    return render(request, "review/error_500.html", status=500)


def error_403(request, exception):
    return render(request, "review/error_403.html", status=403)
