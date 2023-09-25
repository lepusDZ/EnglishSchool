from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import Photo

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

            EmailMessage(
                'Contact Form Submission from {}, {} pack'.format(name, subject),
                message,
                'emailgarant2@gmail.com',  # Send from (your website)
                ['emailgarant@gmail.com'],  # Send to (your admin email)
                [],
                reply_to=[email]  # Email from the form to get back to
            ).send()

            return redirect('main:home')

        # If form is not valid, re-render the page with the form and any errors
        context = self.get_context_data()
        context['form'] = form
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
            phone = form.cleaned_data['subject']

            EmailMessage(
                'Contact Form Submission from {}, {} Pack'.format(name, subject),
                '{}, {}'.format(phone, message),
                'emailgarant2@gmail.com',  # Send from (your website)
                ['emailgarant@gmail.com'],  # Send to (your admin email)
                [],
                reply_to=[email]  # Email from the form to get back to
            ).send()

            return redirect('main:home')

        # If form is not valid, re-render the page with the form and any errors
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)