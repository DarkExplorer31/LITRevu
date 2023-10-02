from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomePage(View):
    template_name = "review/home.html"
    user = None

    @method_decorator(login_required)
    def get(self, request):
        self.user = request.user
        return render(request, self.template_name)
