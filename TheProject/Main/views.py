from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Main, Photo


class Home(TemplateView):
    template_name = 'main/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.all()
        return context