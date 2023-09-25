from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path("contact/", Contact.as_view(), name="contact"),
]