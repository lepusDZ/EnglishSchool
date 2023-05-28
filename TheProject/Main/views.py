from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
# from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Main

class Home(ListView):
    model = Main
    template_name = 'main/landing.html'