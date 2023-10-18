from django.urls import path, include
from .views import * 

urlpatterns = [
    path('login/', login_request, name = 'login'),
    path('logout/', logout_request, name = 'logout'),
    path('schedule/', Schedule.as_view(), name="schedule"),
    path('getpost/', telegram_bot, name='telegram_bot'),
]