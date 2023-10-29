from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Photo
from .tasks import *

class Home(TemplateView):
    template_name = 'main/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.all()
        context['form'] = ContactForm()
     
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            phone = form.cleaned_data['phone']

            send_mail.delay(name, email, message, subject, phone)
            email_back.delay(email)

            messages.success(request, "<strong>Повідомлення надіслано!</strong> Незабаром вам прийде підтвердження на ваш емейл.")
            return redirect('main:home')

        # If form is not valid, re-render the page with the form and any errors
        context = self.get_context_data()
        context['form'] = form
        messages.error(request, "<strong>Помилка!</strong> Спробуйте ще раз або напишіть нам в інстаграмі.")
        return self.render_to_response(context)

class Contact(TemplateView):
    template_name='main/contact.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            phone = form.cleaned_data['phone']

            send_mail.delay(name, email, message, subject, phone)
            email_back.delay(email)

            messages.success(request, "<strong>Повідомлення надіслано!</strong> Незабаром вам прийде підтвердження на ваш емейл.")
            return redirect('main:home')

        # If form is not valid, re-render the page with the form and any errors
        context = self.get_context_data()
        context['form'] = form
        messages.error(request, "<strong>Помилка!</strong> Спробуйте ще раз або напишіть нам в інстаграмі.")
        return self.render_to_response(context)