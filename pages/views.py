from django.shortcuts import render

from pages.models import AboutPage


def about(request):
    return render(request, "pages/about.html", {"about": AboutPage.get()})
