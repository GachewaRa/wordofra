from django import forms

class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text="Enter your email to subscribe to the newsletter.")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # You can add custom validation logic for the email field here if necessary
        return email

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    is_newsletter_subscribed = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'is_newsletter_subscribed']


#from django.contrib.auth.forms import AuthenticationForm

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
#                                                              'placeholder': 'Email or Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
#                                                                  'placeholder': 'Password'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email or Username'}))
    password = forms.CharField(widget=forms.PasswordInput)