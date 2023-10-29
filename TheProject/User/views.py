from .models import Homework, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from calendar import monthrange
from django.utils import timezone
from django.utils.timezone import activate

# bot stuff
import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .botCr import TELEGRAM_API_URL
import re
from .usertasks import *

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:home")
        else:
            error_messages = extract_error_messages(form.errors)
            for error in error_messages:
                messages.error(request, error)
    form = NewUserForm()
    return render(request=request, template_name="user/register.html", context={"register_form": form})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main:home")
            else:
                error_messages = extract_error_messages(form.errors)
                for error in error_messages:
                    messages.error(request, error)
        else:
            error_messages = extract_error_messages(form.errors)
            for error in error_messages:
                messages.error(request, error)
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    return redirect("main:home")


def extract_error_messages(errors):
    error_messages = []
    for field, field_errors in errors.items():
        if field == "__all__":
            error_messages.extend(field_errors)
        else:
            for error in field_errors:
                error_messages.append(error)
    return error_messages

class Schedule(TemplateView):
    template_name = "user/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Calculate the dates for the current month
        today = datetime.today()
    
        year = today.year
        month = today.month

        # Find the number of days in the month
        _, num_days_in_month = monthrange(year, month)

        # Calculate the first and last day of the month
        first_day_of_month = today.replace(day=1)
        
        last_day_of_month = today.replace(day=num_days_in_month)
        last_day_of_month = last_day_of_month.replace(hour=23, minute=59, second=59)
        
        # Calculate last month
        # last_month = first_day_of_month - datetime.timedelta(days=1)
        #  _, num_days_in_last_month = monthrange(year, month)

        # Find the weekday of the 1st day (0 = Monday, 1 = Tuesday, ...)
        weekday_of_first_day = first_day_of_month.weekday()

        # Calculate the number of days to pad before the 1st day
        padding_days = [""] * weekday_of_first_day

        # Calculate the days of the month
        days_in_month = padding_days + [int(i) for i in range(1, num_days_in_month + 1)]
        # Create a grid of days for the entire month
        weeks_in_month = [days_in_month[i:i+7] for i in range(0, len(days_in_month), 7)]
        
        #
        
        homework = Homework.objects.filter(user=user, date__gte=first_day_of_month, date__lte=last_day_of_month).order_by("date")
        
        homework_by_day = {}

        for hw in homework:
            day = hw.date.day
            if day not in homework_by_day:
                homework_by_day[day] = []
            homework_by_day[day].append(hw)
                    
        context['user'] = user
        context['weeks_in_month'] = weeks_in_month
        context['month_name'] = today.strftime("%B %Y")
        context['today'] = today
        context['homework'] = homework
        context['homework_by_day'] = homework_by_day
        
        return context

@csrf_exempt
def telegram_bot(request):
    if request.method == 'POST':
        update = json.loads(request.body.decode('utf-8'))
        handle_update(update)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest('Bad Request')

def handle_update(update):
    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    user = CustomUser.objects.filter(telegram_id=chat_id).first()
    match = re.match(r"/start\s(\d+)$", text)


    if user:
        if text == "/hw":
            homework = Homework.objects.filter(user=user, date__gte=datetime.today()).order_by("date")
            if homework:
                answer = ""
                for hw in homework:
                    hw.date = hw.date.astimezone(timezone.get_current_timezone())

                    answer += f"Title: {hw.title}\nDescription: {hw.description}\nDue date: {hw.date.strftime('%Y-%m-%d %H:%M')}\nHomework file: {hw.file}\n\n"
                    
                send_message({
                        'chat_id': chat_id,
                        'text': answer
                    })
            else:
                send_message({
                        'chat_id': chat_id,
                        'text': 'There is no upcoming homework, yay!'
                    })
        else:
            send_message({
                    'chat_id': chat_id,
                    'text': 'Please use /hw to see the upcoming homework'
                })
    elif not user and match:
         integer_part = match.group(1)
         user = CustomUser.objects.get(pk=integer_part)
         user.telegram_id = chat_id
         user.save()
         send_message({
                    'chat_id': chat_id,
                    'text': f'This chat id was assigned to the user {user.first_name} {user.last_name}'
                })
    else:
        send_message({
                    'chat_id': chat_id,
                    'text': 'Visit our website for more information -\nYou can connect your telegram to your account in the schedule tab'
                })

