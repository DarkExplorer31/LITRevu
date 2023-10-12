"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import review.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        authentication.views.LoginPageView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("home/", review.views.HomePage.as_view(), name="home"),
    path(
        "signup/", authentication.views.SignupPageView.as_view(), name="signup"
    ),
    # Ticket management
    path(
        "ticket/creation/",
        review.views.TicketCreation.as_view(),
        name="ticket_creation",
    ),
    path(
        "ticket/update/<int:pk>/",
        review.views.TicketUpdate.as_view(),
        name="ticket_update",
    ),
    path(
        "ticket/delete/<int:pk>/",
        review.views.DeleteTicket.as_view(),
        name="delete_ticket",
    ),
    # Review management
    path(
        "review/creation/?ticket=<int:ticket_id>/",
        review.views.ReviewOnlyCreation.as_view(),
        name="review_only_creation",
    ),
    path(
        "review/creation/",
        review.views.ReviewWithTicketCreation.as_view(),
        name="review_with_ticket_creation",
    ),
    path(
        "review/update/<int:pk>/",
        review.views.ReviewUpdate.as_view(),
        name="review_update",
    ),
    path(
        "review/delete/<int:pk>/",
        review.views.DeleteReview.as_view(),
        name="review_delete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

handler404 = "review.views.error_404"
handler500 = "review.views.error_500"
