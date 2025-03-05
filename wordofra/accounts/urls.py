from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserLoginView, NewsletterSubscriptionView, NewsletterOptInView, 
    NewsletterUnsubscribeView, UserNewsletterUnsubscribeView
)


urlpatterns = [
    # Newsletter related endpoints
    path('newsletter/subscribe/', NewsletterSubscriptionView.as_view(), name='newsletter-subscribe'),
    path('newsletter/opt-in/', NewsletterOptInView.as_view(), name='newsletter-opt-in'),
    path('newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter-unsubscribe'),
    path('user/newsletter/unsubscribe/', UserNewsletterUnsubscribeView.as_view(), name='user-newsletter-unsubscribe'),
]