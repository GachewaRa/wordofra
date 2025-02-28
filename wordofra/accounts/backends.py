from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Normalize username or email by converting to lowercase
        if email:
            email = email.lower()
        if username:
            username = username.lower()

        try:
            user = UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            try:
                # If no user with that username exists, try with email (case-insensitive)
                user = UserModel.objects.get(email__iexact=email)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
