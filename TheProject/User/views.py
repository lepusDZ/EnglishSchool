from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login
from django.contrib import messages


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="user/register.html", context={"register_form":form})


# дописать def login(), разобраться с messages