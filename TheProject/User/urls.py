from django.urls import path
from .views import * 

urlpatterns = [
    path('login/', login_request, name = 'login'),
    path('logout/', logout_request, name = 'logout'),
    path('profile/', user_profile, name = 'profile'),
]