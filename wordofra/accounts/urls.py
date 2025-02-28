from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserLoginView, NewsletterSubscriptionView, NewsletterOptInView, 
    NewsletterUnsubscribeView, UserNewsletterUnsubscribeView
)

urlpatterns = [
    # Djoser URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # Custom JWT token with our extended functionality
    path('auth/jwt/custom-login/', UserLoginView.as_view(), name='custom-login'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Newsletter related endpoints
    path('newsletter/subscribe/', NewsletterSubscriptionView.as_view(), name='newsletter-subscribe'),
    path('newsletter/opt-in/', NewsletterOptInView.as_view(), name='newsletter-opt-in'),
    path('newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter-unsubscribe'),
    path('user/newsletter/unsubscribe/', UserNewsletterUnsubscribeView.as_view(), name='user-newsletter-unsubscribe'),
]