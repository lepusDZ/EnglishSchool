from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm
from django.shortcuts import render, redirect


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


def user_profile(request):
    user = request.user
    fields = [(field.verbose_name, getattr(user, field.name))
              for field in user._meta.fields]
    return render(request, template_name='user/profile.html', context={'user': user, 'fields': fields})


def extract_error_messages(errors):
    error_messages = []
    for field, field_errors in errors.items():
        if field == "__all__":
            error_messages.extend(field_errors)
        else:
            for error in field_errors:
                error_messages.append(error)
    return error_messages