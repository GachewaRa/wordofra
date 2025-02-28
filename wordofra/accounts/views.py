from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer, NewsletterUnsubscribeSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import NewsletterSubscriberSerializer
from .models import CustomUser, NewsletterSubscriber
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth.hashers import check_password


class LoginRateThrottle(AnonRateThrottle):
    rate = '5/hour'
    scope = 'login_attempts'


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Step 1: Retrieve user from database
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


        # Step 2: Check if account is locked
        if user.is_account_locked():
            return Response(
                {"error": "Account temporarily locked. Try again in 30 minutes."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Step 3: Check credentials manually first
        if not check_password(password, user.password):
            # Invalid password
            current_attempts = user.increment_failed_login()
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Step 4: Password is correct, now generate token
        user.reset_failed_login()
        
        # Generate token using the serializer
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():  # This should now always succeed
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Authentication error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#NEWSLETTER SUBSCRIPTION VIEW

class NewsletterSubscriptionView(APIView):
    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            name = serializer.validated_data.get('name', '') #get name if it is provided.
            NewsletterSubscriber.objects.get_or_create(email=email, defaults={'name':name})
            return Response({'message': 'Subscription successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#NEWSLETTER OPT-IN VIEW FOR LOGGED-IN USERS

class NewsletterOptInView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.is_newsletter_subscribed = True
        request.user.save()
        NewsletterSubscriber.objects.get_or_create(email=request.user.email)
        return Response({'message': 'Opt-in successful'}, status=status.HTTP_200_OK)
    

class NewsletterUnsubscribeView(APIView):
    def post(self, request):
        serializer = NewsletterUnsubscribeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                subscriber = NewsletterSubscriber.objects.get(email=email)
                subscriber.delete()
                
                # Also update user model if exists
                try:
                    user = CustomUser.objects.get(email=email)
                    user.is_newsletter_subscribed = False
                    user.save()
                except CustomUser.DoesNotExist:
                    pass
                    
                return Response(
                    {"message": "Successfully unsubscribed from newsletter"},
                    status=status.HTTP_200_OK
                )
            except NewsletterSubscriber.DoesNotExist:
                return Response(
                    {"message": "Email not found in subscribers list"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserNewsletterUnsubscribeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user.is_newsletter_subscribed = False
        user.save()
        
        # Also remove from NewsletterSubscriber if exists
        try:
            subscriber = NewsletterSubscriber.objects.get(email=user.email)
            subscriber.delete()
        except NewsletterSubscriber.DoesNotExist:
            pass
            
        return Response(
            {"message": "Successfully unsubscribed from newsletter"},
            status=status.HTTP_200_OK
        )



#USER DELETION VIEWS

# class RequestAccountDeletionView(APIView):
#     permission_classes = (IsAuthenticated,)
    
#     def post(self, request):
#         # Generate unique token with expiration
#         token = generate_deletion_token(request.user)
#         # Send email with confirmation link
#         send_deletion_confirmation_email(request.user.email, token)
#         return Response({"message": "Confirmation email sent"}, status=status.HTTP_200_OK)
    

# class ConfirmAccountDeletionView(APIView):
#     def get(self, request):
#         token = request.query_params.get('token')
#         user = verify_deletion_token(token)
#         if user:
#             user.delete()
#             return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    

# #NEWSLETTER UNSUBSCRIPTION EMAIL VIEWS

# class RequestNewsletterUnsubscribeView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         if not email:
#             return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
#         subscriber = NewsletterSubscriber.objects.filter(email=email).first()
#         if subscriber:
#             # Generate unsubscribe token
#             token = generate_unsubscribe_token(email)
#             # Send email with unsubscribe link
#             send_unsubscribe_email(email, token)
            
#         # Always return success to prevent email enumeration
#         return Response({"message": "If your email exists in our system, you will receive an unsubscription link"}, 
#                       status=status.HTTP_200_OK)