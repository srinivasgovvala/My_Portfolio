import re
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Hidden honeypot field to block automated spam bots
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
        label=''
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'id_name',
                'class': 'form-input',
                'placeholder': 'Your Name',
                'required': True,
                'maxlength': '200',
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'id_email',
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
                'required': True,
                'autocomplete': 'email'
            }),
            'subject': forms.TextInput(attrs={
                'id': 'id_subject',
                'class': 'form-input',
                'placeholder': 'Subject of your message',
                'required': True,
                'maxlength': '300'
            }),
            'message': forms.Textarea(attrs={
                'id': 'id_message',
                'class': 'form-input',
                'placeholder': 'Write your message here...',
                'rows': 5,
                'required': True
            }),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get('honeypot', '')
        if value:
            # Bot filled the invisible honeypot field
            raise ValidationError("Spam detected.")
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Please provide your name.")
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("Please provide a valid email address.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")
        return email

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject:
            raise ValidationError("Please provide a subject.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise ValidationError("Please write your message.")
        if len(message) < 5:
            raise ValidationError("Message is too short (minimum 5 characters).")
        return message
