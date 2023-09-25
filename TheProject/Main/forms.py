from django import forms
from django.core.validators import EmailValidator


LESSON_CHOICES= [
    ('solo', 'Груповий'),
    ('duo', 'Дуо'),
    ('group', 'Індивідуальний'),
    ]

class ContactForm(forms.Form):
    subject= forms.CharField(widget=forms.Select(choices=LESSON_CHOICES))
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Ім\'я'}))
    email = forms.CharField(validators=[EmailValidator()],widget=forms.TextInput(attrs={'placeholder': 'Емейл'}))
    phone = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder': 'Телефон'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ваше повідомлення'}))