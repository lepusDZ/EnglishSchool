from django import forms
from django.core.validators import EmailValidator


LESSON_CHOICES= [
    ('solo', 'Груповий'),
    ('duo', 'Дуо'),
    ('group', 'Індивідуальний'),
    ]

class ContactForm(forms.Form):
    subject = forms.CharField(
        widget=forms.Select(choices=LESSON_CHOICES),
    )

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ім\'я*', 'class':'form-control'}),
        error_messages={'required': 'Скажіть, як нам до вас звертатися',},
    )

    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'Емейл*', 'class':'form-control', 'type':'email'}),
        error_messages={'required': 'Скажіть, на який емейл нам надіслати відповідь'},
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class':'form-control'}),
        required=False
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Ваше повідомлення',}),
        required=False
    )