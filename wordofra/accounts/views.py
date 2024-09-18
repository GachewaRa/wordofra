from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import NewsletterSubscriber
from .forms import NewsletterSubscriptionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .forms import NewsletterSubscriptionForm



from .forms import CustomUserCreationForm  # Ensure this uses the custom form


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user but don't commit yet
            user.set_password(form.cleaned_data['password1'])  # Set password securely
            user.is_newsletter_subscribed = form.cleaned_data.get('is_newsletter_subscribed', False)  # Set newsletter subscription
            user.save()  # Save user with all data
            auth_login(request, user)  # Log the user in
            return redirect('login')
        else:
            print(form.errors)  # Log any form errors
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


from .forms import LoginForm
from django.http import HttpResponse


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('home')  # Redirect to the home page or a dashboard
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})



def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            NewsletterSubscriber.objects.get_or_create(email=email)
            return redirect('subscription_success')
    else:
        form = NewsletterSubscriptionForm()
    return render(request, 'accounts/subscribe.html', {'form': form})

@login_required
def opt_in_newsletter(request):
    if request.method == 'POST':
        request.user.is_newsletter_subscribed = True
        request.user.save()
        NewsletterSubscriber.objects.get_or_create(email=request.user.email)
        return redirect('opt_in_success')
    return render(request, 'accounts/opt_in.html')

def subscription_success(request):
    return render(request, 'accounts/subscription_success.html')

