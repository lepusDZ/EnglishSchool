import time
from celery import shared_task
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_mail(name, email, message, subject, phone):
    context = {
        'email': email,
        'name': name,
        'subject': subject,
        'phone': phone,
        'message': message,
    }
    
    html_body = render_to_string("email/send_mail.html", context)
    
    adminMessage = EmailMultiAlternatives(
                subject='Нова форма!',
                body="",
                from_email='noreply@parrotschool.kh.ua',
                to=['emailgarant@gmail.com'],
                reply_to=[email],
                )
    
    adminMessage.attach_alternative(html_body, "text/html")
    adminMessage.send(fail_silently=False)
    
@shared_task
def email_back(email):
        html_body = render_to_string("email/email_back.html")

        
        userMessage = EmailMultiAlternatives(
                subject='Ми отримали ваше повідомлення!',
                body="",
                from_email='noreply@parrotschool.kh.ua',
                to=[email]
                )
        
        userMessage.attach_alternative(html_body, "text/html")
        userMessage.send(fail_silently=False)